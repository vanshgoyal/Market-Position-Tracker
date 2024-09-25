from __future__ import unicode_literals

from django.db import models

import datetime
# Create your models here.

class Order_position_open(models.Model):
	Trade_Choice=(
		('CE','Call'),
		('PE','Put'),
		)
	seg = models.CharField(max_length=128,default="NFO")
	acc_id = models.CharField(max_length=128,null=True)
	trade_name = models.CharField(null=True,max_length = 255)
	trade_qty = models.IntegerField(default=0)
	trade_price = models.FloatField(default=0,max_length=10)
	buy_or_sell = models.CharField(default="SELL",max_length=10)
	trade_time = models.CharField(max_length=10)
	b_w_l = models.CharField(null=True,blank=True,max_length=10)
	user_id = models.CharField(max_length=128,null=True)
	strike_price = models.FloatField(default=0,max_length=10)
	expiry_date = models.DateField(null=True)
	opt_type = models.CharField(null=True,max_length=2,choices=Trade_Choice)
	symbol = models.CharField(null=True,max_length=255)
	trade_date = models.DateField(default=datetime.date.today)
	trade_uid = models.IntegerField(default=0)
	covering_rate = models.FloatField(default=0,max_length=10)

class Order_position_close(models.Model):
	Trade_Choice=(
		('CE','Call'),
		('PE','Put'),
		)
	seg = models.CharField(max_length=128,default="NFO")
	acc_id = models.CharField(max_length=128,null=True)
	trade_name = models.CharField(null=True,max_length = 255)
	trade_qty = models.IntegerField(default=0)
	trade_price = models.FloatField(default=0,max_length=10)
	buy_or_sell = models.CharField(default="SELL",max_length=10)
	trade_time = models.CharField(max_length=10)
	b_w_l = models.CharField(null=True,blank=True,max_length=10)
	user_id = models.CharField(max_length=128,null=True)
	strike_price = models.FloatField(default=0,max_length=10)
	expiry_date = models.DateField(null=True)
	opt_type = models.CharField(null=True,max_length=2,choices=Trade_Choice)
	symbol = models.CharField(null=True,max_length=255)
	trade_date = models.DateField(default=datetime.date.today)
	trade_uid = models.IntegerField(default=0)

class user_details(models.Model):
	user = models.CharField(max_length=128,null=True)
	pwd = models.CharField(max_length=128,null=True)