import json
import time
import urllib.request
from kafka import KafkaProducer

API_KEY = "62ebd294a838133f3a07500d5a40e74603e23d82" 
url = "https://api.jcdecaux.com/vls/v1/stations?apiKey={}".format(API_KEY)

producer = KafkaProducer(bootstrap_servers="localhost:9092")

while True:
    response = urllib.request.urlopen(url)
    stations = json.loads(response.read().decode())
    for station in stations:
        producer.send("velib-topic", json.dumps(station).encode())
        print(station)
        

    
    