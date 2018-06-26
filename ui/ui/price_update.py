from .db import get_ebay_items, get_price_formula, create_batchlog_item, create_run_item,get_all_sellers_account,query_set_to_list
from .utils import get_run_id
from .factory import get_amazonscraper, get_proxyhandler
from .price_update_function import get_active_seller_account,assign_proxy,scrape_again,get_amazon_info,\
				get_ebay_obj_to_update,is_eligible_for_out_of_stock,get_cost_components,\
				get_final_cost,is_needed_to_update_info_on_ebay,get_clear_price,get_required_handlers
from .models import *
import re


def get_current_seller_id(all_seller_account_of_current_user): 
	for seller_accounts in all_seller_account_of_current_user:
			current_seller_id = seller_accounts.get("id")
	return current_seller_id


def get_amazon_asin_to_update(ebay_item):
	amazon_asin = ebay_item.custom_label
	print("amazon asin",amazon_asin)
	amazon_asin_re = re.findall(r'\d+', amazon_asin)
	print("amazon asin re",amazon_asin_re)
	if len(amazon_asin_re)>0:
		return amazon_asin
	else:
		# print("inside else of get asin")
		return None


def get_update_item_status(is_updated,ebay_item,ebay_obj_to_update):

	if is_updated and ebay_item and ebay_obj_to_update.get("Quantity") != "0":
		ebay_item.status = "monitored"
		ebay_item.quantity = "2"
		input("press enter")
	elif ebay_item and ebay_obj_to_update.get("Quantity") == "0":
		input("unmonitored occured..press enter")
		ebay_item.status = "unmonitored"
	if ebay_item:
		ebay_item.is_active = True
		ebay_item.save()

def process_ebay_item(ebay_item,amazon_handler, proxy_handler, ebay_handler,seller_id):
	print("inside process_ebay_item",ebay_item,seller_id)
	input("inside process_ebay_item")
	amazon_asin = get_amazon_asin_to_update(ebay_item)
	# print("amazon_asin",amazon_asin)
	# amazon_asin = "B000M8Q02M"
	if amazon_asin is not None:
		print("amzon asin",amazon_asin)
		amazon_info = get_amazon_info(amazon_asin,amazon_handler,proxy_handler)
		print("amzon info...........",amazon_info)
		current_seller_formula = get_price_formula(seller_id=seller_id)
		if not current_seller_formula:
			print("formula for current seller not found skipping......")
			exit(0)	
		ebay_obj_to_update = get_ebay_obj_to_update(amazon_info,current_seller_formula,ebay_item)
		print("ebay item to update.......................",ebay_obj_to_update)
		ebay_price_obj = {"Item":ebay_obj_to_update}
		# input("please enter")
		# is_updated = ebay_handler.set_item_price(item_price_dict = ebay_price_obj)
		is_updated = True
		update_status = get_update_item_status(is_updated,ebay_item,ebay_obj_to_update)
		needed = is_needed_to_update_info_on_ebay(amazon_info,ebay_item)


def price_updater(seller_id,token):
	# print("seller id",seller_id)
	# seller_obj = SellerTokens.objects.get(id = seller_id)
	# token = seller_obj.token
	# print("token",token)
	run_id = get_run_id()
	run = create_run_item(run_id=run_id)
	ebay_items = get_ebay_items(seller_id=seller_id,status__in=['monitored','unmonitored'])
	amazon_handler, ebay_handler, proxy_handler = get_required_handlers(token)
	count = 0
	for item in ebay_items:
		try:
			count = count + 1
			print("count...............",count)
			print("process_ebay_item",item,seller_id)
			input("process_ebay_item")
			process_ebay_item(item,amazon_handler, proxy_handler, ebay_handler,seller_id)
		except Exception as e:
			print("inside exception")
			# batch_log = create_batchlog_item(run_id = run_id,seller = seller_id,ebay_id=item.ebay_id,error_log = e)
			print("error!!!",e)


# price_updater(23,'fgtbt')
def get_active_seller_account(current_user,is_active):
	seller_accounts = get_all_sellers_account(user_id=current_user)
	seller_accounts = query_set_to_list(seller_accounts)
	return seller_accounts

def all_seller_price_updater():
	current_user = '1'
	all_seller_account_of_current_user = get_active_seller_account(current_user,1)
	if all_seller_account_of_current_user:
		for seller_accounts in all_seller_account_of_current_user:
			current_seller_id = seller_accounts.get("id")
			seller_token = seller_accounts.get("token")
			if not seller_token:
				print("seller_token not found for current seller account skipping...." )
				continue
			price_updater(current_seller_id,seller_token)