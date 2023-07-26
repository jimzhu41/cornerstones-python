from datetime import datetime
from flask import render_template, Flask, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.models import User
from app.main import main


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/explore', methods=['GET', 'POST'])
def explore():
    return render_template('explore.html')
