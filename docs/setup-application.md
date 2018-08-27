# Setting up Application
The application is a single Python script `run.py` which is managed by supervisor that handles starting it on boot and restarting it after any fatal errors. (_Python is not my first language so be easy_)

The application 

### Install Python Libraries
```
sudo apt-get install git-core build-essential python-dev
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
cd .. && sudo rm -rf Adafruit_Python_DHT/

pip install AWSIoTPythonSDK
```
### Upload Application Code
- Update `run.py` to match your sensor and GPIO port:
    - To use correct library for your sensor. `Adafruit_DHT.DHT11`, `Adafruit_DHT.DHT22` or `Adafruit_DHT.AM2302`
    - GPIO port
    - Default report requency - defaults to 60 seconds
- Download [VeriSign Class 3 Public Primary G5 root CA](https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem) certificate and save as `rootCA.pem` in `./devices/certs`
- Upload contents of `./device/` directory to Pi - should include two Python scripts and certs used for MQTT.

### Run Test Application
Run to test sensor library and ports are all setup correct and reporting values
```
python test-sensor.py
```

---

## Create Certificates and Register Pi in AWS IoT

### Create Device Keys & Certificate
Save the output `certificatePem` to `device/certs/cert.pem` and `PrivateKey` to `device/certs/private.key`.
```
aws iot create-keys-and-certificate --set-as-active

{
    "certificateArn": "arn:aws:iot:us-east-1:1234567890:cert/xxxxxxxxx",
    "certificatePem": "-----BEGIN CERTIFICATE-----...",
    "keyPair": {
        "PublicKey": "-----BEGIN PUBLIC KEY-----...",
        "PrivateKey": "-----BEGIN RSA PRIVATE KEY-----..."
    },
    "certificateId": "xxxxxxxxx"
}
```

### Attached Certificate to Policy
```
aws iot attach-policy \
    --policy-name temperature-system-policy \
    --target <certifcateArn>
```

### Create Thing
```
aws iot create-thing --thing-name pi2 --thing-type-name temperature

{
    "thingArn": "arn:aws:iot:us-east-1:1234567890:thing/pi2",
    "thingName": "pi2",
    "thingId": "920b2a20-63b4-468d-860a-2b4a9735cd2c"
}
```

### Attach Thing to Certificate
```
aws iot attach-thing-principal \
    --thing-name pi2 \
    --principal <certificateArn>
```