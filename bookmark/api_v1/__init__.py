# coding=utf-8

from flask import Blueprint, render_template
from flask_restful import Api

#bp = Blueprint('apiv1', __name__, url_prefix='/api/v1')
bp=Blueprint('apiv1', __name__,
             url_prefix='/api/v1',
          template_folder='templates',
          static_folder='static')

@bp.route('/<user_url_slug>/hello')
def hello(user_url_slug):
    # Do some stuff
    return render_template('hello.html', un=user_url_slug)

#@bp.route('/<user_url_slug>/login')
#def hello2(user_url_slug):
#    # Do some stuff
#    return render_template('login.html')

from bp_login import *

api = Api(bp)
