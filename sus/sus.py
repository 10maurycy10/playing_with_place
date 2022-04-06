import sys
from tqdm import tqdm
import numpy as np
from PIL import Image, ImageDraw

# nano sus
# 111
# 122
# 111
# 1 1

# nano sus + backpack
# 1111
# 1122
#  111
#  1 1

suses = [
    # 111
    # 122
    # 111
    # 1 1
    [
        [1,1,1],
        [1,2,2],
        [1,1,1],
        [1,0,1]
    
    ],
    # 1111
    # 1122
    #  111
    #  1 1
    [
        [1,1,1,1],
        [1,1,2,2],
        [0,1,1,1],
        [3,1,5,1]
    ],
    #  111
    # 1122
    # 1111
    #  1 1
    [
        [0,1,1,1],
        [1,1,2,2],
        [1,1,1,1],
        [3,1,4,1]
    ]
]

img = Image.open("test.png")

img = np.array(img)

susmap = np.ndarray((img.shape[0], img.shape[1]))
susmap.fill(0)

if img.ndim != 2:
    print("image not grayscale or indexed, bailing")
    exit(1)
    
def sustest(x, y, sus):
    #print(sus)
    if img.shape[0] < len(sus) + x:
        return False
    # buffer to store assocations between the color in the sus template and actual colors
    buf = [None,None,None,None,None,None,None,None,None,None,None,None]
    for susx in range(len(sus)):
        if img.shape[1] < len(sus[susx]) + y:
            return False
        for susy in range(len(sus[susx])):
            img_color_idx = img[x + susx][y + susy]
            sus_idx = sus[susx][susy]
            #if sus_idx != 0:
            if buf[sus_idx] == None:
                buf[sus_idx] = img_color_idx
            else:
                if img_color_idx != buf[sus_idx]:
                    #print("Regecting sus at " + str(x) + "," + str(y) + " is " + str(img_color_idx) + " should be " + str(buf[sus_idx]))
                    return False
    #print(buf)
    # Ensure buffer has no duplicats, we dont want to classify empty space as sus
    for i in range(len(buf)):
        if buf[i] != None:
            for e in range(len(buf)):
                if buf[i] == buf[e] and e != i:
                    #print("regecting sus " + str(i) + "," + str(e))
                    return False
    return True
    
sus_count = 0
for x in tqdm(range(img.shape[0])):
    for y in range(img.shape[1]):
        for sus in suses:
            if sustest(x,y,sus):
                print("found sus: " + str(x) + "," + str(y))
                sus_count = sus_count + 1
                susmap[x][y] = susmap[x][y] + 1

print("found " + str(sus_count) + " amungi")

susmap = (susmap * 255).clip(0,255)
Image.fromarray(np.uint8(susmap)).save("map.png")
