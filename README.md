# Test BigModel & User System

这是一个综合项目，包含两个主要模块：

1. **QwQ大语言模型智能体演示** - 基于LangChain与QwQ-32B模型交互
2. **用户管理系统** - 完整的用户注册、登录、信息管理功能

## 项目概览

```
test-bigmodel-claudecode/
├── # 用户管理系统
├── mini_api.py              # 简化版API服务（推荐使用）
├── main.py                  # 完整版API服务
├── user_system.db           # SQLite数据库
├── config.py                # 配置文件
├── database.py              # 数据库连接
├── models/                  # 数据模型
├── api/                     # API路由
├── schemas/                 # 数据模式
├── utils.py                 # 工具函数
│
├── # QwQ智能体演示
├── examples/                # QwQ演示代码
│   ├── qwq_simple_demo.py
│   ├── qwq_agent_demo.py
│   └── qwq_agent_demo_enhanced.py
│
├── # 测试和文档
├── tests/                   # 测试脚本
├── docs/                    # 项目文档
├── PROJECT.md               # 完整项目文档
└── requirements.txt          # 依赖包
```

## 快速开始

### 用户管理系统（推荐）

```bash
# 启动简化版服务（无需安装依赖）
python mini_api.py

# 服务地址：http://localhost:8000
# API文档：http://localhost:8000/docs
```

### QwQ智能体演示

```bash
# 安装依赖
pip install langchain-qwq==0.3.4

# 运行演示
python examples/qwq_simple_demo.py
```

## 用户管理系统

### 功能特性

- 用户注册和登录
- JWT Token认证
- 用户信息管理
- 会话管理
- 密码加密

### API接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 服务信息 |
| `/health` | GET | 健康检查 |
| `/api/users/register` | POST | 用户注册 |
| `/api/users/login` | POST | 用户登录 |
| `/api/users/me` | GET | 获取当前用户信息 |
| `/api/users/profile/{username}` | GET | 获取指定用户信息 |

### 测试账号

| 用户名 | 密码 |
|--------|------|
| testuser | password123 |
| admin | admin |

### 快速测试

```bash
# 健康检查
curl http://localhost:8000/health

# 用户登录
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

详细文档请查看 [PROJECT.md](PROJECT.md)

## QwQ智能体演示

### 功能特点

- 使用 langchain-qwq 0.3.4 包
- 连接到本地 QwQ-32B 模型
- 简单的对话交互功能
- 错误处理和编码兼容性

### 配置说明

- **base_url**: `http://192.168.20.68:3000/v1/`
- **model**: `QwQ-32B`
- **api_key**: 本地部署可用任意值

### 运行演示

```bash
# 简单版本
python examples/qwq_simple_demo.py

# 基础版本
python examples/qwq_agent_demo.py

# 增强版本
python examples/qwq_agent_demo_enhanced.py
```

## 技术栈

### 用户管理系统

**简化版本**:
- Python 3.x
- SQLite
- 标准库

**完整版本**:
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic

### QwQ智能体

- LangChain
- QwQ-32B 模型

## 项目文档

- [完整项目文档](PROJECT.md) - 详细的项目说明和API文档
- [API文档](docs/README-API.md) - API接口详细说明
- [设置指南](docs/setup_guide.md) - 环境配置指南

## 许可证

本项目仅供学习和测试使用。

## 贡献

欢迎提交Issue和Pull Request。