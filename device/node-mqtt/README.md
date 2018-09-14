
### Install NodeJS on Raspberry Pi
```
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
```

## Install Driver
```
// check for latest verson http://www.airspayce.com/mikem/bcm2835/index.html
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.56.tar.gz
tar zxvf bcm2835-1.56.tar.gz
cd bcm2835-1.xx
./configure
make
sudo make check
sudo make install
```