from django.conf.urls import  include, url
from django.contrib import admin
from .views import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Examples:
    # url(r'^$', 'ui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/rq/', include('django_rq.urls')),
	
	url(r'^$', HomeView.as_view(), name='home'),
	url(r'^login/$', auth_views.login, name='login'),
    # url(r'^accounts/', include('allauth.urls')),
    url(r'^logout/$', auth_views.logout,{'next_page': '/login'}, name='logout'),
	url(r'^upload-csv/$', EbayFileUploadView.as_view(), name='upload-csv'),
	url(r'^upload-proxies/$', ProxyLoaderView.as_view(), name='upload-proxies'),
	url(r'^dashboard-values/$', DashboardValuesView.as_view(), name='dashboard-values'),
	# url(r'^update-price-formula/(?P<pk>[0-9]+)/$', UpdateAmazonEbayFormula.as_view(), name='update-price-formula'),
	# url(r'^price-formula/$', AmazonEbayFormula.as_view(), name='price-formula'),
	# url(r'^price-formula/$', CreateEbayFormula.as_view(), name='price-formula'),
	url(r'^price-formula/$', UpdateEbayFormula.as_view(), name='price-formula'),
	url(r'^download-ebay-csv/$', DownloadEbayCsv.as_view(), name='download-ebay-csv'),
	url(r'^init-run-details/$', InitRunDetails.as_view(), name='init-run-details'),
	url(r'^reset-tables/$', ResetForNewRun.as_view(), name='reset-tables'),
	url(r'^kill-celery/$', ShutdownCeleryInstance.as_view(), name='kill-celery'),
	url(r'^start-celery/(?P<process>[0-9]+)/$', StartCeleryInstance.as_view(), name='start-celery'),
	url(r'^start-process/$', StartProcess.as_view(), name='start-process'),
	url(r'^search-seller/(?P<pk>[0-9]+)/$', SearchSellerView.as_view(), name='search-seller'),
	url(r'^search-seller-item/$', SearchSellerItemView.as_view(), name='search-seller-item'),
	url(r'^search-amazon-item/$', SearchAmazonItem.as_view(), name='search-amazon-item'),
	url(r'^start-seller-search/(?P<seller_id>[a-zA-Z0-9-_]+)/$', StartSellerSearch.as_view(), name='start-seller-search'),
	url(r'^update-ebay-items/$', UpdateEbayItems.as_view(), name='update-ebay-items'),
	url(r'^update-all-ebay-items/$', UpdateAllEbayItems.as_view(), name='update-all-ebay-items'),
	url(r'^edit-ebay-items/$', EditEbayItems.as_view(), name='edit-ebay-items'),
	url(r'^get-sellers-item/$', SearchSellerNameView.as_view(), name='get-sellers-item'),
	url(r'^get-pending-items/$', GetPendingItemsView.as_view(), name='get-pending-items'),
	url(r'^manual-pending-item-add/$', ManualPendingItemAddView.as_view(), name='manual-pending-item-add'),
	url(r'^add-ebay-sellers-item/$', InsertEbaySellerItems.as_view(), name='add-ebay-sellers-item'),
	url(r'^get-ebay-sellers-item/$', SearchSellerItemNameView.as_view(), name='get-ebay-sellers-item'),
	url(r'^get-ebay-sellers-itemm/$', SearchSellerItemNameView2.as_view(), name='get-ebay-sellers-itemm'),
	url(r'^ebay-keyset-add/$', EbaySellerKeysetView.as_view(),name='ebay-keyset-add'),
	url(r'^add-ebay-keyset/$', AddEbaySellerKeysetView.as_view(),name='add-ebay-keyset'),
	url(r'^get-ebay-seller-keyset/$', GetEbaySellerKeysetView.as_view(),name='get-ebay-seller-keyset'),
	url(r'^pending-ebay-items/$', csrf_exempt(InsertPendingEbayItems.as_view()),name='pending-ebay-items'),
	url(r'^view-pending-ebay-items/$', PendingEbayItems.as_view(),name='view-pending-ebay-items'),
	url(r'^delete-pending-ebay-items/$', DeletePendingEbayItems.as_view(),name='delete-pending-ebay-items'),
	url(r'^export-csv-seller-items/$', ExportCsvSellerItems.as_view(),name='export-csv-seller-items'),
	url(r'^ebay-profit-calculator/$', EbayProfitCalculatorView.as_view(),name='ebay-profit-calculator'),
	url(r'^get-ebay-profit/$', csrf_exempt(EbayProfitCalculator.as_view()),name='get-ebay-profit'),
	url(r'^set-item-margin/$', SetItemMarginView.as_view(),name='set-item-margin'),
	url(r'^set-item-stock-level/$', SetItemStockLevelView.as_view(),name='set-item-stock-level'),
	url(r'^flag-seller-ebay-items/$', csrf_exempt(FlagSellerItems.as_view()),name='flag-seller-ebay-items'),
	url(r'^adminer/$', AdminerView.as_view(),name='adminer'),
	# url(r'^test-rq/$', TestRqView.as_view(),name='test-rq'),
	url(r'^ebay-connect/$', EbayConnect.as_view(),name='ebay-connect'),
	url(r'^login-page-to-ebay/$', LoginPageToEbay.as_view(),name='login-page-to-ebay'),
	url(r'^multi-ebay-account/$', MultiEbayAccountSettingPage.as_view(),name='multi-ebay-account'),
	url(r'^activate-seller-account/$', ActivateSellerAccount.as_view(),name='activate-seller-account'),
	url(r'^search-seller-reports/$', SearchSellerReports.as_view(),name='search-seller-reports'),
	url(r'^search-seller-reports-data/$', SearchSellerReportsData.as_view(),name='search-seller-reports-data'),
	
	# url(r'^update-price-formula/(?P<pk>[0-9]+)$', AmazonEbayFormula.as_view(), name='update-price-formula'),
	# url(r'^update-price-formula/$', AmazonEbayFormula.as_view(), name='update-price-formula'),
    url(r'^admin/', include(admin.site.urls)),

]
urlpatterns += staticfiles_urlpatterns()