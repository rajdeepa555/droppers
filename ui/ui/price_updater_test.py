
from .db import get_ebay_items, query_set_to_list, get_all_active_sellers_account, \
				get_price_formula, get_existing_value, create_ebay_item,set_ebay_items_to_inactive, \
				create_batchlog_item, create_run_item
from .utils import get_simple_list_from_list_dict, get_value_from_dict, \
				 make_amazon_url, get_float,get_run_id,make_amazon_url_for_list_primes
from .factory import get_ebayhandler, get_amazonscraper, get_proxyhandler
from .helpers import is_value_empty
from .parsers import parse_ebay_item
import re
from django.forms.models import model_to_dict
import csv

def get_active_seller_account(current_user,is_active):
	seller_accounts = get_all_active_sellers_account(user_id=current_user,is_active=is_active)
	seller_accounts = query_set_to_list(seller_accounts)
	return seller_accounts


def get_total_no_of_pages(ebay_handler):
	o = ebay_handler.get_all_items()
	no_of_pages = get_value_from_dict(o,["ActiveList","PaginationResult","TotalNumberOfPages"])
	# print("no_of)pagesssssss",no_of_pages)
	return no_of_pages


def get_ebay_item_list(ebay_handler,page = 1):
	ebay_items_list = []
	if ebay_handler:
		ebay_items_list = ebay_handler.get_all_items(page_number=page)
		# print("eeeeeeebay itemmmmmmm listttttt",ebay_items_list)
	return ebay_items_list

def get_ignored_items_list(seller_id):
	ignored_items = get_ebay_items(seller_id=seller_id,status="ignored")
	ignored_items = query_set_to_list(ignored_items)
	ignored_items = get_simple_list_from_list_dict(ignored_items,"ebay_id")
	return ignored_items

def remove_ignore_items(ebay_items_list,seller_id,ignored_items = None):
	ebay_list_after_remove_ignored = []
	if ebay_items_list:
		if not ignored_items:
			ignored_items = get_ignored_items_list(seller_id)
		# print("ebay_items_list",ebay_items_list)
		for ebay_item in ebay_items_list:
			if "ItemID" in ebay_item and ebay_item["ItemID"] not in ignored_items:
				ebay_list_after_remove_ignored.append(ebay_item)
	return ebay_list_after_remove_ignored

def get_ebay_items_list_from_ebay_response(ebay_response):
	if ebay_response:
		ebay_items_list = get_value_from_dict(ebay_response,["ActiveList","ItemArray","Item"])
		if not isinstance(ebay_items_list,list):
			ebay_items_list = [ebay_items_list]
	return ebay_items_list

def get_amazon_asin_from_ebay_dict(ebay_item):
	amazon_asin = None
	if ebay_item and "SKU" in ebay_item:
		amazon_asin = ebay_item["SKU"]
	return amazon_asin	

def assign_proxy(amazon_handler,proxy_handler):
	current_proxy = proxy_handler.get_proxy()
	amazon_handler.proxies.update({"https":current_proxy})

def scrape_again(amazon_handler,amazon_asin):
	amazon_handler.get_prime_detail = True
	amazon_url = make_amazon_url_for_list_primes(amazon_asin)
	res = amazon_handler.scrape_with_error(amazon_url)
	res["price"] = amazon_handler.prime_price
	res["is_prime"] = amazon_handler.is_prime
	res["in_stock"] = amazon_handler.in_stock
	return res

def get_amazon_info(amazon_asin,amazon_handler,proxy_handler):
	print("amazonasssssssssssssin",amazon_asin)
	print("amzonnnnnnnnnhandler",amazon_handler)
	print("proxxxxxxxxxxxxxy",proxy_handler)
	assign_proxy(amazon_handler,proxy_handler)
	amazon_url = make_amazon_url(amazon_asin)
	amazon_handler.asin = amazon_asin
	res = amazon_handler.scrape_with_error(amazon_url)
	retry = 0
	if res.get("is_prime") == False or res.get("in_stock") == False or res.get("price") == '':
		res = scrape_again(amazon_handler,amazon_asin)


	while res is None or "503" in res or amazon_handler.is_captcha_in_response:
		if amazon_handler.is_captcha_in_response or "503" in res:
			assign_proxy(amazon_handler,proxy_handler)

			res = amazon_handler.scrape_with_error(amazon_url)
			if res.get("is_prime") == False or res.get("in_stock") == False or res.get("price") == '':
				res = scrape_again(amazon_handler,amazon_asin)
			retry += 1
		if retry == 5:
			print("I think proxies are not working")
			break
	if retry == 5:
		exit(0)
	# if len(prime_price)>0:
		# print("prime_price",prime_price)
		# res["price"] = prime_price
		# res["is_prime"] = True

	return res



def get_final_cost(cost_components):
	price = cost_components.get("price")
	margin_perc = cost_components.get("margin_perc") * price/100
	fixed_margin = cost_components.get("fixed_margin")
	cost = price + cost_components.get("ebay_listing_fee") + cost_components.get("paypal_fees_fixed")
	if margin_perc < fixed_margin:
		cost = cost + fixed_margin
	else:
		cost = cost + margin_perc
	p = 1 - ((cost_components.get("ebay_final_value_fee") + cost_components.get("paypal_fees_perc"))/100)
	cost_after_profit = get_float(cost / p)
	print(".............price after formula...........................................",cost_after_profit)
	return cost_after_profit

def is_eligible_for_out_of_stock(item):
	return_value = False
	print('is_value_empty(item.get("price"))',is_value_empty(item.get("price")),'item.get("in_stock")',item.get("in_stock"),'item.get("is_prime")',item.get("is_prime"))
	if is_value_empty(item.get("price")) or item.get("in_stock") == False or item.get("is_prime") == False:
		return_value = True
	return return_value


def get_existing_ebay_item(existing_ebay_items_queryset, ebay_item_dict):
	# print("ebay_item_dict",ebay_item_dict)
	ebay_id = ebay_item_dict.get("ItemID")
	# print("eeeeeeeeeeeeee_id",ebay_id)
	existing_item = get_existing_value(existing_ebay_items_queryset, ebay_id=ebay_id)
	print("existing eeeeeeeeeeeeeeeee",existing_item)
	return existing_item

def is_needed_to_update_info_on_ebay(amazon_info,ebay_info):
	return True

def is_eligible_for_ebay_update():
	return True

def get_clear_price(p_str):
	f_str = None
	if p_str:
		price = re.findall("[0-9\.]+",p_str)
		if len(price)>0:
			f_str = get_float(float("".join(price)))
	return f_str

def get_cost_components(amazon_info,price_formula_obj,existing_ebay_obj):
	cost_components = {}
	# print("price_formula_obj",price_formula_obj)
	cost_components["price"] = get_clear_price(amazon_info.get("price"))
	cost_components["margin_perc"] = price_formula_obj.get("perc_margin")
	cost_components["fixed_margin"] = price_formula_obj.get("fixed_margin")
	cost_components["ebay_listing_fee"] = price_formula_obj.get("ebay_listing_fee")
	cost_components["paypal_fees_fixed"] = price_formula_obj.get("paypal_fees_fixed")
	cost_components["ebay_final_value_fee"] = price_formula_obj.get("ebay_final_value_fee")
	cost_components["paypal_fees_perc"] = price_formula_obj.get("paypal_fees_perc")
	if existing_ebay_obj:
		if existing_ebay_obj.margin_perc:
			cost_components["margin_perc"] = existing_ebay_obj.margin_perc
		if existing_ebay_obj.minimum_margin:
			cost_components["fixed_margin"] = existing_ebay_obj.minimum_margin
	return cost_components


def get_ebay_obj_to_update(amazon_info,price_formula_obj,existing_ebay_info,ebay_id):
	ebay_obj = {}
	ebay_obj["ItemID"] = ebay_id
	is_out_of_stock = is_eligible_for_out_of_stock(amazon_info)
	if is_out_of_stock:
		ebay_obj["Quantity"] = "0"
	else:
		cost_components = get_cost_components(amazon_info,price_formula_obj,\
						existing_ebay_info)
		ebay_price = get_final_cost(cost_components)
		ebay_obj["Quantity"] = "2"
		ebay_obj["StartPrice"] = ebay_price

	return ebay_obj

def process_ebay_item(ebay_item,amazon_handler, proxy_handler, \
					ebay_handler, existing_ebay_items_list, current_seller_formula,\
					current_seller_id,file,out):
	amazon_asin = get_amazon_asin_from_ebay_dict(ebay_item)
	amazon_info = get_amazon_info(amazon_asin,amazon_handler,proxy_handler)
	existing_ebay_item = get_existing_ebay_item(existing_ebay_items_list,ebay_item)
	ebay_id = ebay_item.get("ItemID")
	ebay_obj_to_update = get_ebay_obj_to_update(amazon_info,\
					current_seller_formula,existing_ebay_item,ebay_id)
	if existing_ebay_item is None:
		existing_ebay_item = create_ebay_item(**parse_ebay_item(ebay_item,current_seller_id))
	print("ebay_obj_to_update",ebay_obj_to_update)
	ebay_price_obj = {"Item":ebay_obj_to_update}
	print("ebay_price_obj.....................",ebay_price_obj)
	print("fillllleeeeeeee",file)
	file.writerow([ebay_obj_to_update["ItemID"],ebay_obj_to_update["Quantity"],ebay_obj_to_update.get("StartPrice","")])
	out.flush()
	# is_updated = ebay_handler.set_item_price(item_price_dict = ebay_price_obj)
	is_updated = True
	print('ebay_price_obj.get("Quantity")',ebay_obj_to_update.get("Quantity"),'existing_ebay_item',existing_ebay_item)
	if is_updated and existing_ebay_item and ebay_obj_to_update.get("Quantity") != "0":
		existing_ebay_item.status = "monitored"
		existing_ebay_item.quantity = "2"
	elif existing_ebay_item and ebay_obj_to_update.get("Quantity") == "0":
		print("inserting unmonitored")

		existing_ebay_item.status = "unmonitored"
	if existing_ebay_item:
		existing_ebay_item.is_active = True
		existing_ebay_item.save()
		print("item saved")
	needed = is_needed_to_update_info_on_ebay(amazon_info,ebay_item)

def testing_facade():
	current_user = '1'
	all_seller_account_of_current_user = get_active_seller_account(current_user,1)
	run_id = get_run_id()
	run = create_run_item(run_id=run_id)
	if all_seller_account_of_current_user:
		for seller_accounts in all_seller_account_of_current_user:

			current_seller_id = seller_accounts.get("id")
			is_set = set_ebay_items_to_inactive(current_seller_id)
			if not is_set:
				continue
			current_seller_formula = get_price_formula(seller_id=current_seller_id)
			
			if not current_seller_formula:
				print("formula for current seller not found skipping......")
				continue 
			seller_token = seller_accounts.get("token")
			if not seller_token:
				print("seller_token not found for current seller account skipping...." )
				continue
			ebay_handler = get_ebayhandler(seller_token)
			ignored_items_list = get_ignored_items_list(current_seller_id)
			no_of_pages = get_total_no_of_pages(ebay_handler)
			if no_of_pages and int(no_of_pages)>0:
				out = open("update.csv","w")
				file = csv.writer(out)
				file.writerow(["ItemID","Quantity","StartPrice"])
				no_of_pages = int(no_of_pages)
				for page in range(1,no_of_pages+1):
					print("page no:",page," of ",no_of_pages)
					ebay_items_response = get_ebay_item_list(ebay_handler,page)
					ebay_items = get_ebay_items_list_from_ebay_response(ebay_items_response)
					if not ebay_items and isinstance(ebay_items,list):
						print("invalid ebay_items list")
						continue
					ebay_items_after_remove_ignored = remove_ignore_items(ebay_items,\
													current_seller_id, ignored_items_list)
					existing_ebay_items_list = get_ebay_items(seller_id=current_seller_id)
					amazon_handler = get_amazonscraper()
					proxy_handler = get_proxyhandler()
					for ebay_item in ebay_items_after_remove_ignored:
						try:
							process_ebay_item(ebay_item,amazon_handler, proxy_handler,\
								 ebay_handler, existing_ebay_items_list, current_seller_formula,\
								 current_seller_id,file,out)
						except Exception as e:
							batch_log = create_batchlog_item(run_id = run_id,seller = current_seller_id,ebay_id=ebay_item["ItemID"],error_log = e)
							print("error!!!",e)
				
# testing_facade()
def update_ebay_item(data,current_user):
	for ebay_item in data:
		all_seller_account_of_current_user = get_active_seller_account(current_user,1)
		run_id = get_run_id()
		run = create_run_item(run_id=run_id)
		if all_seller_account_of_current_user:
			for seller_accounts in all_seller_account_of_current_user:
				current_seller_id = seller_accounts.get("id")
				current_seller_formula = get_price_formula(seller_id=current_seller_id)
				print("curretnt seller formula",current_seller_formula)
				seller_token = seller_accounts.get("token")
				ebay_handler = get_ebayhandler(seller_token)
				existing_ebay_items_list = get_ebay_items(seller_id=current_seller_id)
				amazon_handler = get_amazonscraper()
				proxy_handler = get_proxyhandler()
				process_ebay_item_new(ebay_item,amazon_handler, existing_ebay_items_list,proxy_handler,\
									 ebay_handler, current_seller_formula,\
									 current_seller_id)
	return True
def process_ebay_item_new(ebay_items,amazon_handler,existing_ebay_items_list,proxy_handler,ebay_handler,current_seller_formula,current_seller_id):
	amazon_asin = ebay_items.get("SKU")
	amazon_info = get_amazon_info(amazon_asin,amazon_handler,proxy_handler)
	ebay_id = ebay_items.get("ebay_id")
	existing_ebay_item = get_existing_ebay_item(existing_ebay_items_list,ebay_items)
	ebay_obj_to_update = get_ebay_obj_to_update(amazon_info,\
		current_seller_formula,existing_ebay_item,ebay_id)
	ebay_price_obj = {"Item":ebay_obj_to_update}
	# print("eeeeeeeeeeeeeeeeeeebayyyyyyyyyyyupdater ",ebay_price_obj)
	is_updated = ebay_handler.set_item_price(item_price_dict = ebay_price_obj)
	is_updated = True
	if is_updated and existing_ebay_item and ebay_obj_to_update.get("Quantity") != "0":
		existing_ebay_item.status = "monitored"
		existing_ebay_item.quantity = "2"
		# print("in monitored")
	elif existing_ebay_item and ebay_obj_to_update.get("Quantity") == "0":

		existing_ebay_item.status = "unmonitored"
	if existing_ebay_item:
		existing_ebay_item.is_active = True
		existing_ebay_item.save()
		print("item saved")
	# print("existing_ebay_item",model_to_dict(existing_ebay_item))
	# needed = is_needed_to_update_info_on_ebay(amazon_info,ebay_items)









# testing_facade_new(data)