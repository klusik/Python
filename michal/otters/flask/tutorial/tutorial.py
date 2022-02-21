# flask tutorial https://www.youtube.com/watch?v=mqhxxeeTbu0
import flask

app = flask.Flask(__name__)

@app.route("/")
def home():
    return"Hello! This is the main paige <h1>Hello<h1>"

@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return flask.redirect(flask.url_for("home"))

if __name__ == "__main__":
    app.run()
