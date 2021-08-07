import json
import PIL.Image
import pygame as pg
from utils.ImgToASCII import ImgToASCII
import cv2
from tqdm import tqdm

SETTINGS = {}

with open("config.json") as config:
    SETTINGS = json.load(config)

ASCII_CHARS = [x for x in SETTINGS["ASCIIArray"]]
IMG_WIDTH = SETTINGS["ImageWidth"]
SCREEN_RES = tuple(int(r) for r in SETTINGS["ScreenResolution"].split(' '))
FONT_LOC = SETTINGS["fontName"]
FONT_SIZE = SETTINGS["fontSize"]
FPS = SETTINGS["fps"]

pg.init()
pg.display.set_caption("ASCII Art Visualizer")

screen = pg.display.set_mode(SCREEN_RES)
setfps = pg.time.Clock()
font = pg.font.Font(FONT_LOC, FONT_SIZE)

vidcap = cv2.VideoCapture('assets/ご注文はうさぎですか？？ ED2.mp4')

video_data = []


def process_frame(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = PIL.Image.fromarray(img)
    raw_data = ImgToASCII(img, ASCII_CHARS, IMG_WIDTH)
    video_data.append(raw_data["data"])
    global height, width
    height = raw_data["dimension"][0]
    width = raw_data["dimension"][1]


success = True
count = 1

while True:
    success, image = vidcap.read()
    if not success:
        break
    process_frame(image)
    print(f"Processed #{count} Frames")
    count += 1


ascii_dict = {}
for c in ASCII_CHARS:
    ascii_dict[c] = font.render(c, True, (255, 255, 255))


def Visualize(pixels):
    for index, data in enumerate(pixels):
        row = index/width
        col = index % width
        rowpos = row*SCREEN_RES[0]/width
        colpos = col*SCREEN_RES[1]/height
        screen.blit(ascii_dict[data], (colpos, rowpos))


frame = 0


def Loop():
    global frame
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    Visualize(video_data[frame])
    frame += 1
    if(frame >= len(video_data)):
        frame = 0

    pg.display.flip()
    setfps.tick(FPS)


while True:
    Loop()
