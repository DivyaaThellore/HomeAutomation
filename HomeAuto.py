#!/usr/bin/env python3
#############################################################################
# Filename    : DHT11.py
# Description :	read the temperature and humidity data of DHT11
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
import time
import requests
import math
import random

ledPin = 18    # RPI Board pin11
DHTPin = 11     #define the pin of DHT11

TOKEN = "A1E-Zu5858mz1VC3y8h8aU26WM7A0zWhnN"  # Put your TOKEN here
DEVICE_LABEL = "homeautomation"  # Put your device label here 
VARIABLE_LABEL_1 = "temperature"  # Put your first variable label here
VARIABLE_LABEL_2 = "humidity"  # Put your second variable label here
VARIABLE_LABEL_3 = "position"  # Put your second variable label here


DEVICE = "homeautomation" # Assign the device label to obtain the variable
MINTEMP = "mintemperature" # Assign the variable label to obtain the variable value
MAXTEMP = "maxtemperature" # Assign the variable label to obtain the variable value
MINHUMIDITY = "minhumidity" # Assign the variable label to obtain the variable value
MAXHUMIDITY = "maxhumidity" # Assign the variable label to obtain the variable value

DELAY = 1  # Delay in seconds

def build_payload(variable_1, variable_2, variable_3, value_1, value_2):
    # Creates two random values for sending data
    #value_1 = random.randint(-10, 50)
    #value_2 = random.randint(0, 85)

    # Creates a random gps coordinates
    lat = random.randrange(34, 36, 1) + \
        random.randrange(1, 1000, 1) / 1000.0
    lng = random.randrange(-83, -87, -1) + \
        random.randrange(1, 1000, 1) / 1000.0
    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: {"value": 1, "context": {"lat": lat, "lng": lng}}}

    return payload

def get_var(device, variable):
    try:
        url = "http://things.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}".format(device, variable)

        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        print(url)
        return req.json()['last_value']['value']
    except:
        pass


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def loop():
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    sumCnt = 0              #number of reading times 
    while(True):
        sumCnt += 1         #counting number of reading times
        chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        print ("The sumCnt is : %d, \t chk    : %d"%(sumCnt,chk))
        if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            print("DHT11,OK!")
            print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))

            payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3,dht.temperature,dht.humidity)

            print("[INFO] Attemping to send data")
            post_request(payload)
            print("[INFO] finished")

            minControlTemp = get_var(DEVICE, MINTEMP)
            print("min control temperature {0}".format(minControlTemp))
            if (minControlTemp < dht.temperature):
                print("Start AC")
                switchOn()
            else:
                print("No AC needed")
                switchOff()


        elif(chk is dht.DHTLIB_ERROR_CHECKSUM): #data check has errors
            print("DHTLIB_ERROR_CHECKSUM!!")
        elif(chk is dht.DHTLIB_ERROR_TIMEOUT):  #reading DHT times out
            print("DHTLIB_ERROR_TIMEOUT!")
        else:               #other errors
            print("Other error!")


        time.sleep(1)       

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	#GPIO.setup(18,GPIO.OUT)
	
def switchOn():
    print("LED on")
    GPIO.output(18,GPIO.HIGH)
	
def switchOff():
    print ("LED off")
    GPIO.output(18,GPIO.LOW)    



if __name__ == '__main__':
    print ('Program is starting ... ')
    setup()

    try:
        loop()
    except KeyboardInterrupt:
        
	GPIO.cleanup()
        exit()

        	


