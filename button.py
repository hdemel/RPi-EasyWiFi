import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
state = False

time.sleep(10)
os.system('sudo ifdown wlan0')
os.system('sudo cp /home/pi/gpf/supportingfiles/interfaces.bak /etc/network/interfaces')
os.system('sudo ifup wlan0')

while True:
    input_state = GPIO.input(18)
    if input_state == False:
        if state == False:
		print('Turning on WIFI configurator')
		os.system('sudo ifdown wlan0')
		os.system('sudo cp /home/pi/gpf/supportingfiles/interfaces.ap /etc/network/interfaces')
		os.system('sudo ifup wlan0')
		os.system('sudo service hostapd start')
		os.system('sudo service dnsmasq start')
		os.system('sudo python /home/pi/gpf/httpserver.py')
		state = True
	        time.sleep(0.2)

