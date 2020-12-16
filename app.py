from flask import Flask, render_template, jsonify, request, redirect, url_for


app = Flask(__name__)


@app.route('/')
@app.route('/test')
def test():
    return render_template('test.html')
# @app.route('/index')
# def index():
#     return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
