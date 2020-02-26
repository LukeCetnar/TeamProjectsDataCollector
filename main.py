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
# https://pypi.org/project/smbus2/Library for I2C
# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/ Library for GPIO



# defining the api-endpoint  
API_ENDPOINT = "http://pastebin.com/api/api_post.php"
  
# your API key here 
API_KEY = "XXXXXXXXXXXXXXXXX"
  



current_millis = lambda: int(round(time.time() * 1000))

#in millis 
POLL_INTERVAL = 3000

def initPins():
    #figure what library to use maybe even do some C stuff
    pass
    
def initIC2():
    #need library
    pass
def main():
    initPins()
    initIC2()
    #get inital time
    start = current_millis()
    millis = start
    while(1):
        #data willl be collected every few seconds i suppose
        if(current_millis() > (POLL_INTERVAL + millis)):
            temp = getTemp()
            date = getDateTime()
            ph = getPH()
            wLevel = getWLevel()
            status = getStatusB()
            toCSV(date,ph,temp,status,wLevel,0)
            millis = current_millis()
            
        else:
            time.sleep(0.001)
   
    
    
    

def getPH():
    return 7
def getTemp():
    return 26
def getStatusB():
    return '0x0B'
def getWLevel():
    return 0.75
def setStatus(status):
    pass
def setTemp(temp):
    pass


def getDateTime():
    # Done
    # completed will get currrent date time and output to correct format
    now = datetime.now()
    dt_string = now.strftime("%Y%d%m%H%M%S")
    return dt_string

def postData(dt_string, phVal, tempVal, statusB, wLevel,setTemp):
    # data to be sent to api 
    data = {'date_time':dt_string, 'temp' : tempVal, 'ph' : phVal, 'status' : statusB,'wlevel' : wLevel} 
    r = requests.post(url = API_ENDPOINT, data = data)

def getData():
    r = requests.get(url = URL, params = PARAMS) 
    # extracting data in json format 
    data = r.json()




    
main()