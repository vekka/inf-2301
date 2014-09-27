
import socket 
import sys
import os
import string
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
import base64

class Client():
	def __init__(self, address='localhost', port=50000):
		self.address = address
		self.port = port
		self.disk = "client_disk"
		self.fileData = ""
		self.rsaKeySize = 2048
		self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
		randomGenerator = Random.new().read
		
		self.rsaKey = RSA.generate( self.rsaKeySize, randomGenerator )
		
		
		self.publicKey = self.rsaKey.publickey()
		self.privateKey = self.rsaKey
			
	#if len(sys.argv) > 1:
		#pass
		print "sys.argv: ", sys.argv
	#else:
	#	print "No server address supplied, tries connecting to default localhost:50000"
		

	#received key from server, use it to decrypt file data
	def DecryptFileData(self, ciphertext  ):
		#extract portion of ciphertext to find init. vector used in decryption
		
		#print "IV size in client = ", len(iv)
		
		#create aes object to decrypt the ciphertext
		self.decobj = AES.new( self.aesKey, AES.MODE_CBC, self.iv )
		plaintext = self.decobj.decrypt( ciphertext )
		
		#plaintext is returned from decrypt method, but remove padding before returning it
		
		return plaintext
		
	def getFile(self):
		aesKeySize = 32 #in bytes
		datasize = 4096
		# request size is set to be 32 bytes. so client`s public rsa start after byte nr. 32
		# the server must be aware of this of course
		request = "the file name being requested   "
		
		#send request and own asymmetric key(public part of rsa key pair)
		myPublickeyAndRequest = request + self.publicKey.exportKey()
		self.socket.connect( (self.address,self.port) )
		
		#send public part of RSA
		self.socket.sendall( myPublickeyAndRequest )
		
		
		#receive encrypted aes key from server
		encryptedAESKey = self.socket.recv( 256 )
		
		print "LEN ENCRYPTED AES", len(encryptedAESKey)
		# Decrypt 'AES key' with own private RSA key
		decryptedAESKey = self.rsaKey.decrypt( encryptedAESKey )
		self.iv = decryptedAESKey[:16]
		self.aesKey = decryptedAESKey[16:]		
	
	
		encryptedFile = self.socket.recv( datasize )

		
		
		# Use this AES key to decrypt the file received ( receives IV + actual file data )
		plaintext = self.DecryptFileData( encryptedFile )
		
		print "'" + plaintext + "'", len(plaintext)
		padding = int(plaintext[:3], 16)
		plaintext = plaintext[4:-padding]
		
		
		print "'" + plaintext + "'", len(plaintext)
		
		self.writeFile( plaintext )
		#print "encrypted aes key: ", encryptedAESKey
		#print "decrypted aes from server: ", decryptedAESKey
		
	
		self.socket.close()
		
		
		
	def writeFile(self, datatoWrite ):
	
		file = open( os.path.join( self.disk, "test.txt" ), "wb" )
		
		file.write( datatoWrite )
		file.close()
		
if __name__ == '__main__':
	c = Client()
	c.getFile()
	
	