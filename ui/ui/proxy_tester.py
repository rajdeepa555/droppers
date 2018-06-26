import urllib.request  as urllib2 
import requests

proxy_list = ["173.232.119.209:3128","196.16.83.163:3128","196.16.83.208:3128","196.17.155.1:3128","196.16.83.117:3128","173.232.119.170:3128","213.184.121.12:3128","196.19.254.251:3128","172.245.169.26:3128","173.232.119.160:3128","196.18.132.250:3128","196.18.132.135:3128","172.245.169.236:3128","196.19.254.51:3128","173.232.119.15:3128","172.245.169.186:3128","45.72.87.84:3128","196.17.155.37:3128","196.17.155.91:3128","196.17.155.213:3128","196.18.132.190:3128","196.18.132.146:3128","196.19.254.230:3128","45.72.87.112:3128","196.19.254.110:3128","45.72.87.24:3128","196.16.83.203:3128","213.184.121.78:3128","196.17.155.75:3128","172.245.169.121:3128","213.184.121.17:3128","172.245.169.49:3128","196.17.155.82:3128","196.18.132.160:3128","196.17.155.119:3128","45.72.87.30:3128","213.184.121.139:3128","173.232.119.221:3128","172.245.169.18:3128","173.232.119.222:3128","196.18.132.3:3128","213.184.121.90:3128","196.19.254.218:3128","45.72.87.3:3128","213.184.121.123:3128","196.16.83.99:3128","196.17.155.188:3128","196.16.83.236:3128","45.72.87.71:3128","196.19.254.85:3128"]


# for proxy in proxy_list:
# 	try:
# 		proxies = {"https":"https://"+proxy,"http":"http://"+proxy}
# 		print("proxy",proxy)
# 		opener = urllib2.build_opener()
# 		# opener.addheaders = {'Accept-Language': ['en'], Accept-Encoding': ['gzip,deflate'], 'Accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'], 'User-Agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')}
# 		opener.addheaders = [('Accept-Language','en'),('Accept-Encoding','gzip,deflate'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('User-Agent','Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
# 		# {'Accept-Language': ['en'], 'Accept-Encoding': ['gzip,deflate'], 'Accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'], 'User-Agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')}
# 		# opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36')]
# 		proxy = urllib2.ProxyHandler(proxies)
# 		opener = urllib2.build_opener(proxy)

# 		url = "https://www.amazon.in"

# 		response = urllib2.urlopen(url,timeout=5)
# 		print("response",response.status)
# 	except Exception as e:
# 		print("Error....",e)


for proxy in proxy_list:
	# try:
		proxies = {"https":"https://"+proxy,"http":"http://"+proxy}
		url = "https://www.amazon.in"
		print("proxy",proxy)
		headers = {'Accept-Language': 'en', 'Accept-Encoding': 'gzip,deflate', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'}

		response = requests.get(url, headers=headers,proxies=proxies)
		print("response",response.status_code)
	# except Exception as e:
		# print("Error....",e)