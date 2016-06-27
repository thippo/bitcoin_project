#!/usr/bin/python
# -*- coding: utf-8 -*-

import http.client
import urllib
import json
import hashlib
import time

def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    data = sign+'secret_key='+secretKey
    return  hashlib.md5(data.encode("utf8")).hexdigest().upper()

def httpGet(url,resource,params=''):
    conn = http.client.HTTPSConnection(url, timeout=10)
    conn.request("GET",resource + '?' + params)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    return json.loads(data)

def httpPost(url,resource,params):
    headers = {
        "Content-type" : "application/x-www-form-urlencoded",
    }
    conn = http.client.HTTPSConnection(url, timeout=10)
    temp_params = urllib.parse.urlencode(params)
    conn.request("POST", resource, temp_params, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    params.clear()
    conn.close()
    return json.loads(data)

class OKCoin():

    def __init__(self,url,apikey,secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey

    #获取OKCOIN现货行情信息
    def ticker(self, symbol='btc_cny'):
        RESOURCE = "/api/v1/ticker.do"
        params = ''
        params = 'symbol='+symbol
        return httpGet(self.__url,RESOURCE,params)

    #获取OKCOIN现货市场深度信息
    def depth(self, symbol='btc_cny', size=3, merge=1):
        RESOURCE = "/api/v1/depth.do"
        params = 'symbol='+symbol+'&size='+str(size)+'&merge='+str(merge)
        return httpGet(self.__url,RESOURCE,params)

    #获取OKCoin最近600交易信息
    def trades(self, symbol='btc_cny', since=''):
        RESOURCE = "/api/v1/trades.do"
        params = 'symbol='+symbol+'&since='+str(since)
        return httpGet(self.__url,RESOURCE,params)

    #获取比特币或莱特币的K线数据
    def kline(self, symbol='btc_cny', type='1min', size=3, since=''):
        RESOURCE = "/api/v1/kline.do"
        params = 'symbol='+symbol+'&type='+type+'&size='+str(size)+'&since='+str(since)
        return httpGet(self.__url,RESOURCE,params)

    #获取用户现货账户信息
    def userinfo(self):
        RESOURCE = "/api/v1/userinfo.do"
        params ={}
        params['api_key'] = self.__apikey
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,RESOURCE,params)

    #下单交易
    def trade(self, price, amount, type='buy', symbol='btc_cny'):
        RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key':self.__apikey,
            'symbol':symbol,
            'type':type,
            'price':str(price),
            'amount':str(amount)
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,RESOURCE,params)

    #获取OKCoin历史交易信息(非个人)
    def trade_history(self, symbol='btc_cny', since=''):
        RESOURCE = "/api/v1/trade_history.do"
        params = {
            'api_key':self.__apikey,
            'symbol':symbol,
            'since':str(since)
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,RESOURCE,params)

    #批量下单
    def batch_trade(self, type, orders_data, symbol='btc_cny'):
        RESOURCE = "/api/v1/batch_trade.do"
        params = {
            'api_key':self.__apikey,
            'symbol':symbol,
            'type':type,
            'orders_data':orders_data
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,RESOURCE,params)

    #撤销订单
    def cancel_order(self, orderId, symbol='btc_cny'):
        RESOURCE = "/api/v1/cancel_order.do"
        params = {
             'api_key':self.__apikey,
             'symbol':symbol,
             'order_id':orderId
        }
        params['sign'] = buildMySign(params,self.__secretkey)
        return httpPost(self.__url,RESOURCE,params)

    #获取用户的订单信息
    def order_info(self, orderId=-1, symbol='btc_cny'):
         RESOURCE = "/api/v1/order_info.do"
         params = {
             'api_key':self.__apikey,
             'symbol':symbol,
             'order_id':orderId
         }
         params['sign'] = buildMySign(params,self.__secretkey)
         return httpPost(self.__url,RESOURCE,params)

    #批量获取用户订单
    def orders_info(self, orderId, type=0, symbol='btc_cny'):
         RESOURCE = "/api/v1/orders_info.do"
         params = {
             'api_key':self.__apikey,
             'symbol':symbol,
             'order_id':orderId,
             'type':tradeType
         }
         params['sign'] = buildMySign(params,self.__secretkey)
         return httpPost(self.__url,RESOURCE,params)

    #获取历史订单信息，只返回最近七天的信息
    def order_history(self, currentPage=1, pageLength=20, status=0, symbol='btc_cny'):
           RESOURCE = "/api/v1/order_history.do"
           params = {
              'api_key':self.__apikey,
              'symbol':symbol,
              'status':status,
              'current_page':currentPage,
              'page_length':pageLength
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #提币BTC/LTC
    def withdraw(self, withdraw_address, withdraw_amount, chargefee, trade_pwd, symbol='btc_cny'):
           RESOURCE = "/api/v1/withdraw.do"
           params = {
              'api_key':self.__apikey,
              'withdraw_address':withdraw_address,
              'withdraw_amount':withdraw_amount,
              'chargefee':chargefee,
              'trade_pwd':trade_pwd,
              'symbol':symbol
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #取消提币BTC/LTC
    def cancel_withdraw(self, withdraw_id, symbol='btc_cny'):
           RESOURCE = "/api/v1/cancel_withdraw.do"
           params = {
              'api_key':self.__apikey,
              'withdraw_id':withdraw_id,
              'symbol':symbol
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #查询提币BTC/LTC信息
    def withdraw_info(self, withdraw_id, symbol='btc_cny'):
           RESOURCE = "/api/v1/withdraw_info.do"
           params = {
              'api_key':self.__apikey,
              'withdraw_id':withdraw_id,
              'symbol':symbol
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #查询提币手续费
    def order_fee(self, order_id, symbol='btc_cny'):
           RESOURCE = "/api/v1/order_fee.do"
           params = {
              'api_key':self.__apikey,
              'order_id':order_id,
              'symbol':symbol
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #获取放款深度前10
    def lend_depth(self, symbol='btc_cny'):
           RESOURCE = "/api/v1/lend_depth.do"
           params = {
              'api_key':self.__apikey,
              'symbol':symbol
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #查询用户借款信息
    def borrows_info(self, symbol='btc_cny'):
           RESOURCE = "/api/v1/borrows_info.do"
           params = {
              'api_key':self.__apikey,
              'symbol':symbol
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #申请借款
    def borrow_money(self, amount, days, rate, symbol='btc_cny'):
           RESOURCE = "/api/v1/borrow_money.do"
           params = {
              'api_key':self.__apikey,
              'symbol':symbol,
              'amount':amount,
              'rate':rate,
              'days':days
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #取消借款申请
    def cancel_borrow(self, borrow_id, symbol='btc_cny'):
           RESOURCE = "/api/v1/cancel_borrow.do"
           params = {
              'api_key':self.__apikey,
              'symbol':symbol,
              'borrow_id':borrow_id
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #获取借款订单记录
    def borrow_order_info(self, borrow_id):
           RESOURCE = "/api/v1/borrow_order_info.do"
           params = {
              'api_key':self.__apikey,
              'borrow_id':borrow_id
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #用户还全款
    def repayment(self, borrow_id):
           RESOURCE = "/api/v1/repayment.do"
           params = {
              'api_key':self.__apikey,
              'borrow_id':borrow_id
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #未还款列表
    def unrepayments_info(self, currentPage=1, pageLength=20, symbol='btc_cny'):
           RESOURCE = "/api/v1/unrepayments_info.do"
           params = {
              'api_key':self.__apikey,
              'symbol':symbol,
              'current_page':currentPage,
              'page_length':pageLength
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)

    #获取用户提现/充值记录
    def account_records(self, currentPage=1, pageLength=20, type=0, symbol='btc_cny'):
           RESOURCE = "/api/v1/account_records.do"
           params = {
              'api_key':self.__apikey,
              'symbol':symbol,
              'type':type,
              'current_page':currentPage,
              'page_length':pageLength
           }
           params['sign'] = buildMySign(params,self.__secretkey)
           return httpPost(self.__url,RESOURCE,params)