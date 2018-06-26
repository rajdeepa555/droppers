from .factory import get_ebayhandler
from .helpers_ebay import get_page_number,get_ebay_item_list,get_ebay_items_list_from_ebay_response
from .parsers import parse_ebay_item
import csv

def get_item_in_csv(seller_id, seller_token):
	print("inside insssserttttt data")
	ebay_handler = get_ebayhandler(seller_token)
	print("after ebay_handler")
	no_of_pages = get_page_number(ebay_handler)
	print("no of pages",no_of_pages)
	if no_of_pages:
		file = csv.writer(open("output1.csv","w"))
		for page in range(1,no_of_pages+1):
			ebay_items_response = get_ebay_item_list(ebay_handler,page)
			ebay_items = get_ebay_items_list_from_ebay_response(ebay_items_response)
			# print("eeeeeeebay item................................................",ebay_items)
			count=0
			parselist = []
			for item in ebay_items:
				count = count + 1
				parsed_data = parse_ebay_item(item,seller_id)
				parselist.append(parsed_data)
				file.writerow([count,parsed_data])
