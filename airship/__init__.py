import os
import json
import time

from flask import Flask, render_template

from groundstation import logger
log = logger.getLogger(__name__)

# XXX We won't always be using the github adaptor!!
from groundstation.protocols import github as github_protocol
from groundstation.gref import Gref

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
        return render_template("index.html",
                channels_json=channels_json(station, True),
                current_time=time.time())

    @app.route("/debug")
    def index():
        return render_template("debug.html",
                channels_json=channels_json(station, True),
                current_time=time.time())

    @app.route("/channels")
    def list_channels():
        return channels_json(station)

    @app.route("/grefs/<channel>")
    def list_grefs(channel):
        return grefs_json(station, channel)

    @app.route("/gref/<channel>/<path:identifier>")
    def fetch_gref(channel, identifier):
        adaptor = github_protocol.GithubReadAdaptor(station, channel)
        gref = Gref(station.store, channel, identifier)
        log.info("Trying to fetch channel: %s identifier: %s" %
                (channel, identifier))
        thread = adaptor.get_issue(gref)
        root = thread.pop()

        response = []

        while thread:
            node = thread.pop()
            data = json.loads(node.data)
            response.append(data)
        return jsonate({"content": response}, False)

    return app
