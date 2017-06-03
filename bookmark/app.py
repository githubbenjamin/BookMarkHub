# coding=utf-8

from flask import Flask


def create_app():
    # 创建应用实例
    app = Flask(__name__)

    initialize(app)
    register_blueprints(app)
    return app


def initialize(app):
    # 加载所有flask扩展
    from bookmark.extends import api
    for i in (api, ):
        i.init_app(app)


def register_blueprints(app):
    # 注册所有蓝图
    from bookmark import api_v1
    for i in (api_v1,):
        app.register_blueprint(i.bp)
