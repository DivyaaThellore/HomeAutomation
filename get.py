import requests
import random
import time

TOKEN = "A1E-Zu5858mz1VC3y8h8aU26WM7A0zWhnN" # Assign your Ubidots Token
DEVICE = "homeautomation" # Assign the device label to obtain the variable
MINTEMP = "mintemperature" # Assign the variable label to obtain the variable value
MAXTEMP = "maxtemperature" # Assign the variable label to obtain the variable value
MINHUMIDITY = "minhumidity" # Assign the variable label to obtain the variable value
MAXHUMIDITY = "maxhumidity" # Assign the variable label to obtain the variable value
DELAY = 5  # Delay in seconds

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


if __name__ == "__main__":
    while True:
        print(get_var(DEVICE, MINTEMP))
        print(get_var(DEVICE, MAXTEMP))
        print(get_var(DEVICE, MINHUMIDITY))
        print(get_var(DEVICE, MAXHUMIDITY))
        time.sleep(DELAY)