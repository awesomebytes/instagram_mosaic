Let's make mosaics from instagram photos!

![r0sw3l's profile photo mosaic](https://raw.githubusercontent.com/awesomebytes/instagram_mosaic/master/user_downloads/r0sw3l_mosaic.jpg)

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

First step, let's get the profile photo of a user, but I don't want to get into the Instagram API yet.

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

Now we need to download images, or even better, thumbnails of the user last images. For this we need to use instagram's API. This is done in `download_ig_user_images.py`.

First off you will need to register your app at https://instagram.com/developer/ to get a `client id` and a `client secret`. To use my code you'll need to edit `ig_client_data.py` and put your own keys at the lines:

    my_client_id = "288d2c1b60dc425ea9689f886d5ed011"
    my_client_secret = "99a3f8f308ee461fb85d2127371af411"

(These keys are not real, but they are as long as real ones).

First thing I discovered is that Instagram's API uses the user ID for doing queries. So I needed a way to get the user ID from the username, thanks to [this stackoverflow question](http://stackoverflow.com/questions/11796349/instagram-how-to-get-my-user-id-from-username) I got it right.

We need to do an API call to `"https://api.instagram.com/v1/users/search?q=" + username + "&client_id=" + client_id` with the username, there we will get a JSON string with the users that start with the given username and their fields: 'username', 'id', 'profile_picture' and 'full_name'.

Then we can do an api call to `user_recent_media(user_id=user_id)` which uses a pagination scheme which I figured out thanks to [this other stackoverflow thread](http://stackoverflow.com/questions/23442696/what-does-next-mean-here-python-instagram-api). When you do:

    recent_media, next = api.user_recent_media(user_id=userid)

You get the `recent_media` structure and a `next` object that you can use to get the next page:

    more_media, next = api.user_recent_media(with_next_url=next)

Also this media is a JSON structure [documented here](https://instagram.com/developer/endpoints/media/) (click on RESPONSE in the /media/media-id)

The interesting bit:

    "images": {
        "low_resolution": {
            "url": "http://distillery.s3.amazonaws.com/media/2010/07/16/4de37e03aa4b4372843a7eb33fa41cad_6.jpg",
            "width": 306,
            "height": 306
        },
        "thumbnail": {
            "url": "http://distillery.s3.amazonaws.com/media/2010/07/16/4de37e03aa4b4372843a7eb33fa41cad_5.jpg",
            "width": 150,
            "height": 150
        },
        "standard_resolution": {
            "url": "http://distillery.s3.amazonaws.com/media/2010/07/16/4de37e03aa4b4372843a7eb33fa41cad_7.jpg",
            "width": 612,
            "height": 612
        }

There is already a thumbnail, cool! I access it doing `media.images['thumbnail'].url` as you'll see in the code.

Then I did a little function to generate a basic webpage with the last photos, so we can execute:

    > python download_ig_user_images.py r0sw3l
    Username: r0sw3l userdata is: {u'username': u'r0sw3l', u'profile_picture': u'https://igcdn-photos-h-a.akamaihd.net/hphotos-ak-xfa1/t51.2885-19/11428697_944597985591767_1329843489_a.jpg', u'id': u'41404550', u'full_name': u'Sam'}
    r0sw3l IG user id is: 41404550
    Querying for images...
    Querying for extra images... (Got 20 until now)
    Querying for extra images... (Got 40 until now)
    Querying for extra images... (Got 60 until now)
    Querying for extra images... (Got 80 until now)
    Got 91 last r0sw3l thumbnail photos
    Created: user_r0sw3l_last_photos.html

You can check the simple web generated [here](http://htmlpreview.github.io/?https://raw.githubusercontent.com/awesomebytes/instagram_mosaic/master/user_r0sw3l_last_photos.html).

===

Having a profile photo and thumbnails, we should now generate a mosaic, shouldn't we?

Well now we just grab the profile photo, grab the last images of the user, and call mosaic with both things and some default parameters!

This is implemented in `create_profile_mosaic.py`.

And the final results are:

![r0sw3l's profile photo mosaic](https://raw.githubusercontent.com/awesomebytes/instagram_mosaic/master/user_downloads/r0sw3l_mosaic.jpg)



