from futu import *
import os

def get_history_kline_quota():
     # 从环境变量读取FUTU API配置
    futu_host = os.environ.get('FUTU_HOST', '127.0.0.1')
    futu_port = int(os.environ.get('FUTU_PORT', 11111))
    
    result_data = []
    quote_ctx = OpenQuoteContext(host=futu_host, port=futu_port)
    ret, data = quote_ctx.get_history_kl_quota(get_detail=False)
    quote_ctx.close()
    if ret == RET_OK:
        return {
            'used': data[0],
            'available': data[1]
        }
    else:
        return None
    