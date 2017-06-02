from t_printer_lib import *
import picamera
import datetime,time,os,sys,glob
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageEnhance

#IMPORTANT STUFF here
CONTRAST_VALUE = 2
BRIGHTNESS_VALUE = 4.6
PRINTER = 'ZJ-58-4'

if not os.path.exists('output'):
    os.makedirs('output')

files_path = os.path.join('output', '*')
files = sorted(
    glob.iglob(files_path), key=os.path.getctime, reverse=True)
print files[0]
name = files[0]
name = name.replace('.bmp','')
name = name.replace('output/','')
M_ID = name

if len(sys.argv) == 2:
    serialport = sys.argv[1]
else:
    serialport = ThermalPrinter.SERIALPORT
if not os.path.exists(serialport):
    sys.exit("ERROR: Serial port not found at: %s" % serialport)
print "Testing printer on port %s" % serialport
p = ThermalPrinter(serialport=serialport)

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = picamera.PiCamera()
camera.resolution = (384, 1500)
camera.rotation = 180

os.system('clear')

while True:
    input_state = GPIO.input(3)
    if input_state == False:
        camera.capture('/home/pi/FC_island/output/tmp.jpg')
        image_file = Image.open('/home/pi/FC_island/output/tmp.jpg')
        enhancer = ImageEnhance.Brightness(image_file)
        img_bright = enhancer.enhance(BRIGHTNESS_VALUE)
        enhancer = ImageEnhance.Contrast(img_bright)
        output = enhancer.enhance(CONTRAST_VALUE)
        output.save('/home/pi/FC_island/output/tmp.jpg')
        image_file = Image.open('/home/pi/FC_island/output/tmp.jpg')
        image_file = image_file.convert('1')
        filename = (str(M_ID) + '.bmp')
        image_file.save('/home/pi/FC_island/output/'+filename)
        os.remove('/home/pi/FC_island/output/tmp.jpg')
        p.inverse(True)
        p.bold(True)
        p.justify("C")
        time.sleep(0.5)
        p.print_text("Fictional Island JDW2017\nMoment #"+str(M_ID)+"\n")
        time.sleep(0.5)
        os.system('lpr -P '+PRINTER+' -o fit-to-page /home/pi/FC_island/output/'+filename)
        time.sleep(0.5)
        os.system('lpr -P '+PRINTER+' -o scaling=200 /home/pi/FC_island/src/fc_spacer.bmp')
        time.sleep(0.5)
        #p.linefeed(3)
        M_ID = M_ID + 1
        time.sleep(1)
