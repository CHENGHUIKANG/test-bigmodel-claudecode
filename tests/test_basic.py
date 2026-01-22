# 基础功能测试
import sys

def test_python_version():
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    return True

def test_imports():
    try:
        print("测试基本模块导入...")
        import json
        print("✓ json导入成功")

        import datetime
        print("✓ datetime导入成功")

        import hashlib
        print("✓ hashlib导入成功")

        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def create_database_schema():
    # 创建基础的SQL脚本
    sql_script = """
-- 创建数据库
CREATE DATABASE IF NOT EXISTS user_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE user_db;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
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

-- 创建用户会话表
CREATE TABLE IF NOT EXISTS user_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    access_token VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_sessions_active ON user_sessions(is_active);

-- 插入测试用户（密码是 password123 的bcrypt哈希）
INSERT IGNORE INTO users (username, email, password_hash, full_name, bio)
VALUES
('testuser', 'test@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPkU2Cslq', '测试用户', '这是一个测试用户');

"""

    with open('init_sql.sql', 'w', encoding='utf-8') as f:
        f.write(sql_script)
    print("✓ SQL脚本已创建: init_sql.sql")

if __name__ == "__main__":
    print("=== 基础环境测试 ===")

    # 1. 测试Python版本
    if test_python_version():
        print("✓ Python环境正常")
    else:
        print("✗ Python环境异常")
        sys.exit(1)

    # 2. 测试基本模块导入
    if test_imports():
        print("✓ 基础模块正常")
    else:
        print("✗ 基础模块异常")

    # 3. 创建数据库脚本
    create_database_schema()

    print("\n=== 测试完成 ===")
    print("\n后续步骤：")
    print("1. 手动安装依赖：pip install fastapi uvicorn sqlalchemy pymysql pydantic")
    print("2. 在MySQL中执行 init_sql.sql 创建数据库和表")
    print("3. 运行 python main.py 启动服务")