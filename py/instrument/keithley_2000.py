import time
from lib.ar488 import ar488

class keithley_2000(object):
    def __init__(self, port, baudrate, timeout):
        self.gpib = ar488(port,baudrate,timeout)
        print("port name: {}".format(self.gpib.ser.name))
        print("baudrate: {}".format(self.gpib.ser.baudrate))
        print("timeout: {}".format(self.gpib.ser.timeout))

        print("reading version from AR488:")
        print(">> " + self.gpib.query("++ver"))

        print("current self.gpib address:")
        print(">> " + self.gpib.get_current_address())
        print("setting address to 1")
        self.gpib.set_address(1)
        print("new self.gpib address:")
        print(">> " + self.gpib.get_current_address())

        print("assert IFC to make AR488 the controller-in-charge")
        self.gpib.write("++ifc")

        print("turn on auto 2 mode (auto-read after query)")
        self.gpib.write("++auto 2")
        print("verify auto mode: ")
        print(">> " + self.gpib.query("++auto"))

        print("get IDN message")
        print(">> " + self.gpib.query("*IDN?"))

        print("check SCPI version")
        print(">> " + self.gpib.query("SYST:VERS?"))

    def measure_voltage(self):
        print("measure voltage")