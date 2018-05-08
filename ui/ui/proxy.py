from .models import Proxy
import math

class CProxy(object):
	
	def __init__(self,no_of_threads,group_index):
		self.proxy_list = []
		self.current_proxy = None
		self.no_of_threads = no_of_threads
		self.group_index = group_index
		self._prepare_proxy_list()

	def _get_offset(self):
		proxy_start_index = 0
		proxy_end_index = 0
		proxy_in_a_group = int(math.floor(float(len(self.proxy_list))/float(self.no_of_threads)))
		proxy_start_index = self.group_index*proxy_in_a_group
		if self.no_of_threads == (self.group_index+1):
			proxy_end_index = len(self.proxy_list)
		else:
			proxy_end_index = proxy_start_index+(proxy_in_a_group)
		return proxy_start_index,proxy_end_index


	def _add_https_prefix(self,proxy):
		return "https://"+proxy

	def _prepare_proxy_list(self):
		proxy_list = Proxy.objects.filter(is_active=1)
		if proxy_list is not None and len(proxy_list)>0:
			all_proxies = []
			for proxy in proxy_list: 
				all_proxies.append(self._add_https_prefix(proxy.proxy))
			self.proxy_list = all_proxies
			start_index, end_index = self._get_offset()
			self.proxy_list = all_proxies[start_index:end_index+1]


	def _get_next_proxy_index(self):
		next_proxy_index = 0
		if self.current_proxy is not None:
			current_proxy_index = self.proxy_list.index(self.current_proxy)
			next_proxy_index =   (current_proxy_index+1) % len(self.proxy_list)
		return next_proxy_index

	def get_proxy(self):
		if self.proxy_list is not None and len(self.proxy_list)>0:
			self.current_proxy = self.proxy_list[self._get_next_proxy_index()]
		return self.current_proxy

	