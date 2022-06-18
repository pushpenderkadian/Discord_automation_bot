import os
import time

runner = 'y'
#  Starting the driver code 
while runner =='y':
    #taking the choice from user for different bot operations 
    choice = int(input('''
    1. Just Login into the discord (To login into your discord account)
    2. send message(To send messages through your discord account) 
    3. Log usernames(To scrape usernames from servers)
    4. Join Servers(To join different servers from your discord account fetched from invites.txt)
    5. General Chat(To send messages )
    6. Manage Filters
    7. Manage Skips
    8. Exit
    '''))
    #proceeding with the code according to the choice entered by user 
    if choice==1:

        os.system('python just_login.py')
    
    elif choice==2:
    
        os.system('python send_messages.py')
    
    elif choice==3:
    
        os.system('python log_usernames.py')    
    
    elif choice==4:
    
        os.system('python joinservers.py')    
    
    elif choice==5:
    
        os.system('python general_chat.py')    
    
    elif choice==6:
    
        os.system('python manage_filters.py')    
    
    elif choice==7:
    
        os.system('python manage_skip.py')    
    
    elif choice==8:
        break      

print("Thanks for using discord bot")
time.sleep(4)
exit()
    