import os

from dotenv import load_dotenv

from app import create_app

# 加载.env文件中的环境变量（如果存在）
load_dotenv()

app = create_app()

if __name__ == "__main__":
    # 设置默认的开发环境配置
    if not os.environ.get("API_TOKEN"):
        os.environ["API_TOKEN"] = "dev_token_for_testing"
        print("警告: 使用默认开发Token，生产环境请设置API_TOKEN环境变量")

    if not os.environ.get("FUTU_HOST"):
        os.environ["FUTU_HOST"] = "127.0.0.1"

    if not os.environ.get("FUTU_PORT"):
        os.environ["FUTU_PORT"] = "11111"

    # 启动应用
    is_debug = os.environ.get("FLASK_ENV") == "development"
    if is_debug:
        print("debug mode")
        print("API_TOKEN", os.environ.get("API_TOKEN"))
        print("FUTU_HOST", os.environ.get("FUTU_HOST"))
        print("FUTU_PORT", os.environ.get("FUTU_PORT"))
    else:
        print("production mode")
        print("FUTU_HOST", os.environ.get("FUTU_HOST"))
        print("FUTU_PORT", os.environ.get("FUTU_PORT"))
    app.run(host="0.0.0.0", port=15000, debug=is_debug)
