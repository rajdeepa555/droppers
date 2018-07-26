from .db import get_seller_token, create_temp_ebay_item, make_temp_table_empty, \
				delete_items_not_available_on_ebay, get_ebay_objects_to_insert, create_ebay_obj
from .utils import get_value_from_dict,get_sellers_account
from .factory import get_ebayhandler
from .parsers import parse_ebay_item
from .helpers_ebay import get_page_number, get_ebay_items_list_from_ebay_response


def parse_and_insert_to_db(item,seller_id):
	parsed_data = parse_ebay_item(item,seller_id)
	print("parsed_data",parsed_data)
	create_temp_ebay_item(**parsed_data)

def get_and_process_ebay_items(ebay_handler,page_number,seller_id):
	ebay_response = ebay_handler.get_all_items(page_number=page_number)
	if ebay_response is not None:
		ebay_items_list = get_ebay_items_list_from_ebay_response(ebay_response)
		for item in ebay_items_list:
			parse_and_insert_to_db(item,seller_id)


def get_ebay_items_and_insert_to_temp_table(seller_id):
	print("seller id ..............",seller_id)
	seller_token = get_seller_token(seller_id)
	ebay_handler = get_ebayhandler(seller_token)
	no_of_pages = get_page_number(ebay_handler)+1
	for i in range(1,no_of_pages):
		print("processing page", i," out of ", no_of_pages)
		get_and_process_ebay_items(ebay_handler,i,seller_id)

def insert_new_items_available_on_ebay(seller_id):
	ebay_object_to_insert = get_ebay_objects_to_insert(seller_id)
	if ebay_object_to_insert:
		for ebay_obj in ebay_object_to_insert:
			create_ebay_obj(ebay_obj,seller_id)

def sync_ebay_item(seller_id):
	done = make_temp_table_empty()
	print("sellerrr id",seller_id)
	done = get_ebay_items_and_insert_to_temp_table(seller_id)
	done = delete_items_not_available_on_ebay(seller_id)
	done = insert_new_items_available_on_ebay(seller_id)

def sync_all_ebay_item():
	current_user = '1'
	all_seller_account_of_current_user = get_sellers_account(current_user)
	if all_seller_account_of_current_user:
		for seller_accounts in all_seller_account_of_current_user:
			current_seller_id = seller_accounts.get("id")
			seller_token = seller_accounts.get("token")
			print("seller",current_seller_id,seller_token)
			is_update = seller_accounts.get("is_update")
			if not seller_token:
				print("seller_token not found for current seller account skipping...." )
				continue
			if is_update:
				print("current seller id ",current_seller_id)
				done = make_temp_table_empty()
				done = get_ebay_items_and_insert_to_temp_table(current_seller_id)
				done = delete_items_not_available_on_ebay(current_seller_id)
				done = insert_new_items_available_on_ebay(current_seller_id)
