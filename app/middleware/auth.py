import os

from flask import jsonify, request


def auth():
    """
    Bearer认证中间件，从环境变量获取TOKEN
    """
    # 排除OPTIONS请求和不需要认证的路径
    if request.method == "OPTIONS":
        return None

    # 获取环境变量中的TOKEN
    api_token = os.environ.get("API_TOKEN")
    if not api_token:
        return jsonify({"error": "服务器未配置认证令牌"}), 500

    # 检查请求头中的认证信息
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "缺少认证信息"}), 401

    try:
        # 检查Bearer令牌格式
        auth_type, token = auth_header.split(" ", 1)
        if auth_type.lower() != "bearer":
            return jsonify({"error": "认证类型必须为Bearer"}), 401

        # 验证令牌
        if token != api_token:
            return jsonify({"error": "认证令牌无效"}), 401

    except ValueError:
        return jsonify({"error": "认证格式不正确"}), 401

    # 认证通过，继续请求
    return None
