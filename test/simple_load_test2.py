"""
简化的负载测试脚本
专注于测试核心功能
"""
import asyncio
import aiohttp
import time
import random
import string
from datetime import datetime


class SimpleLoadTest:
    """简化的负载测试类"""
    
    def __init__(self, base_url="http://localhost:8000/api", concurrent_users=5, test_duration=30):
        self.base_url = base_url
        self.concurrent_users = concurrent_users
        self.test_duration = test_duration
        self.results = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': []
        }
    
    async def login(self, session):
        """登录获取令牌"""
        url = f"{self.base_url}/auth/login/"
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        try:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    token_data = await response.json()
                    return token_data.get('access')
                else:
                    return None
        except Exception:
            return None
    
    async def get_articles(self, session, token):
        """获取文章列表"""
        url = f"{self.base_url}/getposts/"
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        
        start_time = time.time()
        try:
            async with session.get(url, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 200:
                    self.results['successful_requests'] += 1
                    return True
                else:
                    self.results['failed_requests'] += 1
                    return False
        except Exception:
            self.results['failed_requests'] += 1
            return False
    
    async def search_articles(self, session, token):
        """搜索文章"""
        keywords = ['测试', '文章', 'Vue', 'Django']
        keyword = random.choice(keywords)
        url = f"{self.base_url}/searchposts/?keyword={keyword}"
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        
        start_time = time.time()
        try:
            async with session.get(url, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 200:
                    self.results['successful_requests'] += 1
                    return True
                else:
                    self.results['failed_requests'] += 1
                    return False
        except Exception:
            self.results['failed_requests'] += 1
            return False
    
    async def create_article(self, session, token):
        """创建文章"""
        url = f"{self.base_url}/pubposts/"
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            "title": f"测试文章{random.randint(1, 100)}",
            "content": "这是测试文章的内容",
            "category": random.choice([6, 7])
        }
        
        start_time = time.time()
        try:
            async with session.post(url, json=data, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 201:
                    self.results['successful_requests'] += 1
                    return True
                else:
                    self.results['failed_requests'] += 1
                    return False
        except Exception:
            self.results['failed_requests'] += 1
            return False
    
    async def user_simulation(self, session, user_id):
        """模拟用户行为"""
        # 登录
        token = await self.login(session)
        if not token:
            print(f"用户 {user_id} 登录失败")
            return
        
        print(f"用户 {user_id} 开始模拟行为...")
        
        # 在测试时间内持续执行操作
        start_time = time.time()
        while time.time() - start_time < self.test_duration:
            # 随机选择一个操作
            actions = [
                self.get_articles,
                self.search_articles,
                self.create_article,
            ]
            
            action = random.choice(actions)
            
            # 执行操作
            if action == self.create_article:
                await action(session, token)
            else:
                await action(session, token)
            
            # 随机等待
            await asyncio.sleep(random.uniform(0.5, 2.0))
        
        print(f"用户 {user_id} 完成模拟行为")
    
    async def run_test(self):
        """运行负载测试"""
        print(f"开始负载测试: {self.concurrent_users} 并发用户，持续 {self.test_duration} 秒")
        print("=" * 50)
        
        # 创建HTTP会话
        connector = aiohttp.TCPConnector(limit=self.concurrent_users * 2)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            start_time = time.time()
            
            # 创建用户任务
            tasks = []
            for i in range(self.concurrent_users):
                task = asyncio.create_task(self.user_simulation(session, i))
                tasks.append(task)
            
            # 等待所有任务完成
            await asyncio.gather(*tasks, return_exceptions=True)
            
            total_time = time.time() - start_time
            print(f"负载测试完成，总耗时: {total_time:.2f} 秒")
    
    def print_results(self):
        """打印测试结果"""
        print("\n" + "=" * 50)
        print("负载测试结果")
        print("=" * 50)
        
        print(f"总请求数: {self.results['total_requests']}")
        print(f"成功请求数: {self.results['successful_requests']}")
        print(f"失败请求数: {self.results['failed_requests']}")
        
        if self.results['total_requests'] > 0:
            success_rate = (self.results['successful_requests'] / self.results['total_requests']) * 100
            print(f"成功率: {success_rate:.2f}%")
        
        if self.results['response_times']:
            avg_response_time = sum(self.results['response_times']) / len(self.results['response_times'])
            min_response_time = min(self.results['response_times'])
            max_response_time = max(self.results['response_times'])
            
            print(f"\n响应时间统计:")
            print(f"平均响应时间: {avg_response_time:.3f} 秒")
            print(f"最小响应时间: {min_response_time:.3f} 秒")
            print(f"最大响应时间: {max_response_time:.3f} 秒")
            
            if self.test_duration > 0:
                rps = self.results['total_requests'] / self.test_duration
                print(f"每秒请求数 (RPS): {rps:.2f}")


async def main():
    """主函数"""
    print("博客系统简化负载测试")
    print("请确保系统正在运行 (python manage.py runserver)")
    print("=" * 50)
    
    # 创建测试实例
    test = SimpleLoadTest(concurrent_users=5, test_duration=30)
    
    # 运行测试
    await test.run_test()
    
    # 打印结果
    test.print_results()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
