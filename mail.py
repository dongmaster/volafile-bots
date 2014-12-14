from volapi import Room
import time
import re

# Options
name = "MailBot"
room = "PHS-Nb"
password = "password"

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
do_not_send = False

def onmessage(msg):
	global messages
	global is_staff
	global do_not_send
	
	try:
		if re.search(name, msg.nick, re.I) == None:
			is_staff = myoc.get_user_stats(msg.nick)['staff']
	except Exception:
		print("Could not get info about user.")
	
	if msg.msg == "!mbkill" and is_staff == True and msg.nick.lower() == "dongmaster":
		myoc.post_chat("Goodbye, cruel world!")
		myoc.listen(onmessage = False)
		myoc.clear()
		myoc.close()
	
	if re.search(name, msg.nick, re.I) == None:
		splitmsg = msg.msg.split(' ', 2)
		
		if splitmsg[0] == "!w" or splitmsg[0] == "!whisper" or splitmsg[0] == "!m" or splitmsg[0] == "!mail" and len(splitmsg) == 3:
			reciever = splitmsg[1]
			sender = msg.nick
			message = splitmsg[2]
			
			
			messages[reciever.lower()] = {
				'reciever' : reciever,
				'sender' : sender,
				'message' : message
			}
			
			print("got message \n reciever: " + reciever + "\n sender: " + sender + "\n message: " + message)
			myoc.post_chat("Added to mail pool.")
			
			if msg.nick.lower() == sender.lower():
				do_not_send = True

	
	try:
		if do_not_send == False:
			dict = messages[msg.nick.lower()]
			dict_reciever = dict['reciever']
			dict_sender = dict['sender']
			dict_message = dict['message']

			#myoc.post_chat(str(dict_reciever) + ", " + str(dict_sender) + " sent you a message: " + str(dict_message))
			myoc.post_chat("From: " + str(dict_sender) + "\nTo: " + dict_reciever + " \n" + str(dict_message))
			del messages[msg.nick.lower()]
	except Exception:
		print("Failed to deliver mail.")
		
	do_not_send = False

myoc.listen(onmessage = onmessage)
