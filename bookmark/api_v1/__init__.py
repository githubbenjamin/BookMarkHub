# coding=utf-8

from flask import Blueprint
from flask_restful import Api

bp = Blueprint('apiv1', __name__, url_prefix='/api/v1')
api = Api(bp)
