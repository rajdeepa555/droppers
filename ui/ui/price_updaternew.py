from .utils import get_boolean


def apply_price_formula(amazon_info,apply_price_formula_obj,ebay_item):
	ebay_obj = {}
	ebay_obj["ItemID"] = ebay_item.ebay_id
	is_out_of_stock = get_ebay_obj_to_update(amazon_info)
	if is_out_of_stock == True:
		ebay_obj["Quantity"] = "0"
	else:
		cost_components = get_cost_components(amazon_info,price_formula_obj,ebay_item)
		ebay_price = get_final_cost(cost_components)
		ebay_obj["Quantity"] = "2"
		ebay_obj["StartPrice"] = ebay_price
	return ebay_obj

def get_ebay_obj_to_update(amazon_info):
	"""
		1. if price is not available then put this in out of stock
		2. if item is not prime same as above
		3. if item is out of stock same as above
		4. else create a proper ebay obj and return
	"""
	current_price = amazon_info.get("price")
	is_in_stock = get_boolean(amazon_info.get("in_stock"))
	is_prime = get_boolean(amazon_info.get("is_prime"))
	
	out_of_stock = False
	if current_price is None or len(str(current_price))<1:
		out_of_stock = True
	elif is_in_stock == False:
		out_of_stock = True
	elif is_prime == False:
		out_of_stock = True
	return out_of_stock


def get_amazon_info(ebay_item):
	return None

def process_ebay_item(ebay_item, amazon_handler, proxy_handler, ebay_handler):
	amazon_info = get_amazon_info(ebay_item)
	ebay_obj_to_update = get_ebay_obj_to_update(amazon_info)
	

def price_updater(seller_id):
	all_ebay_items = get_all_ebay_items(seller_id)
	amazon_handler, proxy_handler, ebay_handler = get_required_handlers()
	for ebay_item in all_ebay_items:
		process_ebay_item(ebay_item, amazon_handler, proxy_handler, ebay_handler) 


