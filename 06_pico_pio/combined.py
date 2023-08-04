import PulseDecoder
import time
import board
import rp2pio
import adafruit_pioasm

decoder = PulseDecoder.PulseDecoder(_IR_Pin=board.GP7)

hello = """
.program hello
loop:
    pull
    out pins, 1    
; This program uses a 'jmp' at the end to follow the example.  However,
; in a many cases (including this one!) there is no jmp needed at the end
; and the default "wrap" behavior will automatically return to the "pull"
; instruction at the beginning.
    jmp loop
"""

led_quarter_brightness = adafruit_pioasm.assemble(
"""
    pull
    out pins, 1    
    out pins, 0 [2]
    out pins, 1
"""
)
assembled = adafruit_pioasm.assemble(hello)

sm = rp2pio.StateMachine(
    led_quarter_brightness,
    frequency=2000,
    first_out_pin=board.GP15,
)
print("real frequency", sm.frequency)

while True:
    
    decodedCode = decoder.getCode()
    
    if not decodedCode == None:
        print(decodedCode)
        sm.write(bytes((1,)))
    #else:
        #sm.write(bytes((0,)))