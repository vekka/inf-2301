
import socket
import string
import sys
import os
from Crypto.Cipher import AES
import base64

class Server():
	def __init__(self, ipaddr='0.0.0.0', port=50000):
		self.text = "oh hello"
		self.port = port
		self.ipaddress = ipaddr
		
		if len(sys.argv) > 1:
			self.filename = os.path.join("server_disk", sys.argv[1])
			print "file: " + self.filename
		else:
			print "Need a file as an argument"
			sys.exit(1)
			
		self.fileData = self.readFile()

		print "filedata: " + self.fileData
		
	def readFile(self):

		file = open( self.filename, "rb" )
		fileData = file.read()
		file.close()
		return fileData
	
	def listen(self):
		try:
			s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			s.bind( (self.ipaddress,self.port) )
			s.listen(5)
		except socket.error:
			if socket:
				socket.close()
			print 'error occurred while creating and binding socket'
			sys.exit(-1)
		
		while True:
			(cli,cliaddr) = s.accept()
			
			data = cli.recv(4096)
			if data:
				cli.sendall( self.fileData )
			
			cli.close()
		
		
		
if __name__== '__main__':
	s = Server()
	s.listen()

	