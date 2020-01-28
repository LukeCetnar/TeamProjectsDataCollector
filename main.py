from datetime import datetime
import csv

def main():
    print("something")
    toCSV(getDateTime(),25,7,23,'0x0B')

def collectPH():
    print("somthing else")

def getDateTime():
    # completed will get currrent date time and output to correct format
    now = datetime.now()
    dt_string = now.strftime("%Y%d%m%H%M%S")
    return dt_string

def toCSV(dt_string, phVal, tempVal, statusB, level):
    #this will not work in the long run dont be a dummy
    with open('output'+dt_string+'.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
    


main()