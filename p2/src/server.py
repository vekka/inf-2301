
import socket
import sys
import os
import base64
import Crypto.Util.Counter
from Crypto.Cipher import AES
from Crypto import Random

# Symmetric key: use AES with CRT mode
class Server():
	def __init__(self, ipaddr='0.0.0.0', port=50000):
		self.text = "oh hello"
		self.port = port
		self.ipaddress = ipaddr
		random = Random.new()
		
		#random key, 16 bytes or 128 bits. AES supports 128, 192 and 256 bits keys
		self.key = random.read( AES.key_size[0] )

		#random initialization vector. 
		IV = Random.new().read(AES.block_size)
		print "key size = ", AES.key_size[0]
		
		#a counter for each block. A block is 16 bytes
		ctr = Crypto.Util.Counter.new(128, initial_value=long(IV.encode('hex'), 16))
		encobj = AES.new( self.key, AES.MODE_CTR, counter = ctr )
		
		if len(sys.argv) > 1:
			self.filename = os.path.join("server_disk", sys.argv[1])
			print "file: " + self.filename
		else:
			print "Need a file as an argument"
			sys.exit(1)
		
		#read plaintext
		self.fileData = self.readFile()
		
		#make plaintext into ciphertext
		self.cipherText = encobj.encrypt( self.fileData )
		
		print "key = ", self.key
		print "plaintext = ", self.fileData
		print "ciphertext = ", self.cipherText
		
	def readFile(self):

		file = open( self.filename, "rb" )
		fileData = file.read()
		file.close()
		return fileData
	
	def listen(self):
		maxsize = 4096
		try:
			s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			s.bind( (self.ipaddress,self.port) )
			s.listen(5)
		except socket.error:
			if socket:
				socket.close()
			print 'error occurred while creating and binding socket'
			sys.exit(-1)
		
		condition = True
		while condition:
			(cli,cliaddr) = s.accept()
			
			requestData = cli.recv(maxsize)
			if requestData:
				cli.sendall( self.key )
				cli.sendall( self.cipherText )
		
			condition = False
			cli.close()
		
		
		
if __name__== '__main__':
	s = Server()
	s.listen()

	