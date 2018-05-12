from .ebay import EbayHandler
from .amazonapi import AmazonScraper
from .proxy import CProxy

def get_ebayhandler(seller_auth_token=None):
	obj = EbayHandler()
	if seller_auth_token:
		obj.token = seller_auth_token
		obj.update_trading_api()
	return obj

def get_amazonscraper(locale="UK"):
	obj = AmazonScraper(locale=locale)
	return obj

def get_proxyhandler():
	obj = CProxy(1,0)
	return obj
