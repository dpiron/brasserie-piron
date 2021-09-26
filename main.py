from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = 'gfdxgbnyfhg'  # os.environ.get("SECRET_KEY")
Bootstrap(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/beer')
def beer():
    return render_template("beer.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
