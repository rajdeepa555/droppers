import re
from .utils import get_simple_list_from_list_dict, get_value_from_dict, \
				 make_amazon_url, get_float,get_run_id
# from .utils import get_float
from .factory import get_ebayhandler
from .parsers import parse_ebay_item

def get_int(val):
	if val and isinstance(val,int)\
	 or (isinstance(val,str) and val.isdigit())\
	 or isinstance(val,float):
		val = int(float(str(val)))
	else:
		val = None
	return val

def get_page_number(ebay_handler):
	o = ebay_handler.get_all_items()
	no_of_pages = get_value_from_dict(o,["ActiveList","PaginationResult","TotalNumberOfPages"])
	no_of_pages = get_int(no_of_pages)
	print("nooooo offfffff pageee",no_of_pages)
	return no_of_pages

def get_ebay_item_list(ebay_handler,page=1):
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
