from .models import EbaySellerItems, SellerTokens, EbayPriceFormula, \
					BatchLogger, AmazonRun, TempEbayItems
from django.forms.models import model_to_dict

def get_ebay_items(**filters):
	ebay_items = EbaySellerItems.objects.filter(**filters)
	return ebay_items

def set_ebay_items_to_inactive(seller_id):
	ebay_items = EbaySellerItems.objects.filter(seller_id = seller_id).update(is_active = False)
	return True

def query_set_to_list(query_set,list_of_values=None):
	query_set_list = []
	if query_set:
		query_set_list = list(query_set.values())
	return query_set_list


def get_all_sellers_account(**filters):
	all_sellers = SellerTokens.objects.filter(**filters)
	return all_sellers

def get_all_active_sellers_account(**filters):
	all_sellers = SellerTokens.objects.filter(**filters)
	return all_sellers

def get_price_formula(**filters):
	formula_dict = None
	formula_obj = EbayPriceFormula.objects.filter(**filters)
	if formula_obj is not None and len(formula_obj)>0:
		formula_obj = formula_obj.first()
		formula_dict = model_to_dict(formula_obj)
	return formula_dict

def get_existing_value(query_set,**filters):
	value = None
	if query_set:
		value = query_set.filter(**filters)
	if value and len(value)>0:
		value = value.first()
	else:
		value = None
	return value

def create_ebay_item(**params):
	ebay_obj = None
	try:
		ebay_obj = EbaySellerItems.objects.create(**params)
	except Exception as e:
		print("error in create_ebay_item",e)
		params["product_name"] = "title contains some latin word, not able to parse"
		ebay_obj = EbaySellerItems.objects.create(**params)
	return ebay_obj

def create_temp_ebay_item(**params):
	ebay_obj = None
	try:
		ebay_obj = TempEbayItems.objects.create(**params)
	except Exception as e:
		print("error in create_temp_ebay_item",e)
		params["product_name"] = "title contains some latin word, not able to parse"
		ebay_obj = TempEbayItems.objects.create(**params)
	return ebay_obj

def create_batchlog_item(**params):
	batch_obj = None
	try:
		batch_obj = BatchLogger.objects.create(**params)
	except:
		pass
	return batch_obj

def create_run_item(**params):
	run_obj = None
	try:
		run_obj = AmazonRun.objects.create(**params)
	except:
		pass
	return run_obj

def get_seller_token(seller_id):
	seller_token = None
	try:
		seller_token = SellerTokens.objects.get(id=seller_id).token
	except:
		print('seller_id:',seller_id," does not exists...")
	return seller_token

def create_insert_ebay_item(ebay_id,parsed_data):
	try:
		# print("inside try")
		ebay_obj,created = EbaySellerItems.objects.get_or_create(ebay_id=ebay_id,defaults=parsed_data)
	except Exception as e:
		# print("inside except")
		parsed_data["product_name"] = "title contains some latin word, not able to parse"
		ebay_obj,created = EbaySellerItems.objects.get_or_create(ebay_id=ebay_id,defaults=parsed_data)
	ebay_obj.is_active = True
	# print("trueeeeeee",ebay_obj.is_active)
	ebay_obj.save()
	return ebay_obj


def make_temp_table_empty():
	TempEbayItems.objects.all().delete()

def delete_items_not_available_on_ebay(seller_id):
	temp_ids = TempEbayItems.objects.all()
	temp_ids = list(temp_ids.values_list('ebay_id',flat=True))
	extra_items_in_db = EbaySellerItems.objects.filter(seller_id=seller_id).exclude(ebay_id__in=temp_ids)
	extra_items_in_db.delete()

def get_ebay_objects_to_insert(seller_id):
	existing_ebay_ids = EbaySellerItems.objects.filter(seller_id=seller_id)
	existing_ebay_ids = list(existing_ebay_ids.values_list('ebay_id',flat=True))
	temp_ebay_objs_to_insert = TempEbayItems.objects.all().exclude(ebay_id__in=existing_ebay_ids)
	return temp_ebay_objs_to_insert


def create_ebay_obj(temp_obj,seller_id):
	ebay_obj = None
	print("seller id in create ebay................")
	if temp_obj is not None:
		ebay_obj = EbaySellerItems()
		ebay_obj.ebay_id = temp_obj.ebay_id
		ebay_obj.photo = temp_obj.photo
		ebay_obj.product_name = temp_obj.product_name
		ebay_obj.custom_label = temp_obj.custom_label
		ebay_obj.price = temp_obj.price
		ebay_obj.quantity = temp_obj.quantity
		ebay_obj.no_of_times_sold = temp_obj.no_of_times_sold
		ebay_obj.date_of_listing = temp_obj.date_of_listing
		ebay_obj.seller_id = seller_id
		ebay_obj.is_active = True
		ebay_obj.save()
	return ebay_obj
