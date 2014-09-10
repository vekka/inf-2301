
import socket
import sys


class WebServer():
	def __init__(self, port=8080):
		self.address = "0.0.0.0"
		self.port = str(port)
	
	def printInfo(self):
		print "WebServer is set up with the following config:"
		print "- Address = '" + self.address + ":" + self.port + "'"
	
	


if __name__ == '__main__':
	ws = WebServer();
	ws.printInfo()
