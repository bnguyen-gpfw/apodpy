#!/usr/bin/env python

"""apod.py: Downloads Astronomy Picture of the Day for local use and creates a wallpaper version"""

__author__     = "Dede Lamb"
__copyright__  = "Copyright 2017 Dede Lamb"
__credits__    = ["Dede Lamb"]
__license__    = "GPL"
__version__    = "3.0"
__maintainer__ = "Dede Lamb"
__email__      = "ddlala27@gmail.com"
__status__     = "Development"


import json
from urllib.request import urlopen, urlretrieve
from os.path import splitext, isfile, realpath
from PIL import Image
from datetime import datetime
from pytz import timezone


# smart crop image to aspect ratio (no scaling)
# rotates the image if it's a better fit
def im_create_wp(im, aspect_width, aspect_height):
    w, h = im.size

    if h > w:
        im = im.transpose(Image.ROTATE_90)
        w, h = im.size

    guess_h = int(w * aspect_height / aspect_width)
    guess_w = int(h * aspect_width / aspect_height)
    if h > guess_h:
        top = (h - guess_h) / 2
        box = (0, top, w, top + guess_h)
        im = im.crop(box)
    elif w > guess_w:
        left = (w - guess_w) / 2
        box = (left, 0, left + guess_w, h)
        im = im.crop(box)

    return im


# APOD API https://api.nasa.gov/api.html#apod
# DEMO_KEY or get a key from https://api.nasa.gov/index.html#apply-for-an-api-key
api_key = 'DEMO_KEY'

#set date at US Eastern Standard so we are in sync with the API
#this is because of an error in the API
date_string = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d')

basepath = realpath(__file__)
basepath = basepath[0:basepath.rfind('/') + 1]
todaypath = basepath + date_string
jsonpath = todaypath + '.json'


if isfile(jsonpath):
    print("I have today's APOD")
    print(jsonpath)

else:
    print("I am fetching today's APOD manifest")
    url = 'https://api.nasa.gov/planetary/apod?api_key={}&date={}&hd=True'
    response = urlopen(url.format(api_key, date_string))
    response_text = response.readall().decode('utf-8')
    data = json.loads(response_text)

    print('I got a response: {} ({} US/Eastern)'.format(data['title'], data['date']))

    imex = splitext(data['hdurl'])[1]
    data['imagepath'] = todaypath + '.original' + imex
    data['wallpath'] = todaypath + '.wall' + imex
    data['thumbpath'] = todaypath + '.thumb' + imex

    print('I am getting the image from ' + data['hdurl'])
    urlretrieve(data['hdurl'], data['imagepath'])
    print('I have saved it at ' + data['imagepath'])

    im = Image.open(data['imagepath'])
    im = im_create_wp(im, 16, 9)
    im.save(data['wallpath'])
    print('I have saved a wallpaper copy at ' + data['wallpath'])

    im = Image.open(data['imagepath'])
    size = 128, 128
    im.thumbnail(size)
    im.save(data['thumbpath'])
    print('I have saved a thumbnail at ' + data['thumbpath'])

    print('Saving APOD manifest with local images')
    json.dump(data, open(jsonpath, 'w'))
    print(jsonpath)

