from .utils import get_simple_list_from_list_dict, get_value_from_dict, \
				 make_amazon_url, get_float,get_run_id,make_amazon_url_for_list_primes
from .factory import get_ebayhandler, get_amazonscraper, get_proxyhandler
from .helpers import is_value_empty
import re, csv

def get_total_no_of_pages(ebay_handler):
	o = ebay_handler.get_all_items()
	no_of_pages = get_value_from_dict(o,["ActiveList","PaginationResult","TotalNumberOfPages"])
	return no_of_pages


def get_ebay_item_list(ebay_handler,page = 1):
	ebay_items_list = []
	if ebay_handler:
		ebay_items_list = ebay_handler.get_all_items(page_number=page)
	return ebay_items_list


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


def get_final_cost(price):
	profit = open("formula.txt","r").read()
	profit = profit.strip()
	if len(profit) < 1:
		exit(0)
	else:
		print("profit",profit)
		final_cost = (price + float(profit) + .3 ) / .871
		print("final cost",final_cost)
		return final_cost

def is_eligible_for_out_of_stock(item):
	return_value = False
	# print('is_value_empty(item.get("price"))',is_value_empty(item.get("price")),'item.get("in_stock")',item.get("in_stock"),'item.get("is_prime")',item.get("is_prime"))
	if is_value_empty(item.get("price")) or item.get("in_stock") == False or item.get("is_prime") == False:
		return_value = True
	return return_value




def get_clear_price(p_str):
	f_str = None
	if p_str:
		price = re.findall("[0-9\.]+",p_str)
		if len(price)>0:
			f_str = get_float(float("".join(price)))
	return f_str


def get_ebay_obj_to_update(ebay_id):
	ebay_obj = {}
	ebay_obj["ItemID"] = ebay_id
	ebay_obj["Quantity"] = "0"
	return ebay_obj

def dump_to_csv(csv_instance, amazon_asin ,amazon_info, ebay_info,file_obj):
	csv_instance.writerow([amazon_asin, amazon_info.get("price"), amazon_info.get("is_prime"),\
		amazon_info.get("in_stock"), ebay_info.get("StartPrice"), ebay_info.get("Quantity"), ebay_info.get("ItemID") ])
	# print("final....",[amazon_asin, amazon_info.get("price"), amazon_info.get("is_prime"),\
		# amazon_info.get("in_stock"), ebay_info.get("StartPrice"), ebay_info.get("Quantity"), ebay_info.get("ItemID") ])
	file_obj.flush()

def process_ebay_item(ebay_item, ebay_handler):
	# amazon_asin = 'B00QGJ1ZEY'
	ebay_id = ebay_item.get("ItemID")
	ebay_obj_to_update = get_ebay_obj_to_update(ebay_id)
	ebay_price_obj = {"Item":ebay_obj_to_update}
	print("ebay_obj_to_update",ebay_price_obj)
	# input("press enter")
	# dump_to_csv(csv_instance, amazon_asin ,amazon_info,ebay_obj_to_update,file_obj)
	is_updated = ebay_handler.set_item_price(item_price_dict = ebay_price_obj)

def testing_facade():
	ebay_handler = get_ebayhandler()
	ebay_handler.token = 'AgAAAA**AQAAAA**aAAAAA**4X/6Wg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wJnYWnDJiGpg2dj6x9nY+seQ**M30DAA**AAMAAA**tExZITR2pCIuIZaiNDpUrcttSk2B7wA0AUGSH6+xz33SMXYZ2nDPWdGYWHku8tfN1kAhtalvQsfoSsJYUcgafNA5pNE6yYkys87APOuNri1ZLpiZyOxRVvQCdPilgibhUQXs7S2UjIBv5JNWPNLfZmFCqSgEMFlneprXo5CV2wIjlT6p5LaYstB6OqXjGzazukels37HYKyUgeqpglL44ByDtTa0MXzlxTWhSkX9WaHkjDRBSsuQYDFz1BVVXsyBuOO8RwhAXXJ43L0CYYcJ72ReNgLULBDucmFAB9bMzSkSOUbCY3vLYjywx1YQfLsaAvQsOd+SNaAjp8C3yp856wpjFesPyPib72KPDkvxxP7hp+Eh5zLqnufiRJng58uB3LibTurRZn6UuiwRYXCoFuTtrUBLUMehBVexDxsDMrLE1UERyXQQZfZXvBOKF09Prmkl9f56PFUSiUohGxc8KOpK/kLKNJJJtVQ//N5ln89oa2QygEuXk1u0g2iy7rYVZbghdVnap7T5cwYa9hnrG2nJhNjDTQ4taonxb5LJOGEjZ92vJ9DOEBjos1u86ElGRgLFRU1iTYptw5zINYk41FNy2RFX7mlHQlR+J+Vl2XAiBGT2MKeh0nSQOTMuv7QfkdMQ3qRjJYBvNcwYxqfJiIYMWU5qLBB6VahfyXkDgm1dDe1e98ElPxKWTazRlCRT++WOJlPJLE0GHnYYjQGJh4I7HhF/fwaNZzy1Pe7hRIPz1BY7Mymmc4uNA3VMboKA'
	ebay_handler.update_trading_api()
	no_of_pages = get_total_no_of_pages(ebay_handler)
	print("no_of_pages",no_of_pages)
	file_obj = open('ebay_amazon7.csv','w')
	csv_instance = csv.writer(file_obj,0)
	csv_instance.writerow(["amazon_asin","amazon price","is_prime","in_stock","ebay_price","ebay_quantity","ebay_id"])
	if no_of_pages and int(no_of_pages)>0:
		no_of_pages = int(no_of_pages)
		for page in range(1,no_of_pages+1):
			print("page no:",page," of ",no_of_pages)
			if page<75:
				continue
			ebay_items_response = get_ebay_item_list(ebay_handler,page)
			ebay_items = get_ebay_items_list_from_ebay_response(ebay_items_response)
			if not ebay_items and isinstance(ebay_items,list):
				print("invalid ebay_items list")
				continue
			# amazon_handler = get_amazonscraper()
			# proxy_handler = get_proxyhandler()
			for ebay_item in ebay_items:
				try:
					# amazon_handler.get_prime_detail = False
					process_ebay_item(ebay_item,ebay_handler)

					# input("process_ebay_item")
				except Exception as e:
					# batch_log = create_batchlog_item(run_id = run_id,seller = current_seller_id,ebay_id=ebay_item["ItemID"],error_log = e)
					print("error!!!",e)
		
testing_facade()
