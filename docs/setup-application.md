## Setting up sensor software

http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/

__Install Python Libraries__
```
sudo apt-get install git-core build-essential python-dev
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
cd .. && sudo rm -rf Adafruit_Python_DHT/

pip install AWSIoTPythonSDK
```

__Test Application__
```
python test-sensor.py
```