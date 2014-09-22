
import socket
import sys
import os
import string
import base64
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random

# Symmetric key: use AES with CBC mode. a disadvantage with CBC: block cipher,
# needs to pad the plaintext blocks before encryption ( must be multiple of "block size", here: 16 bytes)

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
			
	def CreateAESKey(self):
		randobj = Random.new()
	
		# pseudo random init. vector. For security reason it should not be used again, but rather
		#create a new one every time we send data
		self.iv = randobj.read(AES.key_size[0])	
		#random key, 16 bytes or 128 bits. AES supports 128, 192 and 256 bits keys
		self.aesKey = randobj.read( AES.key_size[0] )
		

		#a cipher object to be used for encryptions .. symmetric key
		self.aesObj = AES.new( self.aesKey, AES.MODE_CBC, IV = self.iv )
		
			
	def CreateRSA(self, keySize=2048 ):
		randobj = Random.new()
		randnum = randobj.read
		
		self.rsaPair = RSA.generate( keySize, randnum ) 	
		
	def encryptWithAES(self):
		#add padding to make file data a multiple of block size, 16 bytes
		self.addPadding()
		
		#append IV to ciphertext(that is being created)
		self.ciphertext = self.iv + self.aesObj.encrypt( self.fileData )
		self.iv = None

	def showStatus(self):
		print "SERVER SIDE"
		print "aesKey = ", self.aesKey
		print "plaintext(padded version) = ", self.fileData
		print "ciphertext = ", self.ciphertext
		
	def readFile(self):

		file = open( self.filename, "rb" )
		fileData = file.read()
		file.close()
		return fileData
	
	def listen(self):
		maxsize = 4096
		isRequest = 0
		self.CreateRSA()
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
			
			data = cli.recv(maxsize)
			#wait until a request has been received, before creating a new AES key
			
			#received the public part of the client`s RSA Key. use this to encrypt aes key before sending it
			#to the client( together with the encrypted file data )
			if string.find(data, "BEGIN PUBLIC KEY" ) != -1:#public part of rsa key detected
				isRequest = 1
			
			#max size of the file name requested, is set to 32 bytes, everything beyond this point
			#up to "maxSize" is considered the public-part of the client`s RSA
			if isRequest:
				print data
				
				clientsPublicKey = data[32:] #rsa key from client
				self.CreateAESKey() # NEW aes key
				print "not encrypted aes key: ", self.aesKey
				encryptedAES = self.rsaPair.encrypt( self.aesKey, clientsPublicKey )[0]
				
				#print "encrypted aes key: ", encryptedAES
				# iv + encrypted file data
				self.encryptWithAES()
	
	
				#send (RSA)encrypted AES key:
				cli.sendall( encryptedAES )
	
		
			condition = False
			cli.close()
		
		
		
if __name__== '__main__':
	s = Server()
	s.listen()

	