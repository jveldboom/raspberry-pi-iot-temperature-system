from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import Adafruit_DHT, time, json, logging, os

config = {
    "sensor": Adafruit_DHT.AM2302, # Adafruit_DHT.DHT11, Adafruit_DHT.DHT22 or Adafruit_DHT.AM2302
    "gpioPin": 4, # update to match your config
    "clientId": os.environ["CLIENT_ID"],
    "mqttHost": os.environ["MQTT_HOST"],
    "mqttTopic": "temperature",
    "defaultState": {
        "reportFrequency": 60,
        "connected": True
    }
}

state = config["defaultState"]

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# For certificate based connection
shadowClient = AWSIoTMQTTShadowClient(config["clientId"])
shadowClient.configureEndpoint(config["mqttHost"], 8883)
shadowClient.configureCredentials("certs/rootCA.pem", "certs/private.key", "certs/cert.pem")

# AWSIoTMQTTShadowClient configuration
shadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
shadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
shadowClient.configureMQTTOperationTimeout(5)  # 5 sec
shadowClient.configureLastWill(config["clientId"], '{"state":{"reported":{"connected":false}}}', 1)
shadowClient.connect()

mqttClient = shadowClient.getMQTTConnection()

def shadowUpdateCallback(payload, responseStatus, token):
    logger.info("Shadow Update: "+str(payload))

def shadowGetCallback(payload, responseStatus, token):
    global state

    logger.info("Shadow Get: "+json.dumps(payload))
    if responseStatus == "rejected":
        newPayload = {
            "state":{
                "desired": state,
                "reported": state
            }
        }
        deviceShadowHandler.shadowUpdate(json.dumps(newPayload), None, 5)
    else:
        payloadDict = json.loads(payload)
        if "desired" in payloadDict["state"]:
            state = payloadDict["state"]["desired"]

def shadowDeleteCallback(payload, responseStatus, token):
    logger.info("Shadow Delete: "+responseStatus+" "+str(payload))

def shadowDeltaCallback(payload, responseStatus, token):
    global state

    logger.info('Shadow Delta: '+str(payload))
    payloadDict = json.loads(payload)

    for key, value in payloadDict["state"].iteritems():
        state[key] = value

    newPayload = {
        "state":{
            "reported": state,
            "desired": None
        }
    }
    deviceShadowHandler.shadowUpdate(json.dumps(newPayload), None, 5)

def readSensor():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(config["sensor"], config["gpioPin"])
        # convert celsius to fahrenheit
        temperature = temperature * 9/5.0 + 32
        
        # logger.info('Temp={0:0.1f}  Humidity={1:0.1f}%'.format(temperature, humidity))
        return temperature, humidity
    except Exception as err:
        logger.error('Error reading sensor:' +err)
        return 0, 0

def reportSensorReadings():
    temperature, humidity = readSensor()

    # prevent bad data from being reported
    if(temperature == 0 and humidity == 0):
        logger.warn("Invalid sensor values - not reporting")
        return False

    reading = {
        "temperature": temperature,
        "humidity": humidity
    }
    
    logger.info("Publishing: "+config["mqttTopic"]+"/"+config["clientId"]+"/reading "+json.dumps(reading))
    mqttClient.publish(config["mqttTopic"]+"/"+config["clientId"]+"/reading", json.dumps(reading), 1)

#  Create device shadow handler
deviceShadowHandler = shadowClient.createShadowHandlerWithName(config["clientId"], True)
deviceShadowHandler.shadowUpdate('{"state":{"reported": '+json.dumps(state)+'}}', None, 5)
deviceShadowHandler.shadowGet(shadowGetCallback, 5)
deviceShadowHandler.shadowDelete(shadowDeleteCallback, 5)
deviceShadowHandler.shadowRegisterDeltaCallback(shadowDeltaCallback)

while True:
    logger.info("Current State: "+str(state))

    reportSensorReadings()

    time.sleep(state["reportFrequency"])
