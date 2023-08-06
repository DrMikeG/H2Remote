# H2Remote

## 5th August 2023 ##

Today I got the feather 2040 flashing its neo pixel.
I also got it to read from the IR receiver.

I tried to decode the remote protocol - thinking it would encode an RGB value - but I'm pretty sure it's just sending an int for each remote key, and the device is mapping the int to a specific color or behaviour.

Looking at the pin order on the feature, it was actually better to swap back to a vs1838b IR receiver, as the pinout is the compatible (although backwards) with 3v3/GND/A0 on the feather.

![Alt text](./readme_img/PXL_20230805_130158125.jpg)

I also connected the lipo battery (via the switch) which is now being charged (small yellow LED top left)

Next step is to review the TX/RX with the zoom and figure out a common gnd.

On the Pico - I had success with 
``uart2 = busio.UART(board.GP4, board.GP5, baudrate=2400, bits=8, parity=None, stop=1)``

![Alt text](./readme_img/pico_TX.png)

![Alt text](./readme_img/feather_TX.png)

![Alt text](./readme_img/bo_jack.png)


UART1 TX and UART1 RX

From the feather documentation:

>>> CircuitPython I2C, SPI and UART
Note that in CircuitPython, there is a board object each for I2C, SPI and UART that use the pins labeled on the Feather. You can use these objects to initialise these peripherals in your code.
```
board.STEMMA_I2C() uses SCL/SDA
board.SPI() uses SCK/MO/MI
board.UART() uses RX/TX
```

```
UART Pins:
UART0 TX: TX, A2, D12
UART0 RX: RX, A3, D13

UART1 TX: D24, MISO, D6
UART1 RX: D25, D9
```

Using the feather I can successfully communicate with the H2 to start and stop recording.
I had 24/25 backwards for a while - and listening seemed to work.

pin 25 is connected to L on the 2.5mm terminal block
pin 24 is connected to R on the 2.5mm terminal block
pin 10 (pseudo gnd) is connected to V on the 2.5mm terminal block


## 4th August 2023 ##

This evening was my first opportunity to start working with the feather 2040

Firstly, I've solvered up some sprung-clip test leads onto some du pont male breadboard leads.

This allows me to make secure connections to the board without soldering on headers.
Very pleased with that idea.

The feature has a very different list of pins available compare to the pico.
I took the 01_pico_IR example and edited it into 08_feather_IR - editing the default pin from GP22 to D6 and editing the pin in use too.
This was the only modification necessary though.



## 31st July 2023 ##

So, I made a boo boo.
The port on the H2 is current limited to 10mA, and despite my previous readings, the tiny 2040 need 25mA to run.
This isn't a surprise as the 2040 chip needs 20mA to idle.

I can't think of a way around this limit, so my board is going to need external power.
I considered some coin cell batteries, and I might go there, but first I want to try a lipo battery.
I went looking for a charging shim with an on/off switch, but realised that most more larger than the tiny 2040, and would present more
mounting problems.

Since I have lost my size advantage, I have ordered a different board to work with, one with native lipo support.
I considered the pimironi version of this, which has an on/off button, but decided I'm going to want the on/off broken out to the side of the case anyway.



https://learn.adafruit.com/adafruit-feather-rp2040-pico/pinouts
https://io.adafruit.com/blog/tip/2016/12/14/feather-power-switch/
https://learn.adafruit.com/adafruit-feather-m0-basic-proto/power-management#enable-pin

## 23rd July 2023 ##
Another thread to pick at:
https://github.com/radicalrendell/zoom_remote/blob/master/zoomctl.py

https://www.webwork.co.uk/2021/03/wireless-remote-control-for-zoom-h2n.html
https://github.com/lowfriars/ZoomRemote

With Zoom connected with trrs breakout, L (yellow wire) on the breakout connects to ping GP4 on a pico.
Code in 04_pico_zoom_rx can receive bits
0x81,0x80

In some of example code for a zoom H4 remote, there is a handshake

```
# handshake
# return true if connected, false if not
def zhandshake(s):
    # send 00, look for 80, then send A1, look for 80 then we are ready
    s.write('\x00')

    zbyte = s.read(1)
    if (zbyte == '\x80'): s.write('\xa1')
        
    zbyte = s.read(1)
    if (zbyte == '\x80'): return(1) 
    return(0)
```

I don't know if sending A1 would do anything for the H2, because we seem to receive an alternating stream of 80,81,80 as it is.

>> Although the recorder supplies 3.3V power, it's not capable of supplying much current, certainly not enough for a wireless link, so regrettably the wireless interface needs its own power source. The communication protocol was clearly designed by an electrical engineer: it consists of key-down and key-up events being sent to the recorder to signal the press and release of buttons on the physical remote control and an encoded status byte being sent to the remote control to illuminate status LEDs (such as recording-in-progress and level indicators). There is an initial handshake to establish the connection of the remote control. 

https://www.webwork.co.uk/2021/05/wireless-remote-control-for-zoom-h2n.html

>>  The control protocol calls for a code to be sent when a button is pressed and a further code when it is released (this allows, for example, auto-repeat on the Volume controls). The codes corresponding to the "press" event for each button are stored in the keySequence dictionary (the release code is the same for all keys).

Data received from the H2n consists of a singled byte which is encoded as follows (red and green refer to VU meter, both on together corresponds to yellow):

Initially, the Zoom device sends a sequence of two bytes: for the H2n these are 0x80 and 0x81, for other devices they may be 
different, but the high bit of 0x80 appears to be intended to signify that it's a two-byte sequence. 

The service sends "key up" messages to the recorder. 

At some point, the recorder recognises the existence of the remote controller and switches to one-byte
responses with the top bit clear. The contents of each byte represents the status of the recorder as follows:
/// 
/// Bit 7   -   1 for handshake phase, 0 once remote control has been acknowledged
/// Bit 6   -   Green status for recorder channel 3
/// Bit 5   -   Green status for recorder channel 1
/// Bit 4   -   Greet status for recorder channel 2
/// Bit 3   -   Red status for recorder channel 3
/// Bit 2   -   Red status for recorder channel 1
/// Bit 1   -   Red status for recorder channel 2
/// Bit 0   -   1 if recording in progress (alternates 0 and 1 when recording paused)

I think the button up code is:
s.write('\x80\x00')

Gradually building up from the various great bits of example code, I've managed to:
- read the h2 RX line
- 'handshake' with the h2 on its TX line
- interpret the post-handshake byte on the h2 RX line
- Send start/stop record in the TX line

This is currently being done with the UART pins, not with PIO.

I need to understand more about PIO if I want to avoid needing to use UART.

I struggled to get two example running at once, so I'm going to try and build a new example with flashing an LED and reading the IR diode.

https://learn.adafruit.com/intro-to-rp2040-pio-with-circuitpython/using-pio-to-blink-a-led-quickly-or-slowly

## 22nd July 2023 ##

Serial 2400 8b no parity 1 stop (8n1)
Bit order: LSB first, inverted logic: no
https://github.com/raspberrypi/pico-examples/blob/master/pio/uart_rx/uart_rx.pio

"With no activity on the recorder the RX and TX pins show ~2.7 volts"

"When you press the record button on the remote, after a moment the recording LED lights up"

"On the oscilloscope I can see three different square wave patterns for the three different buttons on the TX pin and a single type of square wave
on RX to light the LED."

"The following images show the signal for the record button then that sent in
response to to light the LED.

![Signal sent by the remote when Record pressed](./readme_img/Hacking%20the%20Zoom%20H2n%20Remote%20Control%20_%20g7smy.co.uk.png) Signal sent by the remote when Record pressed

![Signal sent by the Zoom recorder to light the LED in the remote](./readme_img/Hacking%20the%20Zoom%20H2n%20Remote%20Control%20_%20g7smy2.png) Signal sent by the Zoom recorder to light the LED in the remote

![Alt text](image.png)

Can I get the first byte of the response? 0x20

Using teensy example code:
```
// incoming data
Serial2.begin(2400, SERIAL_8N1);  // Remote Receive - RX
Serial3.begin(2400, SERIAL_8N1);  // Remote Transmit - TX
```

https://arduino-pico.readthedocs.io/en/latest/piouart.html

```
Equivalent to the Arduino SoftwareSerial library, an emulated UART using one or two PIO state machines is included in the Arduino-Pico core. This allows for up to 4 bidirectional or up to 8 unidirectional serial ports to be run from the RP2040 without requiring additional CPU resources.

Instantiate a SerialPIO(txpin, rxpin, fifosize) object in your sketch and then use it the same as any other serial port. Even, odd, and no parity modes are supported, as well as data sizes from 5- to 8-bits. Fifosize, if not specified, defaults to 32 bytes.
```

https://learn.adafruit.com/intro-to-rp2040-pio-with-circuitpython?view=all




## 21st July 2023 ##

My TSOP2238 IR diodes arrived today.
These have a different leg ordering to the standard pins I use.

![Alt text](./readme_img/PXL_20230721_122533155.jpg)

Pin 1 (left when facing) - purple wire to GND
Pin 2 - white wire to 3v3
Pin 3 grey wire to GP07 (working with test script 01_pico_IR_PIO)

This works great, so I can plan to solder it on to the Tiny_2040

## 18th July 2023 ##

Serial 2400 8b no parity 1 stop (8n1)
Bit order: LSB first, inverted logic: no
https://github.com/raspberrypi/pico-examples/blob/master/pio/uart_rx/uart_rx.pio

// bytes to start and stop the recorder, a negative number is used as a delay
int record[5] = { 0x81, 0x0, -100, 0x80, 0x0 };  


# 17th July 2023 ##

Tiny 2040 from Pimoroni is compatible with firmware designed for the Raspberry Pi Pico.

It is one-third of the size of a Raspberry Pi Pico & has 16 GPIO pins while Raspberry Pi Pico has 40 pins.

With proper orientations & mapping of the pins, there is no loss of functionality despite lesser pins.

Board has some unique features that Raspberry Pi Pico does not have, such as a dedicated reset button, a fourth ADC pin, RGB LED & USB C port.

![Alt text](./readme_img/tiny2040_back.png)

Pin numbers 
Pin numbers are available on top of the board. 
These are numbered as logically &, these relate to GPIO pin number as per the Pico pinout reference.

Tiny 2040 Pinout
Pinout of the Tiny 2040 shows that it has a total of 16 pins(3 additional pins are for debugging) out of which 12 are I/O pins: 8 digital, 4 analog(12 bit).

![Alt text](./readme_img/tiny2040_pins.png)

The remaining pins are 2X Ground, 1X 5V, and 1X 3.3V. Board supports 2X UART(UART0 and UART1), 1X SPI, and 2X I2C(I2C0 and I2C1) interfaces.

I have been using GP22 (pin 12) on the pico.

I can try and use D0
Or I could try to use D26 (A0) in the tiny, which would be 

I programmed up the Tiny 2048 with the code in 01_pico_IR.
It didn't work because the Tiny doesn't have board.GP22 defined.

I made a copy of the code in 03_tiny2034, including the libraries, and changed the default pin to 7.

It was a bit iffy holding the wires on, but I got the tiny to recognize codes.

Perfect!






IR - Infrared Receiver (TSOP38238)
To use, connect pin 3 (all the way to the right) to 5V power, pin 2 (middle) to ground and listen on pin 1. It doesn't do any decoding of the signal, just passes the 'raw data' along.

![Alt text](./readme_img/tsop.png)

I was puzzling this evening about the layout of my board. Because the gnd pin is in the middle, there was no neat way to pop the part into three adjacent pins on the tiny.

I couldn't figure out why the internet didn't have 100s of tips about how to swap the order of legs, how to bend them around, or shim boards that let you change the order.
I even considered making one.

![Alt text](./readme_img/TSOP4838-specs.png)

Then I learned this - and it's a bit of a revelation.
The TSOP4838 is the same part as the TSOP2238 - except they have different pinning!

I can get OUT,VS,GND - which backwards is GND/VS/OUT - which is the order of the pins I want to use.



## 16th July 2023 ## 

Started work on a shock-mount for the H2.
This will also give me a frame on which to mount the remote?

Time to start on the remote. Some parts have arrived - 2.5mm jacks. TRRS.

Pin one being the tip of the 2.5mm jack plug:
1. Remote Receive – RX
2. Remote Transmit – TX
3. Ground
4. 3.1V – Power

![Alt text](./readme_img/bo_jack.png)

VBUS
![Alt text](./readme_img/pinout.png)


Pico PIO IR decoding:
https://github.com/rdear4/Pico_PIO_IR_Receiver

Let's start for something basic with the IR reading.
https://learn.adafruit.com/ir-sensor/using-an-ir-sensor

Connected up a KY-022 Infrared sensor module to pico WH

Gnd, 3v3 and GP1 (pin 2)

Adafruit CircuitPython IRRemote library on your CircuitPython board.

Flashed on on adafruit-circuitpython-raspberry_pi_pico-en_US-7.3.3.uf2

Copied on lib adafruit_irremote.mpy

Using the code in 00_pico_IR_test, I could identify an IR pulse using my samsung TV remote.
Sensor seems happy running at 3v3

Setup rdear4's pio library. Added adafruit_pioasm.mpy.
Changed module input to pin gp22 (pin 29)

It can read volume codes from my remote.
11100000111000001110000000011111
11100000111000001110000000011111
11100000111000001101000000101111

It can register, but not recognise my Nikon remote.

It can recognise and understand my Edifer remote.
It can recognise and understand my son's cheap LED light remote.

Now I need to write my own PIO programs based on this to detect signals from the H2?


### Tiny 20240 ###
Getting started...
https://www.instructables.com/Introducing-the-Tiny-2040-Microcontroller-IR-Commu/
This even shows a receive IR example!

Plugged in to USB C. Powered, but did not detect. Changed cable. Appeared are rp2.

There is different firmware for the 2mb and 8mb versions! I have the 8mb version.

Copied on adafruit-circuitpython-pimoroni_tiny2040-en_GB-7.3.3.uf2 (not latest, but I used 7.3.3 on picos)



## 14th July 2023 ##

timelapse/timelapse/timelapse

https://www.tomshardware.com/how-to/use-raspberry-pi-camera-with-bullseye

```The latest Raspberry Pi OS is based upon Debian 11 (Bullseye) and with this new release we see the familiar raspistill and raspicam camera commands replaced with a new suite of open source tools dedicated to getting the most from all of the official Raspberry Pi cameras.

Libcamera is a support library for Linux, Android and ChromeOS which was introduced to the Raspberry Pi via a previous Raspberry Pi OS, but it has come into the spotlight due to the changes made for Bullseye. The app offers an easy to use series of tools which can tweak many different camera settings (aperture, color balance, exposure) via a series of switches issued when the command is invoked.``````

Done some very cool things with a raspberry pi 3.
Remote development, touch screen. camera. 3D printed supports.
Setup for time lapse - I think.


## 10th July 2023 ##

Resurrecting a gemma board to run circuit python.

Not sure if my gemma is an M0

https://learn.adafruit.com/adafruit-gemma-m0/circuitpython

Plugged in and turned on.

Double pressed reset. Waiting and button went green.

I studied a project a while ago about reading IR code using PIO.
https://github.com/raspberrypi/pico-examples/tree/master/pio/ir_nec

I didn't use it at the time, but it might be a great starting point for the H2 code generation.

https://github.com/carolinedunn/timelapse/blob/master/README.md

