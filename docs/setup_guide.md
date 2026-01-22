# 用户系统设置指南

## 问题诊断

当前Python版本: 3.13.3
该版本可能存在兼容性问题，建议使用Python 3.11或3.10版本。

## 解决方案

### 方案1: 使用Python 3.11/3.10

1. 安装Python 3.11或3.10版本
2. 设置环境变量
3. 重新安装依赖

### 方案2: 手动安装依赖

在命令行中逐个安装：

```bash
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install sqlalchemy==2.0.23
pip install pymysql==1.1.0
pip install pydantic==2.5.0
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6
pip install pydantic-settings==2.1.0
```

### 方案3: 使用虚拟环境

```bash
python -m venv user_system_env
.\user_system_env\Scripts\activate
pip install -r requirements.txt
```

## 快速测试

创建数据库：

```sql
CREATE DATABASE user_db;
USE user_db;

-- 创建用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    avatar_url VARCHAR(255),
    bio TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入测试用户
INSERT INTO users (username, email, password_hash, full_name, bio)
VALUES ('testuser', 'test@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPkU2Cslq', '测试用户', '测试用户');
```

## 运行服务

依赖安装完成后：

```bash
python main.py
```

API将在 http://localhost:8000 启动
API文档: http://localhost:8000/docs