#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import os
import time

PORT_NUMBER = 80

abspath = '/home/pi/gpf'

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if self.path.endswith(".png"):
				mimetype='image/png'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(abspath + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			wifi_name = form["wifi_name"].value
			wifi_pass = form["wifi_pass"].value
			wpa_supplicant = ["country=CA\n", "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n", "update_config=1\n\n", "network={\n", '\tssid="%s"\n' % wifi_name, '\tpsk="%s"\n' % wifi_pass, "}"]
			fh = open("wpa_supplicant.conf", "w")
			fh.writelines(wpa_supplicant)
			fh.close()
			os.system('sudo mv wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf')
			os.system('sudo cp /home/pi/gpf/supportingfiles/interfaces.bak /etc/network/interfaces')
			self.send_response(200)
			self.end_headers()
			self.wfile.write("Thanks! The device is reconfiguring itself and will reboot and be available on the %s network. Please be patient." % form["wifi_name"].value)
			time.sleep(5)
			os.system('sudo reboot now')
			return			
						
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	
