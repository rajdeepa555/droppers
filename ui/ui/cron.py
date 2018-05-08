import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .utils import get_run_id
# from .tasks import scrape_amazon,start_ebay_update
from .models import EbayRunDetails,AmazonRun,AmazonRunDetails,EbayAmazonPriceFormula,EbayProductsCsvData,EbaySellerSearch
import re
from .ebay import EbayHandler
import math
from .utils import normalize_amazon_url
from .amazonapi import AmazonScraper
from .ebaybot import *
from .proxy import CProxy



def create_random_user_accounts():
	total = 10
	for i in range(total):
		username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
		email = '{}@example.com'.format(username)
		password = get_random_string(50)
		User.objects.create_user(username=username, email=email, password=password)
	return '{} random users created with success!'.format(total)

def init_amazon_run_details():
	amazon_url_list = EbayProductsCsvData.objects.all()
	for row in amazon_url_list:
		new_amazon_details_object = AmazonRunDetails()
		new_amazon_details_object.amazon_url = normalize_amazon_url(row.vendor_url)

def scrape_amazon_urls():
	no_of_threads = 3
	run_id = get_run_id()
	amz_run = AmazonRun()
	amz_run.run_id = run_id
	amz_run.save()
	for i in range(0,no_of_threads):
		# f.apply_async(args=[ingested_file_id], queue='import')
		# scrape_amazon.delay(run_id,i,no_of_threads)
		scrape_amazon.apply_async(args=[run_id,i,no_of_threads])
		print("run_id: ",run_id," group_id: ",i,"no_of_threads: ",no_of_threads)	
	# start_ebay_update.apply_async()

def start_ebay_bot():
	es = EbayScraper(locale="UK")
	es.scrape("https://www.ebay.com/sch/mastershoe/m.html?_nkw=&_armrs=1&_ipg=&_from=")

def scrape_amazon_urls2():
	no_of_threads = 1
	run_id = "RUN_ZTlOm_201710202208"
	# amz_run = AmazonRun()
	# amz_run.run_id = run_id
	# amz_run.save()
	for i in range(0,no_of_threads):
		# f.apply_async(args=[ingested_file_id], queue='import')
		# scrape_amazon.delay(run_id,i,no_of_threads)
		scrape_amazon.apply_async(args=[run_id,i,no_of_threads])
		print("run_id: ",run_id," group_id: ",i,"no_of_threads: ",no_of_threads)	
	# start_ebay_update.apply_async()

def start_ebay_process():
	no_of_threads = 8
	for i in range(0,no_of_threads):
		start_ebay_update.apply_async(args=[i,no_of_threads])
		print("thread id: ",i,"total thread:",no_of_threads)
	print("ebay updater start")