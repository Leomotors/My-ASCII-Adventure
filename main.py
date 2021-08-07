import json
from PIL import Image
import math

SETTINGS = {}

with open("config.json") as config:
    SETTINGS = json.load(config)

ASCII_CHARS = [x for x in SETTINGS["ASCIIArray"]]
IMG_WIDTH = SETTINGS["ImageWidth"]


