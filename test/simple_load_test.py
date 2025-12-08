"""
简化的负载测试脚本
用于调试问题
"""
import asyncio
import aiohttp
import time
from datetime import datetime


async def test_api_calls():
    """测试API调用"""
    base_url = "http://localhost:8000/api"
    
    print("开始API调用测试...")
    
    # 创建HTTP会话
    connector = aiohttp.TCPConnector(limit=10)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        # 登录
        login_url = f"{base_url}/auth/login/"
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        print("尝试登录...")
        try:
            async with session.post(login_url, json=login_data) as response:
                if response.status == 200:
                    token_data = await response.json()
                    token = token_data.get('access')
                    print(f"登录成功，获得令牌")
                else:
                    error_text = await response.text()
                    print(f"登录失败，状态码: {response.status}, 错误: {error_text}")
                    return
        except Exception as e:
            print(f"登录异常: {str(e)}")
            return
        
        # 测试获取文章列表
        print("测试获取文章列表...")
        try:
            async with session.get(f"{base_url}/getposts/") as response:
                if response.status == 200:
                    articles = await response.json()
                    print(f"获取文章列表成功，共 {len(articles)} 篇文章")
                else:
                    print(f"获取文章列表失败，状态码: {response.status}")
        except Exception as e:
            print(f"获取文章列表异常: {str(e)}")
        
        # 测试创建文章
        print("测试创建文章...")
        headers = {'Authorization': f'Bearer {token}'}
        article_data = {
            "title": f"测试文章 {datetime.now()}",
            "content": "这是测试文章的内容",
            "category": 1
        }
        
        try:
            async with session.post(f"{base_url}/pubposts/", json=article_data, headers=headers) as response:
                if response.status == 201:
                    article = await response.json()
                    print(f"创建文章成功: {article.get('title')}")
                else:
                    error_text = await response.text()
                    print(f"创建文章失败，状态码: {response.status}, 错误: {error_text}")
        except Exception as e:
            print(f"创建文章异常: {str(e)}")
        
        # 并发测试
        print("\n开始并发测试...")
        tasks = []
        for i in range(5):
            task = asyncio.create_task(test_concurrent_requests(session, token, i))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in results if r is True)
        print(f"并发测试完成，成功: {success_count}/{len(results)}")


async def test_concurrent_requests(session, token, task_id):
    """测试并发请求"""
    base_url = "http://localhost:8000/api"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        # 测试获取文章列表
        async with session.get(f"{base_url}/getposts/", headers=headers) as response:
            if response.status == 200:
                await response.json()
                return True
            else:
                print(f"任务 {task_id} 失败，状态码: {response.status}")
                return False
    except Exception as e:
        print(f"任务 {task_id} 异常: {str(e)}")
        return False


async def main():
    """主函数"""
    print("简化负载测试")
    print("=" * 50)
    
    start_time = time.time()
    await test_api_calls()
    end_time = time.time()
    
    print(f"\n测试完成，总耗时: {end_time - start_time:.2f} 秒")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()