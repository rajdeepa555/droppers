from .db import get_ebay_items, get_price_formula, create_batchlog_item, create_run_item
from .utils import get_run_id,get_sellers_account
from .factory import get_amazonscraper, get_proxyhandler
from .price_update_function import assign_proxy,scrape_again,get_amazon_info,\
				get_ebay_obj_to_update,is_eligible_for_out_of_stock,get_cost_components,\
				get_final_cost,is_needed_to_update_info_on_ebay,get_clear_price,get_required_handlers,\
				get_amazon_asin_to_update,get_update_item_status
from .models import *
import re



def process_selected_ebay_item(ebay_items,amazon_handler,proxy_handler,ebay_handler,seller_id):

	amazon_asin = get_amazon_asin_to_update(ebay_items)
	if amazon_asin is not None:
		print("amazonasin",amazon_asin)
		amazon_info = get_amazon_info(amazon_asin,amazon_handler,proxy_handler)
		print("amazoninfo.....",amazon_info)
		current_seller_formula = get_price_formula(seller_id=seller_id)
		if not current_seller_formula:
			print("formula for current seller not found skipping......")
			exit(0)
		ebay_obj_to_update = get_ebay_obj_to_update(amazon_info,current_seller_formula,ebay_items)
		ebay_price_obj = {"Item":ebay_obj_to_update}
		
		is_updated = ebay_handler.set_item_price(item_price_dict = ebay_price_obj)
		is_updated = True
		update_status = get_update_item_status(is_updated,ebay_items,ebay_obj_to_update)
		needed = is_needed_to_update_info_on_ebay(amazon_info,ebay_items)	


def update_ebay_item(data):
	for ebay_item in data:
		token = ebay_item.seller.token
		seller_id = ebay_item.seller_id
		print("seller_id",seller_id)
		print("token",token)
		run_id = get_run_id()
		run = create_run_item(run_id=run_id)
		amazon_handler, ebay_handler, proxy_handler = get_required_handlers(token)
		try:
			process_selected_ebay_item(ebay_item,amazon_handler,proxy_handler,ebay_handler,seller_id)
		except Exception as e:
			print("inside exception")
			is_updated = False
			ebay_obj_to_update = {"Quantity":"0"}
			get_update_item_status(is_updated,ebay_item,ebay_obj_to_update)
			batch_log = create_batchlog_item(run_id = run_id,seller = seller_id,ebay_id=ebay_item.ebay_id,error_log = e)
			print("error!!!",e)


