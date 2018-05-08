from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
# Create your models here.
class SellerTokens(models.Model):
    user = models.ForeignKey(User)
    sellername = models.CharField(max_length=255)
    token = models.CharField(max_length = 1000)
    is_active = models.BooleanField(default = False)

    def __str__(self):
        return self.sellername

class EbayProductsCsvData(models.Model):
    seller_account = models.ForeignKey('SellerTokens')
    local_id = models.CharField(max_length=255,default="")
    vendor_url  = models.CharField(max_length=255,default="")
    vendor_variant  = models.CharField(max_length=255,default="")
    vendor_stock    = models.CharField(max_length=255,default="")
    vendor_price    = models.CharField(max_length=255,default="")
    vendor_shipping = models.CharField(max_length=255,default="")
    reference   = models.CharField(max_length=255,default="")
    compare_url = models.CharField(max_length=255,default="")
    compare_variant = models.CharField(max_length=255,default="")
    compare_stock   = models.CharField(max_length=255,default="")
    compare_price   = models.CharField(max_length=255,default="")
    compare_shipping    = models.CharField(max_length=255,default="")
    profit_formula  = models.CharField(max_length=255,default="")
    selling_formula = models.CharField(max_length=255,default="")
    reprice_store   = models.CharField(max_length=255,default="")
    reprice_sku = models.CharField(max_length=255,default="")
    reprice_pause   = models.CharField(max_length=255,default="")
    sales_price = models.CharField(max_length=255,default="")
    estimated_profit    = models.CharField(max_length=255,default="")
    autoCompare = models.CharField(max_length=255,default="")



class EbaySessionID(models.Model):
    session_id = models.CharField(max_length = 255)

class EbayAmazonPriceFormula(models.Model):
    seller_account = models.ForeignKey('SellerTokens')
    minimum_range = models.IntegerField()
    maximum_range = models.IntegerField()
    vendor_tax = models.IntegerField()
    margin = models.IntegerField()
    fixed_margin = models.IntegerField()
    minimum_margin = models.IntegerField()
    paypal_fees_perc = models.IntegerField()
    paypal_fees_fixed = models.IntegerField()
    ebay_fees = models.IntegerField()
    manual_override = models.IntegerField()

class Proxy(models.Model):
    proxy = models.CharField(max_length=25,default="")
    is_active = models.IntegerField(default=1)

class ProxyLog(models.Model):
    proxy = models.CharField(max_length=50,default="")
    url = models.CharField(max_length=255,default="")
    run_id = models.CharField(max_length=255,default="")
    group_id = models.CharField(max_length=255,default="")
    failure_cause = models.CharField(max_length=255,default="")
    failure_time = models.DateTimeField(auto_now=True)


class AmazonRun(models.Model):
    run_id = models.CharField(max_length=255, primary_key=True)
    run_start_time = models.DateTimeField(auto_now=True)
    # run_finish_time = models.DateTimeField(blank=True)

class AmazonRunDetails(models.Model):
    # run_id = models.ForeignKey(AmazonRun, on_delete=models.CASCADE)
    run_id = models.CharField(max_length=255,default="")
    group_id = models.CharField(max_length=255,default="")
    amazon_url = models.CharField(max_length=255,default="")
    scrape_time = models.DateTimeField(auto_now=True)
    price_str = models.CharField(max_length=20,default="")
    is_prime = models.BooleanField(default=False)
    is_ebay_updated = models.BooleanField(default=False)
    in_stock_str = models.CharField(max_length=10,default="")
    proxy_used = models.CharField(max_length=50,default="")
    ebay_id = models.CharField(max_length=30,default="")
    is_eligible_for_ebay_update = models.BooleanField(default=True)
    cause_if_fail = models.CharField(max_length=255,default="")
    

class EbayRunDetails(models.Model):
    seller_account = models.ForeignKey('SellerTokens')
    run_id = models.CharField(max_length=255,default="")
    group_id = models.CharField(max_length=255,default="")
    amazon_url = models.CharField(max_length=255,default="")
    updated_time = models.DateTimeField(auto_now=True)
    price_str = models.CharField(max_length=20,default="")
    in_stock_str = models.CharField(max_length=10,default="")
    ebay_price = models.CharField(max_length=10,default="")
    ebay_stock = models.CharField(max_length=10,default="")
    is_ebay_updated = models.BooleanField(default=False)
    cause_if_fail = models.CharField(max_length=255,default="")
    ebay_url = models.CharField(max_length=255,default="")
    ebay_id = models.CharField(max_length=255,default="")



class EbaySellerSearchReports(models.Model):
    seller_account = models.ForeignKey('SellerTokens',null = True)
    run_id = models.CharField(max_length=255,default="")
    seller_id = models.CharField(max_length=255,default="")
    item_found = models.IntegerField(default= 0)
    date_of_search =  models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255,default = "")


class EbaySellerSearch(models.Model):
    # seller_account = models.ForeignKey('SellerTokens',null = True)
    search_report = models.ForeignKey('EbaySellerSearchReports',null = True)
    run_id = models.CharField(max_length=255,default="")
    seller_id = models.CharField(max_length=255,default="")
    title = models.CharField(max_length=255,default="")
    price_str = models.FloatField(max_length=255,default="-1")
    ebay_url = models.CharField(max_length=255,default="")
    item_sold = models.CharField(max_length=255,default="")
    amazon_url = models.CharField(max_length=1000,default="")
    amazon_price_str = models.CharField(max_length=255,default="")
    is_active = models.BooleanField(default=False)
    added_to_pending = models.BooleanField(default=False)


class EbaySellerSearchPendingItems(models.Model):
    seller_account = models.ForeignKey('SellerTokens')
    run_id = models.CharField(max_length=255,default="")
    seller_id = models.CharField(max_length=255,default="")
    title = models.CharField(max_length=255,default="")
    price_str = models.FloatField(max_length=255,default="-1")
    ebay_url = models.CharField(max_length=255,default="")
    item_sold = models.CharField(max_length=255,default="")
    amazon_url = models.CharField(max_length=1000,default="")
    amazon_price_str = models.CharField(max_length=255,default="")

class EbaySellerItems(models.Model):
    seller = models.ForeignKey('SellerTokens')
    photo = models.CharField(max_length=255,default="")
    product_name = models.CharField(max_length=255,default="")
    ebay_id = models.CharField(max_length=255,primary_key=True)
    custom_label = models.CharField(max_length=255,default="",null = True)
    price = models.FloatField(max_length=255,default="-1")
    quantity = models.IntegerField(default= "-1")
    no_of_times_sold = models.IntegerField(default="-1")
    date_of_listing = models.DateField(auto_now=False)
    margin_perc = models.FloatField(max_length=255,null=True)
    minimum_margin = models.FloatField(max_length=255,null=True)
    stock_level = models.IntegerField(null=True)
    status = models.CharField(max_length=255,default="monitored")
    flag = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    modified_at = models.DateTimeField(auto_now=True)

    def get_modified_date(self):
        return self.modified_at.strftime("%Y-%m-%d %H:%M")
     
# class AddEbaySellerKeyset(models.Model):
#     sellername = models.CharField(max_length=255)
#     appid = models.CharField(max_length=100)
#     devid = models.CharField(max_length=100)
#     certid = models.CharField(max_length=100)
#     token = models.CharField(max_length=1000)

class EbayPriceFormula(models.Model):
    seller = models.ForeignKey('SellerTokens')
    ebay_final_value_fee = models.FloatField(default = 0.0)
    ebay_listing_fee = models.FloatField(default = 0.0)
    paypal_fees_perc = models.FloatField(default = 0.0)
    paypal_fees_fixed = models.FloatField(default = 0.0)
    perc_margin = models.FloatField(default = 0.0)
    fixed_margin = models.FloatField(default = 0.0)

# class Person (models.Model):
   
#     DEGINATION_CHOICE = (
#         ('', 'Select One'),
#         ('Assistant Professor', 'Assistant Professor'),
#         ('Associate Professor', 'Associate Professor'),
#         ('Faculty Member', 'Faculty Member'),
#         ('Graduate Student', 'Graduate Student'),
#         ('Librarian', 'Librarian'),
#         ('Non-Academic', 'Non-Academic'),
#         ('Person', 'Person'),
#         ('Postdoc', 'Postdoc'),
#         ('Professor', 'Professor'),
#         ('Undergraduate Student', 'Undergraduate Student'),
#     )
#     First_name       = models.CharField(max_length=80)
#     Midle_name       = models.CharField(max_length=60, blank=True)
#     Last_name        = models.CharField(max_length=60)
#     name             = models.CharField(max_length=200)
#     catagory         = models.CharField(max_length=20, choices=DEGINATION_CHOICE)
#     phone            = models.CharField(max_length=40)
#     email            = models.CharField(max_length=100)
#     image            = models.FileField()
#     slug             = models.SlugField(max_length=120, blank=True, unique=True)
    
#     def get_absolute_url(self):
#        return reverse('detail', kwargs={"slug": self.slug})
       
#     def _get_unique_slug(self):
#         slug = slugify(self.name)
#         unique_slug = slug
#         num = 1
#         while Person.objects.filter(slug=unique_slug).exists():
#             unique_slug = '{}-{}'.format(slug, num)
#             num += 1
#         return unique_slug
    
#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.slug = self._get_unique_slug()
#         super(Person, self).save(*args, **kwargs)
    
#     def __str__(self):
#         return self.name