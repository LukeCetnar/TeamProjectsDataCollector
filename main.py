#!/usr/bin/env python3
'''
    File name: Main.py
    Author: Luke Cetnar
    Date created: 2/12/2020
    Date last modified: TBD
    Python Version: 3.8+
'''


from datetime import datetime
import time
import csv
import requests
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import os
import glob
import time
 
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')
#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
#https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/ Library for GPIO
#https://pi4j.com/1.2/pins/model-3b-plus-rev1.html pinout 


# RPI HEADER PINS

#3.3V   01##02  5V
#SDA    03##04  5V
#SCL    05##06  GND
#       07##08
#GND    09##10
#HEATER 11##12  LIGHTS
#PUMP   13##14  
#SOLE   15##16
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
    

GAIN = 1
#pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
voltages = {
    1: 4.096,
    2: 6.144,
    3: 6.144,
    4: 1.024,
    8: 0.512,
    16: 0.256
}



# defining the api-endpoint  
API_ENDPOINT = "http://pastebin.com/api/api_post.php"
  
# your API key here 
API_KEY = "XXXXXXXXXXXXXXXXX"
  

#INPUT_PINS = []
OUTPUT_PINS = [11,12,13,15]
#11 - relay block1 heater
#12- relay block2 lighting
#13 relay block3 pump
#15 - relay block4  pump directional solenoid 1/0 

   

current_millis = lambda: int(round(time.time() * 1000))

#in millis 
POLL_INTERVAL = 3000

def initPins():
    GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(INTPUT_PINS, GPIO.IN)
    GPIO.setup(OUTPUT_PINS, GPIO.OUT)
    GPIO.output(OUTPUT_PINS,GPIO.HIGH)
    
    

   
    
    
    

def getDateTime():
    # Done
    # completed will get currrent date time and output to correct format
    now = datetime.now()
    dt_string = now.strftime("%Y%d%m%H%M%S")
    return dt_string

def getStatus():
    status  = 0X00
    status |= 1 if GPIO.input(11) == GPIO.HIGH else 0# heater
    status |= 2 if GPIO.input(12) == GPIO.HIGH else 0# lights
    status |= 4 if GPIO.input(13) == GPIO.HIGH else 0# pump
    status |= 8 if GPIO.input(15) == GPIO.HIGH else 0# solenoid
    return status     
    
    
def setStatus(status):
    GPIO.output(11,GPIO.HIGH) if status & 0x01 else GPIO.output(11,GPIO.LOW)
    GPIO.output(12,GPIO.HIGH) if status & 0x02 else GPIO.output(12,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH) if status & 0x04 else GPIO.output(13,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH) if status & 0x08 else GPIO.output(15,GPIO.LOW)
    
def setTemp(temp):
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    pass
    
def getTemp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
    if equals_pos != -1:
       temp_string = lines[1][equals_pos+2:]
       temp_c = float(temp_string) / 1000.0
    return temp_c

def I2CRead():
    adc = Adafruit_ADS1x15.ADS1115()
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN)
    #print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    values[0] = values[0]*(14/32767)
    values[2] = values[2]/32767
    return [values[0],values[2]]



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
    #get inital time
    start = current_millis()
    millis = start
    ph = 0
    wlevel =0
    date = getDateTime()
    status = 0x00
    while(1):
        #data willl be collected every few seconds i suppose
        #REDO half of them need to be placed into a serial read functions sontosnds;njkn
        if(current_millis() > (POLL_INTERVAL + millis)):
            [ph,wlevel] = I2CRead()
            #temp = getTemp()
            date = getDateTime()
            status = getStatus()
            #postData(date,ph,temp,status,wLevel,0)#implment later
            millis = current_millis()
            status = input('enter status')
            time.sleep(0.01)
        else:
            print('ph: ',ph)
            print('wlevel: ', wlevel)
            print('status: ', hex(status))
            print('date',date , '\n')
     
            
    GPIO.cleanup(OUTPUT_PINS)
   
main()
