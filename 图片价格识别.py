#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 15:49:46 2018

@author: oyc
"""

import pytesseract
import tesserocr
from PIL import Image
image=Image.open('captcha2.png')
#print(pytesseract.image_to_string(image))
price=pytesseract.image_to_string(image).split('¥')
print(price[1])