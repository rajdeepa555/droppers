# from .sync_ebay import insert_data
# from .models import EbaySellerItems
from .helpers_ebay import get_int, get_page_number,get_ebay_item_list,get_ebay_items_list_from_ebay_response
from .factory import get_ebayhandler
# from .sync_ebay import insert_data
from .price_updaternew import get_ebay_obj_to_update

def get_ebay_obj_to_update_test():
	amazon_info = {'price': '','is_stock':True,'is_prime':True}
	c = get_ebay_obj_to_update(amazon_info)
	print("outofstock",c)
	assert(c == True),"case failed"

def get_ebay_obj_to_update_test1():
	amazon_info = {'price':'22','is_stock':False,'is_prime':True}
	c = get_ebay_obj_to_update(amazon_info)
	print("outofstock",c)
	assert(c == True),"case failed"

def get_ebay_obj_to_update_test2():
	amazon_info = {'price':'1','is_stock':True,'is_prime':False}
	c = get_ebay_obj_to_update(amazon_info)
	print(c)
	assert(c == True),"case failed"

get_ebay_obj_to_update_test2()

def no_of_pages_tests():
   c = get_int(None)
   assert(c == None) , "None case failed"

   c = get_int("4")
   assert(c == 4) , "4 case failed"

   c = get_int(4.0000)
   assert(c == 4) , "4.000 case failed"

   c = get_int("one")
   assert(c == None) , "one case failed"

   c = get_int(4)
   assert(c == 4) , "one case failed"

def testing_get_pages():
	seller_token = 'AgAAAA**AQAAAA**aAAAAA**tZoLWw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wNmIqhCZmKowWdj6x9nY+seQ**M30DAA**AAMAAA**xmIRNGY2AS6Tca6Jh8VHjly5PEwgzdQNkUoL/N1P5CvdCNFRaLRUHhjrOZrebBuxm2Ubjd7Up68ZBQHUzZCRkrvK/mM+WIpQslSYyZh02jnctvHofYVM6BOGaR4/3vEYen3akuwiUjh8VfnkgJ0RdikMdga95dr8KNz4uAW88M3IC1WVMu9mD3zeVXw9GqcOdxPXRXOT1SXaEHnaRV6hdn6/etLIJYxaOinARLbKtO3Jikd2DCzaqkiQ94S3xhN3oDapjKHCT1cLmGM7DK/9G3r5xlrL/nt+lvZEIcAvs2r/FPb1kWtsy/Nbj1NoUQiDkQxk6lxH1nuHUOibDPBsVD8YRCayHpcy/hh0PqOteBxD81/CtNeE19YiAlNvJ9kvwkU6opNeKnss3Y5NoynQ/xRRaKggwjt8cYexVTHpsmbPRDdgxuMjmqjgmwxNnOnsJvK8ZwaUIQav0aVx35yNek2q5KHD2WTYR9OyhfOUEnFFSZGkttz6Arm4Fy4zHQVcDGWhmNqK5gPujn8W3K1uEMFQndmywLwkJAq3LWyKCT+hD9lNuqT4qXkmD2UpXrw1aHSX64M/QVs0KNcaRIde9Ip3EptVdPvixyi/4oLSGN6pFZlsRV4BO+fSOJlwGwJ8SojNUHfbZO5zgswfuGJpjTTaXHA/7A8/e0VCYkigKGLfTpCCQYgal2S16HoKva8LMPgBOOfe4/CLCHaKUsXOTnHigfLQZNxqIgGz5e2n8n1FpbItIVtdR3GlDiWEWXe6'	
	ebay_handler = get_ebayhandler(seller_token)
	c = get_page_number(ebay_handler)
	print("c",c)
	assert(type(c) == int) , "one case failed"

def get_ebay_item_list_test():
	seller_token = 'AgAAAA**AQAAAA**aAAAAA**tZoLWw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wNmIqhCZmKowWdj6x9nY+seQ**M30DAA**AAMAAA**xmIRNGY2AS6Tca6Jh8VHjly5PEwgzdQNkUoL/N1P5CvdCNFRaLRUHhjrOZrebBuxm2Ubjd7Up68ZBQHUzZCRkrvK/mM+WIpQslSYyZh02jnctvHofYVM6BOGaR4/3vEYen3akuwiUjh8VfnkgJ0RdikMdga95dr8KNz4uAW88M3IC1WVMu9mD3zeVXw9GqcOdxPXRXOT1SXaEHnaRV6hdn6/etLIJYxaOinARLbKtO3Jikd2DCzaqkiQ94S3xhN3oDapjKHCT1cLmGM7DK/9G3r5xlrL/nt+lvZEIcAvs2r/FPb1kWtsy/Nbj1NoUQiDkQxk6lxH1nuHUOibDPBsVD8YRCayHpcy/hh0PqOteBxD81/CtNeE19YiAlNvJ9kvwkU6opNeKnss3Y5NoynQ/xRRaKggwjt8cYexVTHpsmbPRDdgxuMjmqjgmwxNnOnsJvK8ZwaUIQav0aVx35yNek2q5KHD2WTYR9OyhfOUEnFFSZGkttz6Arm4Fy4zHQVcDGWhmNqK5gPujn8W3K1uEMFQndmywLwkJAq3LWyKCT+hD9lNuqT4qXkmD2UpXrw1aHSX64M/QVs0KNcaRIde9Ip3EptVdPvixyi/4oLSGN6pFZlsRV4BO+fSOJlwGwJ8SojNUHfbZO5zgswfuGJpjTTaXHA/7A8/e0VCYkigKGLfTpCCQYgal2S16HoKva8LMPgBOOfe4/CLCHaKUsXOTnHigfLQZNxqIgGz5e2n8n1FpbItIVtdR3GlDiWEWXe6'	
	ebay_handler = get_ebayhandler(seller_token)
	c = get_ebay_item_list(ebay_handler)
	print("ebay_item_list",c)
	assert(c == dict(c)),"one case failed"

def get_ebay_items_list_from_ebay_response_testing():
	seller_token = 'AgAAAA**AQAAAA**aAAAAA**tZoLWw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wNmIqhCZmKowWdj6x9nY+seQ**M30DAA**AAMAAA**xmIRNGY2AS6Tca6Jh8VHjly5PEwgzdQNkUoL/N1P5CvdCNFRaLRUHhjrOZrebBuxm2Ubjd7Up68ZBQHUzZCRkrvK/mM+WIpQslSYyZh02jnctvHofYVM6BOGaR4/3vEYen3akuwiUjh8VfnkgJ0RdikMdga95dr8KNz4uAW88M3IC1WVMu9mD3zeVXw9GqcOdxPXRXOT1SXaEHnaRV6hdn6/etLIJYxaOinARLbKtO3Jikd2DCzaqkiQ94S3xhN3oDapjKHCT1cLmGM7DK/9G3r5xlrL/nt+lvZEIcAvs2r/FPb1kWtsy/Nbj1NoUQiDkQxk6lxH1nuHUOibDPBsVD8YRCayHpcy/hh0PqOteBxD81/CtNeE19YiAlNvJ9kvwkU6opNeKnss3Y5NoynQ/xRRaKggwjt8cYexVTHpsmbPRDdgxuMjmqjgmwxNnOnsJvK8ZwaUIQav0aVx35yNek2q5KHD2WTYR9OyhfOUEnFFSZGkttz6Arm4Fy4zHQVcDGWhmNqK5gPujn8W3K1uEMFQndmywLwkJAq3LWyKCT+hD9lNuqT4qXkmD2UpXrw1aHSX64M/QVs0KNcaRIde9Ip3EptVdPvixyi/4oLSGN6pFZlsRV4BO+fSOJlwGwJ8SojNUHfbZO5zgswfuGJpjTTaXHA/7A8/e0VCYkigKGLfTpCCQYgal2S16HoKva8LMPgBOOfe4/CLCHaKUsXOTnHigfLQZNxqIgGz5e2n8n1FpbItIVtdR3GlDiWEWXe6'	
	ebay_handler = get_ebayhandler(seller_token)
	ebay_items_response = get_ebay_item_list(ebay_handler)
	c = get_ebay_items_list_from_ebay_response(ebay_items_response)
	print("cccc",c)
	assert(c == list(c)),"case failed"

def insert_data_testing():
	seller_token = 'AgAAAA**AQAAAA**aAAAAA**tZoLWw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wNmIqhCZmKowWdj6x9nY+seQ**M30DAA**AAMAAA**xmIRNGY2AS6Tca6Jh8VHjly5PEwgzdQNkUoL/N1P5CvdCNFRaLRUHhjrOZrebBuxm2Ubjd7Up68ZBQHUzZCRkrvK/mM+WIpQslSYyZh02jnctvHofYVM6BOGaR4/3vEYen3akuwiUjh8VfnkgJ0RdikMdga95dr8KNz4uAW88M3IC1WVMu9mD3zeVXw9GqcOdxPXRXOT1SXaEHnaRV6hdn6/etLIJYxaOinARLbKtO3Jikd2DCzaqkiQ94S3xhN3oDapjKHCT1cLmGM7DK/9G3r5xlrL/nt+lvZEIcAvs2r/FPb1kWtsy/Nbj1NoUQiDkQxk6lxH1nuHUOibDPBsVD8YRCayHpcy/hh0PqOteBxD81/CtNeE19YiAlNvJ9kvwkU6opNeKnss3Y5NoynQ/xRRaKggwjt8cYexVTHpsmbPRDdgxuMjmqjgmwxNnOnsJvK8ZwaUIQav0aVx35yNek2q5KHD2WTYR9OyhfOUEnFFSZGkttz6Arm4Fy4zHQVcDGWhmNqK5gPujn8W3K1uEMFQndmywLwkJAq3LWyKCT+hD9lNuqT4qXkmD2UpXrw1aHSX64M/QVs0KNcaRIde9Ip3EptVdPvixyi/4oLSGN6pFZlsRV4BO+fSOJlwGwJ8SojNUHfbZO5zgswfuGJpjTTaXHA/7A8/e0VCYkigKGLfTpCCQYgal2S16HoKva8LMPgBOOfe4/CLCHaKUsXOTnHigfLQZNxqIgGz5e2n8n1FpbItIVtdR3GlDiWEWXe6'	
	seller_id = 1
	# c = insert_data(seller_id,seller_token)
	print("c",c)
	assert(c!=12345),"e_bay id already exist it will not create"

# insert_data_testing()
# 	seller_token = 'AgAAAA**AQAAAA**aAAAAA**tZoLWw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wNmIqhCZmKowWdj6x9nY+seQ**M30DAA**AAMAAA**xmIRNGY2AS6Tca6Jh8VHjly5PEwgzdQNkUoL/N1P5CvdCNFRaLRUHhjrOZrebBuxm2Ubjd7Up68ZBQHUzZCRkrvK/mM+WIpQslSYyZh02jnctvHofYVM6BOGaR4/3vEYen3akuwiUjh8VfnkgJ0RdikMdga95dr8KNz4uAW88M3IC1WVMu9mD3zeVXw9GqcOdxPXRXOT1SXaEHnaRV6hdn6/etLIJYxaOinARLbKtO3Jikd2DCzaqkiQ94S3xhN3oDapjKHCT1cLmGM7DK/9G3r5xlrL/nt+lvZEIcAvs2r/FPb1kWtsy/Nbj1NoUQiDkQxk6lxH1nuHUOibDPBsVD8YRCayHpcy/hh0PqOteBxD81/CtNeE19YiAlNvJ9kvwkU6opNeKnss3Y5NoynQ/xRRaKggwjt8cYexVTHpsmbPRDdgxuMjmqjgmwxNnOnsJvK8ZwaUIQav0aVx35yNek2q5KHD2WTYR9OyhfOUEnFFSZGkttz6Arm4Fy4zHQVcDGWhmNqK5gPujn8W3K1uEMFQndmywLwkJAq3LWyKCT+hD9lNuqT4qXkmD2UpXrw1aHSX64M/QVs0KNcaRIde9Ip3EptVdPvixyi/4oLSGN6pFZlsRV4BO+fSOJlwGwJ8SojNUHfbZO5zgswfuGJpjTTaXHA/7A8/e0VCYkigKGLfTpCCQYgal2S16HoKva8LMPgBOOfe4/CLCHaKUsXOTnHigfLQZNxqIgGz5e2n8n1FpbItIVtdR3GlDiWEWXe6'	
# 	seller_id = 1 
# 	obj,create = insert_data(seller_id,seller_token)
# 	print("c",
