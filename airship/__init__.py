import os
import json

from flask import Flask, render_template


def channels_json(station, escaped=False):
    channels = [{"name": channel} for channel in station.channels()]
    jsonbody = json.dumps(channels)
    if escaped:
        jsonbody = jsonbody.replace("</", "<\\/")
    return jsonbody


def make_airship(station):
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html", channels_json=channels_json(station, True))

    @app.route("/channels")
    def list_channels():
        return channels_json(station)

    @app.route("/grefs/<channel>")
    def list_grefs(channel):
        return


    return app
