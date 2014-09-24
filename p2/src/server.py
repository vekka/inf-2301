
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
	
		padding = (16 - (len("0x0;" + self.fileData) % 16)) % 16
		
		print len(self.fileData), len(self.fileData) % 16
		self.fileData = hex(padding) + ";" + self.fileData + ' ' * padding
		print len(self.fileData), len(self.fileData) % 16
		
		
		#while (len( self.fileData ) % 16) != 0:
		#	self.fileData += ' ' * ( 16 - len(self.fileData) % 16 )
	
			
	def CreateAESKey(self):
		randGenForIV = Random.new()
		randGenForAesKey = Random.new()
		# pseudo random init. vector. For security reason it should not be used again, but rather
		#create a new one every time we send data
		print "Create AES key with size", AES.key_size[0], "bytes"
		
		self.iv = randGenForIV.read(AES.key_size[0])	
		#random key, 128 bits. AES supports 128, 192 and 256 bit keys
		self.aesKey = randGenForAesKey.read( AES.key_size[0] )
		

		#a cipher object to be used for encryptions .. symmetric key
		self.aesObj = AES.new( self.aesKey, AES.MODE_CBC, IV = self.iv )
		
			
	def CreateRSA(self, keySize=2048 ):
		randGenerator = Random.new().read
	
		self.rsaPair = RSA.generate( keySize, randGenerator )
		self.rsaPublic = self.rsaPair.publickey()
		self.rsaPrivate = self.rsaPair
		
	def encryptWithAES(self):
		#add padding to make file data a multiple of block size, 16 bytes
		self.addPadding()
		
		#append IV to ciphertext(that is being created)
		#self.ciphertext = self.iv + self.aesObj.encrypt( self.fileData )
		self.ciphertext = self.aesObj.encrypt( self.fileData )

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
				self.CreateAESKey() 
				self.encryptWithAES()
				#this is the rsa key from client
				clientsPublicRSA = data[32:] 
				# create NEW aes key
				
				
				
				#use rsa key from client to encrypt the AES key
				#I.e import the public RSA part received from client in order to encrypt the AES key
				#to be used for decrypting the file itself
				key = RSA.importKey( clientsPublicRSA )
				
				#note: can`t figure out what the 2nd paramter to this method is for
				#however it returns a tuple
				print "IV + AES Size:", len(self.iv + self.aesKey)
				encryptedAES = key.encrypt( self.iv + self.aesKey, ""  )[0]
				print "Encrypted Size:", len(encryptedAES)
	
				#send (RSA)encrypted AES key:
				cli.sendall( encryptedAES )
				cli.sendall( self.ciphertext )
				#print "encrypted aes key: ", encryptedAES[0]
				#print "not encrypted aes key: ", self.aesKey
				
		
			condition = False
			cli.close()
		
		
		
if __name__== '__main__':
	s = Server()
	s.listen()

	