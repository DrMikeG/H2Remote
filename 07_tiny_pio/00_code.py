# Tiny 2040 RBG LED control
# Original Micro Python code by Tony Goodhew 11th March 2021
# Ported to Circuit Python

import time
import board
import pwmio
import rp2pio
import adafruit_pioasm


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
#while True:
for _ in range(100):
    LED(0,0,255)
    time.sleep(0.3)
    LED(0,255,0)
    time.sleep(0.3)
    LED(255,0,0)
    time.sleep(0.3)
    
https://learn.adafruit.com/intro-to-rp2040-pio-with-circuitpython/using-pio-to-blink-a-led-quickly-or-slowly

# SPDX-FileCopyrightText: 2021 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Adapted from the example https://github.com/raspberrypi/pico-examples/tree/master/pio/pio_blink


blink = adafruit_pioasm.assemble(
    """
.program blink
    pull block    ; These two instructions take the blink duration
    out y, 32     ; and store it in y
forever:
    mov x, y
    set pins, 1   ; Turn LED on
lp1:
    jmp x-- lp1   ; Delay for (x + 1) cycles, x is a 32 bit number
    mov x, y
    set pins, 0   ; Turn LED off
lp2:
    jmp x-- lp2   ; Delay for the same number of cycles again
    jmp forever   ; Blink forever!
"""
)


while True:
    for freq in [5, 8, 30]:
        with rp2pio.StateMachine(
            blink,
            frequency=125_000_000,
            first_set_pin=board.LED,
            wait_for_txstall=False,
        ) as sm:
            data = array.array("I", [sm.frequency // freq])
            sm.write(data)
            time.sleep(3)
        time.sleep(0.5)
