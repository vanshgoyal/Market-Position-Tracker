from django.shortcuts import render
from django.http import HttpResponse
from forms import upload_file_form
from models import Order_position_open, Order_position_close,user_details
# from datetime import datetime
# from datetime import timedelta
import datetime
import simplejson
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
import pandas as pd
import numpy as np
import csv
from random import randint
import uuid
import math
import re
import requests
import time
import json
# Create your views here.

new_orders = []
extra_orders = []
def got_file(f):
    print ('got_file started')
    fo = open('trade_file.csv', 'w')
    for lines in f:
        fo.write(lines)

    fo.close();
    fs = open('trade_file.csv', 'r')
    line = fs.readline()
    # first only insert sell options into the db
    month_name_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05',
        'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    test_dict = []
    count = 1
    for lines in fs:
        lines = lines.replace('\r\r\n', '')
        lines = lines.replace('/n', '')
        lines = lines.strip()
        lines = lines.split(',')
        if len(lines)>5:
            pass
        else:
            lines = ["a", "a", "aaaaaaa", "a", "a", "a"]
        if (lines[5] == "S") and (lines[0] == "NSEFO") and (lines[2][-3:] != "FUT"):
            #d_str = lines[10].strip()
            #exp_date = int(d_str[:2])
            #exp_month = int(month_name_dict[d_str[2:5]])
            #exp_year = int(d_str[5:])
            sell_check = Order_position_close.objects.all().filter(
            seg=lines[0],
            acc_id=lines[1],
            trade_name=lines[2],
            trade_qty=int(lines[3]),
            trade_price=float(lines[4]),
            buy_or_sell=lines[5],
            trade_time=lines[6],
            b_w_l=lines[7],
            user_id=lines[8],
            strike_price=float(lines[9]),
            expiry_date=datetime.datetime.strptime(lines[10], "%d-%m-%Y"),
            opt_type=lines[11],
            symbol=lines[13],
            trade_uid=lines[12]
            )
            if len(sell_check) == 0:
                sell = Order_position_open.objects.get_or_create(
                    seg=lines[0],
                    acc_id=lines[1],
                    trade_name=lines[2],
                    trade_qty=int(lines[3]),
                    trade_price=float(lines[4]),
                    buy_or_sell=lines[5],
                    trade_time=lines[6],
                    b_w_l=lines[7],
                    user_id=lines[8],
                    strike_price=float(lines[9]),
                    expiry_date=datetime.datetime.strptime(lines[10], "%d-%m-%Y"),
                    opt_type=lines[11],
                    symbol=lines[13],
                    trade_uid=lines[12]
                    )
            # count += 1

    fs.close()

    # now remove all the corresponding buys
    fb = open('trade_file.csv','r')
    line = fb.readline()
    for lines in fb:
        lines = lines.replace('\r\r\n','');
        lines = lines.replace('\n','');
        lines = lines.strip();
        lines = lines.split(',');
        if len(lines)>5:
            pass
        else:
            lines = ["a", "a", "aaaaaaa", "a", "a", "a"]
        sells_list = Order_position_open.objects.all().filter(trade_name=lines[2],buy_or_sell='S').order_by('-trade_price')
        if (lines[5] == "B") and (lines[0] == "NSEFO") and (lines[2][-3:] != "FUT"):
            #d_str = lines[10]
            #exp_date = int(d_str[:2])
            #exp_month = int(month_name_dict[d_str[2:5]])
            #exp_year = int(d_str[5:])
            buy_check = Order_position_close.objects.all().filter(
                    seg=lines[0],
                    acc_id=lines[1],
                    trade_name=lines[2],
                    trade_qty=int(lines[3]),
                    trade_price=float(lines[4]),
                    buy_or_sell=lines[5],
                    trade_time=lines[6],
                    b_w_l=lines[7],
                    user_id=lines[8],
                    strike_price=float(lines[9]),
                    expiry_date=datetime.datetime.strptime(lines[10], "%d-%m-%Y"),
                    opt_type=lines[11],
                    symbol=lines[13],
                    trade_uid=lines[12]
                )
            if (len(sells_list)==0) or (len(buy_check)!=0):
                # buy_open = Order_position_open.objects.get_or_create(
                #     seg = lines[0],
                #     acc_id = lines[1],
                #     trade_name = lines[2],
                #     trade_qty = int(lines[3]),
                #     trade_price = float(lines[4]),
                #     buy_or_sell = lines[5],
                #     trade_time = lines[6],
                #     b_w_l = lines[7],
                #     user_id = lines[8],
                #     strike_price = float(lines[9]),
                #     expiry_date = datetime.date(exp_year, exp_month, exp_date), # d.strftime("%d %b %Y").replace(' ','') gives 03Jun2016
                #     opt_type = lines[11],
                #     symbol = lines[12],
                #     trade_uid = lines[13],
                #     )
                continue
            else:
                sell = sells_list[0]
                buy_close = Order_position_close.objects.get_or_create(
                    seg=lines[0],
                    acc_id=lines[1],
                    trade_name=lines[2],
                    trade_qty=int(lines[3]),
                    trade_price=float(lines[4]),
                    buy_or_sell=lines[5],
                    trade_time=lines[6],
                    b_w_l=lines[7],
                    user_id=lines[8],
                    strike_price=float(lines[9]),
                    expiry_date=datetime.datetime.strptime(lines[10], "%d-%m-%Y"),
                    opt_type=lines[11],
                    symbol=lines[13],
                    trade_uid=lines[12]
                    )
                sell_close = Order_position_close.objects.get_or_create(
                    seg = sell.seg,
                    acc_id = sell.acc_id,
                    trade_name = sell.trade_name,
                    trade_qty = sell.trade_qty,
                    trade_price = sell.trade_price,
                    buy_or_sell = sell.buy_or_sell,
                    trade_time = sell.trade_time,
                    b_w_l = sell.b_w_l,
                    user_id = sell.user_id,
                    strike_price = sell.strike_price,
                    expiry_date = sell.expiry_date,
                    opt_type = sell.opt_type,
                    symbol = sell.symbol,
                    trade_uid = sell.trade_uid,
                    trade_date = sell.trade_date
                    )
                sell.delete();
    fb.close()
    return

def upload_order_file(request):
    x = request.session.get('username')
    y = request.session.get('password')
    if x or y:

        if request.method == 'POST':
            form = upload_file_form(request.POST, request.FILES)
            if request.FILES['trade_file'].name.split('.')[-1] != 'csv':
                return render(request, 'order_maker/upload_order_file.html',{'form':form,'filetype_err':'Uploaded file should be CSV file','uploaded':False})
            else:
                if form.is_valid():
                    got_file(request.FILES['trade_file'])
                    return show_open(request,form)    
        else:
            form = upload_file_form()
        return render(request, 'order_maker/upload_order_file.html',{'form':form,'filetype_err':"",'uploaded':False})

    else:
        msg = 'Session Expired, Log in again.'
        return render(request, 'login.html',{'filetype_err':msg})

def show_open(request,form):
    return render(request, 'order_maker/upload_order_file.html',{'form':form,'filetype_err':"",'uploaded':True})

def generate(request):
    x = request.session.get('username')
    y = request.session.get('password')
    if x or y:
        sell_list = Order_position_open.objects.all().order_by('symbol','expiry_date','opt_type', 'trade_name', '-trade_price')#.filter(buy_or_sell='SELL')
        return render(request, 'order_maker/generate.html',{'sells':sell_list})
    else:
        msg = 'Session Expired, Log in again.'
        return render(request, 'login.html',{'filetype_err':msg})

def closed(request):
    x = request.session.get('username')
    y = request.session.get('password')
    if x or y:
        SYMBOL = request.POST.get('Symbol')
        Trade_Date = request.POST.get('Trade_Date')
        Expiry_Date = request.POST.get('Expiry_Date')
        temp_list = Order_position_close.objects.filter().order_by('symbol','expiry_date','trade_date','trade_time')#.filter(buy_or_sell='SELL')
        sell_list = []
            
        if not SYMBOL and not Trade_Date and not Expiry_Date:
            sell_list = Order_position_close.objects.all().order_by('-trade_date')#.filter(buy_or_sell='SELL')

        if Expiry_Date and not Trade_Date:
            temp_list = Order_position_close.objects.filter(expiry_date=Expiry_Date).order_by('symbol','expiry_date','trade_date','trade_time')
            if SYMBOL:
                for i in temp_list:
                    if SYMBOL in str(i.trade_name):
                        sell_list.append(i)
            else:
                sell_list = temp_list

        if Trade_Date and not Expiry_Date:
            temp_list = Order_position_close.objects.filter(trade_date=Trade_Date).order_by('symbol','expiry_date','trade_date','trade_time')
            if SYMBOL:
                for i in temp_list:
                    if SYMBOL in str(i.trade_name):
                        sell_list.append(i)
            else:
                sell_list = temp_list

        if SYMBOL and not Expiry_Date and not Trade_Date:
            for i in temp_list:
                if SYMBOL in str(i.trade_name):
                    sell_list.append(i)
        

        if Trade_Date and Expiry_Date:
            temp_list = Order_position_close.objects.filter(expiry_date=Expiry_Date, trade_date=Trade_Date).order_by('symbol','expiry_date','trade_date','trade_time')
            if SYMBOL:
                for i in temp_list:
                    if SYMBOL in str(i.trade_name):
                        sell_list.append(i)
            else:
                sell_list = temp_list

        if(len(sell_list) > 2000):
            sell_list = sell_list[0:2000]
        
            sell_list = sell_list[0:2000]
            
        return render(request, 'closed/generate.html',{'sells':sell_list})
    else:
        msg = 'Session Expired, Log in again.'
        return render(request, 'login.html',{'filetype_err':msg})

@csrf_exempt
def record(request):
    if request.method == 'POST':
        data = simplejson.loads(request.body)
        for ids in data:
            ids_int = int(ids);
            sell = Order_position_open.objects.get(id=ids_int)
            sell.covering_rate = float(data[ids])
            sell.save()
        return HttpResponse('<h3 style="color:Blue">covering rates stored</h3>')

class MyClass:
    trade_price = 0.0
    qty = 0
    trade_time = ""
    option_type = ""
    strike_price = 0
    expiry_date = ""

    def __init__(self,p,q,t,o,s,e):
        self.trade_price = p
        self.qty = q
        self.trade_time = t
        self.option_type = o
        self.strike_price = s
        self.expiry_date = e

def pnl(request):
    x = request.session.get('username')
    y = request.session.get('password')
    if x or y:
        SYMBOL = request.POST.get('Symbol')
        t_name = request.POST.get('trade_name')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        sell_list = []
        result = []

        if from_date or to_date:
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
            while(from_date <= to_date):
                temp_list = Order_position_close.objects.filter(trade_date=from_date).order_by('symbol','expiry_date','trade_time')
                if t_name:
                    temp_list = Order_position_close.objects.filter(trade_date=from_date, trade_name=t_name).order_by('symbol','expiry_date','trade_time')

                if not SYMBOL:
                    sell_list.extend(temp_list)
                    from_date = from_date + datetime.timedelta(days = 1)
                else:
                    temp_symbol = []
                    for i in temp_list:
                        if SYMBOL in str(i.trade_name):
                            temp_symbol.append(i)

                    sell_list.extend(temp_symbol)
                    from_date = from_date + datetime.timedelta(days = 1)

            sell = defaultdict(lambda:[])
            buy = defaultdict(lambda:[])
            # pnl_cum =  defaultdict(lambda:defaultdict)

            for i in sell_list:
                if i.buy_or_sell == "SELL":
                    pnl_amount = i.trade_price * i.trade_qty
                    result.append({'Symbol': i.symbol, 'Trade': i.trade_name,'option_type':i.opt_type,'qty':i.trade_qty,'trade_time':i.trade_time,'stk_price':i.strike_price,'expiry_date':i.expiry_date,'buy_price':0,'sell_price':i.trade_price,'trade_date':i.trade_date,'pnl_amt':pnl_amount})
                    
                    # sell[i.trade_name].append(sell_obj)

                if i.buy_or_sell == "BUY":
                    pnl_amount = -i.trade_price * i.trade_qty
                    result.append({'Symbol': i.symbol, 'Trade': i.trade_name,'option_type':i.opt_type,'qty':i.trade_qty,'trade_time':i.trade_time,'stk_price':i.strike_price,'expiry_date':i.expiry_date,'buy_price':i.trade_price,'sell_price':0,'trade_date':i.trade_date,'pnl_amt':pnl_amount})
                    
                    # if len(sell[i.trade_name]) > 0:
                    #     obj = sell[i.trade_name][0]
                    #     pnl_amount = float(obj.trade_price)- float(i.trade_price)
                    #     pnl_amount *= float(i.trade_qty)
                    #     result.append({'Symbol': i.symbol, 'Trade': i.trade_name,'option_type':i.opt_type,'qty':i.trade_qty,'trade_time':obj.trade_time,'stk_price':i.strike_price,'expiry_date':i.expiry_date,'buy_price':i.trade_price,'sell_price':obj.trade_price,'trade_date':obj.trade_date,'pnl_amt':pnl_amount})
                    #     del sell[i.trade_name][0]
                    # else:
                    #   buy_obj = MyClass(i.trade_price, i.trade_qty, i.trade_time, i.opt_type, i.strike_price, i.expiry_date,i.trade_date)
                    #   buy[i.trade_name].append(buy_obj) 

            # for key in buy:
            #   if len(sell[key]) > 0:
            #       obj = sell[key][0]
            #       pnl_amount = float(obj.trade_price)- float(buy[key][0].trade_price)
            #       pnl_amount *= float(buy[key][0].qty)
            #       a = re.search('[0-9]',key)
            #       sym = key[0:a.start()]
            #       result.append({'Symbol':sym, 'Trade': key,'option_type':key[-2:],'qty':buy[key][0].qty,'trade_time':buy[key][0].trade_time,'stk_price':buy[key][0].strike_price,'expiry_date':buy[key][0].expiry_date,'buy_price':buy[key][0].trade_price,'sell_price':obj.trade_price,'trade_date':'','pnl_amt':pnl_amount})
            #       del sell[key][0]
            #       del buy[key][0]

        return render(request, 'pnl/generate.html', {'sells':result})
    else:
        msg = 'Session Expired, Log in again.'
        return render(request, 'login.html',{'filetype_err':msg})


