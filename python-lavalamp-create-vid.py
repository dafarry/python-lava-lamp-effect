#!/usr/bin/env python3

import numpy as np
from subprocess import Popen, PIPE

width, height, colors = 720, 480, 255
ymax, xmax = 3.5, 5
frames = 500

rgbcolors = np.uint8([[253,231,36],[78,1,94]])
y, x = np.ogrid[ymax:-ymax:height*1j, -xmax:xmax:width*1j]
cy, cx = np.cos(2 * y), np.cos(2 * x)
ppmheader = b"P6\n%d %d\n%d\n" % (width, height, colors)

ffmpeg = ('ffmpeg -y -f image2pipe -vcodec ppm -r 30 '
          '-i - -pix_fmt yuv420p lavalamp-vid.mp4')
pipe = Popen(ffmpeg.split(), stdin=PIPE)

for frame in range(frames):
    phase = 2 * np.pi * frame / frames
    plane = cx * np.cos(y + phase) > cy * np.sin(y + phase)
    rgbimg = rgbcolors[plane.astype(np.uint8)].tobytes()
    pipe.stdin.write(ppmheader + rgbimg)
    
pipe.stdin.close()
pipe.wait()


