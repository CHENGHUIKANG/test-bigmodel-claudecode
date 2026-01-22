# 用户管理系统 - 项目文档

## 项目概述

这是一个基于Python的用户管理系统，提供完整的用户注册、登录、登出和信息管理功能。项目包含两个版本：

1. **完整版本** (`main.py`): 基于FastAPI + MySQL，功能完整
2. **简化版本** (`mini_api.py`): 基于Python内置模块 + SQLite，无需安装依赖

## 项目结构

```
test-bigmodel-claudecode/
├── # 核心文件
├── README.md                # 项目说明文档（本文件）
├── mini_api.py              # 简化版API服务（推荐使用）
├── main.py                  # 完整版API服务
├── user_system.db           # SQLite数据库文件
│
├── # 配置文件
├── config.py                # 数据库配置
├── database.py              # 数据库连接
├── .env                     # 环境变量配置
├── requirements.txt          # Python依赖（完整版）
│
├── # 数据模型
├── models/
│   ├── __init__.py
│   ├── user.py             # 用户模型
│   └── session.py          # 会话模型
│
├── # API路由
├── api/
│   ├── __init__.py
│   └── users.py           # 用户相关API路由
│
├── # 数据模式
├── schemas/
│   ├── __init__.py
│   └── user.py            # 用户数据模式
│
├── # 工具函数
├── utils.py               # 密码加密、JWT等工具
├── init_db.py             # 数据库初始化
│
├── # 测试文件
├── quick_test.py          # 快速测试脚本
├── test_api.py            # API测试脚本（完整版）
│
├── # QwQ大模型演示（原始项目）
├── qwq_simple_demo.py
├── qwq_agent_demo.py
└── qwq_agent_demo_enhanced.py
```

## 快速开始

### 方案一：使用简化版本（推荐）

**优势**：无需安装任何依赖，直接运行

```bash
# 1. 启动服务
python mini_api.py

# 2. 访问API
# 服务地址：http://localhost:8000
# API文档：http://localhost:8000/docs
```

### 方案二：使用完整版本

需要安装依赖和配置MySQL数据库

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置数据库
# 创建MySQL数据库 user_db
# 修改 .env 中的数据库连接信息

# 3. 初始化数据库
python init_db.py

# 4. 启动服务
python main.py
```

## API接口文档

### 基础接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/` | 服务信息 |
| GET | `/health` | 健康检查 |

### 用户接口

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | `/api/users/register` | 用户注册 | 不需要 |
| POST | `/api/users/login` | 用户登录 | 不需要 |
| GET | `/api/users/me` | 获取当前用户信息 | 需要 |
| GET | `/api/users/profile/{username}` | 获取指定用户信息 | 不需要 |

### 接口详情

#### 1. 用户注册

**请求**:
```bash
POST /api/users/register
Content-Type: application/json

{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "full_name": "新用户",
    "phone": "13800138000",
    "bio": "个人简介"
}
```

**响应**:
```json
{
    "message": "注册成功"
}
```

#### 2. 用户登录

**请求**:
```bash
POST /api/users/login
Content-Type: application/json

{
    "username": "testuser",
    "password": "password123"
}
```

**响应**:
```json
{
    "access_token": "xxxxx",
    "token_type": "bearer",
    "refresh_token": "xxxxx"
}
```

#### 3. 获取当前用户信息

**请求**:
```bash
GET /api/users/me
Authorization: Bearer {access_token}
```

**响应**:
```json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "测试用户",
    "phone": "1234567890",
    "bio": "测试用户",
    "is_active": true,
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00"
}
```

#### 4. 获取指定用户信息

**请求**:
```bash
GET /api/users/profile/testuser
```

**响应**:
```json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "测试用户",
    "phone": "1234567890",
    "bio": "测试用户",
    "is_active": true,
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00"
}
```

## 数据库设计

### users 表（用户表）

| 字段 | 类型 | 描述 | 约束 |
|------|------|------|------|
| id | INTEGER | 用户ID | 主键，自增 |
| username | TEXT | 用户名 | 唯一，非空 |
| email | TEXT | 邮箱 | 唯一，非空 |
| password_hash | TEXT | 密码哈希 | 非空 |
| full_name | TEXT | 全名 | 可空 |
| phone | TEXT | 手机号 | 可空 |
| avatar_url | TEXT | 头像URL | 可空 |
| bio | TEXT | 个人简介 | 可空 |
| is_active | BOOLEAN | 是否激活 | 默认true |
| is_verified | BOOLEAN | 是否验证 | 默认false |
| created_at | TIMESTAMP | 创建时间 | 自动 |
| updated_at | TIMESTAMP | 更新时间 | 自动 |

### user_sessions 表（会话表）

| 字段 | 类型 | 描述 | 约束 |
|------|------|------|------|
| id | INTEGER | 会话ID | 主键，自增 |
| user_id | INTEGER | 用户ID | 外键，非空 |
| refresh_token | TEXT | 刷新令牌 | 唯一，非空 |
| access_token | TEXT | 访问令牌 | 可空 |
| is_active | BOOLEAN | 是否激活 | 默认true |
| expires_at | TIMESTAMP | 过期时间 | 非空 |
| created_at | TIMESTAMP | 创建时间 | 自动 |

## 测试账号

系统预置了以下测试账号：

| 用户名 | 密码 | 邮箱 |
|--------|------|------|
| testuser | password123 | test@example.com |
| admin | admin | admin@example.com |

## 安全特性

1. **密码加密**: 使用SHA256对密码进行哈希存储
2. **Token认证**: 支持JWT风格的token认证机制
3. **会话管理**: 支持refresh token和access token
4. **CORS支持**: 支持跨域资源共享

## 测试方法

### 使用curl测试

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

### 使用Python测试

```bash
python quick_test.py
```

## 技术栈

### 简化版本
- Python 3.x
- SQLite
- 标准库: http.server, sqlite3, json, hashlib, secrets

### 完整版本
- Python 3.x
- FastAPI - Web框架
- SQLAlchemy - ORM框架
- PyMySQL - MySQL驱动
- Pydantic - 数据验证
- python-jose - JWT处理
- passlib - 密码加密

## 常见问题

### Q: 如何停止服务？
A: 按 `Ctrl+C` 停止服务，或在命令行执行 `taskkill /F /IM python.exe` (Windows)

### Q: 数据库文件在哪里？
A: `user_system.db` 在项目根目录下

### Q: 如何重置数据库？
A: 删除 `user_system.db` 文件，重新启动服务会自动创建

### Q: 完整版本和简化版本有什么区别？
A:
- 简化版本：无需安装依赖，使用SQLite，适合快速测试
- 完整版本：功能更完整，使用MySQL，适合生产环境

## 项目历史

1. **原始项目**: QwQ大语言模型演示
2. **当前版本**: 添加了完整的用户管理系统功能

## 许可证

本项目仅供学习和测试使用。

## 联系方式

如有问题，请提交Issue或联系项目维护者。