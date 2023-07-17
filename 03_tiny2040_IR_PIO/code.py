import PulseDecoder
import time
import board

decoder = PulseDecoder.PulseDecoder(_IR_Pin=board.GP7)

while True:
    
    decodedCode = decoder.getCode()
    
    if not decodedCode == None:
        print(decodedCode)