pybot
===
#### A Python-Based IRC Chat Bot

Pybot is a flexible, IRC chat bot written entirely in Python.  Pybot is intended to be as self-contained as possible, so all of the IRC connectivity is performed using Python's built-in '_socket' library.  For chatting capability, Cort Stratton's open-source PyAIML is used.  PyAIML is a Python-based interpreter for Artificial Intelligence Markup Language (AIML) sets.

Getting Started
---
Running pybot is very easy.  Assuming you have downloaded all of the source files:

### Quick Start
The easiest way to get started with pybot is to use the default AIML set and predicates list.  If you choose to do this, then you only need to open "pybot.py" and specify your IRC host as HOST.  You may also need to change the PORT number.  After setting the host, open Python and navigate to the pybot directory.  Type `import pybot` and that's it!

Pybot should start and connect to the provided IRC server.  You can chat privately with pybot, as well as issue commands.  See the Commands section for more details.

### Building a Custom Chat Bot
If you desire to create a more customized chat bot, follow the steps below.

#### 1. Get the desired AIML sets
This step is optional.  The Professor is included with pybot as the default set because it is released under the same license (MIT) as pybot.  However, if you wish to use another AIML set, just place any AIML sets you wish in the folder "aiml sets".  The Standard AIML set, A.L.I.C.E., Encyclopedia, Fake Captain Kirk, and the Professor are all freely available, along with many others.

#### 2. Set the predicates
This step is optional.  A default list of predicates is provided, but you may set whatever predicates you wish in the file "predicates.txt".  All of pybot's important data is read from here.  This includes characteristics of the chat bot, like name, location, age, gender, along with other bits of interest, like favorite sports teams and hobbies.  You can add any predicate you wish, but you must provide a value for it.  Note that not all AIML sets will use the same predicates.

#### 3. Specify IRC settings
This step is required.  To connect pybot to an IRC server, you must provide a valid IRC host.  In the file "pybot.py", set HOST to be your IRC host.  You may need to change the PORT number as well.  If you wish, you can add a list of channels for pybot to join upon connection.  For example, to have the chat bot join the channels "#botTalk" and "#chatbot" you would set CHANNELS to `CHANNELS = ["#botTalk", '#chatbot"]`.

#### 4. Learn new AIML sets
This step is only required if you wish to use another AIML set than the Professor.  Simply change the line `pybot.learn("aiml sets/Professor/*")` to `pybot.learn("aiml sets/<YOUR AIML SET HERE>/*")`.

You can have multiple learn directives if you wish to load several AIML sets.  Note that the most-recently learned set will "overwrite" previous patterns if they are the same pattern.  For example, if you load A.L.I.C.E., then the Professor, the chat bot will behave more like the Professor than A.L.I.C.E., although some of A.L.I.C.E.'s behavior will also be present.

#### 5. Run pybot
After setting all of the desired properties, open Python and navigate to the pybot source directory.  Type `import pybot` and pybot, or whatever name you have set for the chat bot, will connect to the IRC server you provided.

Commands
---
Pybot supports several basic commands to control IRC operations.  Commands are sent in the form of IRC messages with the prefix `<nick>:cmd` followed by the command or commands. Make sure that pybot is either present in the current channel, or message pybot directly, otherwise, there will be no response to your commands.  For the following examples, the chat bot's nickname is assumed to be 'pybot'.

#### -channels
###### Defintion:
List all currently-joined channels.

###### Usage:
`pybot:cmd -channels`

#### -chatlevel
###### Defintion:
Set or get the current chatlevel.  If a number is provided as the next argument, then the bot will attempt to set that number as the chatlevel.  Else, it will simply return the current chatlevel.  Valid chatlevels are:

- <1: Silence.  The bot will respond only to commands, no other conversation.
- 1: Standard.  The bot will chat freely in private messages and respond to channels when it's name is mentioned.  Furthermore, it can "listen" for conversations.  If the same user addresses the bot twice by name, it will begin to converse freely with that user.  After a period of silence, the bot will no longer listen to the user.
- >1: Free Talk.  The bot will respond to everyone, everywhere, at any time.

###### Usage:
Get current chatlevel: `pybot:cmd -chatlevel`

Set current chatlevel: `pybot:cmd -chatlevel #`

#### -join
###### Defintion:
Join the specified channels.  Any number of channels may be given as arguments.

###### Usage:
`pybot:cmd -join channel_1 channel_2 channel_3 ...`


#### -leave
###### Defintion:
Leave the specified channels.  The bot must be in a channel to leave it.

###### Usage:
`pybot:cmd -leave channel_1 channel_2 channel_3 ...`

#### -listen
###### Defintion:
Listen or un-listen the specified users.  A user will automatically become "listened" to when contacting the bot twice in a row by name.  When listening, the bot will talk freely with the user, whether mentioned by name or not.  After a period of silence, the user will no longer be listened to by the bot.  This command gives greater control over the automatic process.  It will toggle whether a user is being listened to or not.

###### Usage:
`pybot:cmd -listen user_1 user_2 user_3 ...`

#### -listening
###### Defintion:
Toggle whether the automatic "listen" mode is active.

###### Usage:
`pybot:cmd -listening`

#### -listenlist
###### Defintion:
List the current users being listened to by the bot.

###### Usage:
`pybot:cmd -listenlist`

#### -msg
###### Defintion:
Send the given message to the specified user.

###### Usage:
`pybot:cmd -msg receiver message`

#### -responsedelay
###### Defintion:
Regulates how quickly the bot will respond.  The delay is set in seconds and can be any positive decimal value.  Since the delay is used to control how frequently the bot checks the buffer, a shorter delay will cause higher memory and CPU usage.  Longer delays are useful if two bots are chatting to each other, as it will prevent rapidly flooding the channel.

###### Usage:
Get current responsedelay: `pybot:cmd -responsedelay`

Set current responsedelay: `pybot:cmd -responsedelay #`

#### -succinct
###### Defintion:
Toggles the bot's succinct conversation mode.  When active, the bot will only make single-sentence statements.  This option is primarily important if the bot is conversing with another bot, as it ensures that message length does not grow without bound.

###### Usage:
`pybot:cmd -succinct`

Licensing
---
Pybot is released under the MIT license, along with the included AIML set, the Professor.  PyAIML is released under the FreeBSD license.