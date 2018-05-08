import datetime
from django.utils.crypto import get_random_string
import string
import re
import math
from .models import EbaySellerItems

def normalize_amazon_url(url):
	amazon_url = url
	#remove everything after hash
	amazon_url = amazon_url.split("#")[0]
	if 'https' not in amazon_url and 'http' in amazon_url:
		amazon_url = amazon_url.replace('http','https')
	return amazon_url

def get_run_id():
	current_datetime = datetime.now().strftime("%Y%m%d%H%M")
	random_id = 'RUN_{}'.format(get_random_string(5, string.ascii_letters))
	return random_id+"_"+current_datetime

def make_amazon_url(asin):
	return "https://amazon.com/dp/"+str(asin)

def make_amazon_url_for_list_primes(asin):
	return "https://www.amazon.com/gp/offer-listing/%s?f_primeEligible=true"+str(asin)

def is_eligible_for_ebay_update(price,in_stock,is_prime,stock):
	is_eligible = False
	price_str = ""
	stock_str = "0"
	print("is_prime",is_prime)
	print("is_prime_type: ",type(is_prime))
	if price is not None and in_stock is not None and len(price)>0 and is_prime is not False:
		clear_price = re.findall("[0-9.]+",price)
		if len(clear_price)>0:
			print("clear_price",clear_price)
			price_str = str(float("".join(clear_price)))
			if in_stock == "True" or in_stock==True:
				if stock:
					stock_str = stock
				else:
					stock_str = "2"
		is_eligible = True

	return is_eligible,price_str,stock_str

def get_float(num):
	return_value = 0.00
	try:
		return_value = math.ceil(num*100)/100
	except:
		pass
	return return_value

def get_current_time():
	return datetime.datetime.now()

def get_time_diff_from_now(old_time):
	now = datetime.datetime.now()
	previous = old_time
	time_delta = now - previous
	exact_diff = divmod(time_delta.days*86400+time_delta.seconds,60)
	second_diff = exact_diff[1]
	return second_diff


def format_val(value):
	return format(value,'.2f')

def get_value_from_dict(dict_object,attrs_list):
	final_value = dict_object
	if len(attrs_list)>0:
		for attr in attrs_list:
			if attr in final_value:
				final_value = final_value.get(attr)
			else:
				final_value = None
				break
	else:
		final_value = None
	return final_value