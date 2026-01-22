#!/usr/bin/env python3
"""
简化版用户管理系统 - 使用Python内置模块
不依赖外部库，直接使用SQLite数据库
"""

import sqlite3
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sqlite3

# 数据库初始化
def init_db():
    conn = sqlite3.connect('user_system.db')
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            phone TEXT,
            bio TEXT,
            is_active BOOLEAN DEFAULT 1,
            is_verified BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 创建会话表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            refresh_token TEXT UNIQUE NOT NULL,
            access_token TEXT,
            is_active BOOLEAN DEFAULT 1,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # 插入测试用户
    cursor.execute('SELECT id FROM users WHERE username = ?', ('testuser',))
    if not cursor.fetchone():
        password_hash = hashlib.sha256('password123'.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, bio)
            VALUES (?, ?, ?, ?, ?)
        ''', ('testuser', 'test@example.com', password_hash, '测试用户', '测试用户'))

    conn.commit()
    conn.close()

# 工具函数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    return hashlib.sha256(password.encode()).hexdigest() == hashed_password

def generate_token():
    return secrets.token_urlsafe(32)

# API处理器
class UserAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.wfile.write(response)

    def parse_json_data(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))

    def get_db_connection(self):
        return sqlite3.connect('user_system.db')

    # 注册用户
    def do_POST(self):
        path = urlparse(self.path).path

        if path == '/api/users/register':
            try:
                data = self.parse_json_data()

                conn = self.get_db_connection()
                cursor = conn.cursor()

                # 检查用户名是否已存在
                cursor.execute('SELECT id FROM users WHERE username = ?', (data['username'],))
                if cursor.fetchone():
                    self.send_json_response({'error': '用户名已存在'}, 400)
                    return

                # 检查邮箱是否已存在
                cursor.execute('SELECT id FROM users WHERE email = ?', (data['email'],))
                if cursor.fetchone():
                    self.send_json_response({'error': '邮箱已被注册'}, 400)
                    return

                # 创建用户
                password_hash = hash_password(data['password'])
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, full_name, phone, bio)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (data['username'], data['email'], password_hash,
                      data.get('full_name'), data.get('phone'), data.get('bio')))

                conn.commit()
                conn.close()

                self.send_json_response({'message': '注册成功'})

            except Exception as e:
                self.send_json_response({'error': str(e)}, 500)

        elif path == '/api/users/login':
            try:
                data = self.parse_json_data()

                conn = self.get_db_connection()
                cursor = conn.cursor()

                # 查找用户
                cursor.execute('SELECT * FROM users WHERE username = ?', (data['username'],))
                user = cursor.fetchone()

                if not user or not verify_password(data['password'], user[3]):
                    self.send_json_response({'error': '用户名或密码错误'}, 401)
                    return

                if not user[7]:
                    self.send_json_response({'error': '用户账号已被禁用'}, 400)
                    return

                # 生成token
                access_token = generate_token()
                refresh_token = generate_token()

                # 保存会话
                expires_at = datetime.now() + timedelta(days=7)
                cursor.execute('''
                    INSERT INTO user_sessions (user_id, refresh_token, access_token, expires_at)
                    VALUES (?, ?, ?, ?)
                ''', (user[0], refresh_token, access_token, expires_at))

                conn.commit()
                conn.close()

                self.send_json_response({
                    'access_token': access_token,
                    'token_type': 'bearer',
                    'refresh_token': refresh_token
                })

            except Exception as e:
                self.send_json_response({'error': str(e)}, 500)

        else:
            self.send_json_response({'error': '接口不存在'}, 404)

    # 获取用户信息
    def do_GET(self):
        path = urlparse(self.path).path

        if path == '/api/users/me':
            # 简化版：返回测试用户信息
            self.send_json_response({
                'id': 1,
                'username': 'testuser',
                'email': 'test@example.com',
                'full_name': '测试用户',
                'phone': '1234567890',
                'bio': '测试用户',
                'is_active': True,
                'is_verified': False,
                'created_at': '2024-01-01T00:00:00'
            })

        elif path.startswith('/api/users/profile/'):
            username = path.split('/')[-1]
            self.send_json_response({
                'id': 1,
                'username': username,
                'email': 'test@example.com',
                'full_name': '测试用户',
                'phone': '1234567890',
                'bio': '测试用户',
                'is_active': True,
                'is_verified': False,
                'created_at': '2024-01-01T00:00:00'
            })

        elif path == '/':
            self.send_json_response({'message': '欢迎使用用户管理系统API'})

        elif path == '/health':
            self.send_json_response({'status': 'healthy'})

        else:
            self.send_json_response({'error': '接口不存在'}, 404)

def run_server():
    init_db()
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, UserAPIHandler)
    print("服务器启动在 http://localhost:8000")
    print("API文档: http://localhost:8000")
    print("按 Ctrl+C 停止服务器")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()