from futu import *
from datetime import datetime, timedelta
import pandas as pd
import os

SysConfig.set_proto_fmt(ProtoFMT.Protobuf)

def get_history_kline(code, start=None, end=None, max_count=1000, ktype=KLType.K_DAY, autype=AuType.QFQ):
    """
    获取历史K线数据
    
    参数:
        code (str): 股票代码
        start (str, optional): 开始日期, 格式为'YYYY-MM-DD'
        end (str, optional): 结束日期, 格式为'YYYY-MM-DD'
        max_count (int, optional): 每页获取的最大记录数
        ktype (KLType, optional): 周期类型
        autype (AuType, optional): 复权类型
        
    返回:
        str: JSON格式的K线数据
    """
    if end is None:
        end = datetime.now().strftime('%Y-%m-%d')
    if start is None:
        # 获取一个月前的日期
        start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # 从环境变量读取FUTU API配置
    futu_host = os.environ.get('FUTU_HOST', '127.0.0.1')
    futu_port = int(os.environ.get('FUTU_PORT', 11111))
    
    result_data = []
    quote_ctx = OpenQuoteContext(host=futu_host, port=futu_port)
    
    ret, data, page_req_key = quote_ctx.request_history_kline(
        code, start=start, end=end, max_count=max_count, 
        ktype=ktype, autype=autype, session=Session.ALL
    )
    
    if ret == RET_OK:
        result_data.append(data)
    else:
        print('error:', data)
    
    while page_req_key != None:  # 请求后面的所有结果
        # print('*************************************')
        ret, data, page_req_key = quote_ctx.request_history_kline(
            code, start=start, end=end, max_count=max_count, 
            ktype=ktype, autype=autype, 
            page_req_key=page_req_key, session=Session.ALL
        )
        
        if ret == RET_OK:
            result_data.append(data)
        else:
            print('error:', data)
    
    # print('All pages are finished!')
    quote_ctx.close()
    
    if result_data:
        data = pd.concat(result_data, ignore_index=True)
        data = data.sort_values(by='time_key', ascending=False)
        data = data.reset_index(drop=True)
        # format to json
        return data.to_json(orient='records')
    
    return None 


def get_capital_flow(code, start=None, end=None, period_type=PeriodType.DAY):
    """
    获取股票的资金流向数据
    
    参数:
        code (str): 股票代码
        start (str, optional): 开始日期, 格式为'YYYY-MM-DD'
        end (str, optional): 结束日期, 格式为'YYYY-MM-DD'
        period_type (PeriodType, optional): 周期类型
        
    返回:
        str: JSON格式的资金流向数据
    """
    if end is None:
        end = datetime.now().strftime('%Y-%m-%d')
    if start is None:
        start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # 从环境变量读取FUTU API配置
    futu_host = os.environ.get('FUTU_HOST', '127.0.0.1')
    futu_port = int(os.environ.get('FUTU_PORT', 11111))
    
    quote_ctx = OpenQuoteContext(host=futu_host, port=futu_port)
    
    ret, data = quote_ctx.get_capital_flow(
        code, start=start, end=end, period_type=period_type
    )
    quote_ctx.close()
    
    if ret == RET_OK:
        return data.to_json(orient='records')
    else:
        print('error:', data)
    
    return None
    
def get_capital_distribution(code):
    """
    获取股票的资金分布数据
    
    参数:
        code (str): 股票代码
        
    返回:
        str: JSON格式的资金分布数据
    """
    # 从环境变量读取FUTU API配置
    futu_host = os.environ.get('FUTU_HOST', '127.0.0.1')
    futu_port = int(os.environ.get('FUTU_PORT', 11111))
    
    quote_ctx = OpenQuoteContext(host=futu_host, port=futu_port)
    
    ret, data = quote_ctx.get_capital_distribution(code)
    quote_ctx.close()
    
    if ret == RET_OK:
        return data.to_json(orient='records')
    else:
        print('error:', data)
    
    return None
    

def get_stock_kdj(code, start=None, end=None):
    data = get_history_kline(code, start, end)
    if data is None:
        return None
    data = pd.read_json(data)
    data = data.sort_values(by='time_key', ascending=False)
    data = data.reset_index(drop=True)
    return data