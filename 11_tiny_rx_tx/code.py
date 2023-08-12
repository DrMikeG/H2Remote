import PulseDecoder
import time
import board
import pwmio
import busio


AMBER = (255, 191, 0)
RED = (255, 0, 0)
RED_DIM = (100, 0, 0)
GREEN = (0, 255, 0)
GREEN_DIM = (0, 100, 0)
BLUE = (0, 0, 255)


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

def LED(RGB):
    r,g,b = RGB
    rduty = int(65535 -(65535 * r/255))
    gduty = int(65535 -(65535 * g/255))
    bduty = int(65535 -(65535 * b/255))
#    print(rduty)
#    print(gduty)
#    print(bduty)
    rpwm.duty_cycle = rduty
    gpwm.duty_cycle = gduty
    bpwm.duty_cycle = bduty

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


uart2 = busio.UART(board.GP4, board.GP5, baudrate=2400, bits=8, parity=None, stop=1)



print("Flusing UART")
# Flush UART buffer
while uart2.in_waiting > 0:
    _ = uart2.read(1)
print("Done flusing UART")

decoder = PulseDecoder.PulseDecoder(_IR_Pin=board.GP29)


print("Begin reading from UART 2")

LED(AMBER)

# Variable to store the last received time
last_received_time = time.monotonic()
stateKnown = False
stateIsRecording = False

print("Starting loop")
while True:

    # Handle any incoming data on serial 2
    while uart2.in_waiting > 0:
        LED(BLUE)
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
                LED(RED)
            else:
                LED(GREEN)

    # Nothing to read from serial 2 right now
    if not stateKnown:
        LED(AMBER)
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
                    LED(GREEN_DIM) # Wink to show you are doing something
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
                    LED(GREEN)
            elif color_value == 12: # Red Off button
                if stateIsRecording:
                    LED(RED_DIM)  # Wink to show you are doing something
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
                    LED(RED)
        else:
            print(decodedCode)
