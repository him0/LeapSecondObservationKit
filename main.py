#!/usr/bin/env python
# -*- coding: utf-8 -*-

#2015年7月1日の「うるう秒」観察ツール
#2015年7月1日“8時59分60秒”挿入

import ntplib
import time
import threading
import queue

que = queue.Queue()
#thread数を増やせば誤差は減る
num_of_thread = 1200
leap_unix_time = 1435708800

def get_time(c, i):
    time.sleep(i)
    
    while True:
        response = c.request("ntp.nict.jp")
        
        unix_time = response.orig_time
        unix_time = float(unix_time)
        unix_time = int(unix_time)
        
        leap = response.leap
        
        if (leap_unix_time - 10) <= unix_time and unix_time < leap_unix_time:
            print("\033[33m" + str(leap) + " : " + str(unix_time) + "\033[0m")
        elif unix_time == leap_unix_time:
            print("\033[31m" + str(leap) + " : " + str(unix_time) + "\033[0m")
        else:
            print(str(leap) + " : " + str(unix_time))
        
        time.sleep(num_of_thread)

def make_threads(c):
    connect = c
    
    for i in range(0, num_of_thread):
        thread = threading.Thread(target=get_time, args=(connect, i))
        que.put(thread)

def excute():
    while not que.empty():
        thread = que.get()
        thread.start()

if __name__=="__main__":
    connect = ntplib.NTPClient()
    make_threads(connect)
    excute()
    
    
    
    
