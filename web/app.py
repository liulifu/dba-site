#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, abort, request
import json
import os

app = Flask(__name__)

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT, 'cases.json')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    CASES = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', cases=CASES[:6])

@app.route('/portal')
def portal():
    return render_template('portal.html')



@app.route('/cases')
def cases():
    return render_template('cases_v2.html', cases=CASES)

@app.route('/cases/<slug>')
def case_detail(slug):
    for c in CASES:
        if c.get('slug') == slug:
            return render_template('case_detail_v2.html', c=c)
    abort(404)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(ROOT, 'static'), filename)

@app.route('/healthz')
def healthz():
    return 'ok', 200

@app.route('/learn')
def learn():
    return render_template('learn.html')

if __name__ == '__main__':
    # CI trigger: no functional change

    # Respect PORT/LISTEN_PORT for PaaS/local dev; container uses gunicorn in Dockerfile
    port = int(os.environ.get('PORT') or os.environ.get('LISTEN_PORT') or 8080)
    app.run(host='0.0.0.0', port=port, threaded=True)
