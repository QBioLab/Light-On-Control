'''
Light on control code
| Version | Commit
| 1.0     | xiaojs
| 2.0beta | real time control, friendly-use, log record@hf
'''

import serial
import time
import os
import sys

from tkinter import filedialog
from tkinter import *

################################Parameters Handler###################################
## Hardware and log control paramters
csv_file = ''
serial_port = 'COM8'
ser = ''
total_line = 0
isRespone = 0
isCSVCounter = 0
config_file = ''
log_time = time.strftime("%Y%m%d-%H%M", time.localtime())
log_file = open('light-on-ctrl'+log_time+'.log', 'w+')
log_file.write('# Here are log of LIGHT ON experiment\n')

serial_port = '/dev/ttyUSB1'
try:
    config_file = open('light-on-ctrl.config', 'r+')
except IOError:
    config_file = open('light-on-ctrl.config', 'w') 
    config_file.write('# Here are hardware configure, please use # to commit\n')
    config_file.write('# Only choose the first one config\n')

else:
    config_line = config_file.readline()
    while(not config_line == ''):
        if(not config_line[0] == '#'):
            serial_port = config_line[0:-1] # only choose first one and remove '\n'
            break
            # Todo: add other case
        config_line = config_file.readline()

confirm = 'C'
while( not (confirm == 'Y')):
    if confirm == 'S':
        print(serial_port)
        try:
            ser = serial.Serial(serial_port, 57600)
        except:
            print('Please check computer serial port')
            serial_port = input('Please type correct serial port: ')
        else:
            print('COM8 Open in host computer Succefully')
            config_file.write(serial_port+'\n')
            print('Test LIGHT ON Board by Flash 3 times')
            isRespone = 0
            for i in range(3):
                isRespone = ser.write('&ALL_1000_S#'.encode())
                print('!!!')
                time.sleep(0.5)
                isRespone = ser.write('&ALL_0000_S#'.encode())
                time.sleep(0.5)
            # Todo: add no response handling
            print('If no flase, please check line connection & board problem')
            print('Program will continue')
            confirm = 'Y'
            '''
            if isRespone > 0:
                print('Fail to pass command to board, please check line connection')
                isContinue = input('Do you want to contiue without'+
                        'serial connenction or retry (Y/Q/R): ')
                if isContinue == 'Y':
                    confirm = 'Y'
                elif isContinue == 'R':
                    confirm = 'S'
                else:
                    confirm = 'Q'
            '''
    elif confirm == 'C':
        root = Tk()
        root.withdraw()
        root.csv_file =  filedialog.askopenfilename(
            title = "Select file",
            filetypes = (("csv files","*.csv"),("all files","*.*")))
        csv_file = root.csv_file
        try:
            csv_file_test = open (csv_file, 'r')
        except IOError:
            print('Error CSV file pathway')
            confirm = 'C'
            isCSVCounter = isCSVCounter + 1
            if isCSVCounter > 3:
                print('Error CSV file more than 3 times')
                confirm = 'Q'
        else: 
            total_line = len(csv_file_test.readlines())
            #Todo: row number error handling
            print('load CSV succefully:'+csv_file)
            confirm = 'S'
    elif confirm == 'Q':
        print('Exit programm now...')
        sys.exit()




#ser.write('&SCH_0300_0300_0900_1200_1500_1800_2100_2400_2700_3000_3300_3600_0000_0600_0900_1200_1500_1800_2100_2400_2700_3000_3300_3600_S#'.encode())

#######################################LIGHT ON#######################################
## LIGHT ON control paramter
data = open(csv_file, "r")
interval = 60 #second
count = 0 
temp = 1
command = '&SCH'+'_%s'*24+'_S#'

print('\n------------------Parameters--------------------------')
print('  COM: ' + serial_port )
log_file.write('COM: ' + serial_port +'\n')
print('  CSV: ' + csv_file)
log_file.write('  CSV: ' + csv_file + '\n')
print('  Interval:', interval,'s')
log_file.write('Interval: %d'%interval+'s'+'\n')
total_time = total_line*interval/3600
print('  Total Time:', total_time, 'hrs')
log_file.write('Total Time: %d'%total_time + 'hrs')
print('------------------------------------------------------\n')

confirm = input('Is Everything Correct? Type Y to start or type Q to restart\n(Y/N): ')
if not confirm == 'Y':
    sys.exit()

print('LIHGT ON!')
log_file.write('LIHGT ON begin in %s'%(time.strftime("%Y%m%d-%H", time.localtime())))

## LIGHT ON control flow handler
start_time = time.time()
last_time = start_time
line = data.readline()
line = line.strip()
sentence = command%(tuple([i.zfill(4) for i in line.split(",")]))
print(tuple([i.zfill(4) for i in line.split(",")]))
isread = 0
while(True):
    ser.write(sentence.encode())
    last_time = time.time()
    count += 1
    isread = 0
    while(time.time()- last_time < interval):
        if(isread == 0):
            line = data.readline()
            if line == '':
                sys.exit()
            else:
                isread = 1
                line = line.strip()
                sentence = command%(tuple([i.zfill(4) for i in line.split(",")]))
                print(tuple([i.zfill(4) for i in line.split(",")]))
                if count*interval/60%10== 0:
                    print(count*interval/3600, 'hrs in', total_time, 'hrs')

log_file.write('LIGHT ON stop at %s'%(time.strftime("%Y%m%d-%H", time.localtime())))
data.close()
config_file.close()
log_file.close()

