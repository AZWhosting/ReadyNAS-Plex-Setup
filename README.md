## Installation of my Plex Setup on ReadyNAS 


#### Install vim
```
apt-get install vim
```
#### Install git
```
apt-get install git
```
#### Install Python 2.7.11 | http://python.org
````
apt-get install build-essential checkinstall
apt-get install zlib1g-dev libsqlite3-dev openssl libssl-dev
cd /usr/src
wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
tar xzf Python-2.7.11.tgz
cd Python-2.7.11
./configure
make
make install
python -V
```
#### Install mono 4.0+ | http://www.mono-project.com/docs/getting-started/install/linux/#libgdiplus-debian-80-and-later-not-ubuntu
```
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
echo "deb http://download.mono-project.com/repo/debian wheezy main" | tee /etc/apt/sources.list.d/mono-xamarin.list
apt-get update
echo "deb http://download.mono-project.com/repo/debian wheezy-libjpeg62-compat main" | tee -a /etc/apt/sources.list.d/mono-xamarin.list
apt-get install mono-complete
mono -V
```
#### Install Cheetah | https://pypi.python.org/pypi/Cheetah/2.4.4
```
mkdir /data/tmp/
cd /data/tmp/
wget https://pypi.python.org/packages/source/C/Cheetah/Cheetah-2.4.4.tar.gz#md5=853917116e731afbc8c8a43c37e6ddba
tar -xzf Cheetah-2.4.4.tar.gz
cd Cheetah-2.4.4
python setup.py install
```

#### Installing PlexRequests.NET | 3579 | https://github.com/tidusjar/PlexRequests.Net
```
cd /data/
mkdir opt/
mkdir opt/PlexRequests/
wget https://github.com/tidusjar/PlexRequests.Net/releases/download/v1.6.0/PlexRequests.zip
unzip PlexRequests.zip
mv Release/* opt/PlexRequests/
mozroots --import --ask-remove 
mono /data/opt/PlexRequests/PlexRequests.exe
```

#### Install SickRage | 8081 | https://github.com/SickRage/SickRage
```
cd /data/
git clone https://github.com/SickRage/SickRage /data/opt/SickRage
python /data/opt/SickRage/SickBeard.py
```

#### Install CouchPotato | 5050 | https://couchpota.to/#linux // FIX ME
```
git clone https://github.com/CouchPotato/CouchPotatoServer.git /data/opt/CouchPotato
python /data/opt/CouchPotato/CouchPotato.py
```

#### Install Transmission-daemon | 9091 | https://transmissionbt.com
```
apt-get install transmission-daemon
service transmission-daemon stop
vim /var/lib/transmission-daemon/info/settings.json
```
##### Edit the following to:
```
"download-dir": "/data/PlexStorage/Downloads/TV",
"incomplete-dir": "/data/PlexStorage/Downloads/Incomplete",
"rpc-password": "$PASSWORD",
"rpc-username": "$USERNAME",
"rps-whitelist-enabled": false,
```
```
service transmission-daemon start
```
##### If you need multiple transmission clients: | 9092 | https://transmissionbt.com
```
service transmission-daemon stop
cp /usr/bin/transmission-daemon /usr/bin/transmission-daemon2 
cp /etc/init.d/transmission-daemon /etc/init.d/transmission-daemon2 
cp -a /var/lib/transmission-daemon /var/lib/transmission-daemon2 
cp -a /etc/transmission-daemon /etc/transmission-daemon2 
cp /etc/default/transmission-daemon /etc/default/transmission-daemon2
ln -sf /etc/transmission-daemon2/settings.json /var/lib/transmission-daemon2/info/settings.json
vim /etc/init.d/transmission-daemon2
```
##### Edit the following to:
```
Provides:	transmission-daemon2
NAME=transmission-daemon2
```
```
vim /var/lib/transmission-daemon2/info/settings.json
```
##### Edit the following to:
```
"download-dir": "/data/PlexStorage/Downloads/Movies",
"peer-port": 51414,
"rpc-port": 9092,
"rpc-password": "$PASSWORD",
"rpc-username": "$USERNAME",
```
```
vim /etc/default/transmission-daemon2
```
##### Edit the following to:
```
CONFIG_DIR="/var/lib/transmission-daemon2/info"
update-rc.d transmission-daemon2 defaults
service transmission-daemon start
service transmission-daemon2 start
```

#### Install Headphones | 8181 | https://github.com/rembo10/headphones
```
git clone https://github.com/rembo10/headphones.git /data/opt/headphones
```
##### Create config files
```
python /data/opt/headphones
vim /data/opt/headphones/config.ini
```
##### Edit the following:
```
http_host = 0.0.0.0	
```
#### Install PlexPy REQUIRES PLEXPASS | https://github.com/drzoidberg33/plexpy
```
git clone https://github.com/drzoidberg33/plexpy.git /data/opt/plexpy
vim /etc/init.d/plexpy
chmod +x /etc/init.d/plexpy
update-rc.d plexpy defaults
service plexpy start
```

#### Install Muximux | /site/ | https://github.com/mescon/Muximux
##### Make folder 'site' via ReadyNAS admin page, allow HTTP access
```
apt-get install php5 php-pear php5-mysql
git clone https://github.com/mescon/Muximux.git /data/site
```

#### Install IPTV (Hockey) | https://github.com/Cigaras/IPTV.bundle
```
git clone https://github.com/Cigaras/IPTV.bundle.git /apps/plexmediaserver/MediaLibrary/Plex\ Media\ Server/Plug-ins/IPTV.bundle
```
##### NHL Scrape Script
```
apt-get install python-pip
apt-get install libxml2-dev libxslt-dev python-dev
pip install lxml
pip install requests
cp NHL.py /apps/plexmediaserver/MediaLibrary/Plex\ Media\ Server/Plug-ins/IPTV.bundle/Contents/Resources/
/usr/bin/python  /apps/plexmediaserver/MediaLibrary/Plex\ Media\ Server/Plug-ins/IPTV.bundle/Contents/Resources/NHL.py
```


## Starting At Boot

#### SickRage
```
vim /etc/init.d/SickRage
```
##### Paste init.d Script
```
chmod +x /etc/init.d/SickRage
update-rc.d SickRage defaults
service SickRage start
```
#### CouchPotato
```
cp /data/opt/CouchPotato/init/ubuntu /etc/init.d/couchpotato
touch /etc/default/couchpotato
vim /etc/default/couchpotato
```
##### Config
```
CP_USER       couchpotato # username to run couchpotato under (couchpotato)
CP_HOME       /data/opt/CouchPotato
CP_DATA       /data/opt/CouchPotato
CP_PIDFILE    /data/opt/CouchPotato/couchpotato.pid
PYTHON_BIN    /usr/local/bin/python
```
```
chmod +x /etc/init.d/couchpotato
service couchpotato start
```
#### PlexRequests
```
vim /etc/init.d/PlexRequests
```
##### Paste init.d Script
```
chmod +x /etc/init.d/PlexRequests
update-rc.d PlexRequests defaults
service PlexRequests start
```
#### Headphones
```
vim /etc/init.d/headphones
```
##### Paste init.d Script
```
chmod +x /etc/init.d/headphones
update-rc.d headphones defaults
service headphones start
```