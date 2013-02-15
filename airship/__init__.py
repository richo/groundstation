import os
import json

from flask import Flask


def make_airship(station):
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html",
                channels=station.channels())

    @app.route("/channels")
    def list_channels():
        return json.dumps(station.channels())

    return app
