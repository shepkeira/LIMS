from barcode import Code128
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
import numpy as np
from os.path import exists
import os
from PIL import Image

class Barcoder:
    def __init__(self):
        self.type = 'CODE128'

    # creates a barcode based on the code provided
    # returns path to barcode image
    def createBarcode(self, code):
        file_name = 'barcodes/' + code + '_barcode.jpg'
        if exists(file_name):
            return 'static/' + file_name
        with open('static/' + file_name, 'wb') as f:
            Code128(code, writer=ImageWriter()).write(f)
        return 'static/' + file_name

    def __readBarcode(self, image):
        print("read------------------------------------------------")
        print(image)
        barcode = decode(image)
        print(barcode)
        for obj in barcode:
            print("trying obj")
            points = obj.polygon
            (x,y,w,h) = obj.rect
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))

            barcodeData = obj.data.decode("utf-8")
            barcodeType = obj.type
            
            return barcodeData
        

    # reads a barcode in from the camera
    # returns the barcode code
    def scanBarcode(self,my_image_path):
        img_path = os.path.basename(my_image_path)
        image_path_2 = os.path.join("./uploads/images", img_path)

        img = Image.open(image_path_2)
        
        barcode = self.__readBarcode(img)
        return barcode
