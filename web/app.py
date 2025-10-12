#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, abort
import json
import os

app = Flask(__name__)

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT, 'cases.json')
PDF_NAME = '刘力夫_DBA_简历_CN_v3.pdf'

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    CASES = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', cases=CASES[:6])

@app.route('/resume')
def resume():
    pdf_exists = os.path.exists(os.path.join(ROOT, 'static', PDF_NAME))
    return render_template('resume.html', pdf_exists=pdf_exists, pdf_name=PDF_NAME)

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

if __name__ == '__main__':
    # CI trigger: no functional change

    # Respect PORT/LISTEN_PORT for PaaS/local dev; container uses gunicorn in Dockerfile
    port = int(os.environ.get('PORT') or os.environ.get('LISTEN_PORT') or 8080)
    app.run(host='0.0.0.0', port=port, threaded=True)
