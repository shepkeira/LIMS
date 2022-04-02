"""
functions related to barcodes
"""
import os
from os.path import exists
from barcode import Code128
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
import numpy as np
from PIL import Image

class Barcoder:
    """
    Barcode class containing functions related to
    creating and reading barcodes
    """
    def __init__(self):
        self.type = 'CODE128'

    def create_barcode(self, code):
        """
        creates a barcode based on the code provided
        returns path to barcode image
        """
        file_name = 'barcodes/' + code + '_barcode.jpg'
        if exists(file_name):
            return 'static/' + file_name
        with open('static/' + file_name, 'wb') as file:
            Code128(code, writer=ImageWriter()).write(file)
        return 'static/' + file_name

    def read_barcode_image(self, image):
        """
        read barcode images
        """
        barcode = decode(image)
        for obj in barcode:
            points = obj.polygon
            # (x,y,w,h) = obj.rect
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            barcode_data = obj.data.decode("utf-8")
            return barcode_data

    def scan_barcode(self,my_image_path):
        """
        reads a barcode in from the camera
        returns the barcode code
        """
        img_path = os.path.basename(my_image_path)
        image_path_2 = os.path.join("./uploads/images", img_path)
        img = Image.open(image_path_2)
        barcode = self.read_barcode_image(img)
        return barcode
