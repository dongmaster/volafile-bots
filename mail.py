#!/usr/bin/python3

from volapi import Room
import time
import json
import re
import os

# Options for the chat bot
name = "MailBot"
room = "PHS-Nb"
password = "password"
commands = [
	"!w",
	"!m",
	"!mail"
]

# Options for the upload bot
name2 = "MailBot"
room2 = "PMqVdQ"

blacklist_recieve_mail = [
	"anon3000"
]

# Don't touch the code below unless you know what you are doing.
myoc = Room(room, name)
file_uploader = Room(room2, name2)



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
	^ Deprecated
	
	New:
	
	'dongmaster' : {
		'url'
	}
'''

messages = {
	
}

should_send = True
should_write = True
can_split = True
blacklisted_user = False

def onmessage(msg):
	global messages
	global should_send
	global should_write
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
		
		if splitmsg[0] in commands and len(splitmsg) >= 3 and can_split == True:
			if splitmsg[1].lower() in blacklist_recieve_mail:
				blacklisted_user = True
				myoc.post_chat("That is a blacklisted user. Sending mail to that person is not allowed.")
			
			if blacklisted_user == False:
				print("it's werking")
				reciever = splitmsg[1]
				sender = msg.nick
				message = splitmsg[2]
				
				try:
					reciever = reciever.replace("/", "")
					reciever = reciever.replace("\\", "")
					print("Safed the filename, i think")
				except Exception:
					should_write = False
					print("Couldn't safe filename. Probably a real error or false positive i dunno lol")
				
				
				if should_write == True:
					text_to_write = str("\n \n From: " + sender + "\n To: " + reciever + "\n Message: \n " + message)
					
					mail_file = open(reciever.casefold(), "ab")
					
					mail_file.write(bytes(text_to_write, 'UTF-8'))
					mail_file.close()
					
					''' Legacy code. This was used for printing out mail in the chat.
					messages[reciever.casefold()] = {
						'reciever' : reciever,
						'sender' : sender,
						'message' : message
					}
					'''
					
					file_uploader.upload_file(reciever.casefold())
					
					time.sleep(1)
					
					#print("got message \n reciever: " + reciever + "\n sender: " + sender + "\n message: " + message)
					myoc.post_chat("Added to mail pool.")
					
					messages[reciever.casefold()] = {
						'reciever' : reciever,
						'sender' : sender.casefold(),
						'url' : file_uploader.files[0].url
					}
					
					if msg.nick.casefold() == sender.casefold():
						should_send = False
						
					print(str(messages))
				elif should_write == False:
					myoc.post_chat("Invalid name.")
	''' Legacy code. This was used for printing out mail in the chat.
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
		
	'''

	try:
		if should_send == True:
			dict = messages[msg.nick.casefold()]
			dict_reciever = dict['reciever']
			dict_sender = dict['sender']
			dict_url = dict['url']
			dict_url = dict_url.split("/")
			dict_url = dict_url[4]
			
			myoc.post_chat("@" + str(dict_url))
	except Exception:
		print("Failed to deliver mail.")
		
		
	should_send = True
	should_write = True
	can_split = True
	blacklisted_user = False

myoc.listen(onmessage = onmessage)
