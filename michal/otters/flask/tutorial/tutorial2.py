# flask tutorial https://www.youtube.com/watch?v=xIgPMguqyws
import flask

app = flask.Flask(__name__)

@app.route("/")
def home():
    return flask.render_template("index.html")
if __name__ == "__main__":
    app.run()
