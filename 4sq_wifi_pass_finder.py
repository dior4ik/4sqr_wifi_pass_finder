#! /usr/bin/python
# -*- coding: utf-8 -*-

import json
import httplib

nbr_req_agree = "n"
req_counter = 1

C_ID = str(raw_input("Enter CLIENT ID of your 4sq app: "))
C_SCRT = str(raw_input("Enter CLENT SECRET of your 4sq app: "))

yx1 = raw_input("Enter lower left coordinate pair from Google Maps in format 'latitude,longitude': ").split(",")
yx2 = raw_input("Enter upper right coordinate pair from Google Maps in format 'latitude,longitude': ").split(",")

print
print "\033[33mATTENTION!!! Next parameter 'step' must be chosen based on the fact that you can do only 500 requests per hour." \
      " If you choose too small 'step', you will be blocked by API server for 1 hour.\033[0m"
print
raw_input("\033[32mPlease, press Enter to continue\033[0m")
print


while nbr_req_agree != "Y":
    nbr_req = 1
    y1 = float(yx1[0])
    y2 = float(yx2[0])

    print
    raw_step = raw_input("Enter step for increasing lower left coordinates to upper right coordinates (I recommend to start from 1000 meters): ")
    print
    step = float(raw_step) / 100000

    while y1 < y2:
        x1 = float(yx1[1])
        x2 = float(yx2[1])
        while x1 < x2:
            nbr_req += 1
            x1 = x1 + step
        else:
            x1 = x2
            nbr_req += 1
        y1 = y1 + step
    else:
        y1 = y2
        x1 = float(yx1[1])
        x2 = float(yx2[1])
        while x1 < x2:
            nbr_req += 1
            x1 = x1 + step
        else:
            x1 = x2

    print
    print "Number of requests with step " + str(raw_step) + " meters: " + str(nbr_req)
    print

    nbr_req_agree = raw_input("\033[33mATTENTION!!! Enter 'Y' if you want to continue or 'n' if you want to set another step value: \033[0m")

else:
    y1 = float(yx1[0])
    x1 = float(yx1[1])
    y2 = float(yx2[0])
    x2 = float(yx2[1])

    print
    print "\033[1;31mLower left coordinate pair from Google Maps is: " + str(y1) + ", " + str(x1)
    print "\033[1;31mUpper right coordinate pair from Google Maps is: " + str(y2) + ", " + str(x2)
    print "\033[1;31mStep is: " + str(raw_step) + " meters\033[0m"
    print

    out_file = raw_input("Enter name for output file: ")
    out_file = open(out_file, "a+")

    print
    raw_input("\033[32mPlease, press Enter to start searching\033[0m")
    print

def data_request():
    connection = httplib.HTTPSConnection('api.foursquare.com')
    connection.request("GET", "/v2/tips/search?v=20150430&ll=" + str(y1) + "%2C" + str(x1) + "&limit=500&query=wifi&client_id=" + C_ID + "&client_secret=" + C_SCRT)
    response = connection.getresponse()
    print "Search nearby venues status: request " + str(req_counter) + " " + str(response.status) + " " + str(response.reason)
    data = response.read()
    connection.close()
    resp = json.loads(data)
    return resp

def response_parser(x):
    for i in x['response']['tips']:
        results = i['venue']['id'] + ',' + i['venue']['name'] + ',' + str(i['venue']['location']['lat']) + ',' + str(i['venue']['location']['lng']) + ',' + i['id'] + ',' + i['text'] + "\n"
        out_file.write(results.encode('utf-8'))


y1 = float(yx1[0])
y2 = float(yx2[0])

while y1 < y2:
    x1 = float(yx1[1])
    x2 = float(yx2[1])
    while x1 < x2:
        response_parser(data_request())
        x1 += step
        req_counter += 1
    else:
        x1 = x2
        response_parser(data_request())
        req_counter += 1
    y1 += step
else:
    y1 = y2
    x1 = float(yx1[1])
    x2 = float(yx2[1])
    while x1 < x2:
        response_parser(data_request())
        x1 += step
        req_counter += 1
    else:
        x1 = x2
        response_parser(data_request())

print "\033[1;31mCongrats!!! Your search is completed\033[0m"