import paho.mqtt.client as mqttClient
import paho.mqtt.publish as pub
import json
import traceback
import csv
from datetime import datetime
import trollius
from trollius import From


HOST_ECLIPSE = "iot.eclipse.org"
HOST_IQUEUE = "iqueue.ics.uci.edu"

class Reading:
    def __init__(self, ids,	timestamp,	event,	value,	lat,alt,lon, prio_class='low',	prio_value=10	):
        self.ids = ids
        self.timestamp = timestamp
        self.event = event
        self.value = value
        self.prio_class = prio_class
        self.prio_value = prio_value
        self.lat = lat
        self.lon = lon
        self.alt = alt

def get_time_diff(ts1, ts2):
    fmt = '%Y-%m-%d %H:%M:%S'    
    tstamp1 = datetime.fromtimestamp(int(ts1)).strftime(fmt)
    tstamp2 =  datetime.fromtimestamp(int(ts2)).strftime(fmt)
    tstamp1 = datetime.strptime(tstamp1, fmt)
    tstamp2 = datetime.strptime(tstamp2, fmt)
    if tstamp1 > tstamp2:
        td = tstamp1 - tstamp2
    else:
        td = tstamp2 - tstamp1
    td_mins = int(round(td.total_seconds() / 60))
    return td.total_seconds()
    

#**** add these lines to download data directly ****#    
# import urllib
# urllib.urlretrieve ("http://www.enviroscale.co.nf/data.csv", "data.csv")


filenm = 'data.csv'
with open(filenm) as csvfile:
    reader = csv.DictReader(csvfile)
    timestamps = []
    readings = []
    for row in reader:
        reading = Reading(row['id'], row['timestamp'], row['event'], row['value'], row['lat'], row['alt'], row['lon'])
        readings.append(reading)
        ts0 = int(row['timestamp'])
        timestamps.append(ts0)  

@trollius.coroutine
def send_data_every_tdiff_seconds():
    k = 0
    num_readings = len(timestamps)
    while True:
        print('Sending data...')
        
        if k+1 == num_readings:
            k = 0
        tdiff = get_time_diff(timestamps[k], timestamps[k+1])
        r = readings[k+1]
        #timestring =  datetime.fromtimestamp(float(r.timestamp)).strftime('%Y-%m-%d %H:%M:%S.%f')
        timestring = int(r.timestamp)
        try:
            lat = float(r.lat)
            lon = float(r.lon)
            alt = float(r.alt)
        except:
            lat = ""
            lon = ""
            alt = ""
        publish(HOST_ECLIPSE, r.event, float(r.value), timestring, lat, lon, alt)
        print tdiff
        k = (k + 1)        
        yield From(trollius.sleep(tdiff))

#PCMAC:  d0df9a95296c (d0:df:9a:95:29:6c)
#PiMac:  74da382afd91
def publish(hostname, event, value,  timestamp, lat, lon, alt, device_id="74da382afd91", prio_class="low", prio_value=10 ):
    d = {"d":
            {
                "timestamp": timestamp,
                "event": event,
                "value": value,
                "prio_class": prio_class,
                "prio_value": prio_value,
                "geotag":{
                    "lat": lat,
                    "lon": lon,
                    "alt": alt
                }
            }
        }
    jsonstr = json.dumps(d)
    msg = jsonstr

    try:
        # "iot-1/d/801f02da69bc/evt/light/json"
        topic = "iot-1/d/" + device_id + "/evt/" + event + "/json"
        #topic = "paho/test/iotBUET/bulk/"
        msgs = [{'topic': topic, 'payload': msg},
                ("paho/test/multiple", "multiple 2", 0, False)]
        pub.single(topic, payload=msg, hostname=hostname, port=1883)
        pub.single(topic+"plotly" , payload=msg, hostname=hostname, port=1883 )
        return True
    except:
        print ("error")
        traceback.print_exc()
        return False

if __name__ == '__main__':
    loop = trollius.get_event_loop()
    try:
        loop.run_until_complete(send_data_every_tdiff_seconds())
    finally:
        loop.close()
