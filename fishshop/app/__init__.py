from flask import Flask
from app.models.base import db
from flask_login import LoginManager

login_manager=LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    login_manager.init_app(app)
    # 返回登录页面
    login_manager.login_view='web.login'
    login_manager.login_message='请先登录或注册'
    db.init_app(app)
    db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)

