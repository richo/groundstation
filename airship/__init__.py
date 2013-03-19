import os
import json
import time

from flask import Flask, render_template, request

from groundstation import logger
log = logger.getLogger(__name__)

# XXX We won't always be using the github adaptor!!
from groundstation.protocols import github as github_protocol
from groundstation.gref import Gref

import pygit2
from groundstation.utils import oid2hex

from groundstation.objects.update_object import UpdateObject

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
        marshalled_thread = adaptor.get_issue(gref)
        root_obj = marshalled_thread["roots"].pop()
        root = root_obj.as_json()
        root["hash"] = oid2hex(pygit2.hash(root_obj.as_object()))

        response = []

        while marshalled_thread["thread"]:
            node = marshalled_thread["thread"].pop()
            data = json.loads(node.data)
            data["parents"] = list(node.parents)
            data["hash"] = oid2hex(pygit2.hash(node.as_object()))
            response.append(data)
        return jsonate({"content": response, "root": root, "tips": marshalled_thread["tips"]}, False)

    @app.route("/gref/<channel>/<path:identifier>", methods=['POST'])
    def update_gref(channel, identifier):
        # adaptor = github_protocol.GithubWriteAdaptor(station, channel)
        gref = Gref(station.store, channel, identifier)
        # Ugly type coercion
        user = request.form["user"]
        body = request.form["body"]
        parents = map(str, json.loads(request.form["parents"]))
        payload = {
                "type": "comment",
                "id": None,
                "body": body,
                "user": user
                }
        update_object = UpdateObject(parents, json.dumps(payload))
        oid = station.write(update_object.as_object())
        station.update_gref(gref, [oid], parents)
        return jsonate({"response": "ok"}, False)

    return app
