
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
		elif string.find(self.request, "post") or string.find(self.request, "POST"):
			self.handlePost(socket)
		else:
			print "unsupported request.."
		
	def handleGet(self, socket):
		response = ''
		found = 0
		list = string.split( self.request )
		token = "index.html"
		newToken = token
		#is requested resource an html file
		for t in list:
			if string.find(t, ".html" ) > -1:
				token = t
				found = 1
				break
			if string.find(t, ".txt" ) > -1:
				token = t
				found = 1
				break
		
		if found:
			newToken = token
			if "/" in token[0:2]:
				newToken = token[1:len(token)]
			
			
			print "requesting file with name: ", newToken
			file = open( newToken, "r" )
			reponse = "200 OK"
			
			body = file.read( self.maxMessageSize )
			response += body
			socket.send( response )
			file.close()
	def handlePost(self, socket ):
		response = ''
		body = "this should be the body to post"
		file = None
		token = newToken = None
		bodyLen = 0
		list = string.split( self.request )
		#is requested resource an html file
		for t in list:
			if string.find(t, ".html" ) > -1:
				print t
				token = t
				break
			if string.find(t, ".txt" ) > -1:
				print t
				token = t
				break
		
		if "/" in token[0:2]:
			newToken = token[1:len(token)]
		else:
			newToken = token
		if newToken:
			file = open( newToken, "w" )
			# FIXME the POST request body should be written to the file here
			file.write( body )
			socket.send( body )
			file.close()


if __name__ == '__main__':
	ws = WebServer();
	ws.printInfo()
	ws.listen()
