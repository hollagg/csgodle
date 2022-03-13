from flask import Flask, request, render_template, make_response, url_for, redirect, send_from_directory
import json
import requests
from csutils import *
import os

app = Flask(__name__)

# Get cookies, lot of this is taken from Fireblend's squirdle app which is dope af
def get_cookie_data(daily=''):
    # Cookies for daily session are prefixed with 'd_'
    prefix = 'd_' if daily else ''
    secret = request.cookies.get(prefix + 'secret_item')
    attempts = int(request.cookies.get(prefix + 't_attempts'))
    return secret, attempts

def show_game_state(is_daily):
    day = get_day_count() if is_daily else None
    secret, attempts = get_cookie_data(daily=is_daily)
    secret_split = secret.split("///")
    secret_present = secret_split[0] + " (" + secret_split[1] + ")"
    items = get_items_json()
    secret_thumb = items[secret_split[0]]["exterior"][secret_split[1]]["url"]
    imgs = [url_for('static', filename=f'{x}.png') for x in ['correct', 'up', 'down', 'wrong']]

    return render_template('daily.html' if is_daily else 'index.html', items=items, day=day,
        secret=secret, secret_present=secret_present, secret_thumb=secret_thumb, attempts=attempts, im=imgs)

# Sets cookies for new games
def handle_new_game(is_daily):
    expire_date = None
    # 24h, since daily
    if is_daily:
        expire_date = datetime.combine(datetime.date(datetime.now()-timedelta(hours=10)),
            datetime.min.time())+timedelta(days=1, hours=10)
    else:
        expire_date = datetime.date(datetime.now())+timedelta(days=7)

    prefix = 'd_' if is_daily else ''

    # Set cookies
    resp = make_response(redirect(url_for('daily' if is_daily else 'index')))
    resp.set_cookie(prefix+'secret_item', get_skin(daily=is_daily), expires=expire_date)
    resp.set_cookie(prefix+'t_attempts', '8', expires=expire_date)
    return resp

@app.route('/')
def index():
    # Set cookies if a new game is requested
    if not 'secret_item' in request.cookies:
        return handle_new_game(is_daily=False)
    return show_game_state(is_daily=False)

@app.route('/daily')
def daily():
    # Set cookies if a new game is requested
    if not 'd_secret_item' in request.cookies:
        return handle_new_game(is_daily=True)
    return show_game_state(is_daily=True)