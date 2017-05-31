import picamera
import datetime,time,os
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageEnhance

CONTRAST_VALUE = 3
BRIGHTNESS_VALUE = 3

if not os.path.exists('output'):
    os.makedirs('output')

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = picamera.PiCamera()
camera.resolution = (384, 1944)
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.rotation = 180

os.system('clear')

while True:
    input_state = GPIO.input(3)
    if input_state == False:
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
        os.system('lpr -P ZJ-58-4 -o fit-to-page /home/FC_island/output/'+filename)
        print (filename+" successfully printed!")
        time.sleep(1)
