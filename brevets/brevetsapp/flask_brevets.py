"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request, render_template, url_for, redirect
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from pymongo import MongoClient
import json
import os

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

#-------------------------------------------------------------------------
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevetsdb
#-------------------------------------------------------------------------

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    
    # FIXME!
    # ------------------------------------------------------------
    
    dist = request.args.get('dist', type=float)
    start = request.args.get('start', arrow.now(), type=str)
    arrow_start = arrow.get(start, 'YYYY-MM-DDTHH:mm')

    app.logger.debug("dist={}".format(dist))
    app.logger.debug("start={}".format(start))

    # -------------------------------------------------------------

    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    open_time = acp_times.open_time(km, 200, arrow.now().isoformat).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, 200, arrow.now().isoformat).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

'''
Incomplete yet.
#----------------------------------------------------------------------------------
@app.route("/display", methods = ["POST"])
def display():
    return flask.render_template('display.html', items=list(db.timestable.find()))


@app.route("/submit", methods=["POST"])
def submit():
    k = request.form.getlist("km")
    size = len(k)
    o = request.form.getlist("open")
    c = request.form.getlist("close")
    
    db.tododb.drop()
    
    for i in range(size):
        items = { 'km': k[i], 'open': o[i], 'close': c[i]}

    db.tododb.insert_one(items)

    return redirect(url_for('index'))
#------------------------------------------------------------------------------------
'''

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
