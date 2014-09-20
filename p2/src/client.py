
import socket 
import sys
import os
import string
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
		
	if len(sys.argv) > 1:
		pass
		print "sys.argv: ", sys.argv
	else:
		print "No server address supplied, tries connecting to default localhost:50000"
		
	def addPadding(self ):
		while (len( self.fileData ) % 16) != 0:
			self.fileData += ' ' * ( 16 - len(self.fileData) % 16 )
	
	#received key from server, use it to decrypt file data
	def DecryptFileData(self, ciphertext  ):
		#extract portion of ciphertext to find init. vector used in decryption
		iv = ciphertext[0:16]
		
		#print "IV size in client = ", len(iv)
		
		#create aes object to decrypt the ciphertext
		self.decobj = AES.new( self.symkey, AES.MODE_CBC, iv )
		plaintext = self.decobj.decrypt( ciphertext[16:] )
		
		#plaintext is returned from decrypt method, but remove padding before returning it
		
		return plaintext
		
	def getFile(self):
		keysize = 32
		datasize = 4096
		request = "get me file"
		self.socket.connect( (self.address,self.port) )
		
		self.socket.sendall( request )
		
		self.symkey = self.socket.recv( keysize )
		ciphertext = self.socket.recv( datasize )
		
		print "CLIENT SIDE"
		print "symkey = ", self.symkey 
		print "IV = ", ciphertext[:16]
		print "ciphertext = ", ciphertext[16:]
		
		plaintext = self.DecryptFileData( ciphertext )
		print "decrypted ciphertext = ",  plaintext
		
		self.writeFile( plaintext.rstrip() )	
		self.socket.close()
		
		
		
	def writeFile(self, datatoWrite ):
	
		file = open( os.path.join( self.disk, "test.txt" ), "wb" )
		
		file.write( datatoWrite )
		file.close()
		
if __name__ == '__main__':
	c = Client()
	c.getFile()
	
	