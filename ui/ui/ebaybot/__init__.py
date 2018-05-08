# -*- coding: utf-8 -*-
import sys
from imp import reload
reload(sys)
# sys.setdefaultencoding('utf8')
import platform
import logging
from requests import Request, Session
import time
import lxml.html
import datetime
# import urllib2
import urllib.request  as urllib2 
from random import randint

UserAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'


class EbayScraper(object):
    
    def __init__(self,locale=None):
        self.domain = self._get_domain(locale)
        self.method = "GET"
        self.request = None
        self.response = None
        self.timeout = 10
        self.proxies = dict()
        self.session = Session()
        self._time = time.time()
        self.response_html = None
        self.response_dict = dict()
        self.response_list = []
        self.is_captcha_in_response = False
        self.proxy_checker = dict()
        self.current_proxy = ""
        self.opener = None
        self.ua_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063','Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5','Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 6.1; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1','Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0','Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0','Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36 OPR/46.0.2597.32','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)','Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36','Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 OPR/46.0.2597.39','Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36']
        self.response_code = None
        self.get_details = False
        self.upc = None
        self.isbn = None
        self.has_next = True
        self.next_url = ''


    def _init(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36')]
        # opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0')]

    def scrape(self,url):
        self._reset()
        # ebay_url = "https://www.ebay.com/sch/vminnovations/m.html?_nkw=&_armrs=1&_ipg=&_from=" 
        self._execute(url)
        return self.response_dict

    def _reset(self):
        self.is_captcha_in_response = False
        self.response_dict = dict()
        self.response = None
        self.response_html = None
        self.request = None
        self.response_code = None

    def change_proxy(self,proxy):
        print("captcha found waiting for 10 sec")
        time.sleep(10)
        self.proxies.update({"https":proxy})


    def _execute(self, url):
        proxy = urllib2.ProxyHandler(self.proxies)
        opener = urllib2.build_opener(proxy)
        # opener = urllib2.build_opener()
        ua = self.ua_list[randint(0,70)]
        opener.addheaders = [('User-Agent', ua)]
        urllib2.install_opener(opener)
        self.response = urllib2.urlopen(url,timeout=5)
        self.process_response()


    def _unicode_text(self,text):
        return text.encode("ascii","ignore")

    def _is_prime(self,hxs):
        prime_strings = ["Dispatched from and sold by Amazon","Dispatched from Amazon","Fulfilled by Amazon"]
        is_prime = False
        for prime_string in prime_strings:
            if len(hxs.xpath('//*[contains(text(),"%s")]' % (prime_string)))>0:
                is_prime = True
                break
        self.response_dict.update({"is_prime":is_prime})

    def _in_stock(self,hxs):
        stock_strings = ["In stock.","left in stock"]
        in_stock = False
        for stock_string in stock_strings:
            if len(hxs.xpath('//*[contains(text(),"%s")]' % (stock_string)))>0:
                in_stock = True
                break
        self.response_dict.update({"in_stock":in_stock})


    def _get_price(self,hxs):
        try:
            price_xpaths = ['//span[@id="priceblock_ourprice"]/text()','//span[@id="priceblock_saleprice"]/text()']
            price_found = False
            for xpath in price_xpaths:
                price = hxs.xpath(xpath)
                if len(price)>0:
                    price = price[0]
                    price_found = True
                    break
            if price_found == False:
                price = ""
            self.response_dict.update({"price":price})
        except:
            log.debug("price not found")



    def _get_ebay_items(self,hxs):
        ul = hxs.xpath("//ul[@id='ListViewInner']/li")
        is_next = hxs.xpath("//a[@aria-label = 'Next page of results']/@aria-disabled")
        if is_next and len(is_next)>0:
            self.has_next = False
            self.next_url = ''
        else:
            next_url = hxs.xpath("//a[@aria-label = 'Next page of results']/@href")
            self.next_url = next_url[0].strip()
            
        if len(ul)>0:
            ul_list = []
            cnt = 0
            for li in ul:
                cnt += 1
                print("Fetching Product...",cnt)
                try:
                    current_li = {}
                    title = li.xpath("./h3/a//text()")
                    title = " ".join(title).strip()
                    ebay_url = li.xpath("h3/a/@href")[0].strip()
                    price1 = li.xpath("ul[contains(@class,'lvprices left space-zero')]/li[@class='lvprice prc']/span/text()")
                    if len(price1)>0:
                        current_li["price"] = price1[0].strip()
                    item_sold = li.xpath("ul[contains(@class,'lvprices left space-zero')]/li[@class='lvextras']//div[@class='hotness-signal red']/text()")
                    if len(item_sold)>0:
                        current_li["item_sold"] = item_sold[0].strip()
                    current_li["title"] = title
                    current_li["ebay_url"] = ebay_url
                    ul_list.append(current_li)
                except Exception as e:
                    print("error with scraping ebay..",e)

            self.response_list = ul_list

    def _get_item_details(self,hxs):
        upc = hxs.xpath("//td[contains(text(),'UPC')]/following-sibling::td/h2[@itemprop = 'gtin13']/text()")
        isbn = hxs.xpath("//td[contains(text(),'ISBN')]/following-sibling::td/h2[@itemprop = 'productID']/text()")
        if upc and upc != None and len(upc)>0:
            upc = upc[0].strip()
            try:
                self.upc = int(upc)
            except:
                self.upc = ''
        else:
            self.upc = ''

        if isbn and isbn != None and len(isbn)>0:
            isbn = isbn[0].strip()
            try:
                self.isbn = int(isbn)
            except:
                self.isbn = ''
        else:
            self.isbn = ''


    def _parse_response(self):
        if "Robot Check" in self.response_html.decode('UTF-8'):
            print("captcha found")
            # f = open("captcha.html","wb")
            # f.write(self.response_html)
            # f.close()
            self.is_captcha_in_response = True
        elif self.response_html:
            doc  = lxml.html.document_fromstring(self.response_html)
            if self.get_details == True:
                self._get_item_details(doc)
            else:
                self._get_ebay_items(doc)

    def _parse_response2(self):
        if "Robot Check" in self.response_html.decode('UTF-8'):
            print("captcha found")
            # f = open("captcha.html","wb")
            # f.write(self.response_html)
            # f.close()
            self.is_captcha_in_response = True
        elif self.response_html:
            doc  = lxml.html.document_fromstring(self.response_html)
            ip = doc.xpath('//font[@size="5"]/b/text()')
            if len(ip)>0:
                self.proxy_checker[self.current_proxy] = ip[0].strip()
            # f_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            # f = open(f_name,"wb")
            # f.write(self.response_html)
            # f.close()

    def process_response(self):
        self.response_code = self.response.code
        if self.response.code==200:
            # self.response_html = self._unicode_text(self.response.read())
            self.response_html = self.response.read()
            self._parse_response()
  

    def _get_domain(self,locale):
        DOMAINS = {
                'CA': 'ca',
                'DE': 'de',
                'ES': 'es',
                'FR': 'fr',
                'IN': 'in',
                'IT': 'it',
                'JP': 'co.jp',
                'UK': 'co.uk',
                'US': 'com',
                'CN': 'cn'
            }
        return DOMAINS[locale]