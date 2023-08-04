import board
import pulseio
import adafruit_irremote
import PulseReader
import time
import PulseReader

class PulseDecoder:

    def __init__(self, _IR_Pin=board.GP22, _maxlen=75, _idle_state=True, _data_pulse_width=560, _sm_freq=256000, _timeout=2**11-1):
        """
        Initialize the PulseDecoder class.

        Parameters:
        - _IR_Pin: The pin used for infrared (IR) communication. Defaults to board.GP22.
        - _maxlen: The maximum length of the pulse sequence. Defaults to 75.
        - _idle_state: The idle state of the pulse. Defaults to True.
        - _data_pulse_width: The expected pulse width of the data signal. Defaults to 560.
        - _sm_freq: The frequency of the state machine. Defaults to 256000.
        - _timeout: The timeout value for the pulse reading. Defaults to 2**11-1.
        - 2**11-1 = 2047
        - NOTE: The timeout of 2047 is equal to half the max number of clock cycles allowed to read a high or low signal.
        """
        self.__DATA_PULSE_WIDTH = _data_pulse_width
        self.reader = PulseReader.PulseReader(_IR_Pin=_IR_Pin, _sm_freq=_sm_freq, _timeout=_timeout)

    def resEqual(self, val, expectedVal, ALLOWED_DEVIATION=0.2):
        return abs(val - expectedVal) < val * ALLOWED_DEVIATION

    def checkZero(self, p1, p2):
        """
        Check if the given pulses represent a zero signal.

        Parameters:
        - p1: The first pulse value.
        - p2: The second pulse value.
        Returns:
        - True if the pulses represent a zero signal, False otherwise.
        """
        return self.resEqual(p1, self.__DATA_PULSE_WIDTH) and self.resEqual(p2, self.__DATA_PULSE_WIDTH)

    def checkOne(self, p1, p2):
        """
        Check if the given pulses represent a one signal.

        Parameters:
        - p1: The first pulse value.
        - p2: The second pulse value.
        Returns:
        - True if the pulses represent a one signal, False otherwise.
        """
        return self.resEqual(p1, self.__DATA_PULSE_WIDTH) and self.resEqual(p2, self.__DATA_PULSE_WIDTH * 3)

    def decodePulse(self, pulse):
        """
        Decode the pulse sequence and return the corresponding code.

        Parameters:
        - pulse: The pulse sequence to be decoded.
        Returns:
        - The decoded code if successful, False otherwise.
        """
        try:
            code = ""

            # Check for repeat signal
            # What is the significance of 9000 and 2250?
            if len(pulse) == 2:
                if self.resEqual(pulse[0], 9000) and self.resEqual(pulse[1], 2250):
                    code = "REPEAT"
                    return code

            # Check for correct start pulses
            # What is the significance of 9000 and 4500?
            if not self.resEqual(pulse[0], 9000) and not self.resEqual(pulse[1], 4500):
                print("Invalid code - Starting pulse error")
                return False

            # Decode the remaining pulses
            # Decode in pairs
            # if combined value is longer than x3 it should be a one
            # one should be n,3n
            # zero should be n,n
            for i in range(2, len(pulse)-1, 2):
                if (pulse[i] + pulse[i+1]) > self.__DATA_PULSE_WIDTH * 3:
                    if self.checkOne(pulse[i], pulse[i+1]):
                        code += "1"
                    else:
                        print(f"Invalid Code - One: {pulse[i+1]} {pulse[i+1]}")
                        return False
                else:
                    if self.checkZero(pulse[i], pulse[i+1]):
                        code += "0"
                    else:
                        print(f"Invalid Code - Zero: {pulse[i+1]} {pulse[i+1]}")
                        return False
            return code

        except Exception as e:
            print(e)
            return False

    def getCode(self):
        """
        This function is called repeatedly from the main program.
        There is no state passed in

        Get the decoded code from the pulse sequence.

        Returns:
        - The decoded code if available, None otherwise.
        """
        tempCode = self.reader.getPulses()

        if tempCode is not None:
            return self.decodePulse(tempCode)

        return None

if __name__ == "__main__":
    
    decoder = PulseDecoder()

    while True:
    
        decodedCode = decoder.getCode()
    
        if not decodedCode == None:
            print(decodedCode)