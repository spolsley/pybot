import sys, socket, string, re

class irc(object):
	
	def __init__(self, host, port, name):
		self.host = host
		self.port = port
		self.name = name
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def send_data(self, data):
		self._sock.send(data + "\n")
		
	def connect(self):
		self._sock.connect((self.host,self.port))
		
	def join(self, channel):
		self.send_data("JOIN %s" % channel)
		
	def leave(self, channel):
		self.send_data("PART %s" % channel)
		
	def simple_login(self):
		self.login(self.name,self.host,None,self.name,self.host,self.name)
		
	def login(self, username, host, password, realname, server, nickname):
		self.send_data("USER %s %s %s %s" % (username, host, server, realname))
		self.send_data("NICK %s" % nickname)
		
	def ping_pong(self, response):
		self.send_data("PONG %s" % response)
		
	def get_data(self):
		return self._sock.recv(1024)
	
	def get_message(self, data):
		parsedData = re.split("(:)(.*)(!)([^:]*)(:)(.*)(\\r)",data)
		temp = parsedData
		temp = temp[4].split(" ")
		# Message in the format of ["Sender name" "Sender host" "Action" "Receiver" "Text"]
		message = [parsedData[2],temp[0],temp[1],temp[2],parsedData[6]]
		return message
		
	def send(self, target, data):
		self.send_data("PRIVMSG %s :%s" % (target, data))
		
	def quit(self):
		self.send_data("QUIT")
		self._sock.close()