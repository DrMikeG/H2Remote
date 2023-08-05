#https://learn.adafruit.com/adafruit-feather-rp2040-pico/built-in-neopixel-led

# Added \libs\adafruit_pixelbuf.mpy
# Added \libs\neopixel.mpy

# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython status NeoPixel red, green, blue example."""
import time
import board
import neopixel
import PulseDecoder

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

decoder = PulseDecoder.PulseDecoder(_IR_Pin=board.A0)

pixel.brightness = 0.0

while True:
    decodedCode = decoder.getCode()
    
    if not decodedCode == None:
        print(decodedCode)
        if isinstance(decodedCode, str) and len(decodedCode) == 32:
            # Skip the first 16 bits and extract the next 5 bits
            five_bit_substring = decodedCode[16:21]
            # Convert the 5-bit substring to an integer
            color_value = int(five_bit_substring, 2)
            # Print the result
            print("Color value as an integer:", color_value)
            if color_value == 18:
                pixel.brightness = 0.3
                pixel.fill((255, 0, 0))
            elif color_value == 2:
                pixel.brightness = 0.3
                pixel.fill((0, 255, 0))
            elif color_value == 10:
                pixel.brightness = 0.3
                pixel.fill((0, 0, 255))
            elif color_value == 26:
                pixel.brightness = 0.3
                pixel.fill((255, 255, 255))                
            elif color_value == 28:
                print("On")
                pixel.brightness = 0.5
                pixel.fill((255, 255, 255))                                
            elif color_value == 12:
                print("Off")
                pixel.brightness = 0.0
            else:
                pixel.brightness = 0.0