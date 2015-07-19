#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

18/07/15
@author: Sammy Pfeiffer

download_ig_user_images.py downloads
the last X images from a instagram user

"""

import sys
import os
import threading
import requests
import json
from instagram.client import InstagramAPI
from instagram.bind import InstagramAPIError

from get_ig_profile_photo import download_image

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


def get_last_media_thumbnails_urls_from_user(username, client_id, client_secret, number_of_photos=15):
    """Return a list of urls of thumbnails for the user,
    None if the user does not exist"""
    api = InstagramAPI(client_id=client_id, client_secret=client_secret)
    user_id = get_user_id_from_username(username, client_id)
    thumbnails_urls = []
    image_counter = 0
    print "Querying for images..."
    try:
        recent_media, next_ = api.user_recent_media(user_id=user_id)
    except InstagramAPIError as e:
        print "Error: instagram.bind.InstagramAPIError"
        print "Exact error: " + str(e)
        return None

    # First get of images, I was getting 33 when asking for 50, and 20 when not specifying
    for media in recent_media:
        image_counter += 1
        thumbnails_urls.append(media.images['thumbnail'].url)
        # If we have enough, stop here
        if image_counter >= number_of_photos:
            return thumbnails_urls
    # Keep getting images until we are done
    while image_counter < number_of_photos:
        print "Querying for extra images... (Got " + str(image_counter) + " until now)"
        try:
            recent_media, next_ = api.user_recent_media(with_next_url=next_)
        except InstagramAPIError:
            # No more images!
            break
        for idx, media in enumerate(recent_media):
            image_counter += 1
            thumbnails_urls.append(media.images['thumbnail'].url)
            # if we have enough, also stop already
            if image_counter >= number_of_photos:
                return thumbnails_urls
    # Return what we got, if we didn't get to satisfy the quantity asked for
    return thumbnails_urls


def download_user_images(username, client_id, client_secret, folder_to_download_path=None, number_of_photos=15):
    print "Downloading " + username + " last " + str(number_of_photos) + " images."
    thumbnails_urls = get_last_media_thumbnails_urls_from_user(username,
                                                               client_id,
                                                               client_secret,
                                                               number_of_photos=number_of_photos)
    if thumbnails_urls is None:
        return

    # Create folder
    if folder_to_download_path is None:
        current_path = os.getcwd()
        folder_to_download_path = current_path + "/user_downloads/" + username
    print "Creating folder: " + folder_to_download_path
    if not os.path.exists(folder_to_download_path):
        os.makedirs(folder_to_download_path)
    else:
        print "Folder " + username + " already exists, we may overwrite stuff."
    print "Downloading " + str(len(thumbnails_urls)) + " images"

    max_threads = 10
    print "Using "  + str(max_threads) + " threads to fasten the download."
    threads_list = []
    filenames = []
    args = []
    for idx, thumb_url in enumerate(thumbnails_urls):
        curr_filename = username + "_" + str(idx).zfill(2) + ".jpg"
        filenames.append(curr_filename)
        args.append([thumb_url, curr_filename, folder_to_download_path])
        threads_list.append(threading.Thread(target=download_image,
                                              args=(thumb_url, curr_filename, folder_to_download_path,)))

    # batch the execution in threads
    curr_threads_number = 0
    to_join_threads = []
    for thread in threads_list:
        thread.start()
        to_join_threads.append(thread)
        curr_threads_number += 1
        # When we get to the number of threads in the pool, start joining threads
        if curr_threads_number >= max_threads:
            print "batch of " + str(max_threads) + " completed, joining..."
            for to_join_thread in to_join_threads:
                to_join_thread.join()
            to_join_threads = []
            curr_threads_number = 0


    #download_image(thumb_url, curr_filename, path=folder_to_download_path)

    print "Finished downloading"
    return folder_to_download_path, filenames


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You must provide an instagram username to download their profile photo."
        print "Usage:"
        print sys.argv[0] + " username"
        exit(0)
    username = sys.argv[1]
    thumbnails_urls = get_last_media_thumbnails_urls_from_user(username, my_client_id,
                                                               my_client_secret, number_of_photos=100)
    if thumbnails_urls is not None:
        print "Got " + str(len(thumbnails_urls)) + " last " + username + " thumbnail photos"
        create_web_from_images(username, thumbnails_urls)

    print "\n\n"
    download_user_images(username, my_client_id, my_client_secret)



