import time
import board
import digitalio
import busio

uart2 = busio.UART(board.GP4, board.GP5, baudrate=2400, bits=8, parity=None, stop=1)

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

# Variable to store the last received time
last_received_time = time.monotonic()

stateKnown = False
stateIsRecording = False

print("Reading from uart 2...")
while True:

    # Check for incoming data on Serial2
    if uart2.in_waiting > 0:
        incoming_byte2 = uart2.read(1)[0]
         # Update the last received time
        #print_byte(2, incoming_byte2)
        #interpret_byte(incoming_byte2)
        if not needsHandshake(incoming_byte2):
            # This useful status  data
            stateIsRecording = isRecording(incoming_byte2)
            print("Updated status. Record={}".format(stateIsRecording))
            last_received_time = time.monotonic()
            stateKnown = True

    if not stateKnown:
        if time.monotonic() - last_received_time >= 5.0:
            print("No status data received for 5 seconds. Sending specific byte.")
            # This code elicits a response
            #print("Poke")
            uart2.write(b'\x80')
            time.sleep(0.01)
            uart2.write(b'\x00')
            time.sleep(0.01)
            uart2.write(b'\xA1')
            time.sleep(0.01)
            uart2.write(b'\x00')
            time.sleep(0.25)
            last_received_time = time.monotonic()
    else:            
        if if_switch_held():
                if stateIsRecording:
                    print("Stop recording")
                else:
                    print("Start recording")
                # Let's try recording?
                uart2.write(b'\x81')
                time.sleep(0.1)  # 100ms delay
                uart2.write(b'\x00')
                time.sleep(0.1)  # 100ms delay
                uart2.write(b'\x80')
                time.sleep(0.1)  # 100ms delay
                uart2.write(b'\x00')
                time.sleep(0.25)