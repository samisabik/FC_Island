import picamera
import datetime,time,os
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageEnhance

if not os.path.exists('output'):
    os.makedirs('output'')

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = picamera.PiCamera()
camera.resolution = (384, 1944)
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.rotation = 180

while True:
    input_state = GPIO.input(3)
    if input_state == False:
        camera.capture('/home/FC_Island/output/tmp.jpg')
        image_file = Image.open('/home/FC_Island/output/tmp.jpg')
        enhancer = ImageEnhance.Brightness(image_file)
        img_bright = enhancer.enhance(3)
        enhancer = ImageEnhance.Contrast(img_bright)
        output = enhancer.enhance(3)
        output.save("tmp.jpg")
        image_file = Image.open("tmp.jpg")
        image_file = image_file.convert('1')
        filename = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.bmp")
        image_file.save('/home/FC_Island/output/'+filename)
        time.sleep(1)
