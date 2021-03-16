from flask import Flask, Response, request, abort, jsonify, render_template, session
import json
import logging
import os

import requests
import yaml

from src.gateway import *
from src.models.shared import *

def create_app(config=None):
    app = Flask(__name__)
    # load app sepcified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    # setup_app(app)
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

app = create_app({
    'SECRET_KEY': 'secret',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    # 'SQLALCHEMY_DATABASE_URI': DB_CONNECTION_STRING,
})


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


'''
Setting up discord webhook with heroku and travis
'''
PAYLOAD_TITLE = "[{repository[name]}:{branch}] Build #{number} {result_text}"
PAYLOAD_DESCRIPTION = "[`{commit:.7}`]({url}) {message}"
PAYLOAD_COMMIT_URL = "https://github.com/{repository[owner_name]}/{repository[name]}/commit/{commit}"
with open("config.yaml") as file:
    config = yaml.load(file)

DISCORD_WEBHOOK = config["discord-webhook"]
COLORS = config["colors"]


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.form["payload"]
    data = json.loads(data)

    # Force lower because yaml uses lower case
    result = data["status_message"].lower()

    color = COLORS[result]

    time = "started_at" if result == "pending" else "finished_at"

    # PHP example just uses array() but that doesn't make sense...
    # Idk, should ask someone who PHPs
    payload = {
        "username": "Travis CI",
        "avatar_url": "https://i.imgur.com/kOfUGNS.png",
        "embeds": [{
            "color": color,
            "author": {
                "name": data["author_name"]
                # TODO: See if author username can be found in
                # Travis' payload, and then
                # `"icon_url" : "https://github.com/USERNAME.png`
                # as described in https://stackoverflow.com/a/36380674
            },
            "title": PAYLOAD_TITLE.format(**data, result_text=result.capitalize()),
            "url": data["build_url"],
            "description": PAYLOAD_DESCRIPTION.format(**data, url=PAYLOAD_COMMIT_URL.format(**data)),
            "timestamp": data[time]
        }]
    }

    resp = requests.request("POST", DISCORD_WEBHOOK, json=payload, headers={"Content-Type": "application/json"})

    # https://stackoverflow.com/a/19569090
    return resp.text, resp.status_code, resp.headers.items()


@app.errorhandler(500)
def server_error(e):
    logging.exception("Error :/")
    return """
    Idk, server error :/
    <pre>{}</pre>
    sorry
    """.format(e), 500
