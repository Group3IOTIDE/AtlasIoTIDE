# AtlasIoTIDE

This is a group project of CNT5517 Mobile Computing which is done by Group 3, which implements an Atlas IoT application IDE.

Before open and run this code, you need to do below preparation:

## 1. Use Python3 and install packages 

> $ pip install pandas
  
> $ pip install pillow

## 2. Install Atlas framework on your RPi
> See https://github.com/AtlasFramework/IoT-DDL

## 3. Keep your things and devices running IDE in the same LAN (or VSS)
It means your RPI should Share the same prefix, ex: 10.254.0.x


## 4. Set multicast ip on your RPi

> $ sudo ip route add 232.0.0.0/8 dev tap0


To use the IDE, run the code from main.py
