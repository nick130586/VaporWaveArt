# The following code was developed by Tim Chinenov
# The script turns a random image into a Vaporwave themed
# image. The program was written in opencv 3.3.1 and python 2.7

# To run the program call the following command in terminal
# python main.py

import os
import sys
import random
import logging
import flickrapi
import cv2
from vaporwave import vaporize

ESCAPE_KEY = 27

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

from urllib.request import urlretrieve
from PIL import Image

filename = "pic"
fullFileName = ("%s.jpg" % filename)
url_template = 'http://farm%(farm_id)s.staticflickr.com/%(server_id)s/%(photo_id)s_%(secret)s.jpg'

def url_for_photo(p):
        return url_template % {
            'server_id': p.get('server'),
            'farm_id': p.get('farm'),
            'photo_id': p.get('id'),
            'secret': p.get('secret'),
        }

def appyEffect():
    img = vaporize()

    cv2.namedWindow(filename, cv2.WINDOW_NORMAL)
    cv2.imshow(filename, img)

    while cv2.getWindowProperty(filename, cv2.WND_PROP_VISIBLE):
        key_code = cv2.waitKey(100)

        if key_code == ESCAPE_KEY:
            break
        elif key_code != -1:
            import time
            start = time.time()
            img = vaporize()
            cv2.imshow(filename, img)
            end = time.time()
            logger.info("Vaporizing and rendering took: %f seconds" % (end-start,))

    cv2.destroyAllWindows()
    sys.exit()

def main():
    args = sys.argv

    if len(args) == 1:
        appyEffect()

    else:
        tag = args[1]

         # Retrieving a random image from Flickr by the tag
        flickr = flickrapi.FlickrAPI('your Flickr API key here', 'your Flickr secret here', cache=True)
        url = url_for_photo(random.choice(flickr.photos_search(tags=tag, per_page=1)[0]))
        urlretrieve(url, filename=fullFileName)

        appyEffect()


if __name__ == "__main__":
    main()
