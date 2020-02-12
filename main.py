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
#import RPi.GPIO as GPIO



current_millis = lambda: int(round(time.time() * 1000))

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
        #Dosent seem to out put to the csv file who knows  ? ? ? ?! ??
        if(current_millis() > (POLL_INTERVAL + millis)):
            temp = getTemp()
            date = getDateTime()
            ph = getPH()
            wLevel = getWLevel()
            status = getStatusB()
            toCSV(date,ph,temp,status,wLevel)
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
def setStatus():
    pass


def getDateTime():
    # completed will get currrent date time and output to correct format
    now = datetime.now()
    dt_string = now.strftime("%Y%d%m%H%M%S")
    return dt_string

def toCSV(dt_string, phVal, tempVal, statusB, wLevel):
    #setting the file to change by the day
    with open('output'+datetime.now().strftime("%Y%d")+'.csv', 'a', newline='') as csvfile:
        fieldnames = ['date_time', 'temp', 'ph', 'status','wlevel']
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
        writer.writerow({'date_time':dt_string, 'temp' : tempVal, 'ph' : phVal, 'status' : statusB,'wlevel' : wLevel})
    
        
    


main()