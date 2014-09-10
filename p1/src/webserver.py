
import socket
import sys


class WebServer():
	def __init__(self, port=8080):
		self.address = "0.0.0.0"
		self.port = port
	
	def printInfo(self):
		print "WebServer is set up with the following config:"
		print "- Address = '" + self.address + ":" + str(self.port) + "'"
	
	def listen(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((self.address, self.port))
			s.listen(5)
		except socket.error:
			print "Failed to create socket"
			sys.exit()

		print "Starting accept-loop"
		while True:
			conn, address = s.accept()
			print "Incoming connection: "
			print "  Conn   : ", conn
			print "  Address: ", address


if __name__ == '__main__':
	ws = WebServer();
	ws.printInfo()
	ws.listen()
