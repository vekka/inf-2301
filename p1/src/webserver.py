
import socket
import sys
import string

class WebServer():
	def __init__(self, port=8080):
		self.address = socket.gethostname()
		self.port = port
		self.maxMessageSize = 4096
		self.request = ""
		self.response = "<html> test nettside er dette </html>"
	def printInfo(self):
		print "WebServer is set up with the following config:"
		print "- Address = '" + self.address + ":" + str(self.port) + "'"
	
	def listen(self):
		size=self.maxMessageSize
		try:
			serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			serversocket.bind((self.address, self.port))
			serversocket.listen(5)
		except socket.error:
			if serversocket:
				serversocket.close()
			print "Failed to create socket"
			sys.exit()

		while True:
			(clientsocket, address) = serversocket.accept()
			self.request = clientsocket.recv(size)
			if len(self.request):
				self.handleRequest( clientsocket )
			
			#clientsocket.close()
			
	def handleRequest(self, socket):
		if string.find(self.request, "GET") > -1:
			print "in handle request now"
			self.handleGet(socket)
		elif string.find(self.request, "POST"):
			print "received post request"
		else:
			print "unsupported request.."
		
	def handleGet(self, socket):
		
		list = string.split( self.request )
		for t in list:
			if string.find(t, ".html" ):
				print "requesting file with name: ", t
				token = t

		socket.send( self.response )
			
				
		
		
		


if __name__ == '__main__':
	ws = WebServer();
	ws.printInfo()
	ws.listen()
