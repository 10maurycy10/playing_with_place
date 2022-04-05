# Generates a all time log scale heat map from a images with names passed in on stdin.
import sys
from tqdm import tqdm
import numpy as np
from PIL import Image, ImageDraw

fps = 60

last_img = np.array(Image.new('RGB', (1000,1000), color = 'black'))

total_diff = np.ndarray((1000,1000,3))
total_diff.fill(0.0)

for i in tqdm(sys.stdin.readlines()):
    # open image and convert to Palatized
    img = Image.open(i.rstrip()).convert('RGB')
    img = np.array(img)
    # Subtract from last capture
    diff = img - last_img
    #diff = last_img - img
    # Sum the diffs
    total_diff = total_diff + abs(diff)
    last_img = img

# Compute log base e of all pixels, the +1 is the avoid taking log(0)
log_diff = np.log(total_diff + 1)
m = log_diff.max()

# normalize the logs to 0 - 255, with sif
#m = m - 1
normlog = (log_diff / m * 255).clip(0, 255)
# convert to 8 bit unsigned and save as imadge
Image.fromarray(np.uint8(normlog)).save("total.png")
