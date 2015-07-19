#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

18/07/15
@author: Sammy Pfeiffer

create_mosaic.py

"""


import osaic
images = ["r0sw3l_00.jpg", "r0sw3l_01.jpg", "r0sw3l_02.jpg",
          "r0sw3l_03.jpg", "r0sw3l_04.jpg", "r0sw3l_05.jpg",
          "r0sw3l_06.jpg", "r0sw3l_07.jpg", "r0sw3l_08.jpg",
          "r0sw3l_09.jpg", "r0sw3l_10.jpg", "r0sw3l_11.jpg",
          "r0sw3l_12.jpg", "r0sw3l_13.jpg", "r0sw3l_14.jpg"]

images_with_path = []
prev_path = "/home/sam/mosaic_ws/user_downloads/r0sw3l/"
for img in images:
    images_with_path.append(prev_path + img)

profile_image = "/home/sam/mosaic_ws/r0sw3l.jpg"
osaic.mosaicify(
    target=profile_image,
    sources=images_with_path,
    tiles=128,
    zoom=8,
    output='/home/sam/mosaic_ws/mosaic_profile.png',
)

