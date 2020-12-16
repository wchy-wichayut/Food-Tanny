from flask import Flask, render_template, jsonify, request, redirect, url_for


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    pass
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
