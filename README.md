# RecordedDataPusher

# Before Starting
Python version 2.7.3
## Dependencies
* trollius  
* json  
* paho-mqtt  
To install a python package via pip:  
> > > > > > > sudo pip install paho-mqtt   
> > > > > > > sudo pip install trollius   

## Description

"recorded_data_publish.py" is the main script to send recorded data from "data.csv" file. 
topic "paho/test/iotBUET/bulk_raw/" (host: "iot.eclipse.org").    
   
Running the script "final_subscriber.py" shows all the data in console.   
When you run the script "dweet_publish.py" you can see data sent here:   
http://dweet.io/follow/iotEnviroSCALE_BUET   
https://freeboard.io/board/AnH7Wi   
