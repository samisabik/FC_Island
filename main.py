from t_printer_lib import *
import picamera
import datetime,time,os,sys
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageEnhance

CONTRAST_VALUE = 2
BRIGHTNESS_VALUE = 4.6
M_ID = 0
if not os.path.exists('output'):
    os.makedirs('output')

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

camera = picamera.PiCamera()
camera.resolution = (384, 1944)
camera.rotation = 180

os.system('clear')

while True:
    input_state = GPIO.input(3)
    p.sleep()
    if input_state == False:
        p.wake()
        camera.capture('/home/FC_island/output/tmp.jpg')
        image_file = Image.open('/home/FC_island/output/tmp.jpg')
        enhancer = ImageEnhance.Brightness(image_file)
        img_bright = enhancer.enhance(BRIGHTNESS_VALUE)
        enhancer = ImageEnhance.Contrast(img_bright)
        output = enhancer.enhance(CONTRAST_VALUE)
        output.save('/home/FC_island/output/tmp.jpg')
        image_file = Image.open('/home/FC_island/output/tmp.jpg')
        image_file = image_file.convert('1')
        filename = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S.bmp')
        image_file.save('/home/FC_island/output/'+filename)
        os.remove('/home/FC_island/output/tmp.jpg')
        p.print_text("Fictional Island JDW2017\n")
        p.print_text("Moment #"+str(M_ID))
        time.sleep(0.1)
        os.system('lpr -P ZJ-58-4 -o fit-to-page /home/FC_island/output/'+filename)
        time.sleep(0.1)
        os.system('lpr -P ZJ-58-4 -o scaling=200 /home/FC_island/src/fc_spacer.bmp')
        print (filename+" successfully printed!")
        M_ID = M_ID + 1
        time.sleep(1)
