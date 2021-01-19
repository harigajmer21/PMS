from flask import Blueprint, render_template


site = Blueprint('site', __name__, url_prefix='/', template_folder='templates')


@site.route('/')
def index():
    return render_template('layout.html')
