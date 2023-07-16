import PulseDecoder
import time

decoder = PulseDecoder.PulseDecoder()

while True:
    
    decodedCode = decoder.getCode()
    
    if not decodedCode == None:
        print(decodedCode)