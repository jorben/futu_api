from app.api.basic_api import basic_bp
from app.api.stock_api import stock_bp


def register_routes(app):
    """
    注册所有API路由到Flask应用
    """
    # 注册股票API蓝图
    app.register_blueprint(stock_bp, url_prefix="/api/stock")
    app.register_blueprint(basic_bp, url_prefix="/api/basic")
