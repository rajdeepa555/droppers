from .db import get_ebay_items, get_price_formula, create_batchlog_item, create_run_item
from .utils import get_run_id,get_sellers_account
from .factory import get_amazonscraper, get_proxyhandler
from .price_update_function import assign_proxy,scrape_again,get_amazon_info,\
				get_ebay_obj_to_update,is_eligible_for_out_of_stock,get_cost_components,\
				get_final_cost,is_needed_to_update_info_on_ebay,get_clear_price,get_required_handlers,\
				get_amazon_asin_to_update,get_update_item_status
from .models import *
import re
import csv


# def get_current_seller_id(all_seller_account_of_current_user):
	# for seller_accounts in all_seller_account_of_current_user:
	# 		current_seller_id = seller_accounts.get("id")
	# return current_seller_id

def dump_to_csv(csv_instance, amazon_asin ,amazon_info, ebay_info,file_obj):
	csv_instance.writerow([amazon_asin, amazon_info.get("price"), amazon_info.get("is_prime"),\
		amazon_info.get("in_stock"), ebay_info.get("StartPrice"), ebay_info.get("Quantity"), ebay_info.get("ItemID") ])
	file_obj.flush()

def process_ebay_item(ebay_item,amazon_handler, proxy_handler, ebay_handler,seller_id,default_stock,csv_instance,file_obj):
	print("seller_id",seller_id)
	# input("inside process_ebay_item")
	amazon_asin = get_amazon_asin_to_update(ebay_item)
	# print("amazon_asin",amazon_asin)
	# amazon_asin = "B0764D5CVY"
	if amazon_asin is not None:
		amazon_info = get_amazon_info(amazon_asin,amazon_handler,proxy_handler)
		print("amazon_info",amazon_info)
		current_seller_formula = get_price_formula(seller_id=seller_id)
		if not current_seller_formula:
			print("formula for current seller not found skipping......")
			exit(0)
		ebay_obj_to_update = get_ebay_obj_to_update(amazon_info,current_seller_formula,ebay_item,default_stock)
		ebay_price_obj = {"Item":ebay_obj_to_update}
		print("ebay_obj_to_update",ebay_obj_to_update)
		# input("press enter")
		is_updated = ebay_handler.set_item_price(item_price_dict = ebay_price_obj)
		is_updated = True
		dump_to_csv(csv_instance, amazon_asin ,amazon_info,ebay_obj_to_update,file_obj)
		update_status = get_update_item_status(is_updated,ebay_item,ebay_obj_to_update,default_stock)
		needed = is_needed_to_update_info_on_ebay(amazon_info,ebay_item)


def price_updater(seller_id,token,default_stock,ebay_id_list):
	run_id = get_run_id()
	run = create_run_item(run_id=run_id)
	file_obj = open('ebay_amazon7.csv','w')
	csv_instance = csv.writer(file_obj,0)
	csv_instance.writerow(["amazon_asin","amazon price","is_prime","in_stock","ebay_price","ebay_quantity","ebay_id"])
	if len(ebay_id_list)>0:
		ebay_items = get_ebay_items(seller_id=seller_id,ebay_id__in=ebay_id_list,status__in=['monitored','unmonitored'])
	else:
		ebay_items = get_ebay_items(seller_id=seller_id,status__in=['monitored','unmonitored'])
	amazon_handler, ebay_handler, proxy_handler = get_required_handlers(token)
	count = 0
	for item in ebay_items:
		try:
			count = count + 1
			print("count ",count)
			process_ebay_item(item,amazon_handler, proxy_handler, ebay_handler,seller_id,default_stock,csv_instance,file_obj)
		except Exception as e:
			print("inside exception")
			is_updated = False
			ebay_obj_to_update = {"Quantity":"0"}
			get_update_item_status(is_updated,item,ebay_obj_to_update,default_stock)
			batch_log = create_batchlog_item(run_id = run_id,seller = seller_id,ebay_id=item.ebay_id,error_log = e)
			print("error!!!",e)
# price_updater(23,'fgtbt')

def all_seller_price_updater():
	current_user = '1'
	all_seller_account_of_current_user = get_sellers_account(current_user)
	if all_seller_account_of_current_user:
		for seller_accounts in all_seller_account_of_current_user:
			current_seller_id = seller_accounts.get("id")
			seller_token = seller_accounts.get("token")
			is_update = seller_accounts.get("is_update")
			default_stock = seller_accounts.get("default_stock")
			print("seller",current_seller_id,seller_token)
			if not seller_token:
				print("seller_token not found for current seller account skipping...." )
				continue
			print("is_update",is_update)
			if is_update:
				print("seleleasfsafs",current_seller_id)
				price_updater(current_seller_id,seller_token,default_stock,[])
			else:
				continue
