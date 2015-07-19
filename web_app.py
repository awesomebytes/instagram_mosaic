#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

19/07/15
@author: Sammy Pfeiffer

"""
from bottle import Bottle, run
from bottle import get, post, request # or route
from bottle import static_file
from create_profile_mosaic import get_mosaic_from_username
from ig_client_data import my_client_secret, my_client_id




if __name__ == "__main__":
    print "Initializing Bottle web app"
    app = Bottle()

    # @app.route('/hello')
    # def hello():
    #     return "Hello World!"
    @app.route('/instamosaic') # or @route('/login')
    def offer_generation():
        return '''
            <form action="/instamosaic" method="post">
                Instagram username: <input name="username" type="text" />
                <input value="Generate mosaic" type="submit" />
            </form>
            Note that the user should not be private.
            The generation of the mosaic may take some time (a minute or more).
        '''

    @app.route('/instamosaic', method='POST') # or @route('/login', method='POST')
    def do_generation():
        username = request.forms.get('username')
        local_path_mosaic = get_mosaic_from_username(username, my_client_id, my_client_secret, 100)
        if local_path_mosaic:
            return "<p>Mosaic: </p>" + "<img src='/static/" + username + "_mosaic.jpg'/>"
        else:
            return "<p>Generation of mosaic failed.</p>"


    @app.route('/static/<filename>')
    def server_static(filename):
        return static_file(filename, root='/home/sam/mosaic_ws/user_downloads/')

    run(app, host='localhost', port=8080)