import PulseDecoder
import time
import board
import busio

# PIO
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


assembled = adafruit_pioasm.assemble(hello)
sm = rp2pio.StateMachine(
    assembled,
    frequency=2000,
    first_out_pin=board.LED,
)
print("real frequency", sm.frequency)

# Use a timeout of zero so we don't delay while waiting for a message.
#uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
uart = busio.UART(board.GP4, board.GP5, baudrate=2400, timeout=0)


while True:

    byte_read = uart.read(1)  # Read one byte over UART lines
    if byte_read:         # Nothing read.
       print(byte_read)

    decodedCode = decoder.getCode()

    if not decodedCode == None:
        print(decodedCode)
