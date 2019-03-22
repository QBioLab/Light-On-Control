import tkinter as tk
import sys
import os
import threading
import serial
import time

serial_port = 'COM8'
isSerialOpen = 0
SerialTryCounter = 0

##################################Hardware#################################
while( (not isSerialOpen) and SerialTryCounter <3):
    try:
        ser = serial.Serial(serial_port, 57600)
    except:
        print('Please check computer serial port')
        serial_port = input('Please type correct serial port: ')
    else:
        print(serial_port+' Open in host computer Succefully')
        print('Test LIGHT ON Board by Flash 3 times')
        for i in range(3):
            ser.write('&ALL_1000_S#'.encode())
            print('!!!')
            time.sleep(0.5)
            ser.write('&ALL_0000_S#'.encode())
            time.sleep(0.5)
        print('If no flase, please check line connection & board problem')
        isContinue = input('Is is correct(Y), or you want to retry(R) or quit(Q): ')
        if isContinue == 'Y':
            isSerialOpen = 1
        else:
            SerialTryCounter += 1

################################Setup GUI#################################
root = tk.Tk()
root.title(u"LIGHT ON Debug Table")

box = {}
label = {}
current = {}
cur_send = []
num = 0
while num < 24:
    key = '%s'%(num+1)
    label_value = tk.Label(text=u'LED %s'%key)
    label[num]  = label_value

    current_value = 'cur_led_%s'%(num+1)
    current[num]  = current_value
    current[num]  = tk.IntVar()
    current[num].set(10)
    cur_send.append(10)

    box_value   = tk.Spinbox(root, from_=0, to=9999, increment=10,
            textvariable=current[num])
    box[num]    = box_value 

    #label[num].grid()
    #box[num].grid()
    num += 1
for row_ in range(4):
    for column_ in range(6):
        label[19-6*row_ + column_-1].grid(row = 3*row_, column = column_)
        box[19-6*row_ + column_-1].grid(row = 3*row_+1, column = column_)

# send command to LIGHT ONN board
def send():
    command = '&SCH'+'_%04d'*24+'_S#'
    for i in range(24):
        cur_send[i] = current[i].get()
    sentence = command%(tuple(i for i in cur_send))
    print(sentence)
    ser.write(sentence.encode())

# set all value to same
def setall(intensity):
    for i in range(24):
        current[i].set(intensity)
    send()
    print("set")


confirm_but = tk.Button(text='update & send', command = send)
confirm_but.grid(row = 3*3+2, column = 5)

all_cur = tk.IntVar()
all_cur.set(10)

all_box = tk.Spinbox(root, from_=0,to=9999,increment=100,
        textvariable=all_cur)
all_but = tk.Button(text='set all', command = setall(all_cur.get()))
all_lab = tk.Label(text=u'All LED')
all_box.grid(row=3*3+2, column = 3)
all_lab.grid(row = 3*3+2, column = 2)
all_but.grid(row = 3*3+2, column = 4)

root.mainloop()


