
import socket 
import sys
import os
import Crypto.Util.Counter
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
		
	
	#received key from server, use it to decrypt file data
	def DecryptFileData(self, ciphertext  ):
		IV = ciphertext[:16]
		
		
		ctr = Crypto.Util.Counter.new(128, initial_value=long(IV.encode('hex'), 16))
		self.decobj = AES.new( self.symkey, AES.MODE_CTR, counter = ctr )
		
		self.plaintext = self.decobj.decrypt( ciphertext )
		
		print "uhh decrypted...?? : ",  base64.b64encode(self.plaintext) 
		
	
	def getFile(self):
		keysize = 32
		datasize = 4096
		request = "get me file"
		self.socket.connect( (self.address,self.port) )
		
		self.socket.sendall( request )
		
		self.symkey = self.socket.recv( keysize )
		ciphertext = self.socket.recv( datasize )
		
		print "CLIENT SIDE"
		print "symkey = ", base64.b64decode( self.symkey )
		print "IV = ", base64.b64decode(  ciphertext[:16] )
		print "ciphertext = ", base64.b64decode( ciphertext[16:] )
		
		self.DecryptFileData(ciphertext)

			
		self.socket.close()
		
		
		
	def writeFile(self):
	
		file = open( os.path.join( self.disk, "test.txt" ), "wb" )
		
		file.write( self.symkey )
		file.close()
		
if __name__ == '__main__':
	c = Client()
	
	c.getFile()
	c.writeFile()
	