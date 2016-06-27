import configparser
import time
import sqlite3
from OkcoinApi import OKCoin
from utils import translate_error,timestamp_to_time,minimum_mean

cf = configparser.ConfigParser()
cf.read("bitcoin.conf")
apikey = cf.get("OKCOINAPI", "apikey")
secretkey = cf.get("OKCOINAPI", "secretkey")
okcoinRESTURL = cf.get("OKCOINAPI", "okcoinRESTURL")
pan_days = cf.getint("STRATEGY", "pan_days")
up_threshold = cf.getfloat("STRATEGY", "up_threshold")
days_mean_threshold_up = cf.getfloat("STRATEGY", "days_mean_threshold_up")
days_mean_threshold_down = cf.getfloat("STRATEGY", "days_mean_threshold_down")
print('Loading configure......Done!')

API_get = OKCoin(okcoinRESTURL,apikey,secretkey)

def get_days_cost_mean():
    conn = sqlite3.connect('bitcoin.db')
    cu = conn.cursor()
    #cu.execute("select cost from indextable where name='daysmean'")
    #days_mean = cu.fetchall()[0][0]
    cu.execute("select cost from indextable where name='costmean'")
    cost_mean = cu.fetchall()[0][0]
    conn.close()
    #print('days_mean',days_mean,'cost_mean',cost_mean)
    print('cost_mean',cost_mean)
    return cost_mean
    #return days_mean,cost_mean

cost_mean = get_days_cost_mean()

def update_days_mean(pan_days=pan_days):
    global days_mean
    data_days = API_get.kline(type='1day', since='', size=pan_days+1)[::-1]
    days_mean = minimum_mean([x[3] for x in data_days[1:]])
    conn = sqlite3.connect('bitcoin.db')
    cu = conn.cursor()
    cu.execute("update indextable set cost="+str(days_mean)+" where name='daysmean'")
    conn.commit()
    conn.close()
    print('update_days_mean......Done!','days_mean',days_mean)
    return data_days[0][0]

def update_cost_mean():
    global cost_mean
    conn = sqlite3.connect('bitcoin.db')
    cu = conn.cursor()
    cu.execute("select sum(cost),sum(amount) from ordertable")
    cu_result = cu.fetchall()[0]
    cost_mean = cu_result[0]/cu_result[1]
    cu.execute("update indextable set cost="+str(cost_mean)+" where name='costmean'")
    conn.commit()
    print('update_cost_mean......Done!')
    conn.close()

def make_decision(the_price):
    #days_mean,cost_mean = get_days_cost_mean()
    if the_price <= cost_mean:
        if 1-the_price/days_mean >= days_mean_threshold_down:
            print('   buy * 2   ',end='')
            return 2
        else:
            print('   buy * 0   ')
            return 0
    elif the_price >= cost_mean and the_price <= cost_mean*(1+up_threshold):
        if 1-the_price/days_mean >= days_mean_threshold_up: 
            print('   buy * 1'   ,end='')
            return 1
        else:
            print('   buy * 0   ')
            return 0
    else:
        print('   buy * 0   ')
        return 0

def smart_buy():
    last_price = float(API_get.ticker()['ticker']['last'])
    print('   last_price',last_price,end='')
    decision = make_decision(last_price)
    conn = sqlite3.connect('bitcoin.db')
    cu = conn.cursor()
    cu.execute("update message set price="+str(last_price)+",buy="+str(decision)+" where name='now'")
    conn.commit()
    conn.close()
    if decision:
        trade_result = API_get.trade(last_price+0.3, 0.01*decision)
        if trade_result['result']:
            order_id = trade_result['order_id']
            print('      order_id',order_id,end='')
            search_time=0
            while search_time <=9:
                time.sleep(5)
                order_info_result =  API_get.order_info(order_id)
                if order_info_result['result'] and order_info_result['orders'][0]['status']==2:
                    conn = sqlite3.connect('bitcoin.db')
                    cu = conn.cursor()
                    cu.execute("insert into ordertable values("+str(order_info_result['orders'][0]['order_id'])+", "\
					                                                              +str(order_info_result['orders'][0]['create_date'])+", "\
																				  +str(order_info_result['orders'][0]['avg_price'])+", "\
																				  +str(order_info_result['orders'][0]['deal_amount'])+", "\
																				  +str(order_info_result['orders'][0]['deal_amount']*order_info_result['orders'][0]['avg_price'])+")")
                    conn.commit()
                    conn.close()
                    print('......Finish!')
                    update_cost_mean()
                    return True
                search_time += 1
            if search_time == 10:
                API_get.cancel_order(order_id)
                print('......Canceled!')
                return False
    return False
            


