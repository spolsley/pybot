from bot import bot

HOST = ""
PORT = 6667
NICK = "pybot"
CHANNELS = []
CHATLEVEL = 1

pybot = bot(HOST, PORT, NICK, CHANNELS, CHATLEVEL)
pybot.learn("aiml sets/Professor/*")
pybot.set_predicates("predicates.txt")

pybot.connect()
pybot.run()