from flask import Flask

from app.api.routes import register_routes
from app.middleware.auth import auth


def create_app():
    app = Flask(__name__)

    # 注册中间件
    app.before_request(auth)

    # 注册路由
    register_routes(app)

    return app
