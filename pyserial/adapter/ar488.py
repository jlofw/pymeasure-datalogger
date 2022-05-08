import serial
import sys

# notes:
# '\r', '\n', and '+' are control characters that must be escaped in binary data
#
# Prologix commands:
# ++addr [1-29]
# ++auto [0 | 1 | 2 | 3]
# ++clr
# ++eoi [0 | 1]
# ++eos [0 | 2 | 3 | 4]
# ++eot_enable [0 | 1]
# ++eot_char [<char>]
# ++help (unsupported)
# ++ifc
# ++llo [all]
# ++loc [all]
# ++lon (unsupported)
# ++mode [0 | 1]
# ++read [eoi | <char>]
# ++read_tmo_ms <time>
# ++rst
# ++savecfg
# ++spoll [<PAD> | all | <PAD1> <PAD2> <PAD3> ...]
# ++srq
# ++status [<byte>]
# ++trg [PAD1 ... PAD15]
# ++ver [real]
#
# Custom AR488 commands:
# ++allspoll
# ++dl
# ++default
# ++macro [1-9]
# ++ppoll
# ++setvstr [string]
# ++srqauto [0 | 1]
# ++repeat count delay cmdstring
# ++tmbus [value]
# ++verbose


class ar488(object):
    """Class to represent AR488 USB-GPIB adapter.
    The AR488 is an Arduino-based USB-GPIB adapter.
    For details see: https://github.com/Twilight-Logic/AR488
    """

    def __init__(self, port, baudrate, timeout):
        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        except:
            sys.exit("error opening serial port {}".format(port))

    def __del__(self):
        self.ser.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.ser.close()

    # Raw GPIB read/write commands
    def write(self, message):
        """Write message to GPIB bus."""
        self.ser.write("{}\r".format(message).encode())

    def read(self):
        """Read from GPIB bus."""
        return self.ser.readline().decode()

    def query(self, message):
        "Write message to GPIB bus and read results."""
        self.write(message)
        return self.read()

    # Prologix commands
    def set_address(self, address):
        """Specify address of GPIB device with which to communicate.
        When the AR488 is in device mode rather than controller mode, this
        instead sets the address of the AR488.
        """

        self.write("++addr {}".format(address))

    def get_current_address(self):
        "Return the currently specified address."""
        return self.query("++addr")