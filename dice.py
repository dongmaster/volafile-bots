from volapi import Room
import time
import re
import random
import datetime

# Options
room_id = "BEEPi"
name = "DiceBot"
password = "password"

slow_mode = False
slow_limit = 5
slow_timer = 45

brb_message = ""
brb_message_real = "Killing myself. You can't !roll anymore. I will be back in: " + str(slow_timer) + " seconds"
return_message = "I have risen from the grave."

# Don't touch the stuff below.
myoc = Room(room_id, name)

time.sleep(2)
myoc.userLogin(password)
time.sleep(2)



print(name + ": Activated")
print("Room: " + room_id)
print("brb message: " + brb_message_real)
print("Return message: " + "I have risen from the grave.")

if slow_mode == True:
	slow_mode_string = "Enabled"
	slow_limit_string = str(slow_limit)
elif slow_mode == False:
	slow_mode_string = "Disabled"
	slow_limit_string = "Unlimited"
	
intro_message = "Hi! I'm DiceBot. Type !roll or !r to get a number between 1 and 6 (inclusive). Alternative syntax: !roll 4 10 or !roll 100. Letters not allowed. Slow mode: " + slow_mode_string + ". Message limit: " + slow_limit_string

myoc.postChat(intro_message)

chat = myoc.getChatLog()
length = 0
counter = 0
slow_counter = 0
allow_roll = True
slept = False

has_posted = False

brb = brb_message

#second = 

while(True):
	if counter >= 13:
		# Reconnects the bot when it reaches the message limit. (It's around 13 messages I think).
		myoc = Room(room_id, name)
		myoc.userLogin(password)
		counter = 0
		time.sleep(0.5)
	
	while length < len(chat):
		last_message = chat[len(chat) - 1].msg
		last_person = chat[len(chat) - 1].nick
		
		# Users named dicebot can't use dicebot. Users with "merc" in their name can't use dicebot.
		# It is like this to filter out the cancer :^)
		if re.search(name, last_person, re.I) == None and re.search("merc", last_person, re.I) == None:
			if last_message == "!roll" or last_message == "!r":
				if slow_counter >= slow_limit and slow_mode == True:
					# enterprise quality code.
					# This is part of the "Slow mode" shit I wrote
					# It just sleeps for slow_timer amount of seconds
					# brb is the Be Right Back message
					myoc.postChat(str(random.randrange(1, 7)) + brb)
					brb_message = brb_message_real
					brb = brb_message
					myoc.postChat(brb)
					
					time.sleep(slow_timer)
					slow_counter = -1
					slept = True
					myoc.postChat(return_message)
					
					# I put the bot to sleep to make it not respond to !rolls after it has killed itself
					time.sleep(0.2) 
					brb_message = ""
					brb = brb_message
					
				if slow_mode == True:
					slow_counter += 1
					
				if slept == False:
					# Can't remember why it's like this but it's for a good reason or someshit
					myoc.postChat(str(random.randrange(1, 7)) + brb)
					time.sleep(0.1)
					
				slept = False
				counter += 1
				
			elif re.search("!roll *", last_message) or re.search("!r *", last_message):
				numbers = last_message.split()
				if len(numbers) == 3:
					not_number = False
					
					try:
						# Check if it's a number
						int(numbers[1])
						int(numbers[2])
					except ValueError:
						not_number = True
					
					if not_number == False and int(numbers[1]) < int(numbers[2]):
						if slow_counter >= slow_limit and slow_mode == True:
							myoc.postChat(str(random.randrange(int(numbers[1]), int(numbers[2]) + 1)) + brb)
							brb_message = brb_message_real
							brb = brb_message
							myoc.postChat(brb)
							
							time.sleep(slow_timer)
							slow_counter = -1
							slept = True
							myoc.postChat(return_message)
							time.sleep(0.2) #I put the bot to sleep to make it not respond to !rolls after it has killed itself
							brb_message = ""
							brb = brb_message
						
						if slow_mode == True:
							slow_counter += 1
							
						if slept == False:
							myoc.postChat(str(random.randrange(int(numbers[1]), int(numbers[2]) + 1)) + brb)
							time.sleep(0.1)
						
						slept = False
						counter += 1
							
					else:
						myoc.postChat("Invalid roll.")
						
				if len(numbers) == 2:
					not_number = False
					
					try:
						int(numbers[1])
					except ValueError:
						not_number = True
					
					if not_number == False and int(numbers[1]) > 0:
						if slow_counter >= slow_limit and slow_mode == True:
							myoc.postChat(str(random.randrange(1, int(numbers[1]) + 1)) + brb)
							brb_message = brb_message_real
							brb = brb_message
							myoc.postChat(brb)
							
							time.sleep(slow_timer)
							slow_counter = -1
							slept = True
							myoc.postChat(return_message)
							time.sleep(0.2) #I put the bot to sleep to make it not respond to !rolls after it has killed itself
							brb_message = ""
							brb = brb_message
						
						if slow_mode == True:
							slow_counter += 1
							
						if slept == False:
							myoc.postChat(str(random.randrange(1, int(numbers[1]) + 1)) + brb)
							time.sleep(0.1)
						
						slept = False
						counter += 1
							
					else:
						myoc.postChat("Invalid roll.")
		counter += 1
		length += 1