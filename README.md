Let's make mosaics from instagram photos!

===

Recently I did some web scrapping finding users in instagram and their profile photo and I thought I could play a bit more with it.

Years ago I also played with making mosaics from photos using python for a project in the university, let's mix both things.

I plan to create a mosaic of the profile photo of an instagram user using their own photos.

===

Our tools:

* Ubuntu 14.04
* Python 2.7
* `requests` python library
* `osaic` [python library for doing mosaics](https://pypi.python.org/pypi/osaic/2.0.0)
* `python-instagram` [instagram official python API](https://github.com/Instagram/python-instagram)

To install osaic correctly I needed to do:

    # Make sure I have the necessary libraries
    sudo apt-get install libjpeg-dev libfreetype6-dev zlib1g-dev libpng12-dev
    # soft link some stuff
    sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
    sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
    sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib
    sudo ln -s /usr/include/freetype2 /usr/include/freetype
    # install PIL with these extra flags
    sudo pip install PIL --allow-external PIL --allow-unverified PIL
    # install osaic
    sudo pip install osaic

===

First step, let's get the profile photo of a user.

I've done that in `get_ig_profile_photo.py` using the requests library to get the website of an user (http://instagram.com/username) and parsing the website finding the place where the profile photo url is found.

The profile photo is in the tag `<meta property="og:image" content="`. So I search for the next closing quotes to get the url. The url looks like:
https://igcdn-photos-h-a.akamaihd.net/hphotos-ak-xfa1/t51.2885-19/11428697_944597985591767_1329843489_a.jpg

Once I have the url I download the user photo and save it to disk using the requests library again `requests.get(user_img_url, stream=True)`.

The final result is executing:

    > ./get_ig_profile_photo.py r0sw3l
	Getting profile photo of r0sw3l at: http://instagram.com/r0sw3l
	User profile image url: https://igcdn-photos-h-a.akamaihd.net/hphotos-ak-xfa1/t51.2885-19/11428697_944597985591767_1329843489_a.jpg
	Saved r0sw3l.jpg

Which downloads my IG profile photo:

![r0sw3l's profile photo](https://raw.githubusercontent.com/awesomebytes/instagram_mosaic/master/r0sw3l.jpg)

Which interestingly is a 150x150px jpeg image, you can check it using imagemagick's `identify` command line tool. (`sudo apt-get install imagemagick`)
    > identify r0sw3l.jpg 
    r0sw3l.jpg JPEG 150x150 150x150+0+0 8-bit DirectClass 9.44KB 0.000u 0:00.000

===








