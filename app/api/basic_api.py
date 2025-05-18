from flask import Blueprint, request, jsonify
from app.services.basic_service import get_history_kline_quota

# 创建蓝图
basic_bp = Blueprint('basic', __name__)

@basic_bp.route('/history_kline_quota', methods=['GET'])
def history_kline_quota():
    return jsonify(get_history_kline_quota())