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
│   │   ├── __init__.py     # API包初始化
│   │   ├── routes.py       # 路由注册
│   │   ├── stock_api.py    # 股票相关API
│   │   └── basic_api.py    # 基础功能API
│   ├── middleware/         # 中间件
│   │   ├── __init__.py     # 中间件包初始化
│   │   └── auth.py         # 认证中间件
│   └── services/           # 服务层
│       ├── __init__.py     # 服务层包初始化
│       ├── stock_service.py # 股票数据服务
│       └── basic_service.py # 基础功能服务
├── Dockerfile              # Docker构建文件
├── run.py                  # 应用入口
└── requirements.txt        # 项目依赖
```

## 环境要求

- Python 3.9+
- Flask 2.0.1
- pandas 1.4.4
- futu-api 9.2.5208

## 安装与运行

### 使用pip安装（推荐）

1. 创建并激活虚拟环境（可选但推荐）：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

### 使用conda安装

如果您使用conda环境，请使用以下命令安装依赖：

```bash
conda install flask=2.0.1 werkzeug=2.0.1
conda install pandas numpy
pip install futu-api==9.2.5208 python-dotenv==1.0.0
```

### 环境变量配置

您可以通过以下两种方式配置环境变量：

1. 直接在系统中设置：

```bash
# Linux/Mac
export API_TOKEN=your_secure_token
export FUTU_HOST=127.0.0.1  # 默认为本地富途牛牛客户端地址
export FUTU_PORT=11111      # 默认为本地富途牛牛客户端端口

# Windows
set API_TOKEN=your_secure_token
set FUTU_HOST=127.0.0.1
set FUTU_PORT=11111
```

2. 创建`.env`文件（推荐用于开发环境）:

```
API_TOKEN=your_secure_token
FUTU_HOST=127.0.0.1
FUTU_PORT=11111
```

**注意**：如果您没有设置`API_TOKEN`，系统将使用默认值`dev_token_for_testing`（仅适用于开发环境）。

### 运行应用

```bash
python run.py
```

应用将在`http://0.0.0.0:15000`上启动。

### Docker部署

您也可以使用Docker部署此应用：

```bash
# 构建Docker镜像
docker build -t futu-api-server .

# 运行容器
docker run -d -p 15000:15000 -e API_TOKEN=your_token -e FUTU_HOST=host.docker.internal -e FUTU_PORT=11111 --name futu-api futu-api-server
```

**注意**：当在Docker中运行时，如果要连接宿主机上的富途牛牛客户端，请使用`host.docker.internal`作为FUTU_HOST的值。

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
| max_count | int | 否 | 每页最大记录数，默认1000 |
| ktype | string | 否 | K线类型，可选值：K_DAY(日K)、K_WEEK(周K)、K_MON(月K)、K_QUARTER(季K)、K_YEAR(年K)、K_1M(1分钟)、K_5M(5分钟)、K_15M(15分钟)、K_30M(30分钟)、K_60M(60分钟)、K_3M(3分钟)，默认为K_DAY |
| autype | string | 否 | 复权类型，可选值：NONE(不复权)、QFQ(前复权)、HFQ(后复权)，默认为QFQ |

**示例：**

```
GET /api/stock/history_kline?code=HK.00700&start=2023-01-01&end=2023-02-01&ktype=K_DAY&autype=QFQ
```

**响应：**

返回JSON格式的K线数据。

**响应字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| code | str | 股票代码 |
| name | str | 股票名称 |
| time_key | str | K线时间 |
| open | float | 开盘价 |
| close | float | 收盘价 |
| high | float | 最高价 |
| low | float | 最低价 |
| pe_ratio | float | 市盈率 |
| turnover_rate | float | 换手率 |
| volume | int | 成交量 |
| turnover | float | 成交额 |
| change_rate | float | 涨跌幅 |
| last_close | float | 昨收价 |

### 获取历史K线配额

```
GET /api/basic/history_kline_quota
```

**请求头：**
```
Authorization: Bearer your_token_here
```

**响应：**

```json
{
  "used": 100,       // 已使用的额度
  "available": 900   // 可用的额度
}
```

## 故障排除

### 依赖问题

如果遇到pandas和numpy的二进制不兼容问题，请尝试：

```bash
conda install pandas numpy
```

或指定兼容的版本：

```bash
conda install pandas=1.4.4 numpy=1.21.5
```

### 认证问题

确保在请求头中正确设置了Authorization，格式为`Bearer your_token_here`，其中`your_token_here`应与环境变量`API_TOKEN`的值相匹配。