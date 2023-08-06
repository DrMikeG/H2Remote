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
import digitalio
import busio

AMBER = (255, 191, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

NEO_WINK = 0.05
NEO_FULL = 0.2

def print_byte(p, b):
    print("RX{}: {:8}\t0x{:x}\t{}".format(p, int(time.monotonic() * 1000), b, b))

def interpret_byte(byte):
    # Bit 7 - Handshake phase (1 for handshake, 0 for acknowledged)
    handshake_phase = bool(byte & 0b10000000)
    # Bit 0 - Recording in progress (alternates 0 and 1 when recording paused)
    recording_in_progress = bool(byte & 0b00000001)
    # Print the decoded properties
    print("Handshake phase:{} Recording in progress:{}".format(handshake_phase,recording_in_progress))

def needsHandshake(byte):
    handshake_phase = bool(byte & 0b10000000)
    return handshake_phase

def isRecording(byte):
    # Bit 7 - Handshake phase (1 for handshake, 0 for acknowledged)
    handshake_phase = bool(byte & 0b10000000)
    # Bit 0 - Recording in progress (alternates 0 and 1 when recording paused)
    recording_in_progress = bool(byte & 0b00000001)
    # Print the decoded properties
    return not handshake_phase and recording_in_progress


uart2 = busio.UART(board.D24, board.D25, baudrate=2400, bits=8, parity=None, stop=1)

print("Flusing UART")
# Flush UART buffer
while uart2.in_waiting > 0:
    _ = uart2.read(1)
print("Done flusing UART")

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

decoder = PulseDecoder.PulseDecoder(_IR_Pin=board.A0)

# Specify the pin you want to control (e.g., board.D13)
gpio_pin = board.D10
# Configure the pin as an output
pin = digitalio.DigitalInOut(gpio_pin)
pin.direction = digitalio.Direction.OUTPUT
# Pull the pin low (set it to logic level 0)
pin.value = False

pixel.brightness = NEO_FULL

print("Begin reading from UART 2")

pixel.fill(AMBER)

# Variable to store the last received time
last_received_time = time.monotonic()
stateKnown = False
stateIsRecording = False

print("Starting loop")
while True:

    # Handle any incoming data on serial 2
    while uart2.in_waiting > 0:
        pixel.fill(BLUE)
        incoming_byte2 = uart2.read(1)[0]
         # Update the last received time
        print_byte(2, incoming_byte2)
        interpret_byte(incoming_byte2)
        if not needsHandshake(incoming_byte2):
            # This useful status  data
            stateIsRecording = isRecording(incoming_byte2)
            print("Updated status. Record={}".format(stateIsRecording))
            last_received_time = time.monotonic()
            stateKnown = True
            if stateIsRecording:
                pixel.fill(RED)
            else:
                pixel.fill(GREEN)

    # Nothing to read from serial 2 right now
    if not stateKnown:
        pixel.fill(AMBER)
        if time.monotonic() - last_received_time >= 5.0:
            print("No status data received for 5 seconds. Performing handshake.")
            # This code elicits a response
            uart2.write(b'\x80')
            time.sleep(0.01)
            uart2.write(b'\x00')
            time.sleep(0.01)
            uart2.write(b'\xA1')
            time.sleep(0.01)
            uart2.write(b'\x00')
            time.sleep(0.25)
            last_received_time = time.monotonic()

    decodedCode = decoder.getCode()
    if not decodedCode == None:
        if isinstance(decodedCode, str) and len(decodedCode) == 32:
            # Skip the first 16 bits and extract the next 5 bits
            five_bit_substring = decodedCode[16:21]
            # Convert the 5-bit substring to an integer
            color_value = int(five_bit_substring, 2)
            # Print the result
            print("Color value as an integer:", color_value)
            if color_value == 28: # Green On button
                
                if not stateIsRecording:
                    pixel.brightness = NEO_WINK # Wink to show you are doing something
                    # Let's try start recording?
                    print("Send start recording")
                    uart2.write(b'\x81')
                    time.sleep(0.1)  # 100ms delay
                    uart2.write(b'\x00')
                    time.sleep(0.1)  # 100ms delay
                    uart2.write(b'\x80')
                    time.sleep(0.1)  # 100ms delay
                    uart2.write(b'\x00')
                    time.sleep(0.25)
                    print("Done sending start recording")
                    pixel.brightness = NEO_FULL
            elif color_value == 12: # Red Off button
                if stateIsRecording:
                    pixel.brightness = NEO_WINK  # Wink to show you are doing something
                    print("Send stop recording")
                    # Let's try stop recording?
                    uart2.write(b'\x81')
                    time.sleep(0.1)  # 100ms delay
                    uart2.write(b'\x00')
                    time.sleep(0.1)  # 100ms delay
                    uart2.write(b'\x80')
                    time.sleep(0.1)  # 100ms delay
                    uart2.write(b'\x00')
                    time.sleep(0.25)
                    print("Done sending stop recording")
                    pixel.brightness = NEO_FULL
        else:
            print(decodedCode)
