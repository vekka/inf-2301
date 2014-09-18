
import socket 
import sys
import os
from Crypto.Cipher import AES
from Crypto import Random
import base64

class Client():
	def __init__(self, address='localhost', port=50000):
		self.address = address
		self.port = port
		self.disk = "client_disk"
		
		self.fileData = ""
	
		self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
		
	
	#received key from server, use it to decrypt file data
	def DecryptFileData(self, key ):
		pass
	
	def getFile(self):
		keysize = 32
		datasize = 4096
		request = "get me file"
		self.socket.connect( (self.address,self.port) )
		
		self.socket.sendall( request )
		
		self.symkey = self.socket.recv( keysize )
		self.fileData = self.socket.recv( datasize )
		
		
		print "(client)key = ", self.symkey
		print "(client)ciphertext = ", self.fileData

			
		self.socket.close()
		
		
		
	def writeFile(self):
	
		file = open( os.path.join( self.disk, "test.txt" ), "wb" )
		
		file.write( self.symkey )
		file.close()
		
if __name__ == '__main__':
	c = Client()
	
	c.getFile()
	c.writeFile()
	