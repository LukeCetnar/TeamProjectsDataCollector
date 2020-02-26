'''
    File name: Main.py
    Author: Luke Cetnar
    Date created: 2/12/2020
    Date last modified: TBD
    Python Version: 3.8
'''
#//TODO..

from datetime import datetime
import time
import csv
import requests
import RPi.GPIO as GPIO 
# https://pypi.org/project/smbus2/Library for I2C
# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/ Library for GPIO
#https://pi4j.com/1.2/pins/model-3b-plus-rev1.html pinout 


# RPI HEADER PINS

#3.3V   01##02  5V
#SDA    03##04  5V
#SCL    05##06  GND
#       07##08
#GND    09##10
#HEATER 11##12  LIGHTS
#PUMP   13##14  SOLENOID
#       15##16
#       17##18
#       19##20
#       21##22
#       23##24
#       25##26
#       27##28
#       29##30
#       31##32
#       33##34
#       35##36
#       37##38
#       39##40
    


# defining the api-endpoint  
API_ENDPOINT = "http://pastebin.com/api/api_post.php"
  
# your API key here 
API_KEY = "XXXXXXXXXXXXXXXXX"
  

    #INPUT_PINS = []
    OUTPUT_PINS = [11,12,13,14]
    #11 - relay block1 heater
    #12- relay block2 lighting
    #13 relay block3 pump
    #14 - relay block4  pump directional solenoid 1/0 
    

current_millis = lambda: int(round(time.time() * 1000))

#in millis 
POLL_INTERVAL = 3000

def initPins():
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(INTPUT_PINS, GPIO.IN)
    GPIO.setup(OUTPUT_PINS, GPIO.OUT)
    
    
def initIC2():
    #need library
    pass

   
    
    
    

def getDateTime():
    # Done
    # completed will get currrent date time and output to correct format
    now = datetime.now()
    dt_string = now.strftime("%Y%d%m%H%M%S")
    return dt_string

def getStatusB():
    status  = "0X00"
    status |= GPIO.input(11)# heater
    status |= GPIO.input(12)*10# lights
    status |= GPIO.input(13)*100# pump
    status |= GPIO.input(14)*1000# solenoid 
    return status     
    
def getPH():
    ph = 0
    
    return ph
    
def getTemp():
    temp = 0
    
    return temp
    
def getWLevel():
    wlevel = 0
    
    return wlevel
    
def setStatus(status):
    pass
    
def setTemp(temp):
    pass




def postData(dt_string, phVal, tempVal, statusB, wLevel,setTemp):
    # data to be sent to api 
    data = {'date_time':dt_string, 'temp' : tempVal, 'ph' : phVal, 'status' : statusB,'wlevel' : wLevel} 
    r = requests.post(url = API_ENDPOINT, data = data)

def getData():
    r = requests.get(url = URL, params = PARAMS) 
    # extracting data in json format 
    data = r.json()

def main():
    initPins()
    initIC2()
    #get inital time
    start = current_millis()
    millis = start
    while(1):
        #data willl be collected every few seconds i suppose
        #REDO half of them need to be placed into a serial read functions sontosnds;njkn
        if(current_millis() > (POLL_INTERVAL + millis)):
            temp = getTemp()
            date = getDateTime()
            ph = getPH()
            wLevel = getWLevel()
            status = getStatusB()
            postData(date,ph,temp,status,wLevel,0)
            millis = current_millis()
            
        else:
            time.sleep(0.001)
            
            
            
    GPIO.cleanup(OUTPUT_PINS)
   
main()