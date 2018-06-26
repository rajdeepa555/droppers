# Create your tasks here
from __future__ import absolute_import, unicode_literals
import string
from .sync_ebay import insert_data
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import csv
from celery import shared_task
from .models import *
import json
from .log import log_amazon_url,log_proxy
from .utils import normalize_amazon_url
from .proxy import CProxy
from .amazon import CAmazon
import datetime
from .amazonapi import AmazonScraper
import time
import re
from .ebay import EbayHandler

import math
from django.forms.models import model_to_dict
import traceback
from .ebaybot import EbayScraper
from django_rq import job
from .utils import *
from .ebay import *
from .helpers import *
from .parsers import parse_ebay_item
from .price_updater import testing_facade
from .csvfile import get_item_in_csv



def get_seller_token(seller_id):
	obj = SellerTokens.objects.get(pk = seller_id)
	return obj.token

def get_ebay_handler(seller_id):
	print("making ebay handler")
	ebay_obj = EbayHandler()
	ebay_obj.token = get_seller_token(seller_id)
	ebay_obj.update_trading_api()
	return ebay_obj

# @shared_task
# def create_random_user_accounts(total):
#		 for i in range(total):
#				 username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
#				 email = '{}@example.com'.format(username)
#				 password = get_random_string(50)
#				 User.objects.create_user(username=username, email=email, password=password)
#		 return '{} random users created with success!'.format(total)

# aso = AmazonScraper(locale="UK")
@job
def print_time_5times():
	f = open("5times.txt","w")
	x = "-1"
	for i in range(0,6):
		x += str(i)
		time.sleep(2)
	f.write("how are you")
	f.close()
	return "process done"

def get_url(aso,keywords):
	url = ''
	for keyword in keywords:
		if keyword and len(keyword)>0:
			url = aso.get_url_for_keyword(keyword)
			if len(url)>10:
				break
		else:
			continue
	return url

@job
def start_ebay_seller_search2(seller_id,report_id):
	print("fetching records for seller_id:",seller_id)
	report_obj = EbaySellerSearchReports.objects.get(pk = report_id)
	reports = EbaySellerSearchReports.objects.filter(pk = report_id)
	reports.update(status = "processing")
	try:
		if seller_id is not None:
			es = EbayScraper(locale="UK")
			ebay_url = "https://www.ebay.com/sch/%s/m.html?_nkw=&_armrs=1&_ipg=50&_from=" % (seller_id)
			while es.has_next:
				es.get_details = False
				es.response_list = []
				es.scrape(ebay_url)
				ebay_url = es.next_url
				if len(es.response_list)>0:
					try:
						es.get_details = True
						for item in es.response_list:
							if 'watching' in item.get("item_sold","").lower():
								print("watuchfsfsafa",item.get("item_sold","").lower())
								continue
							keywords = []
							price = item.get("price","")
							price = price.replace("$","")
							price = price.replace(",","")
							if price == "":
								price = -1
							current_es = EbaySellerSearch()
							current_es.price_str = float(price)
							current_es.seller_id = seller_id
							current_es.title	= item.get("title","")
							current_es.item_sold = item.get("item_sold","")
							ebay_item_url = item.get("ebay_url","#")
							current_es.ebay_url = ebay_item_url
							upc = ''
							isbn = ''
							if len(ebay_item_url)>1:
								es.scrape(ebay_item_url)
								upc = str(es.upc)
								isbn = str(es.isbn)
								# keywords.append(es.upc)

							aso = AmazonScraper(locale="UK")
							proxy_handler = CProxy(1,0)
							current_proxy = proxy_handler.get_proxy()
							aso.proxies.update({"https":current_proxy})
							res = None
							retry = 0
							proxies_not_working = False
							current_url = ""
							price_str = ""
							try:
								while res is None or aso.is_captcha_in_response:
									if retry >= 5:
										print("I think proxies are not working")
										proxies_not_working = True
										break
									title1 = item.get("title","")
									keywords = [upc,isbn,title1]
									url = get_url(aso,keywords)
									if url and len(url)>0:
										current_url = url.strip()
										if current_url.startswith('https://www.amazon.com') or current_url.startswith('www.amazon.com'):
											# print("current_url",current_url)
											pass
										else:
											current_url = "https://www.amazon.com"+current_url
										res = aso.scrape(current_url)
									if aso.is_captcha_in_response or res is None:
										print("no response found. Trying again...")
										time.sleep(5)
										current_proxy = proxy_handler.get_proxy()
										aso.proxies.update({"https":current_proxy})
										aso.change_proxy(current_proxy)
										retry += 1
										continue
								if proxies_not_working:
									print("proxies are not working so exiting")
								price_str = res.get("price","")
								if len(price_str)>0:
									price_str = float(price_str.replace("$","").replace(",",""))

							except Exception as e:
								print("error with amazon scraping",e)
								pass
							try:
								current_es.amazon_price_str = price_str
								current_es.amazon_url = current_url
								current_es.search_report_id = report_obj.pk
								current_es.save()
								ebay_obj = EbaySellerSearch.objects.filter(seller_id = seller_id,search_report_id = report_id).count()
								reports.update(item_found = ebay_obj)						
							except Exception as e:
								print("error!!",e)
								pass
							# break
							# input("press enter")
							# input("scraped url here")
					except Exception as e:
						print("error!!",e)
				break
	except Exception as e:
		print("exception 1 ",e)



	ebay_obj = EbaySellerSearch.objects.filter(seller_id = seller_id,search_report_id = report_id).count()
	reports.update(status = "completed",item_found = ebay_obj)
	return "searching sellers item"


@job
def ebay_price_updater():
	testing_facade()
	# all_ebay_items = EbaySellerItems.objects.filter(status__in=["monitored","unmonitored"])
	# if len(all_ebay_items)>0:
	# 	aso = AmazonScraper(locale="UK")
	# 	proxy_handler = CProxy(1,0)
	# 	current_proxy = proxy_handler.get_proxy()
	# 	aso.proxies.update({"https":current_proxy})
	# 	seller_id = 1
	# 	ebayhandler = get_ebay_handler(seller_id)

	# 	formula_obj=EbayPriceFormula.objects.all().first()
	# 	print("current_proxy",current_proxy)
	# 	count = 0
	# 	for ebay_item in all_ebay_items:
	# 		count += 1
	# 		print("item..",count)
	# 		item_info_to_update_on_ebay = {}
	# 		item_info_to_update_on_ebay["ItemID"] = ebay_item.ebay_id
	# 		print("ebay url","https://www.ebay.com/itm/"+str(ebay_item.ebay_id))
	# 		price_info = {"Item":item_info_to_update_on_ebay}
	# 		if True:
	# 			amazon_url = make_amazon_url(ebay_item.custom_label)
	# 			retry = 0
	# 			res = None
	# 			prime_price = ''
	# 			while res is None or "503" in res or aso.is_captcha_in_response:
	# 				res = aso.scrape_with_error(amazon_url)
	# 				# if res.get("is_prime") == False:
	# 				# 	print("is prime false")
	# 				# 	aso.get_prime_detail = True
	# 				# 	amazon_url = make_amazon_url_for_list_primes(ebay_item.custom_label)
	# 				# 	prime_price = aso.scrape_for_prime(amazon_url)
	# 				# 	if len(prime_price)>0:
	# 				# 		print("prime_price",prime_price)
	# 				# 		res["price"] = prime_price
	# 				# 		res["is_prime"] = True

	# 				if aso.is_captcha_in_response or "503" in res:
	# 					current_proxy = proxy_handler.get_proxy()
	# 					aso.change_proxy(current_proxy)
	# 					retry += 1
	# 				if retry == 5:
	# 					print("I think proxies are not working")
	# 					break
	# 			print("amazon url",amazon_url)
	# 			if is_eligible_for_out_of_stock(res):
	# 				print("item is eligible for out of stock",res)
	# 				item_info_to_update_on_ebay["Quantity"] = "0"
	# 				print("price_info")
	# 				# input("enter")
	# 				is_updated = ebayhandler.set_item_price(item_price_dict = price_info)
	# 				print("is updated,",is_updated)
	# 				ebay_item.status = "unmonitored"
	# 				ebay_item.quantity = 0
	# 				ebay_item.save()
	# 				continue
	# 			else:
	# 				print("inside else...............",res)
	# 				final_cost = get_final_cost(ebay_item,formula_obj,res)
	# 				final_stock = get_final_stock(ebay_item.stock_level)
	# 				print("final_cost",final_cost,"final_stock",final_stock)
	# 				item_info_to_update_on_ebay["Quantity"] = ebay_item.quantity = final_stock
	# 				item_info_to_update_on_ebay["StartPrice"] = ebay_item.price = final_cost
	# 				print("price_info",price_info)
	# 				# input("press enter")
	# 				is_updated = ebayhandler.set_item_price(item_price_dict = price_info)
	# 				ebay_item.status = "monitored"
	# 				ebay_item.save()
	# 		# break	

	return "process finished"



@shared_task
def put_ebay_products_to_db(file_name):
	csv_file = csv.reader(open(file_name,"r"))
	print("file_name: ",file_name)
	is_header = False
	headers = ["local_id","vendor_url","vendor_variant","vendor_stock","vendor_price","vendor_shipping","reference","compare_url","compare_variant","compare_stock","compare_price","compare_shipping","profit_formula","selling_formula","reprice_store","reprice_sku","reprice_pause","sales_price","estimated_profit","autoCompare"]
	total = 0
	for row in csv_file:
		if is_header == False:
			is_header = True
			continue
		product = EbayProductsCsvData()
		product.local_id = row[headers.index("local_id")]
		product.vendor_url = row[headers.index("vendor_url")]
		product.vendor_variant = row[headers.index("vendor_variant")]
		product.vendor_stock = row[headers.index("vendor_stock")]
		product.vendor_price = row[headers.index("vendor_price")]
		product.vendor_shipping = row[headers.index("vendor_shipping")]
		product.reference = row[headers.index("reference")]
		product.compare_url = row[headers.index("compare_url")]
		product.compare_variant = row[headers.index("compare_variant")]
		product.compare_stock = row[headers.index("compare_stock")]
		product.compare_price = row[headers.index("compare_price")]
		product.compare_shipping = row[headers.index("compare_shipping")]
		product.profit_formula = row[headers.index("profit_formula")]
		product.selling_formula = row[headers.index("selling_formula")]
		product.reprice_store = row[headers.index("reprice_store")]
		product.reprice_sku = row[headers.index("reprice_sku")]
		product.reprice_pause = row[headers.index("reprice_pause")]
		product.sales_price = row[headers.index("sales_price")]
		product.estimated_profit = row[headers.index("estimated_profit")]
		product.autoCompare = row[headers.index("autoCompare")]
		product.save()
		total += 1
	return '{} record inserted in ebay products!'.format(total)


def get_current_time():
	return datetime.datetime.now()

def get_time_diff_from_now(old_time):
	now = datetime.datetime.now()
	previous = old_time
	time_delta = now - previous
	exact_diff = divmod(time_delta.days*86400+time_delta.seconds,60)
	second_diff = exact_diff[1]
	return second_diff


@shared_task
def scrape_amazon2(run_id,group_id,no_of_threads):
	print("run_id: ",run_id," group_id: ",group_id,"no_of_threads: ",no_of_threads)
	aso = AmazonScraper(locale="UK")
	proxy_handler = CProxy(no_of_threads,group_id)
	current_url = "https://www.ipchicken.com/"
	counter = 0
	while True:
		if counter == 50:
			break		
		current_proxy = proxy_handler.get_proxy()
		print("current_proxy:",current_proxy)
		aso.current_proxy = current_proxy
		# aso.proxies.update({"http":current_proxy})
		# aso.proxies.update({"https":current_proxy})
		aso.change_proxy(current_proxy)
		res = aso.scrape(current_url)
		counter += 1
	print("final_proxy_list:",aso.proxy_checker)
	return "run_id: "+str(run_id)+" group_id: "+str(group_id)+"no_of_threads: "+str(no_of_threads)+" running"

@shared_task
def start_ebay_seller_search(seller_id):
	print("fetching records for seller_id:",seller_id)
	# EbaySellerSearch.objects.all().delete()
	if seller_id is not None:
		es = EbayScraper(locale="UK")
		ebay_url = "https://www.ebay.com/sch/%s/m.html?_nkw=&_armrs=1&_ipg=&_from=" % (seller_id) 
		print("scraping: ",ebay_url)
		es.scrape(ebay_url)
		if len(es.response_list)>0:
			for item in es.response_list:
				current_es = EbaySellerSearch()
				current_es.seller_id = seller_id
				current_es.title	= item.get("title","")
				current_es.price_str = item.get("price","")
				current_es.item_sold = item.get("item_sold","")
				current_es.ebay_url = item.get("ebay_url","#")
				current_es.save()
	return "searching sellers item"

@shared_task
def scrape_amazon(run_id,group_id,no_of_threads):
	print("run_id: ",run_id," group_id: ",group_id,"no_of_threads: ",no_of_threads)
	aso = AmazonScraper(locale="UK")
	proxy_handler = CProxy(no_of_threads,group_id)
	# amazon_handler = CAmazon(no_of_threads=no_of_threads, group_index=group_id,amazon_run_id=run_id)
	amazon_handler = CAmazon(no_of_threads=no_of_threads, group_index=group_id)
	print("no of products:",len(amazon_handler.amazon_url_list))
	current_proxy = proxy_handler.get_proxy()
	aso.proxies.update({"https":current_proxy})
	counter = 0
	while amazon_handler.get_amazon_url():
		try:
			if counter >=50:
				break
			current_url = amazon_handler.current_url

			# current_url = "https://www.amazon.co.uk/dp/B00KNPGZ8I@332148185971"
			# current_url = "https://www.amazon.co.uk/dp/B01B2Q46MS@332246918410"
			ebay_id = current_url.split("@")[1].strip()
			current_url = current_url.split("@")[0].strip()
			res = None
			retry = 0
			proxies_not_working = False
			while res is None or aso.is_captcha_in_response:
				print("inside while"," res: ",res," is_captcha_in_response:",aso.is_captcha_in_response)
				# time.sleep(1)
				if retry >= 50:
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
					log_proxy(run_id,group_id,current_url,current_proxy,"captcha")
					current_proxy = proxy_handler.get_proxy()
					# aso.proxies.update({"https":current_proxy})
					aso.change_proxy(current_proxy)
					retry += 1
					continue
				if time_diff>3:
					log_proxy(run_id,group_id,current_url,current_proxy,"slow proxy")
					current_proxy = proxy_handler.get_proxy()
					# aso.proxies.update({"https":current_proxy})
					aso.change_proxy(current_proxy)
			if proxies_not_working:
				print("proxies are not working so exiting")
				break
			log_amazon_url(run_id,group_id,current_url,ebay_id,0,res,proxy_used=current_proxy)
			# break
		except Exception as e:
			log_proxy(run_id,group_id,current_url,current_proxy,"error")
			current_proxy = proxy_handler.get_proxy()
			traceback.print_exc()
			print("error waiting for 5 sec",current_url)
			log_amazon_url(run_id,group_id,current_url,ebay_id,0,{"price":"error occured during scrape"},proxy_used=current_proxy)
			time.sleep(5)
			# break
	return "run_id: "+str(run_id)+" group_id: "+str(group_id)+"no_of_threads: "+str(no_of_threads)+" running"

def is_eligible_for_ebay_update2(price,in_stock):
	is_eligible = False
	price_str = ""
	stock_str = "0"
	if price is not None and in_stock is not None and len(price)>0:
		clear_price = re.findall("[0-9.]+",price)
		if len(clear_price)>0:
			price_str = str(float("".join(clear_price)))
			if in_stock == "True":
				stock_str = "2"
			is_eligible = True

	return is_eligible,price_str,stock_str

def is_eligible_for_ebay_update(price,in_stock,is_prime):
	is_eligible = False
	price_str = ""
	stock_str = "0"
	print("is_prime",is_prime)
	print("is_prime_type: ",type(is_prime))
	if price is not None and in_stock is not None and len(price)>0 and is_prime is not False:
		clear_price = re.findall("[0-9.]+",price)
		if len(clear_price)>0:
			price_str = str(float("".join(clear_price)))
			if in_stock == "True":
				stock_str = "2"
	is_eligible = True

	return is_eligible,price_str,stock_str


def get_formula_dict(price_formulas_dict,price_str):
	price = float(price_str)
	for price_formula in price_formulas_dict:
		minimum_range = price_formula["minimum_range"]
		maximum_range = price_formula["maximum_range"]
		if price>=minimum_range and price<maximum_range:
			return price_formula
	return None

@shared_task
def start_ebay_update(thread_id,total_threads):
	while True:
		latest_run_id = AmazonRun.objects.latest('run_start_time')
		print("latest_run_id",latest_run_id)
		if latest_run_id:
			latest_run_id = latest_run_id.run_id
			print("latest_run_id: ",latest_run_id)
			# all_amazon_info_by_run_id = AmazonRunDetails.objects.filter(run_id=latest_run_id,is_ebay_updated=False,is_eligible_for_ebay_update=True,is_prime=True)
			all_amazon_info_by_run_id = AmazonRunDetails.objects.filter(is_ebay_updated=False,is_eligible_for_ebay_update=True)
			if all_amazon_info_by_run_id is not None and len(all_amazon_info_by_run_id)>0:
				ebay_start_index = 0
				ebay_end_index = 0
				ebay_items_in_a_group = int(math.floor(float(len(all_amazon_info_by_run_id))/float(total_threads)))
				ebay_start_index = thread_id*ebay_items_in_a_group
				if total_threads == thread_id+1:
					ebay_end_index = len(all_amazon_info_by_run_id)
				else:
					ebay_end_index = ebay_start_index+ebay_items_in_a_group
				print("ebay_start_index:",ebay_start_index,"ebay_end_index:",ebay_end_index)
				all_amazon_info_by_run_id = all_amazon_info_by_run_id[ebay_start_index:ebay_end_index]
				ebayhandler = EbayHandler()
				
				# price_formula = EbayAmazonPriceFormula.objects.all().first()
				# vendor_tax = price_formula.vendor_tax
				# margin = price_formula.margin
				# fixed_margin = price_formula.fixed_margin
				# minimum_margin = price_formula.minimum_margin
				# paypal_fees_perc = price_formula.paypal_fees_perc
				# paypal_fees_fixed = price_formula.paypal_fees_fixed
				# ebay_fees = price_formula.ebay_fees
				# manual_override	= price_formula.manual_override

				price_formulas = EbayAmazonPriceFormula.objects.all()
				formulas_list = []
				for price_formula in price_formulas:
					current_formula = {}
					current_formula["vendor_tax"] = price_formula.vendor_tax
					current_formula["margin"] = price_formula.margin
					current_formula["fixed_margin"] = price_formula.fixed_margin
					current_formula["minimum_margin"] = price_formula.minimum_margin
					current_formula["paypal_fees_perc"] = price_formula.paypal_fees_perc
					current_formula["paypal_fees_fixed"] = price_formula.paypal_fees_fixed
					current_formula["ebay_fees"] = price_formula.ebay_fees
					current_formula["manual_override"] = price_formula.manual_override
					current_formula["minimum_range"] = price_formula.minimum_range
					current_formula["maximum_range"] = price_formula.maximum_range
					formulas_list.append(current_formula)

				for amazon_info in all_amazon_info_by_run_id:
					print("amazon_info:",amazon_info.price_str)
					print("amazon_info2:",model_to_dict(amazon_info))
					ebay_id = amazon_info.ebay_id
					amazon_price = amazon_info.price_str
					in_stock = amazon_info.in_stock_str
					is_prime = amazon_info.is_prime
					is_eligible,price_str,stock_str = is_eligible_for_ebay_update(amazon_price,in_stock,is_prime)
					price_formulas_dict = None
					if stock_str is not "0" and len(price_str)>0:
						price_formulas_dict = get_formula_dict(formulas_list,price_str)
					print("price_formulas_dict",price_formulas_dict)
					# input("price_formulas_dict")
					
					ebay_obj = EbayRunDetails()
					ebay_obj.run_id = amazon_info.run_id
					ebay_obj.group_id = amazon_info.group_id
					ebay_obj.amazon_url = amazon_info.amazon_url 
					ebay_obj.price_str = amazon_info.price_str #18.95
					ebay_obj.in_stock_str = amazon_info.in_stock_str
					ebay_obj.ebay_id = amazon_info.ebay_id
					ebay_obj.ebay_url = "http://www.ebay.com/itm/"+amazon_info.ebay_id
					ebay_obj.ebay_price = price_str
					ebay_obj.ebay_stock = stock_str
					# if price_formulas_dict is None:
					# 	print("no price formula found for ",amazon_info.amazon_url," so not updating and continue")
					# 	ebay_obj.cause_if_fail = "no price formula found for "+ amazon_info.amazon_url+" so not updating and continue"
					# 	ebay_obj.is_ebay_updated = False
					# 	amazon_info.is_ebay_updated = False
					# 	ebay_obj.save()
					# 	amazon_info.save()
					# 	continue
					if is_eligible == True:
						price_info	= {}
						item = {}
						
						
						# input("new_price")
						item["ItemID"] = ebay_id
						if stock_str is not "0" and price_formulas_dict is not None:
							price_plus_fixed_margin = float(price_str) + price_formulas_dict["fixed_margin"] 
							price_plus_margin = price_plus_fixed_margin + (price_plus_fixed_margin* price_formulas_dict["margin"]/100)
							price_plus_ebay_fees = price_plus_margin + (price_plus_margin* price_formulas_dict["ebay_fees"]/100)
							price_plus_paypal_fees = price_plus_ebay_fees + (price_plus_ebay_fees* price_formulas_dict["paypal_fees_perc"]/100)
							price_plus_paypal_fees = math.ceil(price_plus_paypal_fees)
							new_price = str(price_plus_paypal_fees)
							print("new_price",new_price)
							item["StartPrice"] = new_price
							ebay_obj.ebay_price = new_price
							item["Quantity"] = stock_str
						else:
							item["Quantity"] = "0"
						price_info["Item"] = item
						
						try:
							is_updated = ebayhandler.set_item_price(item_price_dict = price_info)
							# is_updated = True
							if is_updated:
								ebay_obj.is_ebay_updated = True
								amazon_info.is_ebay_updated = True
							else:
								amazon_info.cause_if_fail = "could not update"
								amazon_info.is_eligible_for_ebay_update = False
								ebay_obj.cause_if_fail = "could not update"
						except Exception as e:
							ebay_obj.cause_if_fail = e
							amazon_info.cause_if_fail = e
							amazon_info.is_eligible_for_ebay_update = False
							print("ebay item update error occur for",amazon_info.run_id," amazon_url:",amazon_info.amazon_url)
					else:
						ebay_obj.cause_if_fail = "not eligible"
					print("ebay dict:",model_to_dict(ebay_obj))
					ebay_obj.save()

					amazon_info.save()
					time.sleep(10)
			else:
				time.sleep(300)



# @shared_task
# def create_random_user_accounts(total):
#		 for i in range(total):
#				 username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
#				 email = '{}@example.com'.format(username)
#				 password = get_random_string(50)
#				 User.objects.create_user(username=username, email=email, password=password)
#		 return '{} random users created with success!'.format(total)

# @job
# def sync_db_to_ebay(seller_id):

# 	ebay_obj = EbayHandler()
# 	o = ebay_obj.get_all_items()
# 	item = {}
# 	price_info = {}
# 	item["ItemID"] = '263445985775'

# 	item["StartPrice"] = 82.19
# 	item["Quantity"] = "0"
# 	price_info["Item"] = item
# 	is_updated = ebay_obj.set_item_price(item_price_dict = price_info)

# 	return "DB sync completed"


@job
def sync_db_to_ebay(seller_id,seller_token):
	print("inside syncccccccccccc")
	print("seller info....",seller_id,seller_token)
	insert_data(seller_id,seller_token)
	get_item_in_csv(seller_id, seller_token)
	# all_db_items_list = []
	# latest_items_list = []
	# ignored_list = []
	# exception_list = []
	# all_ebay = EbaySellerItems.objects.filter(seller_id = seller_id)
	# for item in all_ebay:
	# 	all_db_items_list.append(item.ebay_id)
	# ebay_obj = get_ebay_handler(seller_id)
	# o = ebay_obj.get_all_items()
	# no_of_pages = get_value_from_dict(o,["ActiveList","PaginationResult","TotalNumberOfPages"])
	# if no_of_pages:
	# 	no_of_pages = int(no_of_pages)
	# 	if no_of_pages>0:
	# 		# for page in range(1,no_of_pages+1):
	# 		for page in range(1,no_of_pages+1):
	# 			print("page no.",page,no_of_pages)
	# 			current_page_results = ebay_obj.get_all_items(page_number = page)
	# 			items = get_value_from_dict(current_page_results,["ActiveList","ItemArray","Item"])
	# 			if isinstance(items,dict):
	# 				items = [items]
	# 			for item in items:
	# 				parsed_data = parse_ebay_item(item,seller_id)
	# 				print("parsed data.................",parsed_data)
	# 				latest_items_list.append(parsed_data.get("ebay_id",""))
	# 				try:
	# 					ebay_item, created = EbaySellerItems.objects.get_or_create(**parsed_data)
	# 					EbaySellerItems.objects.filter(ebay_id = parsed_data.get("ebay_id","")).update(status="monitored")
	# 					obj = EbaySellerItems.objects.get(ebay_id = parsed_data.get("ebay_id",""))
	# 					print("ebay in db... status update quantity yes",obj.ebay_id,obj.price,obj.quantity,obj.status)
	# 					# input("press enter")
	# 					if not created:
	# 						if obj.quantity < 1:
	# 							ebay_item = EbaySellerItems.objects.filter(ebay_id = parsed_data.get("ebay_id","")).update(status = "unmonitored")
	# 							obj = EbaySellerItems.objects.get(ebay_id = parsed_data.get("ebay_id",""))
	# 							# input("press enter not created")

	# 				except Exception as ex:
	# 					# input("inside frst Exception")
	# 					try:
	# 						ebay_update_obj = EbaySellerItems.objects.filter(ebay_id = parsed_data.get("ebay_id","")) 
	# 						ebay_update_obj.update(quantity = parsed_data.get("quantity","0"),price = parsed_data.get("price"),status="monitored",no_of_times_sold=parsed_data.get("no_of_times_sold",""))
	# 						obj = EbaySellerItems.objects.get(ebay_id = parsed_data.get("ebay_id",""))
	# 						# input("inside try updated")
	# 						if obj.quantity < 1:
	# 							obb = EbaySellerItems.objects.filter(ebay_id = parsed_data.get("ebay_id","")).update(status = "unmonitored")
	# 							obj = EbaySellerItems.objects.get(ebay_id = parsed_data.get("ebay_id",""))
	# 					except Exception as e:
	# 						print("Exception error",e)
	# 						exception_list.append(parsed_data.get("ebay_id",""))
	# 						pass
	# 					print("error",ex)
	# 					# break
	# print("all_db_items_list",len(all_db_items_list))
	# # print("latest_items_list",len(latest_items_list),latest_items_list)
	# ignored_list = list(set(all_db_items_list) - set(latest_items_list))
	# print("ignored list length ",len(ignored_list))
	# print("exception_list",len(exception_list))
	# for item in ignored_list:
	# 	# break
	# 	EbaySellerItems.objects.filter(ebay_id = item).update(status = "ignored")

	return "DB sync completed"