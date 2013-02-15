from flask import Flask, render_template


def make_airship(station):
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html",
                channels=station.channels())

    # class Index(flask.views.MethodView):
    #     def get(self):
    #         return 'GET'
    #     def post(self):
    #         return 'POST'
    # app.add_url_rule('/', view_func=Index.as_view('index'))

    return app
