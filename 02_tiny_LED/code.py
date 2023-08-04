# Tiny 2040 RBG LED control
# Original Micro Python code by Tony Goodhew 11th March 2021
# Ported to Circuit Python

import time
import board
import pwmio

#Setup RGB LED
# Construct PWM objects with RGB LED
rpwm = pwmio.PWMOut(board.LED_R, frequency=1000) # RED GP18
gpwm = pwmio.PWMOut(board.LED_G, frequency=1000) # GREEN GP19
bpwm = pwmio.PWMOut(board.LED_B, frequency=1000) # BLUE GP20

# Turn off
rduty = 65535
gduty = 65535
bduty = 65535
rpwm.duty_cycle = rduty
gpwm.duty_cycle = gduty
bpwm.duty_cycle = bduty

def LED(r,g,b):
    rduty = int(65535 -(65535 * r/255))
    gduty = int(65535 -(65535 * g/255))
    bduty = int(65535 -(65535 * b/255))
#    print(rduty)
#    print(gduty)
#    print(bduty)
    rpwm.duty_cycle = rduty
    gpwm.duty_cycle = gduty
    bpwm.duty_cycle = bduty

LED(255,255,255)
time.sleep(0.3)
LED(255,0,0)
time.sleep(0.3)

# Blink
while True:
    LED(0,0,255)
    time.sleep(0.3)
    LED(0,255,0)
    time.sleep(0.3)
    LED(255,0,0)
    time.sleep(0.3)
    
