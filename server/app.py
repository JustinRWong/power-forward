from flask import Flask, Response, request, abort, jsonify, render_template, session
import json
import logging
import os

import requests
import yaml

from src.gateway import *
from src.models.shared import *
from src.models.saferproxyfix import SaferProxyFix
'''
App setup
'''
def create_app(config=None):
    # load app sepcified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    # setup_app(app)

    # app.wsgi_app = SaferProxyFix(app.wsgi_app) # may not be needed
    return app

# def setup_app(app):
    # Create tables if they do not exist already
    # @app.before_first_request
    # def create_tables():
    #     db.create_all()

    # session = flask_scoped_session(session_factory, app)
    # db.init_app(app)
    # config_oauth(app)
    # app.register_blueprint(bp, url_prefix='')
app = Flask(__name__)
if __name__ == '__main__':
    ## setup app
    app = create_app({
        'SECRET_KEY': 'secret',
        'SQLALCHEMY_TRACK_MODIFICATIONS': True,
        # 'SQLALCHEMY_DATABASE_URI': DB_CONNECTION_STRING,
    })
    ## run web server
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))


'''
App Routes
'''
@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/__healthcheck__', methods=['GET', 'POST'])
def health_check():
    '''
    Health check responds for GET and POST
    GET: returns time time of server receiving request.
    POST: echos parameters and data passeed by request.
    '''
    ## Query parameter argumeents
    query_string_params = request.args

    ## data parameters from http request
    data_params = request.get_json()
    print(data_params)
    if request.method == 'GET':
        posted = { 'params': query_string_params, 'data': data_params}
        return render_template( 'healthcheck.html',
                                title='Healthcheck',
                                ttr={'time of response': time.time(), 'date': datetime.now()},
                                echo=posted)

    if request.method == 'POST':
        form_param = request.form['form_param']
        posted = { 'params': query_string_params, 'data': data_params , 'form_param': form_param}
        return render_template( 'healthcheck.html',
                                title='Healthcheck',
                                ttr={'time of response': time.time(), 'date': datetime.now()},
                                echo=posted)

@app.route('/team')
def display_team():
    return render_template('team.html', title='Team')

@app.route('/map')
def display_map():
    return render_template('map.html', title='Map')

@app.route('/discord', methods=['GET', 'POST'])
def discord():
    '''
    Require a specific token "X-POWER-FORWARD-TOKEN"
    in order to access a page that sends a message directly
    to the discord channel.
    '''
    ## validate a token X-POWER-FORWARD-TOKEN to send direct discord messages
    successful, msg = validate_PF_API_token(request.headers)
    if (not successful):
            # abort(401, success_msg)
            return Response(response={ msg },
                            status=401), 400, {'ContentType':'application/json'}

    if request.method == 'GET':
        return render_template('discord.html', title='Discord messaging')
    if request.method == 'POST':
        ## extract username and message from form
        username = request.form['username']
        message = request.form['message']

        payload = {
            'username': "Justin's Local",
            'avatar_url': "",
            'content': message
        }
        send_to_discord(payload)
        return "pshed"

'''
Edge
'''
@app.before_request
def before_request_func():
    is_not_image_people_request = "people" not in request.url
    is_not_discordbot_request = "Discordbot" not in request.headers.get('User-Agent')
    if is_not_image_people_request and is_not_discordbot_request:
        analytics(request)


@app.errorhandler(500)
def server_error(e):
    logging.exception("Error :/")
    return """
    Idk, server error :/
    <pre>{}</pre>
    sorry
    """.format(e), 500
