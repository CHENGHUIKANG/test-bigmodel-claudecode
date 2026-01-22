# 用户管理系统 API 文档

## 概述

这是一个基于FastAPI和MySQL的用户管理系统，提供用户注册、登录、登出和信息管理等功能。

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置数据库
创建MySQL数据库 `user_db`，并修改 `.env` 文件中的数据库连接信息。

### 3. 初始化数据库
```bash
python init_db.py
```

### 4. 启动服务
```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

### 5. 访问API文档
打开浏览器访问 `http://localhost:8000/docs` 查看Swagger文档。

## API接口

### 用户注册
- **路径**: `POST /api/users/register`
- **描述**: 创建新用户
- **请求体**:
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User",
    "phone": "1234567890",
    "bio": "这是一个测试用户"
}
```
- **响应**: 返回创建的用户信息

### 用户登录
- **路径**: `POST /api/users/login`
- **描述**: 用户登录，返回access token和refresh token
- **请求体**:
```json
{
    "username": "testuser",
    "password": "password123"
}
```
- **响应**:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 用户登出
- **路径**: `POST /api/users/logout`
- **描述**: 用户登出，使所有会话失效
- **认证**: 需要在请求头中包含Bearer Token
- **请求头**: `Authorization: Bearer <access_token>`
- **响应**: 返回成功消息

### 获取当前用户信息
- **路径**: `GET /api/users/me`
- **描述**: 获取当前登录用户的信息
- **认证**: 需要在请求头中包含Bearer Token
- **请求头**: `Authorization: Bearer <access_token>`
- **响应**: 返回用户信息

### 更新当前用户信息
- **路径**: `PUT /api/users/me`
- **描述**: 更新当前登录用户的信息
- **认证**: 需要在请求头中包含Bearer Token
- **请求头**: `Authorization: Bearer <access_token>`
- **请求体**:
```json
{
    "full_name": "新姓名",
    "phone": "0987654321",
    "bio": "更新的个人信息"
}
```
- **响应**: 返回更新后的用户信息

### 获取指定用户信息
- **路径**: `GET /api/users/profile/{username}`
- **描述**: 获取指定用户的信息（无需认证）
- **参数**:
  - `username`: 用户名
- **响应**: 返回用户信息

## 数据库表结构

### users 表
| 字段 | 类型 | 描述 |
|------|------|------|
| id | INT | 主键 |
| username | VARCHAR(50) | 用户名，唯一 |
| email | VARCHAR(100) | 邮箱，唯一 |
| hashed_password | VARCHAR(255) | 加密后的密码 |
| full_name | VARCHAR(100) | 全名 |
| phone | VARCHAR(20) | 手机号 |
| avatar_url | VARCHAR(255) | 头像URL |
| bio | TEXT | 个人简介 |
| is_active | BOOLEAN | 是否激活 |
| is_verified | BOOLEAN | 是否验证 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### user_sessions 表
| 字段 | 类型 | 描述 |
|------|------|------|
| id | INT | 主键 |
| user_id | INT | 用户ID，外键 |
| refresh_token | VARCHAR(255) | 刷新令牌 |
| access_token | VARCHAR(255) | 访问令牌 |
| is_active | BOOLEAN | 是否激活 |
| expires_at | DATETIME | 过期时间 |
| created_at | DATETIME | 创建时间 |
| last_activity | DATETIME | 最后活动时间 |

## 安全特性

1. **密码加密**: 使用bcrypt对密码进行哈希存储
2. **JWT认证**: 使用JWT进行用户认证
3. **会话管理**: 支持refresh token机制
4. **CORS支持**: 配置跨域资源共享

## 环境变量

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| DATABASE_URL | mysql+pymysql://root:root@localhost:3306/user_db | 数据库连接URL |
| SECRET_KEY | your-secret-key-here-change-in-production | JWT密钥 |
| ALGORITHM | HS256 | JWT算法 |
| ACCESS_TOKEN_EXPIRE_MINUTES | 30 | Access Token过期时间（分钟） |
| API_PREFIX | /api | API前缀 |

## 测试示例

### 使用curl测试

```bash
# 用户注册
curl -X POST "http://localhost:8000/api/users/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'

# 用户登录
curl -X POST "http://localhost:8000/api/users/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "password123"}'

# 获取用户信息（需要先登录获取token）
curl -X GET "http://localhost:8000/api/users/me" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 注意事项

1. 在生产环境中，请务必更改默认的SECRET_KEY
2. 建议使用HTTPS来保护API通信
3. 定期更新依赖包以保持安全性
4. 数据库连接信息应妥善保管，不要泄露