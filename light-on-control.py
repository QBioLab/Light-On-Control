
__author__ = 'xiaojs'
import serial
import time
import os
import sys
import argparse
ser = serial.Serial('COM8', 57600)


ser.write('&ALL_0000_S#'.encode())  
ser.write('&ALL_0000_S#'.encode())

ser.write('&SCH_0300_0300_0900_1200_1500_1800_2100_2400_2700_3000_3300_3600_0000_0600_0900_1200_1500_1800_2100_2400_2700_3000_3300_3600_S#'.encode())

ser.write('&ALL_1000_S#'.encode())
#data = open("C:\Users\qblab\Desktop\lightnoise\chenyantest.csv", "r")
#data = open("Y:\chenyan\chenyan20181118.csv", 'r')
data = open("G:\chenyan\six_led\config\mW100mA20190123-2d#.csv", 'r')
interval = 60 #second
count = 0 
temp =1
command = '&SCH'+'_%s'*24+'_S#'
for line in data:
    count += 1
    #f count%temp == 0:
    #print("min:",count*interval/60)
    line = line.strip()
    #print line
    #print command
    #sentence = command % (tuple([i.zfill(4) for i in line.split(",")]))
    print(tuple([i.zfill(4) for i in line.split(",")]))
    sentence = command%(tuple([i.zfill(4) for i in line.split(",")]))
    ser.write(sentence.encode())
    time.sleep(interval)
