
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
		self.symkey = random.read( AES.key_size[0] )
		
		if len(sys.argv) > 1:
			self.filename = os.path.join("server_disk", sys.argv[1])
			print "file: " + self.filename
		else:
			print "Need a file as an argument"
			sys.exit(1)
		
		#read plaintext
		self.fileData = self.readFile()
	
	def encrypt(self):
		# pseudo random init. vector. Since this assignment intends to use counter mode
		#, this is the start value of the counter(initial_value)
		IV = Random.new().read(AES.block_size)
		print "key size = ", AES.key_size
		
		#a counter for each block. A block is 16 bytes
		ctr = Crypto.Util.Counter.new(128, initial_value=long(IV.encode('hex'), 16))
		#a cipher object to be used for encrypting from plaintext ro ciphertext
		self.encobj = AES.new( self.symkey, AES.MODE_CTR, counter = ctr )
		#make plaintext into ciphertext
		
		self.ciphertext = ""
		print type( self.ciphertext )
		#append IV to ciphertext just created
		self.ciphertext = IV + self.encobj.encrypt( self.fileData )

	def showStatus(self):
		print "SERVER SIDE"
		print "key = ", base64.b64encode( self.symkey )
		print "plaintext = ", self.fileData
		print "ciphertext = ", base64.b64encode( self.ciphertext )
		
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
			#wait until a request has been received, before encrypting data or key
			if requestData:
				
				cli.sendall( base64.b64encode(self.symkey) )
				
				self.encrypt()
				
				self.showStatus()
				
				
				cli.sendall( base64.b64encode (self.ciphertext ) )
		
			condition = False
			cli.close()
		
		
		
if __name__== '__main__':
	s = Server()
	s.listen()

	