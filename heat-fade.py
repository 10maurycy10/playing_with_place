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
last_img = np.array(Image.new('RGB', video_res, color = 'black'))

out = np.array(Image.new("RGB", video_res, color="black"))

for i in tqdm(sys.stdin.readlines()):
    # open and convert to RGB
    img = np.array(Image.open(i.rstrip()).convert('RGB'))
    # subtract imadges
    diff = last_img - img
    # scale diffs and clamp to 8 bits
    diffimg = abs(diff * mult).clip(0, 255)
    last_img = img
    # save diff to video
    out = out + diffimg
    video.append_data(np.uint8(out))
    out = out * 0.9

video.close()
