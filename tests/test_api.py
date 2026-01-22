import requests
import json

BASE_URL = "http://localhost:8000/api/users"

def test_user_registration():
    """测试用户注册"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User",
        "phone": "1234567890",
        "bio": "这是一个测试用户"
    }

    response = requests.post(f"{BASE_URL}/register", json=user_data)
    print(f"注册响应状态码: {response.status_code}")
    if response.status_code == 200:
        print("注册成功!")
        print("注册用户信息:", response.json())
        return response.json()
    else:
        print("注册失败:", response.text)
        return None

def test_user_login():
    """测试用户登录"""
    login_data = {
        "username": "testuser",
        "password": "password123"
    }

    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"\n登录响应状态码: {response.status_code}")
    if response.status_code == 200:
        print("登录成功!")
        tokens = response.json()
        print("Access Token:", tokens["access_token"][:50] + "...")
        print("Refresh Token:", tokens["refresh_token"][:50] + "...")
        return tokens
    else:
        print("登录失败:", response.text)
        return None

def test_get_user_profile(access_token):
    """测试获取用户信息"""
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"\n获取用户信息状态码: {response.status_code}")
    if response.status_code == 200:
        print("获取用户信息成功!")
        print("用户信息:", response.json())
    else:
        print("获取用户信息失败:", response.text)

def test_update_user_profile(access_token):
    """测试更新用户信息"""
    headers = {"Authorization": f"Bearer {access_token}"}

    update_data = {
        "full_name": "更新后的姓名",
        "phone": "0987654321",
        "bio": "更新后的个人简介"
    }

    response = requests.put(f"{BASE_URL}/me", json=update_data, headers=headers)
    print(f"\n更新用户信息状态码: {response.status_code}")
    if response.status_code == 200:
        print("更新用户信息成功!")
        print("更新后的信息:", response.json())
    else:
        print("更新用户信息失败:", response.text)

def test_logout(access_token):
    """测试用户登出"""
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(f"{BASE_URL}/logout", headers=headers)
    print(f"\n登出状态码: {response.status_code}")
    if response.status_code == 200:
        print("登出成功!")
        print(response.json())
    else:
        print("登出失败:", response.text)

def test_get_public_profile():
    """测试获取公开用户信息"""
    response = requests.get(f"{BASE_URL}/profile/testuser")
    print(f"\n获取公开用户信息状态码: {response.status_code}")
    if response.status_code == 200:
        print("获取公开用户信息成功!")
        print("用户信息:", response.json())
    else:
        print("获取公开用户信息失败:", response.text)

if __name__ == "__main__":
    print("=== 开始API测试 ===")

    # 1. 测试注册
    user_info = test_user_registration()

    # 2. 测试登录
    tokens = test_user_login()

    if tokens:
        access_token = tokens["access_token"]

        # 3. 测试获取用户信息
        test_get_user_profile(access_token)

        # 4. 测试更新用户信息
        test_update_user_profile(access_token)

        # 5. 测试登出
        test_logout(access_token)

        # 6. 测试获取公开用户信息
        test_get_public_profile()
    else:
        print("无法继续测试，登录失败")

    print("\n=== API测试完成 ===")