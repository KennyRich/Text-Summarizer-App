from flask import Flask, Response, render_template, request, redirect, url_for, json
from summarizer import summarizer
import logging

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summary', methods=['POST'])
def summary():
    email = request.form.get('email')
    name = request.form.get('name')
    message = request.form.get('message')
    summari = summarizer.generate_summary(message, 5)
    return redirect(url_for('result', summary=summari))


@app.route('/<summary>')
def result(summary):
    return render_template('results.html', summary=summary)


if __name__ == '__main__':
    app.run(port=3001)
