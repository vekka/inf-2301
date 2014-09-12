
import socket
import sys
import os
import string

class WebServer():
	def __init__(self, port=8080):
		self.address = "0.0.0.0"
		self.port = port
		self.maxMessageSize = 4096
		self.request = ""
		self.response = "<html> test nettside er dette </html>"
		
		self.hostedDirectory = "./hosted"
		
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
			
			#print self.request
				
			if len(self.request):
				self.handleRequest( clientsocket )
			
			#clientsocket.close()
			
	def handleRequest(self, socket):
		
		requestWithoutCR = self.request.replace("\r", "")
		requestAsList = requestWithoutCR.split('\n')
		requestLine = requestAsList.pop(0)
		requestLineAsList = requestLine.split(' ')
	
		if requestLineAsList[0] == "GET":
			self.handleGet(requestLineAsList, socket)
		elif requestLineAsList[0] == "POST":
			self.handlePost(requestLineAsList, socket)
		else:
			socket.close()
		
	def handleGet(self, requestLineAsList, socket):
	
		responseFile = self.hostedDirectory + requestLineAsList[1]
		if os.path.isdir(responseFile):
			responseFile = responseFile + "/"
			
		if responseFile[-1] == '/':
			responseFile = responseFile + "index.html"
			
		content = ""
		response = "HTTP/1.1 "
		try:
			print "Trying to open file: " + responseFile
			file = open(responseFile, 'rb')
			content = file.read()
			
			response = response + "200 OK\r\n"
			response = response + "Content-Length: " + str(len(content)) + "\r\n\r\n"
			response = response + content
			file.close()
			#print "Response: ", response
		except:
			print "Exception"
			response = response + "404 Not Found\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>"
	
		
		if socket.sendall(response) != None:
			print "Failed to send"
		
		print "Response successfully sent"
		socket.close()
		
		
	def handlePost(self, requestLineAsList, socket):
		requestFile = self.hostedDirectory + requestLineAsList[1]
		if requestFile != self.hostedDirectory + "/test/test.txt":
			response = "HTTP/1.1 403 Forbidden\r\n\r\n<html><body><h1>403 Forbidden</h1></body></html>"
			socket.sendall(response)
			socket.close()
			return
		
		self.request = self.request.replace('\r','')
		body = self.request.split("\n\n")[1]
		
		prefix = "test="
		
		content = body[len(prefix):]
		
		try:
			file = open(requestFile, "a")
			file.write("\n" + content)
			file.close()
			
			self.handleGet(requestLineAsList, socket)
		except:
			print "Exception"
			socket.close()		
		
	

if __name__ == '__main__':
	ws = WebServer();
	ws.printInfo()
	ws.listen()
