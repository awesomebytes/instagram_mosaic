#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

18/07/15
@author: Sammy Pfeiffer

get_ig_profile_photo.py downloads
the profile photo of a given instagram username
if it exists.

"""

import sys
import requests
import shutil

def chars_until_quotes(mystr):
    for i in range(400):
        if mystr[i] == '"':
            return i
    return None

def get_user_image_url(web_str):
    """
    Given the website string return the url of the user image
    :param web_str: the website in a string format
    :return: str with the url of the user image
    """
    # The user image is found in this tag
    interesting_prop = '<meta property="og:image" content="'
    try:
        initial_index = web_str.index(interesting_prop) + len(interesting_prop)
    except ValueError:
        #print "ERROR: substring not found"
        return None
    # The url changes of size, so just check in the next 400 characters for the closing quotes
    image_url_len = chars_until_quotes(web_str[initial_index:initial_index+400])
    if not image_url_len:
        #print "ERROR: No url found for user image"
        return None
    user_img_url = web_str[initial_index:initial_index + image_url_len]
    print "User profile image url: " + user_img_url
    return user_img_url


def download_image(image_url, filename, path=None):
    """Given an image url and a filename, download that image"""
    response = requests.get(image_url, stream=True)
    if path:
        # add slash before filename if not set
        if path[-1] != "/":
            path += "/"
        filename = path + filename
    with open(filename + '.jpg', 'wb') as out_file: # if something is not jpg, im sorry!
        shutil.copyfileobj(response.raw, out_file)
    print "Saved " + filename + ".jpg"


def get_profile_photo_from_username(username, filename=None):
    ig_url = "http://instagram.com/"
    print "Getting profile photo of " + username + " at: " + ig_url + username
    # Get the website
    r = requests.get(ig_url+username)
    web_str = r.content
    # Parse it for the user image url
    user_img_url = get_user_image_url(web_str)

    if user_img_url:
        # Download image with username
        if filename is None:
            filename = username

        download_image(user_img_url, filename)
    else:
        print "Username not found."


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You must provide an instagram username to download their profile photo."
        print "Usage:"
        print sys.argv[0] + " username"
        exit(0)
    username = sys.argv[1]
    get_profile_photo_from_username(username)

