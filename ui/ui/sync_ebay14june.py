from .db import get_ebay_items, query_set_to_list, get_all_active_sellers_account, \
				get_price_formula, get_existing_value, create_ebay_item,set_ebay_items_to_inactive, \
				create_batchlog_item, create_run_item
from .utils import get_simple_list_from_list_dict, get_value_from_dict, \
				 make_amazon_url, get_float,get_run_id
from .factory import get_ebayhandler, get_amazonscraper, get_proxyhandler
# from .helpers import is_value_empty
from .parsers import parse_ebay_item
from .helpers_ebay import get_page_number,get_ebay_item_list,get_ebay_items_list_from_ebay_response
from .models import EbaySellerItems
 
def insert_data(seller_id, seller_token):
	print("inside insssserttttt data")
	ebay_handler = get_ebayhandler(seller_token)
	no_of_pages = get_page_number(ebay_handler)
	print("no of pages",no_of_pages)
	if no_of_pages:
		for page in range(1,no_of_pages+1):
			ebay_items_response = get_ebay_item_list(ebay_handler,page)
			ebay_items = get_ebay_items_list_from_ebay_response(ebay_items_response)
			count=0
			for item in ebay_items:
				count = count + 1
				parsed_data = parse_ebay_item(item,seller_id)
				ebay_id = item['ItemID']
				parsed_data.pop("ebay_id")
				parsed_data["is_active"] = True
				# print("parsed.......",parsed_data)
				try:
					ebay_obj,created = EbaySellerItems.objects.get_or_create(ebay_id=ebay_id,defaults=parsed_data)
					if not created:
						# print("inside not created")
						ebay_obj.is_active = True
						ebay_obj.save()
						# print("isactive...",ebay_obj.is_active)
					# input("enter")
				except Exception as e:
					print("error in create_ebay_item",e)
					parsed_data["product_name"] = "title contains some latin word, not able to parse"
					ebay_obj,created = EbaySellerItems.objects.get_or_create(ebay_id=ebay_id,defaults=parsed_data)
				# if ebay_id in ['263288587131']:
					# print("created.....................................",created)
					# input("get vo vali ebay_id")
