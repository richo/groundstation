import os
import json

from flask import Flask, render_template


def jsonate(obj, escaped):
    jsonbody = json.dumps(obj)
    if escaped:
        jsonbody = jsonbody.replace("</", "<\\/")
    return jsonbody


def channels_json(station, escaped=False):
    channels = [{"name": channel} for channel in station.channels()]
    return jsonate(channels, escaped)


def grefs_json(station, channel, escaped=False):
    grefs = [gref.as_dict() for gref in station.grefs(channel)]
    return jsonate(grefs, escaped)


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
        return grefs_json(station, channel)

    return app
