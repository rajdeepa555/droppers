from .models import AmazonRunDetails,ProxyLog
from datetime import datetime

def log_amazon_url(run_id,group_id,amazon_url,ebay_id,is_ebay_updated,amazon_response_dict,proxy_used=None):
	amazon_log = AmazonRunDetails.objects.filter(amazon_url=amazon_url)
	if amazon_log:
		amazon_log = amazon_log.first()
		amazon_log.run_id = run_id
		amazon_log.group_id = group_id
		# amazon_log.amazon_url = amazon_url
		# amazon_log.ebay_id = ebay_id
		amazon_log.scrape_time = datetime.now() 
		amazon_log.is_ebay_updated = is_ebay_updated
		amazon_log.price_str = amazon_response_dict.get("price","")
		amazon_log.in_stock_str = amazon_response_dict.get("in_stock",False)
		amazon_log.is_prime = amazon_response_dict.get("is_prime",0)
		# print("amazon_response_dict:",amazon_response_dict)
		# print("amazon_log.is_prime:",amazon_log.is_prime)
		amazon_log.proxy_used = proxy_used
		amazon_log.save()
	else:
		print("amazon_url not found",amazon_url)

def log_proxy(run_id,group_id,url,proxy,failure_cause=""):
	proxy_log = ProxyLog()
	proxy_log.proxy = proxy
	proxy_log.url = url
	proxy_log.run_id = run_id
	proxy_log.group_id = group_id
	proxy_log.failure_cause = failure_cause
	proxy_log.save()