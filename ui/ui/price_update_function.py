from .db import get_ebay_items, query_set_to_list, get_all_active_sellers_account
from .utils import make_amazon_url, get_float,get_run_id,make_amazon_url_for_list_primes
from .factory import get_ebayhandler, get_amazonscraper, get_proxyhandler
from .helpers import is_value_empty
import re
import time

def get_required_handlers(token):
	amazon_handler = get_amazonscraper()
	ebay_handler = get_ebayhandler(token)
	proxy_handler = get_proxyhandler()
	return amazon_handler,ebay_handler,proxy_handler

def get_active_seller_account(current_user,is_active):
	seller_accounts = get_all_active_sellers_account(user_id=current_user,is_active=is_active)
	seller_accounts = query_set_to_list(seller_accounts)
	return seller_accounts

def assign_proxy(amazon_handler,proxy_handler):
	current_proxy = proxy_handler.get_proxy()
	print("current proxy",current_proxy)
	amazon_handler.proxies.update({"https":current_proxy})

def scrape_again(amazon_handler,amazon_asin):
	amazon_handler.get_prime_detail = True
	amazon_url = make_amazon_url_for_list_primes(amazon_asin)
	print("new url",amazon_url)
	res = amazon_handler.scrape_with_error(amazon_url)
	print("ressss",res)
	res["price"] = amazon_handler.prime_price
	res["is_prime"] = amazon_handler.is_prime
	res["in_stock"] = amazon_handler.in_stock
	# print("RESSS",res)
	return res


def get_amazon_info(amazon_asin,amazon_handler,proxy_handler):
	amazon_handler.prime_price = ''
	amazon_handler.response_dict = {}
	amazon_handler.asin = amazon_asin
	amazon_handler.get_prime_detail = False
	assign_proxy(amazon_handler,proxy_handler)
	amazon_url = make_amazon_url(amazon_asin)
	amazon_handler.asin = amazon_asin
	print("final url to scrape",amazon_url)
	res = amazon_handler.scrape_with_error(amazon_url)
	print("res after first call",res)
	retry = 0
	if res.get("is_prime") == False or res.get("in_stock") == False or res.get("price") == '':
		res = scrape_again(amazon_handler,amazon_asin)
	while res is None or "503" in res or amazon_handler.is_captcha_in_response:
		time.sleep(5)
		amazon_handler.get_prime_detail = False
		if amazon_handler.is_captcha_in_response or "503" in res:
			assign_proxy(amazon_handler,proxy_handler)
			res = amazon_handler.scrape_with_error(amazon_url)
			# print("res on first scrape",res)
			if res.get("is_prime") == False or res.get("in_stock") == False or res.get("price") == '' or res == {}:
				res = scrape_again(amazon_handler,amazon_asin)
				retry -= 1
				# print("response on again scrape",res)
		retry += 1
		if retry == 8:
			print("I think proxies are not working")
			break
	if retry == 8:
		exit(0)
	return res

def get_amazon_asin_to_update(ebay_item):
	amazon_asin = ebay_item.custom_label
	amazon_asin_re = re.findall(r'\d+', amazon_asin)
	if len(amazon_asin_re)>0:
		return amazon_asin
	else:
		# print("inside else of get asin")
		return None


def get_ebay_obj_to_update(amazon_info,price_formula_obj,ebay_item_obj,default_stock):
	ebay_obj = {}
	ebay_obj["ItemID"] = ebay_item_obj.ebay_id
	is_out_of_stock = is_eligible_for_out_of_stock(amazon_info)
	if is_out_of_stock:
		ebay_obj["Quantity"] = "0"
	else:
		cost_components = get_cost_components(amazon_info,price_formula_obj,ebay_item_obj)
		ebay_price = get_final_cost(cost_components)
		ebay_obj["Quantity"] = str(default_stock)
		ebay_obj["StartPrice"] = ebay_price
		if ebay_item_obj.stock_level and ebay_item_obj.stock_level > 0:
			ebay_obj["Quantity"] = ebay_item_obj.stock_level
	print("ebay object",ebay_obj)
	return ebay_obj


def is_eligible_for_out_of_stock(item):
	return_value = False
	if is_value_empty(item.get("price")) or item.get("in_stock") == False or item.get("is_prime") == False:
		return_value = True
	return return_value

def get_update_item_status(is_updated,ebay_item,ebay_obj_to_update,default_stock):
	if is_updated and ebay_item and ebay_obj_to_update.get("Quantity") != "0":
		if ebay_item.stock_level and ebay_item.stock_level > 0:
			ebay_item.quantity = ebay_item.stock_level
		else:
			ebay_item.quantity = str(default_stock)
		ebay_item.status = "monitored"

	elif ebay_item and ebay_obj_to_update.get("Quantity") == "0":
		ebay_item.status = "unmonitored"
	if ebay_item:
		ebay_item.is_active = True
		ebay_item.price = ebay_obj_to_update.get("StartPrice",ebay_item.price)
		ebay_item.save()
		print("succefully save")


def get_cost_components(amazon_info,price_formula_obj,existing_ebay_obj):
	cost_components = {}
	cost_components["price"] = get_clear_price(amazon_info.get("price"))
	cost_components["margin_perc"] = price_formula_obj.get("perc_margin")
	cost_components["fixed_margin"] = price_formula_obj.get("fixed_margin")
	cost_components["ebay_listing_fee"] = price_formula_obj.get("ebay_listing_fee")
	cost_components["paypal_fees_fixed"] = price_formula_obj.get("paypal_fees_fixed")
	cost_components["ebay_final_value_fee"] = price_formula_obj.get("ebay_final_value_fee")
	cost_components["paypal_fees_perc"] = price_formula_obj.get("paypal_fees_perc")
	if existing_ebay_obj:
		if existing_ebay_obj.margin_perc:
			print("margin perc",existing_ebay_obj.margin_perc)
			cost_components["margin_perc"] = existing_ebay_obj.margin_perc
		if existing_ebay_obj.minimum_margin:
			print("minimum margin",existing_ebay_obj.minimum_margin)
			cost_components["fixed_margin"] = existing_ebay_obj.minimum_margin
	print("cost component",cost_components)
	return cost_components

def get_final_cost(cost_components):
	price = cost_components.get("price")
	margin_perc = cost_components.get("margin_perc") * price/100
	fixed_margin = cost_components.get("fixed_margin")
	cost = price + cost_components.get("ebay_listing_fee") + cost_components.get("paypal_fees_fixed")
	if margin_perc < fixed_margin:
		cost = cost + fixed_margin
		print("cost",cost)
	else:
		cost = cost + margin_perc
		print("else cost",cost)
	p = 1 - ((cost_components.get("ebay_final_value_fee") + cost_components.get("paypal_fees_perc"))/100)
	cost_after_profit = get_float(cost / p)
	print(".............price after formula...........................................",cost_after_profit)
	return cost_after_profit

def is_needed_to_update_info_on_ebay(amazon_info,ebay_info):
	return True

def get_clear_price(p_str):
	f_str = None
	if p_str:
		price = re.findall("[0-9\.]+",p_str)
		if len(price)>0:
			f_str = get_float(float("".join(price)))
	return f_str

