#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 19:13:03 2021

@author: rohitsinha
"""

import urllib.request, urllib.error, urllib.parse
import requests

import requests
import datetime
import json
import pandas as pd

import subprocess
import beepy

from datetime import datetime as dt
import os
import time




COVAXIN="COVAXIN"
COVISHIELD="COVISHIELD"





# leave blank if you want all pincodes in the district
preferred_pincodes=[]

#example - preferred_pincodes=[827013,827006]



# add user here 
#params 0 - Vaccine type -> "*" for any vaccine, "COVAXIN"
#Params 1 - age limit   18 or 45
#params 3 - distric ID - If you do not know the districtID please see in text attached
rohit=["*",18,"242",preferred_pincodes]

# examples 
# sample_user= [COVAXIN,18,341]
# rohit= [COVISHIELD,45,242]



# register user here , comma separated
reg = [rohit]












base = datetime.datetime.today()
date_list = [base]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]
ca="curl -X GET \"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}\" "
ca+="--header \"sec-ch-ua: \\\" Not A;Brand\\\";v=\\\"99\\\", \\\"Chromium\\\";v=\\\"90\\\", \\\"Google Chrome\\\";v=\\\"90\\\"\" "
ca+="--header \"sec-ch-ua-mobile: ?0\" "
ca+="--header \"Upgrade-Insecure-Requests: 1\" "
ca+="--header \"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36\" "
ca+="--header \"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\" "
ca+="--header \"Sec-Fetch-Site: none\" "
ca+="--header \"Sec-Fetch-Mode: navigate\" "
ca+="--header \"dnt: 1\""


def getSlots(vaccine,age,DIST_ID,preferred_pincodes):
    reply=[]
    stra=""

    curl=ca.format(DIST_ID, date_str[0])
    stream = os.popen(curl)
    
    output = stream.read()
    if(len(output)<=0):
        print("failed to connect to cowin server. Please check internet!")
        return reply
    f = json.loads(output)
    centers=f["centers"]
    #time.sleep(5)
    for c in centers:
        sessions = c["sessions"]
        for session in sessions:
            if session["min_age_limit"] == age and  session["available_capacity"]>0 :
                if(vaccine!="*" and session["vaccine"].upper()!=vaccine):
                    stra=stra+session["vaccine"]+"vaccine did not match  \n" 
                    continue
                if(len(preferred_pincodes)>0 and c["pincode"] not in preferred_pincodes):
                    continue
                a="date="+session["date"]
                a=a+" \n location: "+c["name"]
                a=a+" \n"+ c["block_name"]
                a=a+" \n Available Capacity: "+ str(session["available_capacity"])
                a=a+" \n Vaccine: "+ session["vaccine"]
                a=a+" \n age limit:"+str(session["min_age_limit"])
                a=a+" \n pincode: "+str(c["pincode"])
                a=a+" \n from: "+c["from"]
                a=a+" \n to: "+c["to"]
                a=a+" \n address: "+c["address"]
                a=a+" \n slots: "+str(session["slots"])
                print(a)
                reply.append(a)
    return reply
            




while(1):
    print("@@@@@@@ Retrying to get slots")
    try:
        
        for i in reg:
            reply=getSlots("*",i[1],i[2],i[3])
            if (len(reply)>0):
                now = dt.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                print("At least any one vaccine is available at date and time =", dt_string)
                for j in reply:
                    print ("\n<<<<< any  <<<<<<")
                    print (j)
               
        for i in reg:
            reply=getSlots(i[0],i[1],i[2],i[3])
            if (len(reply)>0):
                for j in reply:
                    print ("\n>>>>  your selected vaccine >>>>>>")
                    print (j)
                for i in range(50):
                    beepy.beep(5)
    except:
        print("some error occured while retriving info from cowin server")

    
    time.sleep(60)

    
    

