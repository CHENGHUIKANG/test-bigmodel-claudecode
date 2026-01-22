-- SQLite数据库初始化脚本
-- 创建用户管理系统数据库

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    phone TEXT,
    avatar_url TEXT,
    bio TEXT,
    is_active BOOLEAN DEFAULT 1,
    is_verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户会话表
CREATE TABLE IF NOT EXISTS user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    refresh_token TEXT UNIQUE NOT NULL,
    access_token TEXT,
    is_active BOOLEAN DEFAULT 1,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_active ON user_sessions(is_active);

-- 插入测试用户
INSERT OR IGNORE INTO users (username, email, password_hash, full_name, bio)
VALUES
('testuser', 'test@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', '测试用户', '这是一个测试用户');

INSERT OR IGNORE INTO users (username, email, password_hash, full_name, bio)
VALUES
('admin', 'admin@example.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', '管理员', '系统管理员');

-- 创建测试会话
INSERT OR IGNORE INTO user_sessions (user_id, refresh_token, access_token, expires_at)
VALUES (1, 'refresh_token_123', 'access_token_123', datetime('now', '+7 days'));

-- 查询验证
SELECT '数据库初始化完成!' as message;
SELECT count(*) as user_count FROM users;
SELECT * FROM users;