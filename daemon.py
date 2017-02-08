import os

os.system('sudo ifdown wlan0')
os.system('sudo cp /home/pi/gpf/supportingfiles/interfaces.ap /etc/network/interfaces')
os.system('sudo ifup wlan0')
os.system('sudo service hostapd start')
os.system('sudo service dnsmasq start')
os.system('cd /home/pi/gpf')
os.system('sudo python httpserver.py &')