#---------------------------------------------------------------------#
# File: /home/will22/OneDrive/PiSpace/ByProject/GDomains_DDNS/ddns_update.py
# Project: /home/will22/OneDrive/PiSpace/ByProject/GDomains_DDNS
# Created Date: Sunday, May 8th 2022, 4:18:14 pm
# Description: Python script to update the Google Domains DNS Service
# Author: Will Hall
# Copyright (c) 2022 Lime Parallelogram
# -----
# Last Modified: Sun May 08 2022
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2022-05-08	WH	Added graceful shutdown service
# 2022-05-08	WH	Added configurable timeout (in mins)
# 2022-05-08	WH	Added error code information
# 2022-05-08	WH	Created API call system
#---------------------------------------------------------------------#
# Imports modules
import requests
import time
import signal
from datetime import datetime
import os

# Get environmental variables from docker
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
HOSTNAME = os.environ["HOSTNAME"]
TIMEOUT = os.environ["TIMEOUT"]

# Custom error - raised when the user fails to set environmental variables
class ENVError(Exception):
    def __init__(self):
        super().__init__("ERROR: There was a problem with the provided Environmental Variables")

# Allow graceful shutdown with docker stop
def handle_sigterm(*args):
    raise KeyboardInterrupt()

signal.signal(signal.SIGTERM, handle_sigterm)

# Set headers to include user agent
HEADERS= {
    "user-agent": "limeparallelogram-ddnsupdate pythonrequests"
}

# ----------------- #
# Get current IP from ipify.org and submit API call to google domains
def updateIP():
    myIP = requests.request("GET", "https://api.ipify.org").text
    URL = f"https://{USERNAME}:{PASSWORD}@domains.google.com/nic/update?hostname={HOSTNAME}&myip={myIP}"
    response = requests.request("POST", URL, headers=HEADERS)
    return response

# ----------------- #
# Check error code against documented error codes (source: https://support.google.com/domains/answer/6147083?hl=en-GB#zippy=%2Cuse-the-api-to-update-your-dynamic-dns-record)
def checkErrorStatCode(statcode):
    match statcode:
        case "badauth":
            printTS("The username/password combination isn't valid for the specified host.")
        case "notfqdn":
            printTS("The supplied hostname isn't a valid fully-qualified domain name.")
        case "abuse":
            printTS("Dynamic DNS access for the hostname has been blocked due to failure to interpret previous responses correctly.")
        case "nohost":
            printTS("The hostname doesn't exist, or doesn't have Dynamic DNS enabled.")
        case "911":
            printTS("An error has ocurred with the Google Domains Service. Try again in 5 mins")
        case "conflict":
            printTS("A custom A or AAAA resource record conflicts with the update. Delete the indicated resource record within the DNS settings page and try the update again.")
        case _:
            printTS("Status: "+statcode+" was returned. Exiting.")

# ----------------- #
# Print to output logs including a timestamp           
def printTS(string):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S | ')+string)

# ========================================= #
# Check credentials on first run
if "UNSET" in HOSTNAME+PASSWORD+USERNAME:
    printTS("One or more environmental values have not been configured. Set environmental variables HOSTNAME, PASSWORD and USERNAME to the appropriate values before proceding.")
    raise ENVError

# Convert timeout (mins) to seconds and catch errors
try:
    SECOND_TIMEOUT = int(TIMEOUT)*60
except ValueError:
    printTS("The provided timout value is invalid")
    raise ENVError

response = updateIP().text # Make first request
statcode = response.split(" ")[0] # Split response into status code and payload
printTS("Initial response: " + statcode)

# ========================================= #
# If status code is acceptable, begin the update service
if statcode == "nochg" or statcode == "good":
    printTS("Initial API Request valid. DDNS Service starting")
    running = True

    while running:
        try:
            response = updateIP() # Run update service
            if "good" in response.text: # Log when the IP is updated
                print("IP Updated. Response was: " + response.text)

            time.sleep(SECOND_TIMEOUT)

        except KeyboardInterrupt: # Cleanly shut down system when docker is stopped
            printTS("Stopping DDNS Update Service")
            running = False
else:
    checkErrorStatCode(statcode) # Check the stat code that was generated against list of known errors