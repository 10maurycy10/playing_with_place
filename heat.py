# Generates a heat map from a images with names passed in on stdin.
import sys
from tqdm import tqdm
import numpy as np
from PIL import Image, ImageDraw
import imageio as iio

video_res = (1000,1000)

mult = 1

fps = 60

# use iio to create video
video = iio.get_writer('out.mp4', fps=fps, mode='I')

# buffer for last frame
last_img = Image.new('RGB', video_res, color = 'black')

for i in tqdm(sys.stdin.readlines()):
    # open and convert to RGB
    img = Image.open(i.rstrip()).convert('RGB')
    # subtract imadges
    diff = np.array(last_img) - np.array(img)
    # scale diffs and clamp to 8 bits
    diffimg = abs(diff * mult).clip(0, 255)
    last_img = img
    # save diff to video
    video.append_data(np.uint8(diffimg))

video.close()
