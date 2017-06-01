from t_printer_lib import *
import datetime,time,os,sys
import RPi.GPIO as GPIO
M_ID = 0

if len(sys.argv) == 2:
    serialport = sys.argv[1]
else:
    serialport = ThermalPrinter.SERIALPORT

if not os.path.exists(serialport):
    sys.exit("ERROR: Serial port not found at: %s" % serialport)

p = ThermalPrinter(serialport=serialport)
p.inverse()
p.justify("C")

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

os.system('clear')

while True:
    input_state = GPIO.input(3)
    if input_state == False:
        p.print_text("Fictional Island JDW2017\n")
        p.print_text("Moment #"+str(M_ID))
        M_ID = M_ID + 1
        time.sleep(1)
