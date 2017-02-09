# “WiFi direct” style WiFi setup on a Raspberry Pi
by Harin on February 7, 2017

I was recently contacted and asked to make a few GIF photo frames. I’ve designed and built embedded Raspberry Pi systems before, but those were usually geared towards people who were already familiar with the Raspberry Pi and its idiosyncrasies. The interesting problem here was designing a system that would allow the end user to easily configure and set up WiFi on demand. I stress that this is for the end user! This will not help you if you are trying to set up WiFi on a Raspberry Pi for the first time. This requires some configuring beforehand so you will have to start with a RPi with an internet connection. You could clone the SD cards after set up and would be able to deploy your system much more efficiently.

In the end, what I came up with is a python program that would allow the end user to start up a WiFi configuration mode by pressing a pushbutton. This would then disconnect from any already connected WiFi networks and start up a WiFi hotspot which the user can connect to. The software then hosts a webserver where the user can navigate to and fill in their WiFi network details.

There were a few drawbacks to this method, it would have been much more elegant to have designed a mobile app to interact with the webserver, but given the scope of the project, this was a little ambitious. Another drawback was my inability to get a captive portal type service to work reliably, in its current state the process requires the end user to manually navigate to 10.0.0.1 in order to access the WiFi setup page. As a first iteration of this system though, I was very happy with the results.

In order to make this work I relied heavily on the EW-7811UN WiFi dongle from Edimax. These dongles are tiny and can be made to support AP mode under Raspbian. These was ideal for me because the tiny form factor and the fact that I have used tons of these in previous projects meant that I could easily integrate one into my end design.

I uploaded what I’ve written to github; I’m not a programmer by any means so the code might not be the greatest, but it works. There are four files, *button.py* needs to be run on startup using chron and will monitor a pushbutton and the *httpserver.py* file starts the http server that will host a webform for the end user to input their wifi credentials. I have uploaded a sample index.html to get people started but, I warn you, it’s not very pretty. The three files and the *supportingfiles folder* must reside in a folder named “gpf” in the home directory of the pi user.

You must install two programs on the RPi.

`sudo apt-get install hostapd dnsmasq -y`

Then configure your access point settings by editing /etc/hostapd/hostapd.conf, mine looks like this:

```
interface=wlan0 
ssid=Solder&Flux GIF Photo Frame 
hw_mode=g 
channel=6 
macaddr_acl=0 
auth_algs=1 
ignore_broadcast_ssid=0 
wpa=2 
wpa_passphrase=solderandflux 
wpa_key_mgmt=WPA-PSK 
rsn_pairwise=CCMP
```

You can follow this [guide](http://xmodulo.com/how-to-set-up-dhcp-server-using-dnsmasq.html) on how to set up dnsmasq as a dhcp server on the RPi. Just make sure to use 10.0.0.1 as the RPi’s address and to set the interface to wlan0. The DHCP range should also be within 10.0.0.x.

The next step is to make sure to disable hostapd and dnsmasq from running at startup by typing the following into a terminal:

```
sudo update-rc.d dnsmasq disable
sudo update-rc.d hostapd disable
```

This will prevent hostapd and dnsmasq from interfering when we don’t want them to.

The final step is to create a backup of your current /etc/network/interfaces and place a copy in /home/pi/gpf/supportingfiles by running this command:

`sudo cp /etc/network/interfaces /home/pi/gpf/supportingfiles/interfaces.bak`

Once the software portion is out of the way, you just need to connect a push button to the 12th pin on the GPIO header of your RPi. I’ve used the internal pull ups so you only need to connect the push button to pin 12 and ground.

This is my attempt at making an embedded device where any user can easily reconfigure the wifi settings regardless of skill level. I’m sure there are a lot of improvements to be made to this system but it works for the purposes I need it to for now.