#!/usr/bin/env python
# coding: utf-8

from serial import Serial
from struct import unpack
from time import sleep

class ThermalPrinter(object):

    BAUDRATE = 19200
    TIMEOUT = 3

    black_threshold = 48
    alpha_threshold = 127

    printer = None

    _ESC = chr(27)

    def __init__(self, heatTime=80, heatInterval=2, heatingDots=7, serialport=SERIALPORT):
        self.printer = Serial(serialport, self.BAUDRATE, timeout=self.TIMEOUT)
        self.printer.write(self._ESC) # ESC - command
        self.printer.write(chr(64)) # @   - initialize
        self.printer.write(self._ESC) # ESC - command
        self.printer.write(chr(55)) # 7   - print settings
        self.printer.write(chr(heatingDots))  # Heating dots (20=balance of darkness vs no jams) default = 20
        self.printer.write(chr(heatTime)) # heatTime Library default = 255 (max)
        self.printer.write(chr(heatInterval)) # Heat interval (500 uS = slower, but darker) default = 250
        printDensity = 15 # 120% (? can go higher, text is darker but fuzzy)
        printBreakTime = 15 # 500 uS
        self.printer.write(chr(18))
        self.printer.write(chr(35))
        self.printer.write(chr((printDensity << 4) | printBreakTime))

    def offline(self):
        self.printer.write(self._ESC)
        self.printer.write(chr(61))
        self.printer.write(chr(0))

    def online(self):
        self.printer.write(self._ESC)
        self.printer.write(chr(61))
        self.printer.write(chr(1))

    def sleep(self):
        self.sleep_after(1)

    def sleep_after(self, seconds):

        if seconds:
            sleep(seconds)
            self.printer.write(self._ESC)
            self.printer.write(chr(56))
            self.printer.write(chr(seconds))
            self.printer.write(chr(seconds >> 8))

    def wake(self):
        self.printer.write(chr(255))
        sleep(0.05)
        self.printer.write(self._ESC)
        self.printer.write(chr(56))
        self.printer.write(chr(0))
        self.printer.write(chr(0))

    def has_paper(self):
        status = -1
        self.printer.write(self._ESC)
        self.printer.write(chr(118))
        self.printer.write(chr(0))
        for i in range(0, 9):
            if self.printer.inWaiting():
                status = unpack('b', self.printer.read())[0]
                break
            sleep(0.01)
        return not bool(status & 0b00000100)

    def reset(self):
        self.printer.write(self._ESC)
        self.printer.write(chr(64))

    def linefeed(self, number=1):
        for _ in range(number):
            self.printer.write(chr(10))

    def justify(self, align="L"):
        pos = 0
        if align == "L":
            pos = 0
        elif align == "C":
            pos = 1
        elif align == "R":
            pos = 2
        self.printer.write(self._ESC)
        self.printer.write(chr(97))
        self.printer.write(chr(pos))

    def bold(self, on=True):
        self.printer.write(self._ESC)
        self.printer.write(chr(69))
        self.printer.write(chr(on))

    def font_b(self, on=True):
        self.printer.write(self._ESC)
        self.printer.write(chr(33))
        self.printer.write(chr(on))

    def underline(self, on=True):
        self.printer.write(self._ESC)
        self.printer.write(chr(45))
        self.printer.write(chr(on))

    def inverse(self, on=True):
        self.printer.write(chr(29))
        self.printer.write(chr(66))
        self.printer.write(chr(on))

    def print_text(self, msg, chars_per_line=None):
        if not chars_per_line:
            self.printer.write(msg)
            sleep(0.2)
        else:
            l = list(msg)
            le = len(msg)
            for i in xrange(chars_per_line + 1, le, chars_per_line + 1):
                l.insert(i, '\n')
            self.printer.write("".join(l))
            sleep(0.2)
