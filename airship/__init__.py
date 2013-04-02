import os
import json
import time

from flask import Flask, render_template, request

from groundstation import logger
log = logger.getLogger(__name__)

# XXX We won't always be using the github adaptor!!
from groundstation.protocols import github as github_protocol
from groundstation.gref import Gref, Tip

import pygit2
from groundstation.utils import oid2hex

from groundstation.objects.root_object import RootObject
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

    def set_signing_key(self, keyname):
        self.private_crypto_adaptor = \
                station.get_private_crypto_adaptor(keyname)
    app.set_signing_key = lambda key: set_signing_key(app, key)

    def _update_gref(gref, tips, parents):
        if app.private_crypto_adaptor:
            tips = map(lambda tip: Tip(tip.tip, app.private_crypto_adaptor.sign(tip.tip)), tips)
        station.update_gref(gref, tips, parents)

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
        crypto_adaptor = station.get_crypto_adaptor()
        adaptor = github_protocol.GithubReadAdaptor(station, channel)
        gref = Gref(station.store, channel, identifier)
        log.info("Trying to fetch channel: %s identifier: %s" %
                (channel, identifier))
        marshalled_thread = adaptor.get_issue(gref, crypto_adaptor=crypto_adaptor)
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
        return jsonate({"content": response,
                        "root": root,
                        "tips": marshalled_thread["tips"],
                        "signatures": marshalled_thread["signatures"]}, False)

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
        _update_gref(gref, [Tip(oid,"")], parents)
        return jsonate({"response": "ok"}, False)

    @app.route("/grefs/<channel>", methods=['PUT'])
    def create_gref(channel):
        def _write_object(obj):
            return station.write(obj.as_object())

        name = request.form["name"]
        protocol = request.form["protocol"]
        user = request.form["user"]
        body = request.form["body"]
        title = request.form["title"]
        gref = Gref(station.store, channel, name)
        root = RootObject(name, channel, protocol)
        root_oid = _write_object(root)

        _title = UpdateObject([root_oid], json.dumps({
            "type": "title",
            "id": None,
            "body": title,
            "user": user
            }))
        title_oid = _write_object(_title)

        _body = UpdateObject([title_oid], json.dumps({
            "type": "body",
            "id": None,
            "body": body
            }))
        body_oid = _write_object(_body)

        _update_gref(gref, [Tip(body_oid, "")], [])
        return ""



    return app
