
import socket 
import sys
import string
import os

class Client():
	def __init__(self, address='localhost', port=50000):
		self.address = address
		self.port = port
		self.disk = "client_disk"
	
		self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
		
	
	def getFile(self):
		
		request = "get test.txt"
		self.socket.connect( (self.address,self.port) )
		
		self.socket.sendall( request )
		
		self.fileData = self.socket.recv( 4096 )
		
		self.socket.close()
		
		print self.fileData
		
	def writeFile(self):
	
		file = open( os.path.join( self.disk, "test.txt" ), "wb" )
		
		file.write( self.fileData )
		file.close()
		
if __name__ == '__main__':
	c = Client()
	
	c.getFile()
	c.writeFile()
	