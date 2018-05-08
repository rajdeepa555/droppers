
# Logging
import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.http import HttpResponseRedirect,HttpResponse
from .tasks import put_ebay_products_to_db,start_ebay_seller_search,print_time_5times,\
						 start_ebay_seller_search2,ebay_price_updater,sync_db_to_ebay
# from .models import EbayAmazonPriceFormula,Proxy,EbayProductsCsvData,EbayRunDetails,AmazonRun,AmazonRunDetails,ProxyLog,EbaySellerSearch,EbaySellerItems
from django.shortcuts import render,redirect
from .models import *
from rest_framework import views
from rest_framework.response import Response
import csv
import re
from .utils import *
import os
import time
from ui.cron import scrape_amazon_urls,start_ebay_process
from .ebay import *
import datetime
import json
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .amazonapi import AmazonScraper
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from braces.views import LoginRequiredMixin, CsrfExemptMixin
from .auth import *
from .ebay import EbayHandler
from django.db.models import Count
from .proxy import CProxy
from .helpers import *
import django_rq
from rest_framework.permissions import IsAuthenticated
from .globals2 import current_user

class AdminerView(TemplateView):
		template_name = "adminer.php"
		
class HomeView(LoginRequiredMixin,TemplateView):
		template_name = "index.html"

		def get_context_data(self, **kwargs):
				logger.info("self.request.user.pk",self.request.user.pk)
				current_user = self.request.user.pk
				print("current_user",current_user)
				context = super(HomeView, self).get_context_data(**kwargs)
				dashboard_values = {}
				proxy_count = Proxy.objects.filter(is_active=1).count()
				no_of_products = EbayProductsCsvData.objects.count()
				dashboard_values["proxy_count"] = proxy_count
				dashboard_values["no_of_products"] = no_of_products
				context['dashboard_values'] = dashboard_values

				return context

class EbayProfitCalculatorView(LoginRequiredMixin,TemplateView):
	template_name = "ebay_profit_calculator.html"



def justForTest():
	print_time_5times.delay()
	return Response("job scheduled")

class TestRqView(views.APIView):
	def get(self,request,*args,**kwargs):
		print_time_5times.delay()
		# django_rq.delay(print_time_5times)
		return Response("job scheduled")

def get_seller_name(request):
	user = request.user.pk
	seller_pk = SellerTokens.objects.get(user_id = user,is_active = True).pk
	return seller_pk

class EbayProfitCalculator(LoginRequiredMixin,views.APIView):
	def get(self, request, *args, **kwargs):
		seller_pk = get_seller_name(request)
		formula = EbayPriceFormula.objects.get(seller_id = seller_pk)
		price_formula = {}
		context ={}
		price_formula["ebay_fvf"] = formula.ebay_final_value_fee
		price_formula["perc_margin"] = formula.perc_margin
		price_formula["fixed_margin"] = formula.fixed_margin
		context['price_formula'] = formula
		print (price_formula)
		return Response(price_formula)

	def post(self, request, *args, **kwargs):
		print("request",request.data)
		source_price = request.data["source_price"]
		ebay_fvf_perc = request.data["ebay_fvf"]
		margin_perc = request.data["perc_margin"]
		fixed_margin = float(request.data["fixed_margin"])
		formula_obj=EbayPriceFormula.objects.get(pk=1)
		cost = float(source_price)
		margin_perc = float(margin_perc)
		perc_margin_cost = cost*margin_perc/100
		ebay_fvf_perc = float(ebay_fvf_perc)
		cost1 = 0
		cost2 = 0
		selling_price = 0
		if perc_margin_cost<fixed_margin:
			cost1 = cost+formula_obj.ebay_listing_fee+fixed_margin+formula_obj.paypal_fees_fixed
			expected_profit = fixed_margin
			p = 1-((ebay_fvf_perc + formula_obj.paypal_fees_perc)/100)
			selling_price = cost1/p

		else:
			cost2 = cost+formula_obj.ebay_listing_fee+perc_margin_cost+formula_obj.paypal_fees_fixed
			expected_profit = perc_margin_cost
			p = 1-((ebay_fvf_perc + formula_obj.paypal_fees_perc)/100)
			selling_price = cost2/p


		ebay_final_value_fee = selling_price* ebay_fvf_perc/100
		paypal_fees = (formula_obj.paypal_fees_perc*selling_price/100)+formula_obj.paypal_fees_fixed
		paypal_fees = format_val(paypal_fees)
		ebay_final_value_fee = format_val(ebay_final_value_fee)
		print("selling_price0",selling_price)
		selling_price = round(selling_price,2)
		selling_price = format_val(selling_price)
		expected_profit = format_val(expected_profit)
		context = {"source_price":source_price,"selling_price":selling_price,"ebay_listing_fee":formula_obj.ebay_listing_fee,"ebay_final_value_fee":ebay_final_value_fee,"paypal_fees":paypal_fees,"expected_profit":expected_profit}
		print(context)
		return Response(context)

class EbaySellerKeysetView(LoginRequiredMixin,TemplateView):
		template_name = "add_keyset.html"

class AddEbaySellerKeysetView(LoginRequiredMixin,views.APIView):
		def post(self, request, *args, **kwargs):
			data = {}
			data = request.data
			sellername=data.get("sellername","")
			appid=data.get("appid","")
			devid=data.get("devid","")
			certid=data.get("certid","")
			token=data.get("token","")
			
			db=AddEbaySellerKeyset(sellername=sellername,appid=appid,devid=devid,certid=certid,token=token)
			db.save()
			print("database")

			
			return HttpResponseRedirect('/')

class GetEbaySellerKeysetView(LoginRequiredMixin,views.APIView):
	def get(self,request):
		items_list = []
		keyset=AddEbaySellerKeyset.objects.all()
		if keyset and len(keyset)>0:
			for key in keyset:
				item={}
				item["sellername"]=key.sellername
				item["appid"]=key.appid
				item["devid"]=key.devid
				item["certid"]=key.certid
				item["token"]=key.token
				items_list.append(item)

		return Response(items_list)

class DeletePendingEbayItems(LoginRequiredMixin,views.APIView):

	def post(self, request, *args, **kwargs):
		print("request data",request.data)
		pending_items = request.data
		for items in pending_items:
			item = EbaySellerSearchPendingItems.objects.get(pk=items)
			item.delete()

		res = {}
		return Response(res)

class ManualPendingItemAddView(LoginRequiredMixin,TemplateView):
		template_name = "manual_pending_item_add.html"

class SearchAmazonItem(LoginRequiredMixin,views.APIView):
	def post(self, request, *args, **kwargs):
		response_dict = {}
		keywords = request.data["keyword"]
		keywords = keywords.split(",")
		details = []
		for data in keywords:

			print("datas",data)
			aso = AmazonScraper(locale="UK")
			proxy_handler = CProxy(1,0)
			current_proxy = proxy_handler.get_proxy()
			# values = data.get("values","")[0]
			aso.proxies.update({"https":current_proxy})
			res = None
			retry = 0
			proxies_not_working = False
			current_url = data
			if len(data)< 12:
				current_url = make_amazon_url(data)
				print("sku url ",current_url)
			while res is None or aso.is_captcha_in_response:
				print("inside while"," res: ",res," is_captcha_in_response:",aso.is_captcha_in_response)
				if retry >= 5:
					print("I think proxies are not working")
					proxies_not_working = True
					break
				start_time = get_current_time()
				print("scraping: ",current_url)
				print("proxy in use: ",current_proxy)

				res = aso.scrape(current_url)
				print("inside while"," res: ",res," is_captcha_in_response:",aso.is_captcha_in_response)
				time_diff = get_time_diff_from_now(start_time) 
				if aso.is_captcha_in_response:
					print("response headers",aso.response.headers)
					time.sleep(5)
					current_proxy = proxy_handler.get_proxy()
					# aso.proxies.update({"https":current_proxy})
					aso.change_proxy(current_proxy)
					retry += 1
					continue
				if time_diff>3:
					
					current_proxy = proxy_handler.get_proxy()
					# aso.proxies.update({"https":current_proxy})
					aso.change_proxy(current_proxy)
			if proxies_not_working:
				print("proxies are not working so exiting")
				
			# res = aso.scrape(make_amazon_url(amazon_sku))
			detail={}
			detail["price"] = res.get("price","")
			detail["in_stock"] = res.get("in_stock",True)
			detail["is_prime"] = res.get("is_prime",0)
			detail["title"] = res.get("title","")
			detail["url"] = current_url
			details.append(detail)
			print("response_dict:",res)
		return Response({"details":details})

class PendingEbayItems(LoginRequiredMixin,TemplateView):
	template_name = "pending_ebay_items.html"

class InsertPendingEbayItems(LoginRequiredMixin,views.APIView):

	def post(self, request, *args, **kwargs):
		print("request data",request.data)
		pending_items = request.data
		seller_id = get_seller_name(request)

		try:
			if pending_items[0]["title"]:
				for item in pending_items:
					pend = EbaySellerSearchPendingItems.objects.filter(title=item["title"],seller_account_id = seller_id)
					if not pend:
						price = item["price"].replace("$","")
						pending_set = EbaySellerSearchPendingItems(seller_account_id = seller_id,run_id="",seller_id="",title=item["title"],price_str=0,ebay_url="",item_sold="",amazon_url=item["url"],amazon_price_str=price)
						pending_set.save()
		except:
			print("in except")
			for items in pending_items:
				item = EbaySellerSearch.objects.get(pk=items)
				item_update = EbaySellerSearch.objects.filter(pk=items)
				item_update.update(added_to_pending=True)
				print(item.price_str)
				print(item.ebay_url)
				pend = EbaySellerSearchPendingItems.objects.filter(title=item.title,seller_account_id = seller_id)
				if not pend:
					pending_set = EbaySellerSearchPendingItems(seller_account_id = seller_id,run_id=item.run_id,seller_id=item.seller_id,title=item.title,price_str=item.price_str,ebay_url=item.ebay_url,item_sold=item.item_sold,amazon_url=item.amazon_url,amazon_price_str=item.amazon_price_str)
					pending_set.save()
		# pend = EbaySellerSearchPendingItems.objects.all()

		# for i in pend:
		#	 print("fsd111111111111111111111",i.title)
		# pend.delete()

		res={"ok":"ok"}
	
		return Response(res)

class GetPendingItemsView(LoginRequiredMixin,views.APIView):
	def get(self,request):
		items_list = []
		res = {}
		keyword=request.query_params.get("keyword","")
		page = request.query_params.get('page',1)
		order_by = request.query_params.get('order_by',None)
		seller_account_id = get_seller_name(request)
		ebay_obj = EbaySellerSearchPendingItems.objects.filter(seller_account_id = seller_account_id)
		if(keyword):
			ebay_sellers = ebay_obj.filter(Q(seller_id__icontains=keyword)|Q(title__icontains=keyword))
		else:
			ebay_sellers = ebay_obj
		if order_by is not None and len(order_by)>0:
			order_by_value = ""
			if order_by == "title":
				order_by_value = "title"
			elif order_by == "highestprice":
				order_by_value = "-price_str"
			elif order_by == "lowestprice":
				order_by_value = "price_str"
			ebay_sellers = ebay_sellers.order_by(order_by_value)

		paginator = Paginator(ebay_sellers, 20)
		try:
				page = int(page)
				ebay_sellers = paginator.page(page)
		except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				ebay_sellers = paginator.page(1)
		except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				ebay_sellers = paginator.page(paginator.num_pages)
		l=0
		if ebay_sellers and len(ebay_sellers)>0:
			l = 1
		# ebay_sellers = EbaySellerSearch.objects.all()
		if ebay_sellers and len(ebay_sellers)>0:
			for es in ebay_sellers:
				current_item = {}
				current_item["ebay_url"] = es.ebay_url
				current_item["title"] = es.title
				current_item["price"] = es.price_str
				current_item["item_sold"] = es.item_sold
				current_item["amazon_url"] = es.amazon_url
				current_item["amazon_price_str"] = es.amazon_price_str
				current_item["pk"] = es.pk
				items_list.append(current_item)
		l += 1
		res["items_list"] = items_list
		res["has_previous"] = ebay_sellers.has_previous()
		res["has_next"] = ebay_sellers.has_next()
		if ebay_sellers.has_previous():
			res["previous_page_number"] = ebay_sellers.previous_page_number()
		else:
			res["previous_page_number"] = -1
		if ebay_sellers.has_next():
			res["next_page_number"] = ebay_sellers.next_page_number()
		else:
			res["next_page_number"] = -1
		res["current_page_number"] = ebay_sellers.number
		res["total_page"] = ebay_sellers.paginator.num_pages
		print("total_page",res["total_page"])
		return Response(res)

class UpdateEbayItems(LoginRequiredMixin,CsrfExemptMixin,views.APIView):
	authentication_classes = (UnsafeSessionAuthentication,)
	def post(self, request, *args, **kwargs):
		response_dict = {}
		datas = request.data["values"]
		print("datas",datas)
		aso = AmazonScraper(locale="UK")
		proxy_handler = CProxy(1,0)
		current_proxy = proxy_handler.get_proxy()
		for data in datas:
			# values = data.get("values","")[0]
			ebay_id=data.get("ebay_id","")
			item_obj = EbaySellerItems.objects.get(ebay_id=ebay_id)
			custom_stock = item_obj.stock_level
			if item_obj.status == "ignored":
				continue
			amazon_sku=data.get("amazon_sku","")
			if(amazon_sku==""):
				continue
			aso.proxies.update({"https":current_proxy})
			res = None
			retry = 0
			proxies_not_working = False
			current_url = make_amazon_url(amazon_sku)
			while res is None or aso.is_captcha_in_response:
				print("inside while"," res: ",res," is_captcha_in_response:",aso.is_captcha_in_response)
				# time.sleep(1)
				if retry >= 5:
					print("I think proxies are not working")
					proxies_not_working = True
					break
				start_time = get_current_time()
				print("scraping: ",current_url)
				print("proxy in use: ",current_proxy)

				res = aso.scrape(current_url)
				print("inside while"," res: ",res," is_captcha_in_response:",aso.is_captcha_in_response)
				time_diff = get_time_diff_from_now(start_time) 
				if aso.is_captcha_in_response:
					print("response headers",aso.response.headers)
					time.sleep(5)
					current_proxy = proxy_handler.get_proxy()
					# aso.proxies.update({"https":current_proxy})
					aso.change_proxy(current_proxy)
					retry += 1
					continue
				if time_diff>3:
					
					current_proxy = proxy_handler.get_proxy()
					# aso.proxies.update({"https":current_proxy})
					aso.change_proxy(current_proxy)
			if proxies_not_working:
				print("proxies are not working so exiting")
				break
			# res = aso.scrape(make_amazon_url(amazon_sku))
			price_str = res.get("price","")
			if price_str == "" or len(price_str)== 0:
				update_obj=EbaySellerItems.objects.filter(ebay_id=ebay_id).update(status="unmonitored")
				
			in_stock_str = res.get("in_stock",True)
			is_prime = res.get("is_prime",0)
			is_eligible,price_str,stock_str = is_eligible_for_ebay_update(price_str,in_stock_str,is_prime,custom_stock)
			print("is_eligible",is_eligible,price_str,stock_str)
			if is_eligible:
				if stock_str is not "0" and len(price_str)>0:
					ebay_custom = EbaySellerItems.objects.get(ebay_id=ebay_id)
					formula_obj=EbayPriceFormula.objects.all().first()
					cost = float(price_str)
					if ebay_custom.margin_perc:
						margin_perc = ebay_custom.margin_perc * cost/100
					else:
						margin_perc = formula_obj.perc_margin * cost/100
					if ebay_custom.minimum_margin:
						fixed_margin = ebay_custom.minimum_margin
					else:	
						fixed_margin = formula_obj.fixed_margin
					if margin_perc<fixed_margin:
						cost1 = cost+formula_obj.ebay_listing_fee+fixed_margin+ formula_obj.paypal_fees_fixed
					else:
						cost1 = cost+formula_obj.ebay_listing_fee+margin_perc+ formula_obj.paypal_fees_fixed
					p = 1-((formula_obj.ebay_final_value_fee + formula_obj.paypal_fees_perc)/100)
					cost_after_profit = cost1/p
			price_info	= {}
			item={}
			if stock_str != "0" and len(price_str)>0 and is_prime == True:
				item["StartPrice"] = get_float(cost_after_profit)
				item["Quantity"] = stock_str
				print("new price ",cost_after_profit)
			else:
				item["Quantity"] = "0"
			price_info["Item"] = item
			# cost_after_profit=0
			
			ebayhandler = EbayHandler()
			item["ItemID"] = ebay_id

			is_updated = ebayhandler.set_item_price(item_price_dict = price_info)
			response_dict["is_updated"] = is_updated
			response_dict["item"] = item
			print("is_ updated",is_updated)
			if is_updated:
				current_ebay_item = EbaySellerItems.objects.filter(ebay_id=ebay_id).first()
				try:
					current_ebay_item.price = str(get_float(cost_after_profit))
				except:
					pass
				current_ebay_item.quantity = item["Quantity"]
				current_ebay_item.save()
				print("current_ebay_item",current_ebay_item)
		return Response(response_dict)


class EditEbayItems(LoginRequiredMixin,TemplateView):
	template_name = "edit_ebay_items.html"
	def get(self, request, *args, **kwargs):
		print(dir(request))
		datas = request.data
		res={}
		for data in datas:
			print("edit ebay_item",data)
			res["ebay_id"]="fsfsa"
		return res

class EditAAAaa(LoginRequiredMixin,UpdateView):
		template_name = "form_price_formula.html"
		model = EbayPriceFormula
		success_url = '/'
		# form_class = UserProfileForm
		fields = ['ebay_final_value_fee','ebay_listing_fee','paypal_fees_perc','paypal_fees_fixed','perc_margin','fixed_margin']
		# f

class EditEbayItems1(LoginRequiredMixin,views.APIView):
	authentication_classes = (UnsafeSessionAuthentication,)
	def get(self, request, *args, **kwargs):
		datas = request.data
		res={}
		for data in datas:
			print("edit ebay_item",data)
			ebay_id=data.get("ebay_id","")
			# is_updated = ebayhandler.set_item_price(item_price_dict = price_info)

			# res={}
			# res["is_updated"] = is_updated
			# res["item"] = item
			# print("is_ updated",is_updated)
			# if is_updated:
			#	 current_ebay_item = EbaySellerItems.objects.filter(ebay_id=ebay_id).first()
			#	 current_ebay_item.price = str(get_float(cost_after_profit))
			#	 current_ebay_item.quantity = item["Quantity"]
			#	 current_ebay_item.save()
			#	 print("current_ebay_item",current_ebay_item)
		return Response(res)

class EbayFileUploadView(LoginRequiredMixin,TemplateView):
		template_name = "csv_upload.html"

		def handle_uploaded_file(self,f):
			with open('name.csv', 'wb+') as destination:
				for chunk in f.chunks():
						destination.write(chunk)

		def post(self, request, *args, **kwargs):
			f = request.FILES.getlist('files')[0]
			self.handle_uploaded_file(f)
			put_ebay_products_to_db.delay("name.csv")
			return HttpResponseRedirect('/')


class SearchSellerView(LoginRequiredMixin,TemplateView):
	template_name = "search_seller.html"
	# def post(self, request, *args, **kwargs):
			# proxies = request.FILES.getlist('proxies')
			# report_id = self.kwargs("pk")
			# return render(request,"search_seller.html",{"report_id":report_id})

class SearchSellerItemView(LoginRequiredMixin,TemplateView):
	template_name = "search_seller_item.html"

class SearchSellerNameView(LoginRequiredMixin,views.APIView):
	def get(self,request):
		items_list = []
		res = {}
		keyword=request.query_params.get("keyword","")
		report_id=request.query_params.get("report_id","")
		page = request.query_params.get('page',1)
		order_by = request.query_params.get('order_by',None)
		page_by = request.query_params.get('page_by',50)
		page_by = int(page_by)
		seller_account_id = get_seller_name(request)
		if len(report_id)>0:
			print("report id.............",report_id)
			report_id = int(report_id)
		ebay_search_obj = EbaySellerSearch.objects.filter(search_report_id = report_id,search_report__seller_account_id = seller_account_id)
		if(keyword):
			ebay_sellers = ebay_search_obj.filter(Q(seller_id__icontains=keyword)|Q(title__icontains=keyword))
		else:
			ebay_sellers = ebay_search_obj
		

		if order_by is not None and len(order_by)>0:
			order_by_value = ""
			if order_by == "title":
				order_by_value = "title"
			elif order_by == "highestprice":
				order_by_value = "-price_str"
			elif order_by == "lowestprice":
				order_by_value = "price_str"
			ebay_sellers = ebay_sellers.order_by(order_by_value)

		paginator = Paginator(ebay_sellers, page_by)
		try:
				page = int(page)
				ebay_sellers = paginator.page(page)
		except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				ebay_sellers = paginator.page(1)
		except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				ebay_sellers = paginator.page(paginator.num_pages)
		l=0
		if ebay_sellers and len(ebay_sellers)>0:
			l = 1
		if ebay_sellers and len(ebay_sellers)>0:
			for es in ebay_sellers:
				current_item = {}
				current_item["ebay_url"] = es.ebay_url
				current_item["title"] = es.title
				current_item["price"] = es.price_str
				current_item["item_sold"] = es.item_sold
				current_item["amazon_url"] = es.amazon_url
				current_item["amazon_price_str"] = es.amazon_price_str
				current_item["pk"] = es.pk
				current_item["added_to_pending"] = es.added_to_pending
				if not current_item["added_to_pending"]:
					current_item["added_to_pending"] = 'No'
				else:
					current_item["added_to_pending"] = 'Yes'
				items_list.append(current_item)
		l += 1
		res["items_list"] = items_list
		res["has_previous"] = ebay_sellers.has_previous()
		res["has_next"] = ebay_sellers.has_next()
		if ebay_sellers.has_previous():
			res["previous_page_number"] = ebay_sellers.previous_page_number()
		else:
			res["previous_page_number"] = -1
		if ebay_sellers.has_next():
			res["next_page_number"] = ebay_sellers.next_page_number()
		else:
			res["next_page_number"] = -1
		res["current_page_number"] = ebay_sellers.number
		res["total_page"] = ebay_sellers.paginator.num_pages
		print("total_page",res["total_page"])
		return Response(res)

class ExportCsvSellerItems(LoginRequiredMixin,views.APIView):
	def get(self,request):
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="ebay.csv"'
		seller_id = get_seller_name(request)
		ebay_items = EbaySellerItems.objects.filter(seller_id = seller_id)
		items = []
		writer = csv.writer(response)
		writer.writerow(['Item description','Ebay item number', 'Price','Quantity', 'Custom Label','Status'])

		for item in ebay_items:
			each_item = {}
			each_item["title"] = item.product_name
			each_item["ebay_id"] = item.ebay_id	
			each_item["price"] = item.price	
			each_item["quantity"] = item.quantity	
			each_item["custom_label"] = item.custom_label	
			each_item["status"] = item.status	
			writer.writerow([each_item["title"],each_item["ebay_id"],each_item["price"],each_item["quantity"],each_item["custom_label"],each_item["status"]])
		return response


class SearchSellerItemNameView2(LoginRequiredMixin,views.APIView):
	def get(self,request):
		seller_id = get_seller_name(request)
		
		#input params
		query_list = request.query_params
		
		search_keyword = query_list.get("keyword",None)
		page = query_list.get("page",1)
		order_by = query_list.get("order_by",None)
		status = query_list.get("status",None)
		items_per_page = query_list.get("page_by",None)

		print("items_per_page",items_per_page)

		result_set = EbaySellerItems.objects.filter(pk__gt=0,seller_id = seller_id)
		print("search_keyword",search_keyword)
		if search_keyword:
			result_set = result_set.filter(Q(ebay_id__icontains=search_keyword)|Q(custom_label__icontains=search_keyword)|Q(product_name__icontains=search_keyword))
			print("result_set",result_set)
		count_status = result_set.values("status").annotate(total = Count('status'))

		if status:
			print("status",status)
			result_set = result_set.filter(status=status)


		if order_by:
			order_by_value = ""
			if order_by == "title":
				order_by_value = "product_name"
			elif order_by == "highestprice":
				order_by_value = "-price"
			elif order_by == "lowestprice":
				order_by_value = "price"
			result_set = result_set.order_by(order_by_value)

		if items_per_page:
			try:
				items_per_page = int(items_per_page)
			except:
				items_per_page = 20
		else:
			items_per_page = 20

		paginator = Paginator(result_set, items_per_page)
		
		try:
				page = int(page)
				result_set = paginator.page(page)
		except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				result_set = paginator.page(1)
		except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				result_set = paginator.page(paginator.num_pages)

		response = {}
		l = 1
		for es in result_set:
			current_item = {}
			current_item["item_id"] = (page-1)*items_per_page+l
			current_item["ebay_id"] = es.ebay_id
			current_item["ebay_url"] = "https://www.ebay.com/itm/"+str(es.ebay_id)
			current_item["amazon_url"] = "https://amazon.com/dp/"+str(es.custom_label)
			current_item["photo"] = es.photo
			current_item["custom_label"] = es.custom_label
			current_item["product_name"] = es.product_name
			current_item["last_updated"] = es.get_modified_date()
			current_item["price"] = es.price
			current_item["quantity"] = es.quantity
			current_item["no_of_times_sold"] = es.no_of_times_sold
			current_item["date_of_listing"] = es.date_of_listing
			current_item["margin_perc"] = es.margin_perc
			current_item["minimum_margin"] = es.minimum_margin
			current_item["stock_level"] = es.stock_level
			current_item["status"] = es.status
			if es.status in response:
				response[es.status]["items_list"].append(current_item)
			else:
				response[es.status] = {"items_list":[current_item]}
			# items_list.append(current_item)
			l += 1

		response["count_status"] = count_status
		response["has_previous"] = result_set.has_previous()
		response["has_next"] = result_set.has_next()
		if result_set.has_previous():
			response["previous_page_number"] = result_set.previous_page_number()
		else:
			response["previous_page_number"] = -1
		if result_set.has_next():
			response["next_page_number"] = result_set.next_page_number()
		else:
			response["next_page_number"] = -1
		response["current_page_number"] = result_set.number
		response["total_page"] = result_set.paginator.num_pages
		print("page_by",items_per_page)
		return Response(response)


class SearchSellerItemNameView(LoginRequiredMixin,views.APIView):
	def get(self,request):
		seller_id = get_seller_name(request)
		items_list = []
		res = {}
		keyword=request.query_params.get("keyword","")
		page = request.query_params.get('page',1)
		order_by = request.query_params.get('order_by',None)
		print("page_number",page)
		ebay_items_obj = EbaySellerItems.objects.filter(seller_id=seller_id)
		if(keyword):
			ebay_items = ebay_items_obj.filter(Q(ebay_id__icontains=keyword)|Q(custom_label__icontains=keyword)|Q(product_name__icontains=keyword))
		else:
			ebay_items = ebay_items_obj

		count_status = ebay_items.values("status").annotate(total = Count('status'))
		if order_by is not None and len(order_by)>0:
			order_by_value = ""
			if order_by == "title":
				order_by_value = "product_name"
			elif order_by == "highestprice":
				order_by_value = "-price"
			elif order_by == "lowestprice":
				order_by_value = "price"
			print("order_by_value",order_by_value)
			ebay_items = ebay_items.order_by(order_by_value)

		paginator = Paginator(ebay_items, 50)
		try:
				page = int(page)
				ebay_items = paginator.page(page)
		except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				ebay_items = paginator.page(1)
		except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				ebay_items = paginator.page(paginator.num_pages)
		if ebay_items and len(ebay_items)>0:
			l = 1
			for es in ebay_items:
				current_item = {}
				current_item["item_id"] = (page-1)*50+l
				current_item["ebay_id"] = es.ebay_id
				current_item["ebay_url"] = "https://www.ebay.com/itm/"+str(es.ebay_id)
				current_item["amazon_url"] = "https://amazon.com/dp/"+str(es.custom_label)
				current_item["photo"] = es.photo
				current_item["custom_label"] = es.custom_label
				current_item["product_name"] = es.product_name
				current_item["price"] = es.price
				current_item["quantity"] = es.quantity
				current_item["no_of_times_sold"] = es.no_of_times_sold
				current_item["date_of_listing"] = es.date_of_listing
				current_item["margin_perc"] = es.margin_perc
				current_item["minimum_margin"] = es.minimum_margin
				current_item["stock_level"] = es.stock_level
				current_item["flag"] = es.flag
				items_list.append(current_item)
				l += 1
		res["count_status"] = count_status
		res["items_list"] = items_list
		res["has_previous"] = ebay_items.has_previous()
		res["has_next"] = ebay_items.has_next()
		if ebay_items.has_previous():
			res["previous_page_number"] = ebay_items.previous_page_number()
		else:
			res["previous_page_number"] = -1
		if ebay_items.has_next():
			res["next_page_number"] = ebay_items.next_page_number()
		else:
			res["next_page_number"] = -1
		res["current_page_number"] = ebay_items.number
		res["total_page"] = ebay_items.paginator.num_pages
		return Response(res)

class InsertEbaySellerItems(LoginRequiredMixin,views.APIView):
	def get(self,request):
		seller_id = get_seller_name(request)
		sync_db_to_ebay.delay(seller_id)
		return Response("ok")

class DashboardValuesView(LoginRequiredMixin,views.APIView):
		def get(self,request):
			dashboard_values = {}
			proxy_count = Proxy.objects.filter(is_active=1).count()
			dashboard_values["proxy_count"] = proxy_count
			return Response(dashboard_values)

class StartSellerSearch(LoginRequiredMixin,views.APIView):
	def get(self,request,seller_id):
		print("seller_id:",seller_id)
		# os.system("nohup celery -A ui worker -c 1 > cc.out 2> cc.err &")
		seller_account_id = get_seller_name(self.request)
		reports = EbaySellerSearchReports()
		reports.seller_id = seller_id
		reports.status = "queued"
		reports.seller_account_id = seller_account_id
		reports.save()
		obj = EbaySellerSearchReports.objects.latest('date_of_search')
		start_ebay_seller_search2.delay(seller_id,obj.pk)
		# start_ebay_seller_search2.delay(seller_id)

		return Response({"message":"Search is being processed. Kindly wait and refresh url to check the status of your search."})

class DownloadEbayCsv(LoginRequiredMixin,views.APIView):
		def get(self,request):
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="ebay.csv"'
			latest_run_id = AmazonRun.objects.latest('run_start_time')
			if latest_run_id:
				print("latest_run_id:",latest_run_id.run_id)
				# ebay_list = EbayRunDetails.objects.filter(run_id=latest_run_id.run_id)
				ebay_list = EbayRunDetails.objects.all()
				if ebay_list:
					writer = csv.writer(response)
					writer.writerow(['Run Id','Group Id','Amazon Url','Amazon Price','Amazon Stock','Ebay Price','Ebay Update','Cause If Fail','Ebay Url','Ebay Id'])
					for e in ebay_list:
						run_id = e.run_id
						group_id = e.group_id
						amazon_url = e.amazon_url
						price_str = e.price_str
						clear_price = re.findall("[0-9.]+",price_str)
						if len(clear_price)>0:
							try:
								price_str = str(float("".join(clear_price)))
							except:
								pass
						in_stock_str = e.in_stock_str
						ebay_price = e.ebay_price
						is_ebay_updated = e.is_ebay_updated
						cause_if_fail = e.cause_if_fail
						ebay_url = e.ebay_url
						ebay_id = e.ebay_id
						writer.writerow([run_id,group_id,amazon_url,price_str,in_stock_str,ebay_price,is_ebay_updated,cause_if_fail,ebay_url,ebay_id])
			return response



def scrape_amazon(request):
		html = "<html><body>It is now %s.</body></html>" % now
		return HttpResponse(html)

class InitRunDetails(views.APIView):
	def get(self,request):
			AmazonRunDetails.objects.all().delete()
			amazon_url_list = EbayProductsCsvData.objects.all()
			for row in amazon_url_list:
				new_amazon_details_object = AmazonRunDetails()
				new_amazon_details_object.amazon_url = normalize_amazon_url(row.vendor_url)
				new_amazon_details_object.ebay_id = row.reference.split("hydra")[1].strip()
				new_amazon_details_object.save()
			return Response({"message":"init started"})

class ResetForNewRun(views.APIView):
	def get(self,request):
			# AmazonRunDetails.objects.all().delete()
			EbayRunDetails.objects.all().delete()
			ProxyLog.objects.all().delete()
			return Response({"message":"all tables are reset"})

class StartProcess(views.APIView):
	#check amazon instance running or not
	def get(self,request):	
			all_updated_instances1 = AmazonRunDetails.objects.exclude(run_id="").count()
			print("all_updated_instances1:",all_updated_instances1)
			all_ebay_updated_instances1 = EbayRunDetails.objects.all().count()
			print("all_ebay_updated_instances1:",all_ebay_updated_instances1)
			time.sleep(30)
			all_updated_instances2 = AmazonRunDetails.objects.exclude(run_id="").count()
			print("all_updated_instances2:",all_updated_instances2)
			all_ebay_updated_instances2 = EbayRunDetails.objects.all().count()
			print("all_ebay_updated_instances2:",all_ebay_updated_instances2)
			if all_updated_instances1 == all_updated_instances2:
				# scrape_amazon_urls()
				print("started amazon scraper")
			if all_updated_instances1 == all_updated_instances2:
				start_ebay_process()
				print("started ebay process")
			return Response({"message":"process started"})

class ShutdownCeleryInstance(views.APIView):
	def get(self,request):
		os.system("ps -ef | grep 'celery' | grep -v grep | awk '{print $2}' | xargs kill -9")
		return Response({"message":"all celery instance killed"})

class StartCeleryInstance(views.APIView):
	def get(self,request,process):
		print("no of process:",process)
		os.system("ps -ef | grep 'celery' | grep -v grep | awk '{print $2}' | xargs kill -9")
		os.system("nohup celery -A ui worker -c "+str(process)+" > cc.out 2> cc.err &")
		return Response({"message":"all celery instance started"})

# class AmazonEbayFormula(LoginRequiredMixin,TemplateView):
# 		template_name = "form_price_formula.html"
# 		def get_context_data(self, **kwargs):
# 				seller_id = get_seller_name(self.request)
# 				context = super(AmazonEbayFormula, self).get_context_data(**kwargs)
# 				price_formula = EbayPriceFormula.objects.get(seller_id = seller_id)
# 				context['price_formula'] = price_formula
# 				return context

class AmazonEbayFormula(LoginRequiredMixin,TemplateView):
		template_name = "form_price_formula.html"
		def get(self,request, **kwargs):
				seller_id = get_seller_name(self.request)
				context = {}
				price_formula = {}
				# context = super(AmazonEbayFormula, self).get_context_data(**kwargs)
				obj = EbayPriceFormula.objects.get(seller_id = seller_id)
				# print("objjjjjjjjjjj",obj.pk,obj.ebay_listing_fee)
				context['price_formula'] = obj
				# print("contect...",context)
				# price_formula["ebay_final_value_fee"] = obj.ebay_final_value_fee
				return render(request,"form_price_formula.html",context)

		def post(self,request, **kwargs):
			print("request",request.POST)
			formula = request.POST.dict()
			pk = formula.get("pk","")
			formula.pop('pk', None)
			formula.pop('csrfmiddlewaretoken', None)
			EbayPriceFormula.objects.filter(pk = pk).update(**formula)
			return redirect('price-formula')



# class UpdateAmazonEbayFormula(LoginRequiredMixin,UpdateView):
# 		template_name = "form_price_formula.html"
# 		model = EbayPriceFormula
# 		success_url = '/'
# 		fields = ['seller','ebay_final_value_fee','ebay_listing_fee','paypal_fees_perc','paypal_fees_fixed','perc_margin','fixed_margin']




		

class AddEbaySellerItems(LoginRequiredMixin,CreateView):

	def get(self, request, *args, **kwargs):
		ebay_id = request.query_params.get("ebay_id","")
		product_name = request.query_params.get("product_name","")
		custom_label = request.query_params.get("custom_label","")
		price = request.query_params.get("price","")
		quantity = request.query_params.get("quantity","")
		no_of_times_sold = request.query_params.get("no_of_times_sold","")
		date_of_listing = request.query_params.get("date_of_listing","")
		response = {}
		item, created = EbaySellerItems.objects.get_or_create()
		print(model_to_dict(item))
		item.seller_id = get_seller_name(request)
		item.ebay_id=ebay_id
		item.product_name = product_name
		item.custom_label=custom_label
		item.price=price
		item.quantity=quantity
		item.no_of_times_sold=no_of_times_sold
		item.date_of_listing=date_of_listing
		if created:
			response["message"] = "item created successfully"
		else:
			response["message"] = "not successful"		


class ProxyLoaderView(LoginRequiredMixin,TemplateView):
		template_name = "proxy_loader.html"

		def post(self, request, *args, **kwargs):
			# proxies = request.FILES.getlist('proxies')
			proxies = request.POST['proxies']
			if proxies and len(proxies)>0:
				proxy_list = proxies.split("\n")
				proxy_list = [p.strip() for p in proxy_list if len(p.strip())>0]
				if len(proxy_list)>0:
					for prx in proxy_list:
						prxy = Proxy()
						prxy.proxy = prx
						prxy.save()
			return HttpResponseRedirect('/')

class SetItemMarginView(LoginRequiredMixin,views.APIView):
	def post(self, request, *args, **kwargs):
		margin_perc = request.POST["margin_percent"]
		min_margin = request.POST["margin_value"]
		ebay_id = request.POST["ebay_id"]
		if not margin_perc:
			margin_perc = None
		if not min_margin:
			min_margin = None
		update_obj=EbaySellerItems.objects.filter(ebay_id=ebay_id).update(margin_perc=margin_perc,minimum_margin=min_margin)
		return render(request,"search_seller_item.html",{"ok":"ok"})

class SetItemStockLevelView(LoginRequiredMixin,views.APIView):
	def post(self, request, *args, **kwargs):
		stock_level = request.POST["stock_level"]
		print("stock_level",stock_level)
		ebay_id = request.POST["ebay_id_stock"]
		if stock_level:
			update_obj=EbaySellerItems.objects.filter(ebay_id=ebay_id).update(stock_level=stock_level)
		else:
			update_obj=EbaySellerItems.objects.filter(ebay_id=ebay_id).update(stock_level=None)
		print(EbaySellerItems.objects.get(ebay_id=ebay_id).stock_level)
		return render(request,"search_seller_item.html",{"ok":"ok"})


class FlagSellerItems(LoginRequiredMixin,views.APIView):
	authentication_classes = (UnsafeSessionAuthentication,)

	def post(self, request, *args, **kwargs):
		values = request.data["values"]
		print("ebay_ids",request.data["values"])
		if values:
			for value in values:
				status = value["status"]
				if status == "monitored":
					flag_value = "ignored"
				elif status == "unmonitored":
					flag_value = "ignored"	
				if status == "ignored":
					flag_value = "monitored"

				update_obj=EbaySellerItems.objects.filter(ebay_id=value["ebay_id"]).update(status=flag_value)
		else:
			pass
		return Response({"ok":"ok"})

# class UpdateAllEbayItems(CsrfExemptMixin,views.APIView):
#	 authentication_classes = (UnsafeSessionAuthentication,)
#	 def get(self, request, *args, **kwargs):
#		 all_ebay_items = EbaySellerItems.objects.filter(status__in=["monitored","unmonitored"])
#		 if len(all_ebay_items)>0:
#			 aso = AmazonScraper(locale="UK")
#			 proxy_handler = CProxy(1,0)
#			 current_proxy = proxy_handler.get_proxy()
#			 aso.proxies.update({"https":current_proxy})
#			 ebayhandler = EbayHandler()
#			 formula_obj=EbayPriceFormula.objects.all().first()
#			 response = {}
#			 print("current_proxy",current_proxy)

#			 for ebay_item in all_ebay_items:
#				 # ebay_item = EbaySellerItems.objects.get(ebay_id='263288531740')
#				 item_info_to_update_on_ebay = {}
#				 item_info_to_update_on_ebay["ItemID"] = ebay_item.ebay_id
#				 print("ebay url","https://www.ebay.com/itm/"+str(ebay_item.ebay_id))
#				 price_info = {"Item":item_info_to_update_on_ebay}

#				 if len(ebay_item.custom_label)>0:
#					 amazon_url = make_amazon_url(ebay_item.custom_label)
#					 retry = 0
#					 res = None
#					 while res is None or "503" in res or aso.is_captcha_in_response:
#						 res = aso.scrape_with_error(amazon_url)
#						 print("scraping with error")
#						 if aso.is_captcha_in_response or "503" in res:
#							 current_proxy = proxy_handler.get_proxy()
#							 aso.change_proxy(current_proxy)
#							 retry += 1
#						 if retry == 5:
#							 print("I think proxies are not working")
#							 break

#					 if is_eligible_for_out_of_stock(res):
#						 print("inside is_eligible_for_out_of_stock",res,"ebay_id",ebay_item.ebay_id)
#						 # input("inside is_eligible_for_out_of_stock")
#						 item_info_to_update_on_ebay["Quantity"] = "0"
#						 is_updated = ebayhandler.set_item_price(item_price_dict = price_info)
#						 ebay_item.status = "unmonitored"
#						 ebay_item.save()
#						 continue
#					 else:
#						 final_cost = get_final_cost(ebay_item,formula_obj,res)
#						 final_stock = get_final_stock(ebay_item.stock_level)
#						 print("final_cost",final_cost,"final_stock",final_stock)
#						 item_info_to_update_on_ebay["Quantity"] = ebay_item.quantity = final_stock
#						 item_info_to_update_on_ebay["StartPrice"] = ebay_item.price = final_cost
#						 is_updated = ebayhandler.set_item_price(item_price_dict = price_info)
#						 ebay_item.status = "monitored"
#						 ebay_item.save()
#				 # break		

#		 response["message"] = "process finished"
#		 return Response(response)


class UpdateAllEbayItems(LoginRequiredMixin,CsrfExemptMixin,views.APIView):
  authentication_classes = (UnsafeSessionAuthentication,)
  def get(self, request, *args, **kwargs):
    ebay_price_updater.delay()
    response = {}
    response["message"] = "prices are being updated"
    return Response(response)


class UpdateAllEbayItems2(LoginRequiredMixin,CsrfExemptMixin,views.APIView):
	authentication_classes = (UnsafeSessionAuthentication,)
	def post(self, request, *args, **kwargs):
		seller_account_id = get_seller_name(request)
		response_dict = {}
		# datas = request.data["values"]
		aso = AmazonScraper(locale="UK")
		proxy_handler = CProxy(1,0)
		datas = EbaySellerItems.objects.filter(seller_id = seller_account_id)

		current_proxy = proxy_handler.get_proxy()
		for item_obj in datas:
			print("item_obj",item_obj)
			ebay_id=item_obj.ebay_id
			# item_obj = EbaySellerItems.objects.get(ebay_id=ebay_id)
			custom_stock = item_obj.stock_level
			if item_obj.status == "ignored":
				continue
			amazon_sku=item_obj.custom_label
			if(amazon_sku==""):
				continue
			aso.proxies.update({"https":current_proxy})
			res = None
			retry = 0
			proxies_not_working = False
			current_url = make_amazon_url(amazon_sku)
			while res is None or aso.is_captcha_in_response:
				print("inside while"," res: ",res," is_captcha_in_response:",aso.is_captcha_in_response)
				# time.sleep(1)
				if retry >= 5:
					print("I think proxies are not working")
					proxies_not_working = True
					break
				start_time = get_current_time()
				print("scraping: ",current_url)
				print("proxy in use: ",current_proxy)

				res = aso.scrape(current_url)
				print("inside while"," res: ",res," is_captcha_in_response:",aso.is_captcha_in_response)
				time_diff = get_time_diff_from_now(start_time) 
				if aso.is_captcha_in_response:
					print("response headers",aso.response.headers)
					time.sleep(5)
					current_proxy = proxy_handler.get_proxy()
					# aso.proxies.update({"https":current_proxy})
					aso.change_proxy(current_proxy)
					retry += 1
					continue
				if time_diff>3:
					
					current_proxy = proxy_handler.get_proxy()
					# aso.proxies.update({"https":current_proxy})
					aso.change_proxy(current_proxy)
			if proxies_not_working:
				print("proxies are not working so exiting")
				break
			# res = aso.scrape(make_amazon_url(amazon_sku))
			price_str = res.get("price","")
			if price_str == "" or len(price_str)== 0:
				update_obj=EbaySellerItems.objects.filter(ebay_id=ebay_id).update(status="unmonitored")
				
			in_stock_str = res.get("in_stock",True)
			is_prime = res.get("is_prime",0)
			is_eligible,price_str,stock_str = is_eligible_for_ebay_update(price_str,in_stock_str,is_prime,custom_stock)
			print("is_eligible",is_eligible,price_str,stock_str)
			if is_eligible:
				if stock_str is not "0" and len(price_str)>0:
					ebay_custom = EbaySellerItems.objects.get(ebay_id=ebay_id)
					formula_obj=EbayPriceFormula.objects.all().first()
					cost = float(price_str)
					if ebay_custom.margin_perc:
						margin_perc = ebay_custom.margin_perc * cost/100
					else:
						margin_perc = formula_obj.perc_margin * cost/100
					if ebay_custom.minimum_margin:
						fixed_margin = ebay_custom.minimum_margin
					else:	
						fixed_margin = formula_obj.fixed_margin
					if margin_perc<fixed_margin:
						cost1 = cost+formula_obj.ebay_listing_fee+fixed_margin+ formula_obj.paypal_fees_fixed
					else:
						cost1 = cost+formula_obj.ebay_listing_fee+margin_perc+ formula_obj.paypal_fees_fixed
					p = 1-((formula_obj.ebay_final_value_fee + formula_obj.paypal_fees_perc)/100)
					cost_after_profit = cost1/p
			price_info	= {}
			item={}
			if stock_str != "0" and len(price_str)>0 and is_prime == True:
				item["StartPrice"] = get_float(cost_after_profit)
				item["Quantity"] = stock_str
			else:
				item["Quantity"] = "0"
			price_info["Item"] = item

			ebayhandler = EbayHandler()
			item["ItemID"] = ebay_id

			is_updated = ebayhandler.set_item_price(item_price_dict = price_info)
			response_dict["is_updated"] = is_updated
			response_dict["item"] = item
			print("is_ updated",is_updated)
			if is_updated:
				current_ebay_item = EbaySellerItems.objects.filter(ebay_id=ebay_id).first()
				try:
					current_ebay_item.price = str(get_float(cost_after_profit))
				except:
					pass
				current_ebay_item.quantity = item["Quantity"]
				current_ebay_item.save()
				print("current_ebay_item",current_ebay_item)
			# break
		return Response(response_dict)


def create_default_price_formula(sellername):
	seller_id = SellerTokens.objects.get(sellername = sellername).pk
	ebay_formula = EbayPriceFormula(seller_id = seller_id)
	ebay_formula.save()




class EbayConnect(LoginRequiredMixin,views.APIView):
	def get(self,request,*args,**kwargs):
		ebayhandler = EbayHandler()
		sessionId = EbaySessionID.objects.get(pk = 1).session_id
		token = ebayhandler.get_token_id(sessionId)
		res = {}
		sellername = request.query_params["username"]
		res['username'] = sellername
		res['sessionId'] = sessionId
		st_obj = SellerTokens.objects.filter(sellername = sellername)
		if st_obj:
			st_obj.update(token = token)
		else:
			st = SellerTokens()
			st.sellername = sellername
			st.token = token
			st.user = request.user
			st.save()

		create_default_price_formula(sellername)

		return redirect('multi-ebay-account')

class LoginPageToEbay(LoginRequiredMixin,views.APIView):
	def get(self,request,*args,**kwargs):
		ebayhandler = EbayHandler()
		sessionId = ebayhandler.get_session_id()
		session_obj = EbaySessionID.objects.filter(pk = 1)
		if session_obj:
			session_obj.update(session_id = sessionId)
		else:
			session = EbaySessionID()
			session.session_id = sessionId
			session.save()

		url = "https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&runame=Dean_Ku-DeanKu-GDOshipp-xlffprczu&SessID="+sessionId
		return HttpResponseRedirect(url)


class ActivateSellerAccount(LoginRequiredMixin,views.APIView):
	def get(self,request,*args,**kwargs):
		user = request.user
		seller_obj = SellerTokens.objects.filter(user = user)
		st_list = []
		for st in seller_obj:
			st_dict = {}
			st_dict["sellername"] = st.sellername
			st_dict["pk"] = st.pk
			st_dict["is_active"] = st.is_active
			st_list.append(st_dict)

		return Response({'sellers':st_list})

	def post(self,request,*args,**kwargs):
		user = request.user.pk
		seller = SellerTokens.objects.filter(user_id = user)
		seller.update(is_active = False)
		seller.filter(pk = request.data).update(is_active = True)
		seller = SellerTokens.objects.get(pk = request.data)
		data1 = {}
		data1["name"] = seller.pk
		data1["user_id"] = seller.user_id
		data1["is_active"] = seller.is_active
		return Response({'request':data1})

class MultiEbayAccountSettingPage(LoginRequiredMixin,TemplateView):
	template_name = 'multi_ebay_account.html'

class SearchSellerReports(LoginRequiredMixin,TemplateView):
	template_name = 'search_seller_reports.html'

class SearchSellerReportsData(LoginRequiredMixin,views.APIView):
	def get(self,request,*args,**kwargs):
		keyword = ""
		message = ""
		if request.POST:
			keyword = request.POST
		seller_account_id = get_seller_name(request)
		print("seller seller_account_id",seller_account_id)
		report_obj = EbaySellerSearchReports.objects.filter(seller_account_id = seller_account_id).order_by("-date_of_search")
		seller_reports = []
		logger.info("self.request.user.pk",self.request.user.pk)

		for report in report_obj:
			print("report ",report.pk)
			report_dict = {}
			report_dict["seller_id"] = report.seller_id
			report_dict["item_found"] = report.item_found
			report_dict["date_of_search"] = report.date_of_search
			report_dict["status"] = report.status
			report_dict["pk"] = report.pk
			seller_reports.append(report_dict)
		if len(keyword)>0:
			message = "Your search has been queued. You can view your search status below on refresh."
		return Response({"seller_reports":seller_reports,"message":message})

