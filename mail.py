from volapi import Room
import time
import re

# Options
name = "MailBot"
room = "PHS-Nb"
password = "password"

blacklist = [
	"anon3000"
]

# Don't touch the code below.
myoc = Room(room, name)

try:
	myoc.user.login(password)
except Exception:
	print("Failed to login!")


'''
	Mail syntax:
	
	'dongmaster' : {
		'reciever' : "dongmaster",
		'sender' : "myon",
		'message' : "ur a faget"
	}
'''

messages = {
	
}

is_staff = False
should_send = True
can_split = True
blacklisted_user = False

def onmessage(msg):
	global messages
	global is_staff
	global should_send
	global can_split
	global blacklisted_user
	
	if msg.msg == "!mbkill" and msg.admin == True and msg.nick.casefold() == "dongmaster".casefold():
		myoc.post_chat("Goodbye, cruel world!")
		myoc.listen(onmessage = False)
		myoc.clear()
		myoc.close()
	
	if msg.nick.casefold() != name.casefold():
		try:
			splitmsg = msg.msg.split(' ', 2)
		except Exception:
			print("Could not split message, probably too short.")
			can_split = False
		
		#if splitmsg[0] == "!w" or splitmsg[0] == "!whisper" or splitmsg[0] == "!m" or splitmsg[0] == "!mail":
		if splitmsg[0] in ("!w", "!whisper", "!m", "!mail") and len(splitmsg) >= 3 and can_split == True:
			if splitmsg[1].lower() in blacklist:
				blacklisted_user = True
				myoc.post_chat("That is a blacklisted user. Sending mail to that person is not allowed.")
			
			if blacklisted_user == False:
				print("it's werking")
				reciever = splitmsg[1]
				sender = msg.nick
				message = splitmsg[2]
				
				
				messages[reciever.casefold()] = {
					'reciever' : reciever,
					'sender' : sender,
					'message' : message
				}
				
				print("got message \n reciever: " + reciever + "\n sender: " + sender + "\n message: " + message)
				myoc.post_chat("Added to mail pool.")
				
				if msg.nick.casefold() == sender.casefold():
					should_send = False
	
	try:
		if should_send == True:
			dict = messages[msg.nick.casefold()]
			dict_reciever = dict['reciever']
			dict_sender = dict['sender']
			dict_message = dict['message']

			#myoc.post_chat(str(dict_reciever) + ", " + str(dict_sender) + " sent you a message: " + str(dict_message))
			myoc.post_chat("From: " + str(dict_sender) + "\nTo: " + dict_reciever + " \n" + str(dict_message))
			del messages[msg.nick.casefold()]
	except Exception:
		print("Failed to deliver mail.")
		
	should_send = True
	can_split = True
	blacklisted_user = False

myoc.listen(onmessage = onmessage)
