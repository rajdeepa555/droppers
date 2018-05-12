from .models import EbaySellerItems, SellerTokens, EbayPriceFormula
from django.forms.models import model_to_dict

def get_ebay_items(**filters):
	ebay_items = EbaySellerItems.objects.filter(**filters)
	return ebay_items

def query_set_to_list(query_set,list_of_values=None):
	query_set_list = []
	if query_set:
		query_set_list = list(query_set.values())
	return query_set_list

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
	return value