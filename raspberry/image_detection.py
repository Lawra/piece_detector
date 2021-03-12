#import pygame
import picamera
import time
import requests


# camera.brightness = 50 (0 to 100)
# camera.sharpness = 0 (-100 to 100)
# camera.contrast = 0 (-100 to 100)
# camera.saturation = 0 (-100 to 100)

# camera.exposure_compensation = 0 (-25 to 25)
#camera.meter_mode = 'average'
#camera.rotation = 0
#camera.hflip = False
#camera.vflip = False
#camera.crop = (0.0, 0.0, 1.0, 1.0)

class ImageDetection:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.file_name = 'image_captured.jpg'

        # VARIABLES DE LA CAMARA:
        # NOTA: se podrien passar com a paràmetre d'entrada si es volgues
        self.camera.resolution = (3280, 2464)
        # off,auto,sunlight,cloudy,shade,tungsten,fluorescent,incandescent,flash,horizon
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = (1.4, 1.8)  # roig, blau
        # off,auto,night,nightpreview,backlight,spotlight,sports,snow,beach,verylong,fixedfps,antishake,fireworks
        self.camera.exposure_mode = 'off'
        self.camera.shutter_speed = 20000
        self.camera.iso = 200  # 0 (automatic) (100 to 800)
        # sleep(1)

    def start_camera(self):
        self.camera.start_preview()

    def stop_camera(self):
        self.camera.stop_preview()

    def image_capture(self):
        self.camera.capture(self.file_name)

    def get_pieces_position(self):
        print("sending ...\n")

        # request a la api
        url = "https://lauraferre.net/api/cv/piece_position"  # url de la api
        files = {'image': open(self.file_name, 'rb')}

        # PETICIO A LA API:
        response = requests.post(url, files=files)

        try:
            data = response.json()
        except ValueError:
            print("Response content is not valid JSON")
            data = {'success': "true", 'num_pieces': 0, 'list': []}

        return data
