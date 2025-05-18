# FUTU API 封装

这是一个将富途API封装为RESTful API的Flask应用。

## 功能特点

- 基于Flask框架实现的RESTful API
- 使用Bearer令牌认证保护API接口
- 路由与业务逻辑分离的架构设计
- 中间件方式实现认证机制

## 项目结构

```
├── app/                    # 应用主目录
│   ├── __init__.py         # 应用初始化
│   ├── api/                # API路由定义
│   │   ├── __init__.py
│   │   ├── routes.py       # 路由注册
│   │   └── stock_api.py    # 股票相关API
│   ├── middleware/         # 中间件
│   │   ├── __init__.py
│   │   └── auth.py         # 认证中间件
│   └── services/           # 服务层
│       ├── __init__.py
│       └── stock_service.py # 股票数据服务
├── run.py                  # 应用入口
└── requirements.txt        # 项目依赖
```

## 安装与运行

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 设置环境变量：

```bash
# Linux/Mac
export API_TOKEN=your_secure_token

# Windows
set API_TOKEN=your_secure_token
```

3. 运行应用：

```bash
python run.py
```

## API文档

### 获取历史K线数据

```
GET /api/stock/history_kline
```

**请求头：**
```
Authorization: Bearer your_token_here
```

**请求参数：**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| code | string | 是 | 股票代码，如 HK.00700 |
| start | string | 否 | 开始日期，格式为 YYYY-MM-DD |
| end | string | 否 | 结束日期，格式为 YYYY-MM-DD |
| max_count | int | 否 | 每页最大记录数，默认100 |

**示例：**

```
GET /api/stock/history_kline?code=HK.00700&start=2023-01-01&end=2023-02-01
``` 

### 获取历史K线配额

```
GET /api/basic/history_kline_quota
```