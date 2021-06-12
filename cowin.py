from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from random import random
from io import BytesIO
from playsound import playsound
from datetime import date
import requests, json, pycurl, hashlib, time, cgi, threading

##########################################################
# CONFIG
##########################################################
districtID = "571"
today = date.today().strftime("%d/%m/%Y") # Ex: 12/06/2021
vaccine = "COVAXIN" # OR "COVISHIELD". Leave it empty if you have no preference
dose = "2" # Must be either 1 or 2
min_age_limit = 18 # Should be 18 or 45
##########################################################

otp = ""

class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_POST(self):
        self._set_headers()
        json = parse_qs(self.path[2:])
        global otp
        otp = json['otp'][0]
        print(otp)
    def start():
        print("Hello")

def run(server_class=HTTPServer, handler_class=GP, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    t = threading.Thread(target=httpd.serve_forever)
    t.daemon = True
    t.start()

def postURL(url, payload, headers):
     return requests.post(url, data=payload, headers=headers)

def getURL(url, payload, headers):
     return requests.get(url, data=payload, headers=headers)

def checkVaccineSlot(centers):
    success = False
    for center in centers['centers']:
        for session in center['sessions'] :
            if session['min_age_limit'] == min_age_limit and session['available_capacity_dose' + dose] > 0 :
                output = {}
                output['name'] = str(center['name'])
                output['date'] = str(session['date'])
                output['available_capacity'] = int(session['available_capacity'])
                output['available_capacity_dose1'] = int(session['available_capacity_dose1'])
                output['available_capacity_dose2'] = int(session['available_capacity_dose2'])
                output['min_age_limit'] = int(session['min_age_limit'])
                output['vaccine'] = str(session['vaccine'])
                print(output)
                if output['available_capacity_dose' + dose] > 0 :
                    success = True
    if success :
        print("Vaccine Found!!")
        playsound('alarm.mp3')
    else :
        print("Vaccine Not Found")
run()

mobile = input("Enter your mobile number:")
while mobile == "":
    mobile = input("Enter your mobile number:")
while True:
    requestGenerateOTP = {}
    requestGenerateOTP['mobile'] = mobile
    requestGenerateOTP['secret'] = "U2FsdGVkX1+riZhXlQI+OaFkBTrKOygrTuso2smx7gmp1s1+TzrmCvO+pDfigaSqxD8+xILS7axSGBJWIbC1Nw=="
    requestGenerateOTP = json.dumps(requestGenerateOTP, indent = 4)

    header = {}
    header['Content-Type'] = "application/json"
    header['Accept-Language'] = "en-US"
    header['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    header['sec-ch-ua'] = "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\""

    responseGenerateOTP = postURL("https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP", requestGenerateOTP, header)
    if responseGenerateOTP.status_code != 200:
        continue
    responseGenerateOTPJson = json.loads(responseGenerateOTP.content)
    txnId = responseGenerateOTPJson["txnId"]

    # Un-Comment the next few lines if you wish to enter the OTP manually
    # otp = input("Enter OTP:")
    # while otp == "":
    #     otp = input("Enter OTP:")

    # Comment the next few lines if you wish to enter the OTP manually
    print ("Waiting for OTP")
    while otp == "":
        time.sleep(1)
    print("Got OTP:" + otp)

    otphash = hashlib.sha256(str(otp).encode()).hexdigest()

    validateRequest={}
    validateRequest['otp']=otphash
    validateRequest['txnId']=txnId
    validateRequest = json.dumps(validateRequest, indent = 4)

    responseValidateRequest = postURL("https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp", validateRequest, header)
    if responseValidateRequest.status_code != 200:
        continue
    responseValidateRequest = json.loads(responseValidateRequest.content)

    header["Authorization"] = "Bearer " + responseValidateRequest["token"]
    otp = ""
    login = True
    while login:
        response = getURL('https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=' + districtID + '&date=' + today + '&vaccine=' + vaccine, "", header)
        if response.status_code == 200 :
            checkVaccineSlot(json.loads(response.content))
            time.sleep(20)
        else :
            login = False
    print("Got Logged out! Trying to login again.")