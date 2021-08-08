import json
import PIL.Image
import pygame as pg
from utils.ImgToASCII import ImgToASCII
import cv2
from tqdm import tqdm
import moviepy.editor as mp
import time

SETTINGS = {}

with open("config.json") as config:
    SETTINGS = json.load(config)

ASCII_CHARS = [x for x in SETTINGS["ASCIIArray"]]
IMG_WIDTH = SETTINGS["ImageWidth"]
SCREEN_RES = tuple(int(r) for r in SETTINGS["ScreenResolution"].split(' '))
FONT_LOC = SETTINGS["fontName"]
FONT_SIZE = round(SETTINGS["fontSizeAt120p"] * 120 / IMG_WIDTH)
BRIGHTNESS = SETTINGS["Brightness"]


pg.init()
pg.display.set_caption("ASCII Art Visualizer")

screen = pg.display.set_mode(SCREEN_RES)
setfps = pg.time.Clock()
font = pg.font.Font(FONT_LOC, FONT_SIZE)

VIDEO = "assets/" + input("Enter filename (put in assets folder): ") + ".mp4"

vidcap = cv2.VideoCapture(VIDEO)
vid_fps = vidcap.get(cv2.CAP_PROP_FPS)
vid_length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
vid_duration = vid_length/vid_fps


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


print("Processing ASCII Characters...")
ascii_dict = {}
for c in tqdm(ASCII_CHARS):
    ascii_dict[c] = font.render(c, True, (BRIGHTNESS, BRIGHTNESS, BRIGHTNESS))
print("Processing ASCII Characters Done!")


print("Processing Video...")
for _ in tqdm(range(vid_length)):
    success, image = vidcap.read()
    if not success:
        break
    process_frame(image)
print("Process Video Done!")


def Visualize(pixels):
    for index, data in enumerate(pixels):
        row = index/width
        col = index % width
        rowpos = row*SCREEN_RES[0]/width
        colpos = col*SCREEN_RES[1]/height
        screen.blit(ascii_dict[data], (colpos, rowpos))


frame = 0


def Loop():
    global frame, start_time
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                music.stop()
                frame = 0
                start_time = time.time()
                music.play()

    Visualize(video_data[frame])
    frame += 1
    if(frame >= len(video_data)):
        time_used = time.time() - start_time
        performance: float = vid_duration / time_used
        performance = 1 if performance > 1 else performance
        print(f"Performance Result: {performance * 100}%")
        benchmark_score = 100 * performance**3 * \
            (IMG_WIDTH/120)**2 * (SCREEN_RES[0]*SCREEN_RES[1]/(1280*720))**1.2
        print(f"Benchmark Score: {benchmark_score}")

        frame = 0
        start_time = time.time()
        music.play()

    pg.display.flip()
    setfps.tick(vid_fps)


start_time = time.time()
music.play()

while True:
    Loop()
