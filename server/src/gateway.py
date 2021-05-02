from flask_sqlalchemy import SQLAlchemy
import requests, os
import json, time, hashlib
import datetime as dt
from urllib.parse import urlencode
import random

from models.shared import *
from engine.predictors import apply_knn_weekhour_model
# from models.saferproxyfix import SaferProxyFix

def validate_PF_API_token(headers):
    pf_token = headers.get('X-POWER-FORWARD-TOKEN')
    ## Search neon_token in database of accepted tokens
    if pf_token == None:
        return False, "Invalid Power Forward Token."
    else:
        return pf_token=='SweetToken', "Token received"

def send_to_discord(payload):
    '''
    Function to send a message to discord.
    Payloads should be a dictionary where
    `username` and `content` must be defined.
    '''
    ## relay message to discord channel via webook
    url = os.environ.get('DISCORD_WEBHOOK')
    if url:
        print('FOUND WEWBHOOK')
        print(url)

    response = requests.post(url, json=payload, params={'wait': True})
    return response.status_code

def analytics(req):
    '''
    Analytics collector that gets sent directly to our discord channel.
    '''
    ## get around mulitple proxies
    if req.headers.getlist("X-Forwarded-For"):
       ip = req.headers.getlist("X-Forwarded-For")[0]
    else:
       ip = req.remote_addr
    ip_address = ip
    url = req.url
    device = req.headers.get('User-Agent')
    current_time = dt.datetime.now()
    content_dict = {    "Visit Time":  current_time,
                        "Requester IP": ip_address,
                        "URL Visited": url,
                        "User Agent": device }
    content_str = "GOT A VISITOR!"

    ## store in mongo
    inserted_id = web_visitors.insert_one(content_dict)

    for k, v in content_dict.items():
        content_str = content_str + "\n  > {k}: {v}".format(k=k, v=v)

    payload = {
        'username': "Power Forward App Analytics :)",
        'content': content_str
    }

    send_to_discord(payload)
    #
    # google_analytics_data = {
    #     'v': '1',  # API Version.
    #     'tid': GA_TRACKING_ID,  # Tracking ID / Property ID.
    #     # Anonymous Client Identifier. Ideally, this should be a UUID that
    #     # is associated with particular user, device, or browser instance.
    #     'cid': '555',
    #     't': 'event',  # Event hit type.
    #     'ec': category,  # Event category.
    #     'ea': action,  # Event action.
    #     'el': label,  # Event label.
    #     'ev': value,  # Event value, must be an integer
    # }
    #
    # response = requests.post(
    #     'http://www.google-analytics.com/collect', data=data)
    #
    # # If the request fails, this will raise a RequestException. Depending
    # # on your application's needs, this may be a non-error and can be caught
    # # by the caller.
    # response.raise_for_status()

    return send_to_discord(payload)

def collect_suggestion(city, state, email):
    t = time.time()
    d = dt.datetime.fromtimestamp(t).strftime('%c').replace('  ', ' ').replace(' ', '_').replace(':', '-')
    stored_doc = {"city": city,
                  "state": state,
                  "email": email,
                  "time": t,
                  "datetime": d}
    ## store in mongo
    print('Inserting to db')
    inserted_id = web_suggestions.insert_one(stored_doc)
    print(inserted_id)
    return True

def predict_utilization_rate(lat, long):
    return random.random()

def predict_week_timeseries_utilization_rate(input_dict):
    order = ['lodging', 'supermarket', 'pharmacy', 'park', 'restaurant',
       'clothing_store', 'store', 'school', 'gym', 'library',
       'local_government_office', 'doctor', 'stadium', 'museum', 'church',
       'synagogue']
    x_vector = []
    for k in order:
        x_vector.append(input_dict[k])

    time, rates = apply_knn_weekhour_model(x_vector)
    # print(time, rates)

    return {"ur": [{'time':t, 'rate':r} for t, r in zip(time, rates)] }
