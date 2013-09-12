#!/usr/bin/python

### configuration ######################################
REST_URL="http://192.168.1.10:40405"
HOST="darkstar"
DEVICE_NAME="/home on {0}".format(HOST)
# path in the filesystem for the device 
DEVICE_ADDRESS="/home"      
# interval in minutes between each poll
DEVICE_INTERVAL=1
########################################################

import requests
import json
import sys

### create the device, and if ok, get its id in device_id
print("Creating the device...")
response = requests.post("{0}/device/".format(REST_URL), \
                         headers={'content-type':'application/x-www-form-urlencoded'},
                         data="name={0}&type=plugin&id=diskfree&host={1}&description=a_description&reference=a_reference&device_type=diskfree.disk_usage".format(DEVICE_NAME, HOST))
print("Response : [{0}] {1}".format(response.status_code, response.text))
if response.status_code != 201:
    print("Error")
    sys.exit(1)

device = json.loads(response.text)
device_id = device['id']
print("Device id is '{0}'".format(device_id))


### Just for information, list the parameters for the device_type
print("\n\nList the parameters for the device type...")
response = requests.get("{0}/device/params/diskfree.disk_usage".format(REST_URL))
print("Response : [{0}] {1}".format(response.status_code, response.text))


### And finally, configure the device parameters
print("\n\nConfigure the global parameters...")
response = requests.put("{0}/device/addglobal/{1}".format(REST_URL, device_id), \
                         headers={'content-type':'application/x-www-form-urlencoded'},
                         data="device={0}&interval={1}".format(DEVICE_ADDRESS, DEVICE_INTERVAL))
print("Response : [{0}] {1}".format(response.status_code, response.text))

