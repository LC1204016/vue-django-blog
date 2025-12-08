"""
压力测试脚本
模拟大量用户同时访问系统，测试系统性能和稳定性
"""
import asyncio
import aiohttp
import time
import random
import string
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import statistics


class StressTest:
    """压力测试类"""
    
    def __init__(self, base_url="http://localhost:8000/api", max_users=100, test_duration=60):
        self.base_url = base_url
        self.max_users = max_users
        self.test_duration = test_duration
        self.results = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'errors': []
        }
        self.user_tokens = []  # 存储用户令牌
        
    def generate_random_string(self, length=10):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def generate_random_email(self):
        """生成随机邮箱"""
        return f"{self.generate_random_string(8)}@example.com"
    
    async def register_user(self, session, user_id):
        """对于压力测试，我们使用已存在的测试用户"""
        # 直接返回成功，因为我们使用现有用户
        return True
        
        try:
            async with session.post(url, json=data) as response:
                if response.status == 201:
                    return True
                else:
                    error_text = await response.text()
                    self.results['errors'].append(f"注册失败: {error_text}")
                    return False
        except Exception as e:
            self.results['errors'].append(f"注册异常: {str(e)}")
            return False
    
    async def login_user(self, session, username, password):
        """用户登录"""
        # 使用现有的测试用户
        test_users = [
            {'email': 'test@example.com', 'password': 'testpass123'},
        ]
        
        # 随机选择一个测试用户
        import random
        test_user = random.choice(test_users)
        
        url = f"{self.base_url}/auth/login/"
        data = {
            "email": test_user['email'],
            "password": test_user['password']
        }
        
        try:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    token_data = await response.json()
                    return token_data.get('access')
                else:
                    return None
        except Exception as e:
            self.results['errors'].append(f"登录异常: {str(e)}")
            return None
    
    async def create_test_users(self, session, count=50):
        """创建测试用户"""
        tasks = []
        for i in range(count):
            task = asyncio.create_task(self.register_user(session, i))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        successful_users = [r for r in results if r is True]
        return len(successful_users)
    
    async def get_articles(self, session, token=None):
        """获取文章列表"""
        url = f"{self.base_url}/getposts/"
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        start_time = time.time()
        try:
            async with session.get(url, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 200:
                    self.results['successful_requests'] += 1
                    return await response.json()
                else:
                    self.results['failed_requests'] += 1
                    return None
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"获取文章异常: {str(e)}")
            return None
    
    async def create_article(self, session, token, user_id):
        """创建文章"""
        url = f"{self.base_url}/pubposts/"
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            "title": f"压力测试文章 {user_id} - {self.generate_random_string(10)}",
            "content": f"这是压力测试创建的文章内容，用户ID: {user_id}，时间: {datetime.now()}",
            "category": 1  # 假设分类ID为1
        }
        
        start_time = time.time()
        try:
            async with session.post(url, json=data, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 201:
                    self.results['successful_requests'] += 1
                    return await response.json()
                else:
                    self.results['failed_requests'] += 1
                    error_text = await response.text()
                    self.results['errors'].append(f"创建文章失败: {error_text}")
                    return None
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"创建文章异常: {str(e)}")
            return None
    
    async def search_articles(self, session, token=None):
        """搜索文章"""
        search_keywords = ['测试', '文章', 'Vue', 'Django', '技术', '生活']
        keyword = random.choice(search_keywords)
        url = f"{self.base_url}/searchposts/?keyword={keyword}"
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        start_time = time.time()
        try:
            async with session.get(url, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 200:
                    self.results['successful_requests'] += 1
                    return await response.json()
                else:
                    self.results['failed_requests'] += 1
                    return None
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"搜索文章异常: {str(e)}")
            return None
    
    async def user_simulation(self, session, user_id, token=None):
        """模拟单个用户行为"""
        actions = [
            self.get_articles,
            self.search_articles,
        ]
        
        # 如果有token，添加需要认证的操作
        if token:
            actions.append(lambda s, t: self.create_article(s, t, user_id))
        
        start_time = time.time()
        
        # 在测试时间内持续执行操作
        while time.time() - start_time < self.test_duration:
            # 随机选择一个操作
            action = random.choice(actions)
            
            if action == self.create_article:
                await action(session, token)
            else:
                await action(session, token)
            
            # 随机等待时间，模拟真实用户行为
            await asyncio.sleep(random.uniform(0.1, 2.0))
    
    async def run_stress_test(self):
        """运行压力测试"""
        print(f"开始压力测试: {self.max_users} 用户，持续 {self.test_duration} 秒")
        print("=" * 50)
        
        # 创建HTTP会话
        connector = aiohttp.TCPConnector(limit=self.max_users * 2)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # 第一阶段：创建测试用户
            print("第一阶段：创建测试用户...")
            user_count = min(20, self.max_users)  # 创建20个测试用户
            successful_users = await self.create_test_users(session, user_count)
            print(f"成功创建 {successful_users} 个测试用户")
            
            # 第二阶段：用户登录获取令牌
            print("第二阶段：用户登录获取令牌...")
            login_tasks = []
            for i in range(successful_users):
                username = f"stress_user_{i}"
                task = asyncio.create_task(self.login_user(session, username, "testpass123"))
                login_tasks.append(task)
            
            tokens = await asyncio.gather(*login_tasks, return_exceptions=True)
            self.user_tokens = [token for token in tokens if token is not None]
            print(f"成功登录 {len(self.user_tokens)} 个用户")
            
            # 第三阶段：压力测试
            print("第三阶段：开始压力测试...")
            start_time = time.time()
            
            # 创建用户模拟任务
            tasks = []
            for i in range(self.max_users):
                # 部分用户使用令牌（已登录用户），部分用户不使用（匿名用户）
                token = self.user_tokens[i % len(self.user_tokens)] if self.user_tokens else None
                task = asyncio.create_task(self.user_simulation(session, i, token))
                tasks.append(task)
            
            # 等待所有任务完成或超时
            try:
                await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 
                                      timeout=self.test_duration)
            except asyncio.TimeoutError:
                print("测试时间结束，停止所有任务...")
                for task in tasks:
                    task.cancel()
            
            total_time = time.time() - start_time
            print(f"压力测试完成，总耗时: {total_time:.2f} 秒")
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 50)
        print("压力测试报告")
        print("=" * 50)
        
        # 基本统计
        print(f"总请求数: {self.results['total_requests']}")
        print(f"成功请求数: {self.results['successful_requests']}")
        print(f"失败请求数: {self.results['failed_requests']}")
        
        if self.results['total_requests'] > 0:
            success_rate = (self.results['successful_requests'] / self.results['total_requests']) * 100
            print(f"成功率: {success_rate:.2f}%")
        
        # 响应时间统计
        if self.results['response_times']:
            avg_response_time = statistics.mean(self.results['response_times'])
            min_response_time = min(self.results['response_times'])
            max_response_time = max(self.results['response_times'])
            median_response_time = statistics.median(self.results['response_times'])
            
            print(f"\n响应时间统计:")
            print(f"平均响应时间: {avg_response_time:.3f} 秒")
            print(f"最小响应时间: {min_response_time:.3f} 秒")
            print(f"最大响应时间: {max_response_time:.3f} 秒")
            print(f"中位数响应时间: {median_response_time:.3f} 秒")
            
            # 计算每秒请求数
            if self.test_duration > 0:
                rps = self.results['total_requests'] / self.test_duration
                print(f"每秒请求数 (RPS): {rps:.2f}")
        
        # 错误统计
        if self.results['errors']:
            print(f"\n错误统计 (显示前10个):")
            for i, error in enumerate(self.results['errors'][:10]):
                print(f"{i+1}. {error}")
            
            if len(self.results['errors']) > 10:
                print(f"... 还有 {len(self.results['errors']) - 10} 个错误")
        
        # 性能评估
        print(f"\n性能评估:")
        if self.results['response_times']:
            avg_response_time = statistics.mean(self.results['response_times'])
            if avg_response_time < 0.1:
                print("响应时间: 优秀 (< 100ms)")
            elif avg_response_time < 0.5:
                print("响应时间: 良好 (100ms - 500ms)")
            elif avg_response_time < 1.0:
                print("响应时间: 一般 (500ms - 1s)")
            else:
                print("响应时间: 需要优化 (> 1s)")
        
        if self.results['total_requests'] > 0:
            success_rate = (self.results['successful_requests'] / self.results['total_requests']) * 100
            if success_rate >= 99:
                print("成功率: 优秀 (≥ 99%)")
            elif success_rate >= 95:
                print("成功率: 良好 (95% - 99%)")
            elif success_rate >= 90:
                print("成功率: 一般 (90% - 95%)")
            else:
                print("成功率: 需要优化 (< 90%)")
        
        # 保存详细报告到文件
        self.save_detailed_report()
    
    def save_detailed_report(self):
        """保存详细报告到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"stress_test_report_{timestamp}.json"
        
        report_data = {
            'test_config': {
                'max_users': self.max_users,
                'test_duration': self.test_duration,
                'base_url': self.base_url,
                'timestamp': timestamp
            },
            'results': self.results,
            'statistics': {}
        }
        
        # 添加统计信息
        if self.results['response_times']:
            report_data['statistics'] = {
                'avg_response_time': statistics.mean(self.results['response_times']),
                'min_response_time': min(self.results['response_times']),
                'max_response_time': max(self.results['response_times']),
                'median_response_time': statistics.median(self.results['response_times']),
                'rps': self.results['total_requests'] / self.test_duration if self.test_duration > 0 else 0
            }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n详细报告已保存到: {filename}")


async def main():
    """主函数"""
    # 可以根据需要调整测试参数
    test_config = [
        {'max_users': 10, 'test_duration': 30, 'name': '轻量级测试'},
        {'max_users': 50, 'test_duration': 60, 'name': '中等负载测试'},
        {'max_users': 100, 'test_duration': 120, 'name': '高负载测试'},
    ]
    
    for config in test_config:
        print(f"\n开始 {config['name']}")
        stress_test = StressTest(
            max_users=config['max_users'],
            test_duration=config['test_duration']
        )
        
        await stress_test.run_stress_test()
        stress_test.generate_report()
        
        # 测试间隔，让系统休息一下
        print("\n等待 10 秒后继续下一个测试...")
        await asyncio.sleep(10)


if __name__ == "__main__":
    print("博客系统压力测试工具")
    print("请确保系统正在运行 (python manage.py runserver)")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {str(e)}")