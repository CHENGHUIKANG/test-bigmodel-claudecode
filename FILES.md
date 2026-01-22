# 项目文件说明

## 完整项目结构

```
test-bigmodel-claudecode/
│
├── README.md                    # 项目主文档
├── PROJECT.md                   # 完整项目文档
├── FILES.md                     # 本文件 - 项目文件说明
│
├── .env                         # 环境变量配置（数据库连接等）
├── .gitignore                   # Git忽略文件配置
│
├── requirements.txt             # 完整版依赖（FastAPI版本）
├── requirements_simple.txt      # 简化版依赖
│
├── # 主程序
├── mini_api.py                 # 简化版API服务（推荐使用）
├── main.py                     # 完整版API服务（FastAPI版本）
├── start.bat                   # 快速启动脚本（Windows）
├── clean.bat                   # 清理脚本（Windows）
│
├── # 核心文件
├── config.py                   # 配置管理
├── database.py                 # 数据库连接
├── utils.py                    # 工具函数（密码、Token等）
├── init_db.py                  # 数据库初始化
│
├── # 数据模型
├── models/
│   ├── __init__.py
│   ├── user.py                 # 用户模型
│   └── session.py              # 会话模型
│
├── # API路由
├── api/
│   ├── __init__.py
│   └── users.py                # 用户API路由
│
├── # 数据模式
├── schemas/
│   ├── __init__.py
│   └── user.py                 # 用户数据模式
│
├── # 示例代码
├── examples/
│   ├── qwq_simple_demo.py              # QwQ简单演示
│   ├── qwq_agent_demo.py               # QwQ基础演示
│   └── qwq_agent_demo_enhanced.py     # QwQ增强演示
│
├── # 测试脚本
├── tests/
│   ├── quick_test.py            # 快速测试脚本
│   ├── test_api.py             # API完整测试
│   └── test_basic.py           # 基础功能测试
│
├── # 文档
├── docs/
│   ├── README-API.md           # API接口文档
│   ├── setup_guide.md          # 环境配置指南
│   └── init_sql_lite.sql       # SQL初始化脚本
│
├── # 其他
├── core/
│   └── simple_main.py          # 简单版本主程序
│
└── user_system.db              # SQLite数据库文件（运行后生成）
```

## 文件详细说明

### 核心文件

| 文件 | 说明 | 优先级 |
|------|------|--------|
| `mini_api.py` | 简化版API服务，使用Python内置模块，无需安装依赖 | ⭐⭐⭐ |
| `main.py` | 完整版API服务，基于FastAPI + MySQL | ⭐⭐ |
| `config.py` | 配置管理，从环境变量读取配置 | ⭐⭐⭐ |
| `database.py` | 数据库连接管理 | ⭐⭐⭐ |
| `utils.py` | 工具函数：密码加密、Token生成等 | ⭐⭐⭐ |

### 数据模型

| 文件 | 说明 |
|------|------|
| `models/user.py` | 用户数据模型，定义users表结构 |
| `models/session.py` | 会话数据模型，定义user_sessions表结构 |

### API路由

| 文件 | 说明 |
|------|------|
| `api/users.py` | 用户相关API路由，包含注册、登录等接口 |

### 数据模式

| 文件 | 说明 |
|------|------|
| `schemas/user.py` | Pydantic数据模式，用于请求/响应验证 |

### 示例代码

| 文件 | 说明 |
|------|------|
| `examples/qwq_simple_demo.py` | QwQ模型最简单演示 |
| `examples/qwq_agent_demo.py` | QwQ模型基础演示 |
| `examples/qwq_agent_demo_enhanced.py` | QwQ模型增强演示（处理编码问题）|

### 测试脚本

| 文件 | 说明 |
|------|------|
| `tests/quick_test.py` | 快速测试脚本 |
| `tests/test_api.py` | API完整测试 |
| `tests/test_basic.py` | 基础功能测试 |

### 文档

| 文件 | 说明 |
|------|------|
| `README.md` | 项目主文档，快速开始指南 |
| `PROJECT.md` | 完整项目文档，详细说明 |
| `FILES.md` | 本文件，项目文件说明 |
| `docs/README-API.md` | API接口详细文档 |
| `docs/setup_guide.md` | 环境配置指南 |
| `docs/init_sql_lite.sql` | SQL初始化脚本 |

### 配置和工具

| 文件 | 说明 |
|------|------|
| `.env` | 环境变量配置文件 |
| `requirements.txt` | 完整版Python依赖 |
| `requirements_simple.txt` | 简化版依赖 |
| `start.bat` | Windows快速启动脚本 |
| `clean.bat` | Windows清理脚本 |
| `.gitignore` | Git忽略文件配置 |

## 快速开始指南

### 1. 启动服务（推荐）

**方法一：使用启动脚本（Windows）**
```bash
start.bat
```

**方法二：直接运行**
```bash
python mini_api.py
```

### 2. 测试API

```bash
# 健康检查
curl http://localhost:8000/health

# 获取用户信息
curl http://localhost:8000/api/users/me

# 用户登录
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### 3. 运行测试

```bash
python tests/quick_test.py
```

## 数据库

- **数据库类型**: SQLite（简化版）/ MySQL（完整版）
- **数据库文件**: `user_system.db`
- **数据表**:
  - `users` - 用户表
  - `user_sessions` - 会话表

## 测试账号

| 用户名 | 密码 | 邮箱 |
|--------|------|------|
| testuser | password123 | test@example.com |
| admin | admin | admin@example.com |

## 常用命令

### 服务管理

```bash
# 启动服务
python mini_api.py

# 或使用启动脚本
start.bat

# 停止服务
# 按 Ctrl+C

# 清理数据库
clean.bat
```

### 测试

```bash
# 快速测试
python tests/quick_test.py

# API测试
python tests/test_api.py

# 基础测试
python tests/test_basic.py
```

### QwQ演示

```bash
# 简单演示
python examples/qwq_simple_demo.py

# 基础演示
python examples/qwq_agent_demo.py

# 增强演示
python examples/qwq_agent_demo_enhanced.py
```

## 注意事项

1. **简化版本**（mini_api.py）无需安装依赖，推荐使用
2. **完整版本**（main.py）需要安装依赖和配置MySQL
3. 数据库文件 `user_system.db` 可以删除，重启服务会自动创建
4. 生产环境请修改 `.env` 中的密钥配置
5. 确保端口8000未被占用

## 问题排查

### 服务无法启动

1. 检查端口8000是否被占用
2. 检查Python版本是否正确（3.x）
3. 查看错误日志

### 数据库问题

1. 删除 `user_system.db` 重启服务
2. 检查文件权限

### 测试失败

1. 确保服务正在运行
2. 检查请求格式是否正确
3. 查看服务日志

## 更多信息

- [完整项目文档](PROJECT.md)
- [API接口文档](docs/README-API.md)
- [设置指南](docs/setup_guide.md)