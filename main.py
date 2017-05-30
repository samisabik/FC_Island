import picamera
import datetime,time
import RPi.GPIO as GPIO
from PIL import Image 
from PIL import ImageEnhance

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = picamera.PiCamera()

camera.resolution = (384, 1944)
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.image_effect = 'none'
camera.rotation = 180
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)

while True:
    input_state = GPIO.input(3)
    if input_state == False:
        filename = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.jpg")
        camera.capture('/home/FC_Island/output/'+filename)
        image_file = Image.open("input.jpg") # open colour image
		enhancer = ImageEnhance.Brightness(image_file)
		img_enhanced = enhancer.enhance(3)
		enhancer = ImageEnhance.Contrast(img_enhanced)
		img_enhanced = enhancer.enhance(3)

		img_enhanced.save("input_enhance.jpg")
		image_file = Image.open("input_enhance.jpg") # open colour image
		image_file = image_file.convert('1') # convert image to black and white
		image_file.save('result.bmp')
        
        time.sleep(1)