from django.conf.urls import patterns, url
from order_maker import views

urlpatterns = [
	url(r'^$',views.upload_order_file, name='upload_order_file'),
	url(r'^generate/$',views.generate, name='generate'),
	url(r'^record/$',views.record, name='record'),
	url(r'^closed/$',views.closed, name='closed'),
	url(r'^pnl/$',views.pnl, name='pnl'),
	url(r'^mismatch/$',views.mismatch, name='mismatch'),
	url(r'^NewOrders/$',views.NewOrders, name='NewOrders'),
	url(r'^remove_orders/$',views.remove_orders, name='remove_orders')

	]	
