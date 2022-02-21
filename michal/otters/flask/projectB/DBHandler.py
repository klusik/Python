import flask

app = flask.Flask(__name__)

@app.route("/")
def home():
    dictionary = {'auto':1,
                    "motorka":2,}
    return flask.render_template("index.html", dictionary = dictionary)

# @app.route("/<name>")
# def orders(name):
#    return f"Hello {name}!"

#@app.route("/admin")
#def admin():
#    return flask.redirect(flask.url_for("home"))

@app.route('/', methods=['POST'])
def my_form_post():
    text = flask.request.form['text']
    processed_text = text.upper()
    return processed_text

if __name__ == "__main__":
    app.run()
