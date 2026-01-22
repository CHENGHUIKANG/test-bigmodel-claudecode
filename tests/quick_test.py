#!/usr/bin/env python3
"""
快速测试脚本 - 测试所有用户API接口
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/users"

def test_api():
    print("=== 用户API系统测试 ===\n")

    # 1. 测试服务状态
    print("1. 测试服务状态...")
    try:
        response = requests.get(f"{BASE_URL.replace('/users', '')}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        print("✓ 服务运行正常\n")
    except Exception as e:
        print(f"✗ 服务连接失败: {e}")
        return

    # 2. 测试健康检查
    print("2. 测试健康检查...")
    response = requests.get(f"{BASE_URL.replace('/users', '')}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print("✓ 健康检查正常\n")

    # 3. 获取用户信息
    print("3. 获取用户信息...")
    response = requests.get(f"{BASE_URL}/me")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print("✓ 获取用户信息成功\n")

    # 4. 用户注册测试
    print("4. 用户注册...")
    register_data = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "password123",
        "full_name": "测试用户",
        "bio": "这是一个测试用户"
    }

    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print("✓ 用户注册成功\n")

    # 5. 用户登录测试
    print("5. 用户登录...")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }

    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        tokens = response.json()
        print("登录成功!")
        print(f"Access Token: {tokens['access_token'][:20]}...")
        print(f"Refresh Token: {tokens['refresh_token'][:20]}...")

        # 6. 获取指定用户信息
        print("\n6. 获取指定用户信息...")
        response = requests.get(f"{BASE_URL}/profile/testuser")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        print("✓ 获取用户信息成功\n")

        print("\n=== 所有测试完成! ===")
        print("\nAPI服务器信息:")
        print("- 地址: http://localhost:8000")
        print("- API文档: http://localhost:8000/docs")
        print("- 数据库: SQLite (user_system.db)")
        print("\n可用的接口:")
        print("GET  / - 服务信息")
        print("GET  /health - 健康检查")
        print("POST /api/users/register - 用户注册")
        print("POST /api/users/login - 用户登录")
        print("GET  /api/users/me - 获取当前用户信息")
        print("GET  /api/users/profile/{username} - 获取指定用户信息")

    else:
        print(f"登录失败: {response.text}")

if __name__ == "__main__":
    try:
        test_api()
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中出错: {e}")