# FUTU API 封装

这是一个将富途OpenD的API封装为RESTful API的Flask应用。

## Roadmap [WIP]

- [x] 查询指定标的的历史K线数据接口
- [x] 查询指定标的的资金流向数据接口
- [x] 查询指定标的的资金分布数据接口
- [x] 查询账户的历史K线配额接口
- [ ] 以上接口支持MCP协议

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
├── .pre-commit-config.yaml # Pre-commit配置文件
├── pyproject.toml          # 项目配置和依赖管理
├── uv.lock                 # uv锁定文件
├── Dockerfile              # Docker构建文件
└── run.py                  # 应用入口
```

## 环境要求

- Python 3.9+
- Flask 2.0.1
- futu-api 9.2.5208
- Gunicorn 20.1.0 (生产环境)


## 安装与运行

### 使用uv安装（推荐）

```bash
# 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆仓库
git clone https://github.com/jorben/mcp-futu-api.git
cd mcp-futu-api

# 安装依赖并创建虚拟环境
uv sync
```

### 使用conda安装

如果您使用conda环境，请使用以下命令安装依赖：

```bash
conda create -n mcp-futu-api python=3.9
conda activate mcp-futu-api

# 克隆仓库
git clone https://github.com/jorben/mcp-futu-api.git
cd mcp-futu-api

# 安装依赖
pip install -e .

```

### 环境变量配置

您可以通过以下两种方式配置环境变量：

1. 直接在系统中设置：

```bash
# Linux/Mac
export API_TOKEN=your_secure_token
export FUTU_HOST=127.0.0.1  # 默认为本地富途openD客户端地址
export FUTU_PORT=11111      # 默认为本地富途openD客户端端口

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

## 开发工具

### 代码格式化和检查（Ruff）

本项目使用 [Ruff](https://github.com/astral-sh/ruff) 进行代码格式化和静态检查。Ruff 是一个极快的 Python 代码检查器和格式化工具。

#### 使用方法

```bash
# 使用uv运行（推荐）
uv run ruff check .          # 检查代码
uv run ruff check . --fix    # 检查并自动修复
uv run ruff format .         # 格式化代码

# 直接运行（需要先激活虚拟环境）
ruff check .                 # 检查代码
ruff check . --fix          # 检查并自动修复
ruff format .               # 格式化代码
```

#### Ruff配置

项目的Ruff配置在 `pyproject.toml` 文件中，包括：

- 行长度限制：88字符
- 启用的检查规则：pycodestyle、pyflakes、isort、flake8-bugbear等
- 代码格式化：使用双引号，空格缩进

### Git提交钩子（Pre-commit）

本项目配置了 [pre-commit](https://pre-commit.com/) 钩子，在每次提交前自动运行代码检查和格式化。

#### 安装pre-commit钩子

```bash
# 使用uv安装开发依赖（包含pre-commit）
uv sync --group dev

pre-commit install

```

#### 手动运行pre-commit

```bash
# 对所有文件运行
uv run pre-commit run --all-files

# 对暂存文件运行
uv run pre-commit run
```

#### Pre-commit配置

`.pre-commit-config.yaml` 文件配置了以下钩子：

- **Ruff检查和格式化**：自动修复代码风格问题
- **基础检查**：去除尾随空格、检查YAML/TOML语法、检查合并冲突等

### 运行应用

#### 开发环境

```bash
# 使用uv运行（推荐）
uv run python run.py

```

应用将在`http://0.0.0.0:15000`上启动。

#### 生产环境

使用 Gunicorn 作为 WSGI 服务器：

```bash
# 使用uv运行（推荐）
uv run gunicorn --bind 0.0.0.0:15000 --workers 4 --timeout 120 run:app

# 或者在python环境中运行
gunicorn --bind 0.0.0.0:15000 --workers 4 --timeout 120 run:app
```

参数说明：
- `--bind`: 绑定地址和端口
- `--workers`: 工作进程数，建议设置为 CPU 核心数的 2-4 倍
- `--timeout`: 请求超时时间（秒）
- `run:app`: 应用实例的导入路径

### Docker部署

您也可以使用Docker部署此应用：

```bash
# 构建Docker镜像
docker build -t mcp-futu-api .

# 运行容器
docker run -d -p 15000:15000 -e API_TOKEN=your_token -e FUTU_HOST=host.docker.internal -e FUTU_PORT=11111 --name mcp-futu-api mcp-futu-api
```

**注意**：
1. 当在Docker中运行时，如果要连接宿主机上的富途openD客户端，请使用`host.docker.internal`作为FUTU_HOST的值。
2. Docker镜像默认使用Gunicorn作为生产环境服务器。

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

### 获取股票资金流向数据

```
GET /api/stock/capital_flow
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
| period_type | string | 否 | 周期类型，可选值：DAY(日)、WEEK(周)、MONTH(月)、INTRADAY(实时)，默认为DAY |

**示例：**

```
GET /api/stock/capital_flow?code=HK.00700&start=2023-01-01&end=2023-02-01&period_type=DAY
```

**响应：**

返回JSON格式的资金流向数据。

**响应字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
|in_flow | float | 整体净流入 |
|main_in_flow | float | 主力大单净流入（仅日、周、月周期下有效）|
|super_in_flow | float | 特大单净流入 |
|big_in_flow | float | 大单净流入 |
|mid_in_flow | float | 中单净流入 |
|sml_in_flow | float | 小单净流入 |
|capital_flow_item_time | str | 开始时间 |
|last_valid_time | str |	数据最后有效时间（仅实时周期有效）|

### 获取股票资金分布数据

```
GET /api/stock/capital_distribution
```

**请求头：**
```
Authorization: Bearer your_token_here
```

**请求参数：**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| code | string | 是 | 股票代码，如 HK.00700 |

**示例：**

```
GET /api/stock/capital_distribution?code=HK.00700
```

**响应：**

返回JSON格式的资金分布数据。

**响应字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| capital_in_super | float | 流入资金额度，特大单 |
| capital_in_big | float | 流入资金额度，大单 |
| capital_in_mid | float | 流入资金额度，中单 |
| capital_in_small | float | 流入资金额度，小单 |
| capital_out_super | float | 流出资金额度，特大单 |
| capital_out_big | float | 流出资金额度，大单 |
| capital_out_mid | float | 流出资金额度，中单 |
| capital_out_small | float | 流出资金额度，小单 |
| update_time | str | 更新时间字符串 |

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

### 包管理问题

#### uv相关问题

如果uv命令无法识别，请确保已正确安装并添加到PATH：

```bash
# 重新安装uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或者使用pip安装
pip install uv
```

#### 虚拟环境问题

如果虚拟环境有问题，可以删除并重新创建：

```bash
# 删除现有虚拟环境
rm -rf .venv

# 重新安装依赖
uv sync --group dev
```

### 代码质量工具问题

#### Ruff配置问题

如果Ruff检查失败，请检查配置：

```bash
# 查看当前配置
uv run ruff check --show-settings

# 忽略特定文件
echo "exclude = ['migrations/', '*.pb2.py']" >> pyproject.toml
```

#### Pre-commit钩子问题

如果pre-commit钩子执行失败：

```bash
# 重新安装钩子
uv run pre-commit uninstall
uv run pre-commit install

# 更新钩子
uv run pre-commit autoupdate

# 跳过钩子提交（不推荐）
git commit --no-verify
```

### 认证问题

确保在请求头中正确设置了Authorization，格式为`Bearer your_token_here`，其中`your_token_here`应与环境变量`API_TOKEN`的值相匹配。

### 生产环境注意事项

1. 不要使用 Flask 开发服务器（`python run.py`）在生产环境中运行应用
2. 始终使用 Gunicorn 或其他生产级别的 WSGI 服务器
3. 确保设置了适当的工作进程数（workers）和超时时间
4. 建议使用反向代理（如 Nginx）来处理 SSL 终止和负载均衡
