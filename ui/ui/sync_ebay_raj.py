from .db import get_ebay_items, query_set_to_list, get_all_active_sellers_account, \
				get_price_formula, get_existing_value, create_ebay_item,set_ebay_items_to_inactive, \
				create_batchlog_item, create_run_item,create_insert_ebay_item
from .utils import get_simple_list_from_list_dict, get_value_from_dict, \
				 make_amazon_url, get_float,get_run_id,make_amazon_url_for_list_primes
from .factory import get_ebayhandler, get_amazonscraper, get_proxyhandler
# from .helpers import is_value_empty
from .parsers import parse_ebay_item
# from .helpers_ebay import get_page_number,get_ebay_item_list,get_ebay_items_list_from_ebay_response
from .models import EbaySellerItems
import csv
from .helpers import is_value_empty
 
def get_active_seller_account(current_user,is_active):
	seller_accounts = get_all_active_sellers_account(user_id=current_user,is_active=is_active)
	seller_accounts = query_set_to_list(seller_accounts)
	return seller_accounts

def get_ignored_items_list(seller_id):
	ignored_items = get_ebay_items(seller_id=seller_id,status="ignored")
	ignored_items = query_set_to_list(ignored_items)
	ignored_items = get_simple_list_from_list_dict(ignored_items,"ebay_id")
	return ignored_items

def get_total_no_of_pages(ebay_handler):
	o = ebay_handler.get_all_items()
	no_of_pages = get_value_from_dict(o,["ActiveList","PaginationResult","TotalNumberOfPages"])
	print("no_of)pagesssssss",no_of_pages)
	return no_of_pages

def remove_ignore_items(ebay_items_list,seller_id,ignored_items = None):
	ebay_list_after_remove_ignored = []
	if ebay_items_list:
		if not ignored_items:
			ignored_items = get_ignored_items_list(seller_id)
		print("ebay_items_list",ebay_items_list)
		for ebay_item in ebay_items_list:
			if "ItemID" in ebay_item and ebay_item["ItemID"] not in ignored_items:
				ebay_list_after_remove_ignored.append(ebay_item)
	return ebay_list_after_remove_ignored

def scrape_again(amazon_handler,amazon_asin):
	print("scraping scrape_again")
	print("amazon handlerrr",amazon_handler)
	amazon_handler.get_prime_detail = True
	amazon_url = make_amazon_url_for_list_primes(amazon_asin)
	print("new url",amazon_url)
	res = amazon_handler.scrape_with_error(amazon_url)
	print("ressss",res)
	res["price"] = amazon_handler.prime_price
	res["is_prime"] = amazon_handler.is_prime
	res["in_stock"] = amazon_handler.in_stock
	print("RESSS",res)
	return res

# 


def get_ebay_item_list(ebay_handler,page = 1):
	ebay_items_list = []
	if ebay_handler:
		ebay_items_list = ebay_handler.get_all_items(page_number=page)
		print("eeeeeeebay itemmmmmmm listttttt",ebay_items_list)
	return ebay_items_list

def get_ebay_items_list_from_ebay_response(ebay_response):
	if ebay_response:
		ebay_items_list = get_value_from_dict(ebay_response,["ActiveList","ItemArray","Item"])
		if not isinstance(ebay_items_list,list):
			ebay_items_list = [ebay_items_list]
	return ebay_items_list


def sync_ebay_item():
	current_user = '1'
	all_seller_account_of_current_user = get_active_seller_account(current_user,1)
	run_id = get_run_id()
	run = create_run_item(run_id=run_id)
	if all_seller_account_of_current_user:
		for seller_accounts in all_seller_account_of_current_user:
			current_seller_id = seller_accounts.get("id")
			seller_token = seller_accounts.get("token")
			if not seller_token:
				continue
			is_set = set_ebay_items_to_inactive(current_seller_id)
			if not is_set:
				continue
			ebay_handler = get_ebayhandler(seller_token)
			no_of_pages = get_total_no_of_pages(ebay_handler)
			print("nop",no_of_pages)
			if no_of_pages:
				file_obj = open("insert.csv","w")
				file = csv.writer(file_obj)
				for page in range(1,int(no_of_pages)+1):
					ebay_items_response = get_ebay_item_list(ebay_handler,page)
					ebay_items = get_ebay_items_list_from_ebay_response(ebay_items_response)
					if not ebay_items and isinstance(ebay_items,list):
						print("invalid ebay_items list")
						continue
					# print("ebay itemsssssss",ebay_items)
					for ebay_item in ebay_items:
						insert_data(ebay_item, current_seller_id)


def insert_data(ebay_item,current_seller_id):
	# print("ebay item in insert function......................",ebay_item)
	amazon_asin = ebay_item['SKU']
	ebay_id = ebay_item['ItemID']
	# item_in_stock = check_instock(ebay_item)
	parsed_data = parse_ebay_item(ebay_item,current_seller_id)
	parsed_data.pop("ebay_id")
	parsed_data["is_active"] = True
	# print("parsed.......",parsed_data)
	ebay_obj_to_insert = create_insert_ebay_item(ebay_id,parsed_data)
	# print("object",ebay_obj_to_insert)
	# print("going to enter in if")
	if ebay_item.get("Quantity") != "0":
		# print("this is monitored")
		ebay_obj_to_insert.status = "monitored"
	elif ebay_item.get("Quantity") == "0":
		# print("this id unmonitored")
		ebay_obj_to_insert.status = "unmonitored"
	if ebay_obj_to_insert:
		ebay_obj_to_insert.is_active = True
		ebay_obj_to_insert.save()
		# print("data successfully saved")
	# input("please enter")



# sync_ebay_item()