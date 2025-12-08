"""
简单的连接测试脚本
用于诊断负载测试问题
"""
import asyncio
import aiohttp
import time


async def test_connection():
    """测试基本连接"""
    base_url = "http://localhost:8000/api"
    
    print("测试API连接...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # 测试基本连接
            async with session.get(f"{base_url}/") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ API连接成功: {data}")
                else:
                    print(f"❌ API连接失败，状态码: {response.status}")
                    return False
            
            # 测试文章列表
            async with session.get(f"{base_url}/getposts/") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ 获取文章列表成功，共 {len(data)} 篇文章")
                else:
                    print(f"❌ 获取文章列表失败，状态码: {response.status}")
                    return False
            
            # 测试用户注册
            import random
            import string
            
            def generate_random_string(length=10):
                return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            
            register_data = {
                "username": f"test_user_{generate_random_string(8)}",
                "email": f"{generate_random_string(8)}@example.com",
                "password": "testpass123",
                "password2": "testpass123"
            }
            
            async with session.post(f"{base_url}/auth/register/", json=register_data) as response:
                if response.status == 201:
                    print("✅ 用户注册成功")
                    data = await response.json()
                    
                    # 测试用户登录
                    login_data = {
                        "username": register_data["username"],
                        "password": "testpass123"
                    }
                    
                    async with session.post(f"{base_url}/auth/login/", json=login_data) as login_response:
                        if login_response.status == 200:
                            login_data_result = await login_response.json()
                            print("✅ 用户登录成功")
                            return login_data_result.get('access')
                        else:
                            print(f"❌ 用户登录失败，状态码: {login_response.status}")
                            return False
                else:
                    error_text = await response.text()
                    print(f"❌ 用户注册失败，状态码: {response.status}")
                    print(f"错误信息: {error_text}")
                    return False
    
    except Exception as e:
        print(f"❌ 连接测试异常: {str(e)}")
        return False


async def test_with_token(token):
    """使用令牌测试需要认证的API"""
    if not token:
        print("⚠️  无有效令牌，跳过认证测试")
        return
    
    base_url = "http://localhost:8000/api"
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        
        async with aiohttp.ClientSession() as session:
            # 测试获取用户资料
            async with session.get(f"{base_url}/profile/", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ 获取用户资料成功: {data.get('username')}")
                else:
                    print(f"❌ 获取用户资料失败，状态码: {response.status}")
            
            # 测试创建文章
            article_data = {
                "title": "测试文章",
                "content": "这是测试文章的内容",
                "category": 1
            }
            
            async with session.post(f"{base_url}/pubposts/", json=article_data, headers=headers) as response:
                if response.status == 201:
                    data = await response.json()
                    print(f"✅ 创建文章成功: {data.get('title')}")
                else:
                    error_text = await response.text()
                    print(f"❌ 创建文章失败，状态码: {response.status}")
                    print(f"错误信息: {error_text}")
    
    except Exception as e:
        print(f"❌ 认证测试异常: {str(e)}")


async def main():
    """主函数"""
    print("开始连接诊断测试...")
    print("=" * 50)
    
    # 测试基本连接
    token = await test_connection()
    
    print("\n" + "=" * 50)
    
    # 测试认证功能
    await test_with_token(token)
    
    print("\n" + "=" * 50)
    print("连接诊断测试完成")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {str(e)}")