from flask import Flask, Response, request, abort, jsonify, render_template, make_response, session, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img
import json
import logging
import os

import requests
import yaml

import time

from gateway import *
'''
App setup
'''
def create_app(app, config=None):
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

###############################################
#      Define navbar with logo                #
###############################################
logo = img(src='https://power-forward.web.app/images/PowerForward_icon.png', width="50", style="margin-top:-15px")
#here we define our menu items. Add as needed
topbar = Navbar(View(logo, 'index'),
                View('Home', 'index'),
                View('Map', 'map'),
                View('Simulate', 'simulate'),
                View('Charging Station Map', 'display_charging_station_map'),
                View('Utilization Rates Map', 'display_utilization_map'),
                View('Team', 'display_team')
                )
## 00FF87 neon green;; 40A025 dark green;; 0CC166
# registers the "top" menubar
nav = Nav()
nav.register_element('top', topbar)

###############################################
#          Define flask app                   #
###############################################

app = Flask(__name__)
Bootstrap(app)
###############################################
#             Init and confis our app         #
###############################################
app.jinja_env.cache = {}
app.config["CACHE_TYPE"] = "null"
nav.init_app(app)
if __name__ == '__main__':
    ## setup app
    app = create_app(app, {
        'SECRET_KEY': 'secret',
        'SQLALCHEMY_TRACK_MODIFICATIONS': True,
        # 'SQLALCHEMY_DATABASE_URI': DB_CONNECTION_STRING,
    })

    ## run web server
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))


'''
App Routes
'''

@app.route('/base')
def base():
    return render_template('/base.html')

@app.route('/')
def index():
    template = render_template('index.html',
                                parallax="parallax",
                                jumbo_logo="https://power-forward.web.app/images/PowerForward_Cropped.png",
                                layer="layer")
    response = make_response(template)
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
    return response

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
        print(form_param)
        posted = { 'params': query_string_params, 'data': data_params , 'form_param': form_param}
        return render_template( 'healthcheck.html',
                                title='Healthcheck',
                                ttr={'time of response': time.time(), 'date': datetime.now()},
                                echo=posted)


@app.route('/charging-station-map')
def display_charging_station_map():
    return render_template('charging-station-map.html', title='Charging Station Map')

@app.route('/utilization-map')
def display_utilization_map():
    return render_template('utilization-map.html', title='Utililzation Rates Map')

@app.route('/map', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        print('GOT A MAP POST')
        ## Query parameter argumeents
        query_string_params = request.args
        print(query_string_params)
        data_params = request.get_json()
        lat = query_string_params['lat']
        long = query_string_params['long']
        print(data_params)

        ## Shouldl return a utilization rate
        predicted_utilization_rate  = predict_utilization_rate(lat, long)
        print('RECEVIED coordinattes: ', lat, long, predicted_utilization_rate)
        return {'utilization-rate': predicted_utilization_rate}
    if request.method == 'GET':
        return render_template('map.html',  title='Map')

@app.route('/team')
def display_team():
    if request.method == 'GET':
        return render_template('team.html', title='Team')



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

@app.route("/simulate", methods=['GET', 'POST'])
def simulate():
    data  = [
        ("01-01-2020", 1597),
        ("02-01-2020", 1456),
        ("03-01-2020", 1908),
        ("04-01-2020", 896),
        ("05-01-2020", 755),
        ("06-01-2020", 453),
        ("07-01-2020", 1100),
        ("08-01-2020", 1235),
        ("09-01-2020", 1478),
    ]
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    pois_dict = {
            'lodging': {"label": "Lodging", "max_val":20},
            'supermarket': {"label": "Supermarket", "max_val":20},
            'pharmacy': {"label": "Pharmacy", "max_val":20},
            'park': {"label": "Park", "max_val":20},
            'restaurant': {"label": "Restaurant", "max_val":20},
            'clothing_store': {"label": "Clothing Store", "max_val":20},
            'store': {"label": "Store", "max_val":20},
            'school': {"label": "School", "max_val":20},
            'gym': {"label": "Gym", "max_val":20},
            'library': {"label": "Library", "max_val":20},
            'local_government_office': {"label": "Local Government Office", "max_val":20},
            'doctor': {"label": "Doctor", "max_val":20},
            'stadium': {"label": "Stadium", "max_val":20},
            'museum': {"label": "Museum", "max_val":20},
            'church': {"label": "Church", "max_val":20},
            'synagogue': {"label": "Synagogue", "max_val":20}
           }

    if request.method == 'GET':
        return render_template("simulate.html", title='Simulate', labels=labels, values=values, pois=pois_dict)
    else:
        # print('WE GOT POST')
        ## Query parameter argumeents
        form_dict = request.form
        sanitized_dict = {}
        for k, v in form_dict.items():
            # print("KEY: ", k)
            delimiter = ['Number', 'Range']
            for d in delimiter:
                if d in k:
                    cutoff_idx = len(d)
                    # print(k[:-cutoff_idx])
                    stored_k = k[:-cutoff_idx]
                    sanitized_dict[stored_k] = int(v)

        # print(type(sanitized_dict), sanitized_dict)
        # time = [i for i in range(168)]
        # import random
        # rates = [random.random() for i in range(168)]

        data = predict_week_timeseries_utilization_rate(sanitized_dict)
        # data = {"ur": [{'time':t, 'rate':r} for t, r in zip(time, rates)] }

        # response = app.response_class(
        #     response=json.dumps(data),
        #     status=200,
        #     mimetype='application/json'
        # )
        return jsonify(data)
        # return render_template("simulate.html", title='Simulate', labels=labels, values=values, pois=pois_dict)


'''
Edge
'''
@app.before_request
def before_request_func():
    is_not_image_people_request = "people" not in request.url
    is_not_discordbot_request = "Discordbot" not in request.headers.get('User-Agent')
    # if is_not_image_people_request and is_not_discordbot_request:
    #     analytics(request)


@app.errorhandler(500)
def server_error(e):
    logging.exception("Error :/")
    return """
    Idk, server error :/
    <pre>{}</pre>
    sorry
    """.format(e), 500


'''
Server Requests

'''

@app.route('/suggest-city', methods=['POST'])
def suggest_city():
    '''
    Colleecting user feedback from home page
    '''
    city = request.form['city']
    email = request.form['email']
    state = request.form['state']
    print('Recived: ', city, email)
    success = collect_suggestion(city, state, email)

    return redirect(url_for('index'), )


# @app.route('/api/')
