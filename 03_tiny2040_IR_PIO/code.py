import PulseDecoder
import time
import board

decoder = PulseDecoder.PulseDecoder(_IR_Pin=board.GP29)
# The pin next to 3v is GP29
while True:
    
    decodedCode = decoder.getCode()
    
    if not decodedCode == None:
        print(decodedCode)