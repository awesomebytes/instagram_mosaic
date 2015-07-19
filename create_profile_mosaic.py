#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

18/07/15
@author: Sammy Pfeiffer

create_mosaic.py

"""

from get_ig_profile_photo import get_profile_photo_from_username
from download_ig_user_images import download_user_images
from ig_client_data import my_client_id, my_client_secret

import osaic
import sys

def get_mosaic_from_username(username, client_id, client_secret, number_of_photos=50):
    profile_filename_path = get_profile_photo_from_username(username)
    print "Profile photo at: " + profile_filename_path
    folder_images, filenames = download_user_images(username, my_client_id,
                                                    my_client_secret, number_of_photos=number_of_photos)
    print "Downloaded images at: " + folder_images

    images_with_path = []
    prev_path = folder_images + "/"
    for img in filenames:
        images_with_path.append(prev_path + img)

    profile_image = profile_filename_path
    profile_mosaic_path = profile_filename_path.replace(".jpg", "_mosaic.jpg")
    print "Creating mosaic at: " + profile_mosaic_path
    # TODO: parametrize and at least do 3 settings of mosaicify (tiles and zoom)
    # also probably paralellized creation of them with names corresponding to the quality
    osaic.mosaicify(
        target=profile_image,
        sources=images_with_path,
        tiles=128,
        zoom=8,
        output=profile_mosaic_path,
    )
    return profile_mosaic_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "You must provide an instagram username and optionally the amount of images to download"
        print "Usage:"
        print sys.argv[0] + " username 50"
        exit(0)
    username = sys.argv[1]
    if len(sys.argv) == 3:
        number_of_photos = int(sys.argv[2])
    else:
        number_of_photos = 50
    get_mosaic_from_username(username, my_client_id, my_client_secret, number_of_photos)
    print "Done"

