#!/usr/bin/python

# used with the Raspberry PI as a "Zoom Remote"

print("ZOOM Remote control")

import time
import serial

# configure the serial port
def zconfig_serial():
    s = serial.Serial("/dev/ttyAMA0")
    s.baudrate = 2400
    return(s)

# show the serial port settings
def zshow_serial():
    print s
    print " "
    return


# handshake
# return true if connected, false if not
def zhandshake(s):
    # send 00, look for 80, then send A1, look for 80 then we are ready
    s.write('\x00')

    zbyte = s.read(1)
    if (zbyte == '\x80'): s.write('\xa1')
        
    zbyte = s.read(1)
    if (zbyte == '\x80'): return(1) 
    return(0)


# RELEASE the button
def zrelease():
    s.write('\x80\x00')
    time.sleep(.06)
    return

# press the RECORD button and unpress
def zrec():
    s.write('\x81\x00')
    zrelease()
    return

def zread_led():
    zled(s.read(1))
    return

def zled(bitval):
    # led function
    # Bits:
    # 01 rec
    # 02 mic red
    # 04 line 1 red
    # 08 line 2 red
    # 10 mic green
    # 20 line 1 green
    # 40 line 2 green
    if (chr(bitval) & chr(01)): rec="REC     "
    else: rec="        "

    if (bitval & '\x02'): micr="Mic     "
    else: micr="       "

    if (bitval & '\x04'): l1r="Line1   "
    else: l1r="        "

    if (bitval & '\x08'): l2r="Line2   "
    else: l2r="        "

    if (bitval & '\x10'): micg="Mic     "
    else: micg="       "

    if (bitval & '\x20'): l1g="Line1   "
    else: l1g="        "

    if (bitval & '\x40'): l2g="Line2   "
    else: l2g="        "

    print(rec, " ", micr, " ", l1r, " ", l2r, " ", micg, " ", l1g, " ", l2g)
    return


# snooze for t seconds
def zsleep(t):
    # add error offset for startup time
    t += .2
    time.sleep(t)
    return

########################################
# end functions
########################################

s = zconfig_serial()
