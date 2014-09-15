
import socket
import string
import sys

class Server():
	def __init__(self, ipaddr='0.0.0.0', port=50000):
		self.text = "oh hello"
		self.port = port
		self.ipaddress = ipaddr

	def getArgs(self):
		arglist = list(sys.argv ) 
		num = len(sys.argv)
		
		print arglist
		
		if num >= 1:
			self.filename = arglist[1]
		else:
			print 'need exactly one file as input'
			sys.exit(-1)
		
		print self.filename
	
	def listen(self):
		try:
			s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			s.bind( (self.ipaddress,self.port) )
			s.listen(5)
		except socket.error:
			if socket:
				socket.close()
			print 'error occurred while creating and binding socket'
			sys.exit(-1)
		
		while True:
			(cli,cliaddr) = s.accept()
			
			data = cli.recv()
			if data:
				print data
			
			cli.close()

	def openFile(self, filename ):
		pass
		
if __name__== '__main__':
	s = Server()
	
	s.getArgs()
	