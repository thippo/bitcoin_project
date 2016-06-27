#!/usr/bin/python
# -*- coding: utf-8 -*-

import brain
import time
#import threading

while True:
    today = brain.update_days_mean()
    while True:
        if today != brain.API_get.kline(type='1day', since='', size=3)[::-1][0][0]:
            print('next day')
            break
        print(brain.timestamp_to_time(today/1000))
        if brain.smart_buy():
            while brain.API_get.kline(type='1day', since='', size=3)[::-1][0][0] == today:
                print('         sleep 900s...')
                time.sleep(900)
            break
        print('         sleep 120s...')
        time.sleep(120)

