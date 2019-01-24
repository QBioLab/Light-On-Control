'''
Light on control code
| Version | Commit
| 1.0     | xiaojs
| 2.0     | real time control, friendly-use, log record@hf
| 2.1     | optimal user control interface, fix serial_port config saving bug
          | store log file in direction, add time interval setting up
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
interval = 60 # 60s
csvfile = ''
total_line = 0
isRespone = 0
isSerialCounter = 0
isCSVCounter = 0
config_file = ''
log_dirs = 'light-on-ctrl-log'

    
log_time = time.strftime("%Y%m%d-%H%M", time.localtime())
try:
    log_file = open(log_dirs+'/'+'light-on-ctrl'+log_time+'.log', 'w+')
except:
    os.mkdir(log_dirs)
    log_file = open(log_dirs+'/'+'light-on-ctrl'+log_time+'.log', 'w+')
log_file.write('# Here are log of LIGHT ON experiment\n')

################################Load Serial from File#################################
serial_port = '/dev/ttyUSB0'
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

###############################LIGHTON Function########################################
## LIGHT ON control flow handler
def lighton(interval_, csv_file, isTest):
    data = open(csv_file, "r")
    #interval = 60 #second
    command = '&SCH'+'_%s'*24+'_S#'
    count = 0
    test_duration = 60 #min
    print('\n--------------------Parameters--------------------------')
    print('  COM: ' + serial_port )
    log_file.write('COM: ' + serial_port +'\n')
    print('  CSV: ' + csv_file)
    log_file.write('  CSV: ' + csv_file + '\n')
    print('  Interval:', interval_,'s')
    log_file.write('Interval: %d'%interval+'s'+'\n')
    total_time = total_line*interval_/3600
    print('  Total Time:', total_time, 'hrs')
    log_file.write('Total Time: %d'%total_time + 'hrs')
    if isTest:
        print("  During test model, only flash  5s every time in 2min")
        interval_ = 5
    print('--------------------------------------------------------\n')

    log_file.write('LIHGT ON begin in %s'%(time.strftime("%Y%m%d-%H", time.localtime())))
    start_time = time.time()
    last_time = start_time
    line = data.readline()
    line = line.strip()
    sentence = command%(tuple([i.zfill(4) for i in line.split(",")]))
    print(tuple([i.zfill(4) for i in line.split(",")]))
    isread = 0
    isCountinue = 1
    while( isCountinue ):
        ser.write(sentence.encode())
        last_time = time.time()
        count += 1
        isread = 0
        while(time.time()- last_time < interval_):
            if(isread == 0):
                if isTest and (time.time()-start_time > 2*60 ):
                    isCountinue = 0
                    break
                line = data.readline()
                if line == '':
                    sys.exit()
                else:
                    isread = 1
                    line = line.strip()
                    sentence = command%(tuple([i.zfill(4) for i in line.split(",")]))
                    print(tuple([i.zfill(4) for i in line.split(",")]))
                    if count*interval_/60%10== 0:
                        print(count*interval_/3600, 'hrs in', total_time, 'hrs')
                    if isTest:
                        print((count-1)*interval_, 's in 2min')
    data.close()


################################User Interface#############################################
confirm = 'S'
while( True ):
    if confirm == 'S':  # Configure Serial port
        print(serial_port)
        try:
            ser = serial.Serial(serial_port, 57600)
        except:
            print('Please check computer serial port')
            serial_port = input('Please type correct serial port: ')
            isSerialCounter = isSerialCounter + 1
            confirm = 'S'
        else:
            print(serial_port+' Open in host computer Succefully')
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
            print('If no flase, please check cable connection & board problem')
            isContinue = input('Is is correct(Y), or you want to retry(R) or quit(Q): ')
            if isContinue == 'Y':
                confirm = 'C'
            elif isContinue == 'R':
                confirm = 'S'
            else:
                confirm = 'Q'
    elif confirm == 'C': # Choose CSV file
        root = Tk()
        root.withdraw()
        root.csv_file =  filedialog.askopenfilename(
            title = "Please Select CSV file",
            filetypes = (("csv files","*.csv"),("all files","*.*")))
        csv_file = root.csv_file
        try:
            csv_file_test = open (csv_file, 'r')
        except IOError:
            print('Error CSV file pathway')
            confirm = 'C' #
        else: 
            total_line = len(csv_file_test.readlines())
            #Todo: row number error handling
            print('load CSV succefully:' + csv_file)
            
            confirm = 'I'
    elif confirm == 'I':
        interval_temp = int(input('Please enter interval(1s~120s): '))
        if interval_temp < 1:
            interval = 1
        elif interval_temp > 120:
            interval = 120
        else:
            interval = interval_temp
        confirm = ''

    elif confirm == 'T': # Test model
        isTest = 1
        lighton(interval, csv_file, isTest)
        confirm = ''
    elif confirm == 'Y':  # Enter real light on experiment
        isTest = 0
        lighton(interval, csv_file, isTest)
        break
    elif confirm == 'AO':  # Open all LED
        ser.write('&ALL_1000_S#'.encode())
        confirm = ''
    elif confirm == 'AC':  # Close all LED
        ser.write('&ALL_0000_S#'.encode())
        confirm =''
    elif confirm == 'Q': # End programe
        print('Exit programm now...')
        sys.exit()
    else:
        confirm = input('\nIs Everything Correct?\n'+
            'Type Y(es) to start'+
            '; T(est) to test CSV sequence; C(SV) to rechoose CSV file;\n'+
            'AC(all close) to all LED; AO(all open) to open all LED to 1000\n'+
            'type Q to restart\n(Y/T/C/Q/AC/AO): ')


#ser.write('&SCH_0300_0300_0900_1200_1500_1800_2100_2400_2700_3000_3300_3600_0000_0600_0900_1200_1500_1800_2100_2400_2700_3000_3300_3600_S#'.encode())



log_file.write('LIGHT ON stop at %s'%(time.strftime("%Y%m%d-%H", time.localtime())))
data.close()
config_file.close()
log_file.close()

