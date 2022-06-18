# Discord_automation_bot
This bot is used to send mass DMs to people in servers shared with the used accounts.
The settings for the various functions can be found in the data folder, inside the project folder.
one by one, they are:
- accounts.txt
	Place each account in a separate line, like so:
	email token proxy

- messages.txt
	Just place the message you want to send.

- exclusive_filter.pkl
	exclusive filter file, please do not edit.

- inclusive_filter.pkl
	inclusive filter file, please do not edit.

- invites.txt
	Place the server invites you want the accounts to join, each in a separate line. The discorddesktop app is known to interfere.

- channels.txt
	Place the URLs of the general chats you want to message.

- skip.pkl
	Skip file, please do not edit.

That's all for the txt files. Now, for the other ones:

- general_chat.py
	Run this to message a general chat periodically, from the ones in channels.txt

- joinservers.py
	Run this to join the servers in invites.txt.If you have the desktop app installed,
	you can probably disable it opening links via windows' settings.

- log_usernames.py
	Run this to log users and their roles. This works with method 1, that I'll explain
	shortly. You also need to log users to be able to edit your filters

- manage_time.py
	Upon running this file, you'll be asked a simple question. How much should the bot wait? note, the bot won't always
	wait the specified amount, but rather a proportion of it, depending on what step of the execution it is in.

- manage_skip.py
	Interactive script to add, clear, or see the skip list.

- manage_filters.py
	Interactive script to edit your filters, self explanatory. You'll need to log users to see their roles.
	
- send_messages.py
	This script does the actual goal. Here you'll be asked 3 question before execution
	begins.
	1) Select which servers to message. You can leave this blank to target all
	of them
	2) Exclusive or Inclusive filter: Type E for exclusive and I for inclusive
	3) Method:
		method 1: Messaged logged users. You'll need to run log_usernames.py
		
		first. The log files can be found at the folder target
		
		method 2: Message users through the member list in each server.
		
		You don't need logged usernames to run this.

just run the python file simply after installing requirements from requirement.txt file
