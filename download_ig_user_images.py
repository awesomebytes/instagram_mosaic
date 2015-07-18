#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

18/07/15
@author: Sammy Pfeiffer

download_ig_user_images.py downloads
the last X images from a instagram user

"""

import sys
import requests
import json
from instagram.client import InstagramAPI

# You need to register your own app with IG:
# https://instagram.com/developer/
# Here you can get some extra info if you want:
# http://darkwhispering.com/how-to/get-a-instagram-client_id-key

from ig_client_data import my_client_id, my_client_secret

def get_user_id_from_username(username, client_id):
    """
    Given an username and a client_id to be able to perform the api query
    return the user id of that username
    :param username: str representing the username
    :param client_id: the IG api client id
    :return: str as IG user id or None
    """
    user_data = get_user_data_from_username(username, client_id)
    if user_data is not None:
        user_id = user_data.get("id", None)
        print username\
              + " IG user id is: " + user_id
        return user_id

def get_user_data_from_username(username, client_id):
    """
    Given an username and a client_id to be able to perform the api query
    return the user data (id, profile_picture, full_name)
    :param username: str representing the username
    :param client_id: the IG api client id
    :return: dictionary with keys 'id', 'profile_picture', 'full_name'
    """
    user_id_url = "https://api.instagram.com/v1/users/search?q=" + username + "&client_id=" + client_id
    r = requests.get(user_id_url)
    # The answer is a json that looks like:
    # '{"meta":{"code":200},"data":[{"username":"r0sw3l","profile_picture":"https:\\/\\/igcdn-photos-h-a.akamaihd.net\\/hphotos-ak-xfa1\\/t51.2885-19\\/11428697_944597985591767_1329843489_a.jpg","id":"41404550","full_name":"Sam"},{"username":"r0sw3ll","profile_picture":"https:\\/\\/instagramimages-a.akamaihd.net\\/profiles\\/profile_31248139_75sq_1379872322.jpg","id":"31248139","full_name":"Roswell"}]}'
    dict = json.loads(r.content)
    data = dict.get("data", None)
    # Data is an array of users that start with the given username
    if data:
        for user_data in data:
            if user_data.get("username", None) == username:
                print "Username: " + username + " userdata is: " + str(user_data)
                return user_data
    # If we can't find anything, return None
    return None

def create_web_from_images(username, photo_urls_list):
    with open("user_" + username + "_last_photos.html", "w") as f:
        f.write("<html>\n<body>")
        for photo in photo_urls_list:
            f.write('<img src="%s"/>' % photo)
        f.write("</html>\n</body>")
    print "Created: " + "user_" + username + "_last_photos.html"


def get_last_media_thumbnails_urls_from_user(username, client_id, client_secret, number_of_photos=10):
    api = InstagramAPI(client_id=client_id, client_secret=client_secret)
    user_id = get_user_id_from_username(username, client_id)
    thumbnails_urls = []
    image_counter = 0
    print "Querying for images..."
    recent_media, next_ = api.user_recent_media(user_id=user_id)
    # First get of images, I was getting 33 when asking for 50, and 20 when not specifying
    for media in recent_media:
        image_counter += 1
        thumbnails_urls.append(media.images['thumbnail'].url)
        # If we have enough, stop here
        if image_counter > number_of_photos:
            return thumbnails_urls
    # Keep getting images until we are done
    while image_counter < number_of_photos:
        print "Querying for extra images... (Got " + str(image_counter) + " until now)"
        recent_media, next_ = api.user_recent_media(with_next_url=next_)
        for idx, media in enumerate(recent_media):
            image_counter += 1
            thumbnails_urls.append(media.images['thumbnail'].url)
            # if we have enough, also stop already
            if image_counter + idx + 1 > number_of_photos:
                return thumbnails_urls
    # Return what we got, if we didn't get to satisfy the quantity asked for
    return thumbnails_urls


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You must provide an instagram username to download their profile photo."
        print "Usage:"
        print sys.argv[0] + " username"
        exit(0)
    username = sys.argv[1]
    thumbnails_urls = get_last_media_thumbnails_urls_from_user(username, my_client_id,
                                                               my_client_secret, number_of_photos=100)
    print "Got " + str(len(thumbnails_urls)) + " last " + username + " thumbnail photos"
    create_web_from_images(username, thumbnails_urls)

