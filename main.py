import json
import PIL.Image
import pygame as pg
from utils.ImgToASCII import ImgToASCII
import cv2
from tqdm import tqdm
import moviepy.editor as mp


SETTINGS = {}

with open("config.json") as config:
    SETTINGS = json.load(config)

ASCII_CHARS = [x for x in SETTINGS["ASCIIArray"]]
IMG_WIDTH = SETTINGS["ImageWidth"]
SCREEN_RES = tuple(int(r) for r in SETTINGS["ScreenResolution"].split(' '))
FONT_LOC = SETTINGS["fontName"]
FONT_SIZE = round(SETTINGS["fontSizeAt120p"] * 120 / IMG_WIDTH)

pg.init()
pg.display.set_caption("ASCII Art Visualizer")

screen = pg.display.set_mode(SCREEN_RES)
setfps = pg.time.Clock()
font = pg.font.Font(FONT_LOC, FONT_SIZE)

VIDEO = "assets/ご注文はうさぎですか？？ ED2.mp4"
vidcap = cv2.VideoCapture(VIDEO)
vid_fps = vidcap.get(cv2.CAP_PROP_FPS)
vid_length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

clip = mp.VideoFileClip(VIDEO)
clip.audio.write_audiofile(r"temp/temp.mp3")

music = pg.mixer.Sound("temp/temp.mp3")


video_data = []


def process_frame(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = PIL.Image.fromarray(img)
    raw_data = ImgToASCII(img, ASCII_CHARS, IMG_WIDTH)
    video_data.append(raw_data["data"])
    global height, width
    height = raw_data["dimension"][0]
    width = raw_data["dimension"][1]

print("Processing Video...")
for _ in tqdm(range(vid_length)):
    success, image = vidcap.read()
    if not success:
        break
    process_frame(image)
print("Process Video Done!")

print("Processing ASCII Characters...")
ascii_dict = {}
for c in tqdm(ASCII_CHARS):
    ascii_dict[c] = font.render(c, True, (255, 255, 255))
print("Processing ASCII Characters Done!")

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
        music.play()

    pg.display.flip()
    setfps.tick(vid_fps)

music.play()

while True:
    Loop()
