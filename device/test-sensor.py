import Adafruit_DHT, time, json, logging, os

config = {
    "sensor": Adafruit_DHT.AM2302, # Adafruit_DHT.DHT11, Adafruit_DHT.DHT22 or Adafruit_DHT.AM2302
    "gpioPin": 4, # update to match your config
}

humidity, temperature = Adafruit_DHT.read_retry(config["sensor"], config["gpioPin"])
# convert celsius to fahrenheit
temperature = temperature * 9/5.0 + 32
        
print('Temp={0:0.1f}  Humidity={1:0.1f}%'.format(temperature, humidity))
