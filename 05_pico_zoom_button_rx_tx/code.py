import time
import board
import digitalio
import busio

# Initialize the serial ports
uart2 = busio.UART(board.GP4, board.GP5, baudrate=2400, bits=8, parity=None, stop=1)

uart3 = busio.UART(board.GP12, board.GP13, baudrate=2400, bits=8, parity=None, stop=1)

def print_byte(p, b):
    print("RX{}: {:8}\t0x{:x}\t{}".format(p, int(time.monotonic() * 1000), b, b))

def interpret_byte(byte):
    # Bit 7 - Handshake phase (1 for handshake, 0 for acknowledged)
    handshake_phase = bool(byte & 0b10000000)

    # Bit 6 - Green status for recorder channel 3
    channel_3_green = bool(byte & 0b01000000)

    # Bit 5 - Green status for recorder channel 1
    channel_1_green = bool(byte & 0b00100000)

    # Bit 4 - Green status for recorder channel 2
    channel_2_green = bool(byte & 0b00010000)

    # Bit 3 - Red status for recorder channel 3
    channel_3_red = bool(byte & 0b00001000)

    # Bit 2 - Red status for recorder channel 1
    channel_1_red = bool(byte & 0b00000100)

    # Bit 1 - Red status for recorder channel 2
    channel_2_red = bool(byte & 0b00000010)

    # Bit 0 - Recording in progress (alternates 0 and 1 when recording paused)
    recording_in_progress = bool(byte & 0b00000001)

    # Print the decoded properties
    print("Handshake phase:", handshake_phase)
    print("Channel 3 Green Status:", channel_3_green)
    print("Channel 1 Green Status:", channel_1_green)
    print("Channel 2 Green Status:", channel_2_green)
    print("Channel 3 Red Status:", channel_3_red)
    print("Channel 1 Red Status:", channel_1_red)
    print("Channel 2 Red Status:", channel_2_red)
    print("Recording in progress:", recording_in_progress)

# Example usage with a sample byte
sample_byte = 0b11010101
interpret_byte(sample_byte)

# Set up the GPIO pin connected to the momentary contact switch (GP02)
switch_pin = digitalio.DigitalInOut(board.GP2)
switch_pin.direction = digitalio.Direction.INPUT
switch_pin.pull = digitalio.Pull.UP  # Set the internal pull-up resistor

def if_switch_held():
    time.sleep(0.1)
    switch_state = switch_pin.value
        # Check if the switch is pressed (LOW) or released (HIGH)
    if not switch_state:
        print("Switch held!")
        return True
    return False

def wait_for_switch():
    while True:
        # Read the state of the switch
        switch_state = switch_pin.value
        # Check if the switch is pressed (LOW) or released (HIGH)
        if not switch_state:
            print("Switch is pressed!")
            time.sleep(0.25)
            return
        # Add a small delay before reading the switch again
        time.sleep(0.1)

print("Press switch to begin")
wait_for_switch()

print("Reading from uart 2...")
print("Press Switch to send handshake")
while True:
    # Check for incoming data on Serial2
    if uart2.in_waiting > 0:
        incoming_byte2 = uart2.read(1)[0]
        print_byte(2, incoming_byte2)
        interpret_byte(incoming_byte2)
    if if_switch_held():
        break

print("Send the bytes '\x80\x00' through uart3")
# Send the bytes '\x80\x00' through uart3
uart3.write(b'\x80')
time.sleep(0.1)  # 100ms delay
uart3.write(b'\x00')

time.sleep(0.25)
print("Reading from uart 2...")
print("Press Switch to start recording")
while True:
    # Check for incoming data on Serial2
    if uart2.in_waiting > 0:
        incoming_byte2 = uart2.read(1)[0]
        print_byte(2, incoming_byte2)
    if if_switch_held():
        break

print("Start recording?")        
# Let's try recording?
uart3.write(b'\x81')
time.sleep(0.1)  # 100ms delay
uart3.write(b'\x00')
time.sleep(0.1)  # 100ms delay
uart3.write(b'\x80')
time.sleep(0.1)  # 100ms delay
uart3.write(b'\x00')

print("Reading from uart 2...")
print("Press Switch to stop recording")
while True:
    if uart2.in_waiting > 0:
        incoming_byte2 = uart2.read(1)[0]
        print_byte(2, incoming_byte2)
        interpret_byte(incoming_byte2)
    if if_switch_held():
        break

print("Stop recording?")        
uart3.write(b'\x81')
time.sleep(0.1)  # 100ms delay
uart3.write(b'\x00')
time.sleep(0.1)  # 100ms delay
uart3.write(b'\x80')
time.sleep(0.1)  # 100ms delay
uart3.write(b'\x00')

print("Reading from uart 2...")
while True:
    if uart2.in_waiting > 0:
        incoming_byte2 = uart2.read(1)[0]
        print_byte(2, incoming_byte2)
        interpret_byte(incoming_byte2)
    if if_switch_held():
        break