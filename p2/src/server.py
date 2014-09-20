
import socket
import sys
import os
import string
import base64
from Crypto.Cipher import AES
from Crypto import Random

# Symmetric key: use AES with CBC mode

# we try to create a new key and IV for every transmission

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
		
		#read plaintext
		self.fileData = self.readFile()
	
	def removePadding( self ):
		self.fileData.strip()
	def addPadding(self ):
		while (len( self.fileData ) % 16) != 0:
			self.fileData += ' ' * ( 16 - len(self.fileData) % 16 )
			
	def CreateSymmetricKey(self):
		random = Random.new()
		#random key, 16 bytes or 128 bits. AES supports 128, 192 and 256 bits keys
		self.symkey = random.read( AES.key_size[0] )
			
	def encrypt(self):
		# pseudo random init. vector. For security reason it should not be used again, but rather
		#create a new one every type send encrypted data
		iv = Random.new().read(AES.key_size[0])
		
		print "IV size in server = ", len(iv)
		
		#a cipher object to be used for encrypting from plaintext ro ciphertext
		self.encobj = AES.new( self.symkey, AES.MODE_CBC, IV = iv )

		#add padding to make file data a multiple of block size, 16 bytes
		self.addPadding()
		
		#append IV to ciphertext(that is being created)
		self.ciphertext = iv + self.encobj.encrypt( self.fileData )

	def showStatus(self):
		print "SERVER SIDE"
		print "symkey = ", self.symkey
		print "plaintext(padded version) = ", self.fileData
		print "ciphertext = ", self.ciphertext
		
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
				
				self.CreateSymmetricKey()
				
				cli.sendall( self.symkey )
				
				self.encrypt() #encrypt data from file
				self.showStatus()
				
				cli.sendall( self.ciphertext )
		
			condition = False
			cli.close()
		
		
		
if __name__== '__main__':
	s = Server()
	s.listen()

	