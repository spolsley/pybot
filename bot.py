import sys, string, re
import aiml
from time import time
from irc import irc

class bot():

	def __init__(self, host, port, nick, channels = [], chatlevel = 1):
		self.host = host
		self.port = port
		self.nick = nick
		self.channels = channels
		self.chatlevel = chatlevel
		self.AI = aiml.Kernel()
		self.IRC = irc(self.host,self.port,self.nick)
		self.listen = []
		self.prevsender = ""
		
	def connect(self):
		self.IRC.connect()
		self.IRC.simple_login()
		for channel in self.channels:
			self.IRC.join(channel)

	def learn(self, aimlset):
		self.AI.learn(aimlset)

	def set_predicates(self, filename):
		data = open(filename, "r")
		rows = (row.strip().split("=") for row in data)
		predicates = zip(*(row for row in rows if row))
		predicates[0] = map(lambda x: x.strip().lower(), predicates[0])
		for i in range(0, len(predicates[0])):
			self.AI.setBotPredicate(predicates[0][i],predicates[1][i])

	def determine_receiver(self, sender, receiver):
		if self.nick in receiver:
			return sender
		elif receiver in self.channels:
			return receiver

	def remove_nick(self, message):
		message = re.compile("([:,\-\(\s]*)(" + self.nick + ")([:,\-\)]*)", re.I).sub('',message)
		return message

	def split_response(self, response, limit):
		while response:
			yield response[:limit]
			response = response[limit:]
		
	def send_response(self, receiver, response):
		response = list(self.split_response(response, 400))
		for chunk in response:
			self.IRC.send(receiver,chunk)

	def handle_command(self, message):
		response = ""
		text = re.compile(self.nick + ":cmd",re.I).sub('',message[4])
		text = text.split('-')
		for command in text:
			command = command.split(' ')
			if len(command) > 0:
				if command[0] == "chatlevel":
					try:
						self.chatlevel = int(command[1])
					except:
						pass
					response = response + "My chatlevel is " + str(self.chatlevel) + ". "
				elif command[0] == "join":
					for i in range(1, len(command)):
						if command[i] not in self.channels:
							self.channels.append(command[i])
							response = response + "I am joining " + command[i] + ". "
							self.IRC.join(command[i])
						else:
							response = response + "I have already joined " + command[i] + ". "
				elif command[0] == "leave":
					for i in range(1, len(command)):
						if command[i] in self.channels:
							self.channels.remove(command[i])
							response = response + "I am leaving " + command[i] + ". "
							self.IRC.leave(command[i])
						else:
							response = response + "I'm not in " + command[i] + ". "
				elif command[0] == "channels":
					response = response + "I am currently in these channels: " + " ".join(self.channels) + ". "
				elif command[0] == "msg":
					self.send_response(command[1], " ".join(command[2:len(command)]))
					response = response + "I have sent the message. "
				elif command[0] == "listen":
					for i in range(1, len(command)):
						if command[i] not in self.listen:
							self.listen.append(command[i])
							response = response + "I am now listening to " + command[i] + ". "
						else:
							self.listen.remove(command[i])
							response = response + "I will not listen to " + command[i] + " as much. "
				elif command[0] == "listenlist":
					response = response + "I am listening to: " + " ".join(self.listen) + ". "
		if response == "":
			response = "I'm sorry but I don't understand your command. "
		return response

	def run(self):
		end_time = time() + 1
		while time() < end_time:
			buffer = self.IRC.get_data()
			print buffer
		
		while(True):
			buffer = self.IRC.get_data()
			print buffer
			msg = string.split(buffer)
			if msg[0] == "PING":
				self.IRC.ping_pong(msg[1])
				self.listen = []
			else:
				try:
					# Message = ["Sender name" "Sender host" "Action" "Receiver" "Text"]
					message = self.IRC.get_message(buffer)
					response = ""
					if self.nick == message[0]:
						pass
					else:
						sender = message[0]
						receiver = self.determine_receiver(sender, message[3])
						self.AI.respond("set name " + sender)
						if self.nick + ":cmd" in message[4]:
							response = self.handle_command(message)
							self.send_response(receiver, response)
						elif self.chatlevel < 1:
							pass
						elif self.nick in message[3]:
							response = self.AI.respond(self.remove_nick(message[4]))
							self.send_response(receiver, response)
						elif message[3] in self.channels:
							if self.chatlevel > 1:
								response = self.AI.respond(self.remove_nick(message[4]))
								self.send_response(receiver, response)
							elif self.nick in message[4]:
								if sender == self.prevsender:
									if sender not in self.listen:
										self.listen.append(sender)
								self.prevsender = sender
								response = self.AI.respond(self.remove_nick(message[4]))
								self.send_response(receiver, response)
							elif sender in self.listen:
								response = self.AI.respond(self.remove_nick(message[4]))
								self.send_response(receiver, response)
					print response
				except:
					pass
