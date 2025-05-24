from flask import Blueprint, jsonify, request
from futu import AuType, KLType

from app.services.stock_service import get_history_kline

# 创建蓝图
stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/history_kline", methods=["GET"])
def history_kline():
    """
    获取历史K线数据API

    请求参数:
        code: 股票代码，必填
        start: 开始日期，可选，格式为'YYYY-MM-DD'
        end: 结束日期，可选，格式为'YYYY-MM-DD'
        max_count: 每页最大记录数，可选，默认100
        ktype: 周期类型，可选，默认K_DAY
        autype: 复权类型，可选，默认QFQ

    返回:
        JSON格式的K线数据
    """
    # 获取请求参数
    code = request.args.get("code")
    start = request.args.get("start")
    end = request.args.get("end")
    max_count = request.args.get("max_count", 1000, type=int)
    ktype = request.args.get("ktype", KLType.K_DAY, type=KLType)
    autype = request.args.get("autype", AuType.QFQ, type=AuType)

    # 验证必填参数
    if not code:
        return jsonify({"error": "股票代码不能为空"}), 400

    try:
        # 调用服务层函数获取数据
        result = get_history_kline(code, start, end, max_count, ktype, autype)

        if result:
            return result, 200, {"Content-Type": "application/json"}
        else:
            return jsonify({"error": "未找到数据"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
