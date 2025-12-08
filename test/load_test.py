"""
负载测试脚本
模拟真实用户行为，测试系统在不同负载下的表现
"""
import asyncio
import aiohttp
import time
import random
import string
from datetime import datetime
import json
import statistics
from concurrent.futures import ThreadPoolExecutor


class LoadTest:
    """负载测试类"""
    
    def __init__(self, base_url="http://localhost:8000/api", concurrent_users=20, test_duration=300):
        self.base_url = base_url
        self.concurrent_users = concurrent_users
        self.test_duration = test_duration
        self.results = {
            'user_sessions': [],
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'errors': [],
            'user_actions': []
        }
        
        # 用户行为权重
        self.action_weights = {
            'browse_articles': 40,    # 浏览文章
            'search_articles': 20,    # 搜索文章
            'read_article': 25,       # 阅读文章详情
            'create_article': 5,      # 创建文章
            'edit_article': 3,        # 编辑文章
            'comment_article': 5,     # 评论文章
            'like_article': 2         # 点赞文章
        }
    
    def generate_random_string(self, length=10):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def generate_random_content(self, min_length=50, max_length=500):
        """生成随机内容"""
        length = random.randint(min_length, max_length)
        words = ['测试', '文章', '内容', '系统', '性能', '负载', '用户', '访问', '数据', '功能']
        content = []
        for _ in range(length // 5):
            content.append(random.choice(words))
        return ' '.join(content)
    
    async def register_and_login(self, session, user_id):
        """注册并登录用户"""
        # 对于负载测试，我们使用已存在的测试用户而不是注册新用户
        # 这样可以避免验证码的问题
        test_users = [
            {'email': 'test@example.com', 'password': 'testpass123'},
        ]
        
        # 循环使用测试用户
        test_user = test_users[user_id % len(test_users)]
        
        # 直接登录
        login_url = f"{self.base_url}/auth/login/"
        login_data = {
            "email": test_user['email'],
            "password": test_user['password']
        }
        
        try:
            async with session.post(login_url, json=login_data) as response:
                if response.status == 200:
                    token_data = await response.json()
                    return {
                        'token': token_data.get('access'),
                        'refresh_token': token_data.get('refresh'),
                        'user_id': user_id,
                        'username': test_user['username'],
                        'created_articles': [],
                        'actions': []
                    }
                else:
                    self.results['errors'].append(f"用户 {test_user['username']} 登录失败")
                    return None
        except Exception as e:
            self.results['errors'].append(f"用户 {test_user['username']} 登录异常: {str(e)}")
            return None
        
        try:
            async with session.post(register_url, json=register_data) as response:
                if response.status != 201:
                    return None
        except Exception as e:
            self.results['errors'].append(f"用户 {user_id} 注册失败: {str(e)}")
            return None
        
        # 登录
        login_url = f"{self.base_url}/auth/login/"
        login_data = {
            "username": register_data["username"],
            "password": "testpass123"
        }
        
        try:
            async with session.post(login_url, json=login_data) as response:
                if response.status == 200:
                    token_data = await response.json()
                    return {
                        'token': token_data.get('access'),
                        'refresh_token': token_data.get('refresh'),
                        'user_id': user_id,
                        'username': register_data["username"],
                        'created_articles': [],
                        'actions': []
                    }
                else:
                    self.results['errors'].append(f"用户 {user_id} 登录失败")
                    return None
        except Exception as e:
            self.results['errors'].append(f"用户 {user_id} 登录异常: {str(e)}")
            return None
    
    async def browse_articles(self, session, user_session):
        """浏览文章列表"""
        url = f"{self.base_url}/getposts/"
        headers = {'Authorization': f'Bearer {user_session["token"]}'} if user_session else {}
        
        start_time = time.time()
        try:
            async with session.get(url, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 200:
                    self.results['successful_requests'] += 1
                    articles = await response.json()
                    user_session['actions'].append({
                        'action': 'browse_articles',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': True,
                        'articles_count': len(articles) if isinstance(articles, list) else 0
                    })
                    return articles
                else:
                    self.results['failed_requests'] += 1
                    user_session['actions'].append({
                        'action': 'browse_articles',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': False,
                        'error': response.status
                    })
                    return None
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"浏览文章异常: {str(e)}")
            user_session['actions'].append({
                'action': 'browse_articles',
                'timestamp': time.time(),
                'response_time': time.time() - start_time,
                'success': False,
                'error': str(e)
            })
            return None
    
    async def search_articles(self, session, user_session):
        """搜索文章"""
        keywords = ['Vue', 'Django', '测试', '技术', '文章', '系统', '开发', '前端', '后端']
        keyword = random.choice(keywords)
        url = f"{self.base_url}/searchposts/?keyword={keyword}"
        headers = {'Authorization': f'Bearer {user_session["token"]}'} if user_session else {}
        
        start_time = time.time()
        try:
            async with session.get(url, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 200:
                    self.results['successful_requests'] += 1
                    search_results = await response.json()
                    user_session['actions'].append({
                        'action': 'search_articles',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': True,
                        'keyword': keyword,
                        'results_count': len(search_results) if isinstance(search_results, list) else 0
                    })
                    return search_results
                else:
                    self.results['failed_requests'] += 1
                    user_session['actions'].append({
                        'action': 'search_articles',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': False,
                        'error': response.status
                    })
                    return None
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"搜索文章异常: {str(e)}")
            user_session['actions'].append({
                'action': 'search_articles',
                'timestamp': time.time(),
                'response_time': time.time() - start_time,
                'success': False,
                'error': str(e)
            })
            return None
    
    async def read_article(self, session, user_session, article_id=None):
        """阅读文章详情"""
        if not article_id:
            # 先获取文章列表
            articles = await self.browse_articles(session, user_session)
            if articles and isinstance(articles, list) and len(articles) > 0:
                article_id = random.choice(articles)['id']
            else:
                return None
        
        url = f"{self.base_url}/posts/{article_id}/"
        headers = {'Authorization': f'Bearer {user_session["token"]}'} if user_session else {}
        
        start_time = time.time()
        try:
            async with session.get(url, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 200:
                    self.results['successful_requests'] += 1
                    article = await response.json()
                    user_session['actions'].append({
                        'action': 'read_article',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': True,
                        'article_id': article_id,
                        'article_title': article.get('title', '')
                    })
                    return article
                else:
                    self.results['failed_requests'] += 1
                    user_session['actions'].append({
                        'action': 'read_article',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': False,
                        'error': response.status
                    })
                    return None
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"阅读文章异常: {str(e)}")
            user_session['actions'].append({
                'action': 'read_article',
                'timestamp': time.time(),
                'response_time': time.time() - start_time,
                'success': False,
                'error': str(e)
            })
            return None
    
    async def create_article(self, session, user_session):
        """创建文章"""
        if not user_session:
            return None
        
        url = f"{self.base_url}/pubposts/"
        headers = {'Authorization': f'Bearer {user_session["token"]}'}
        data = {
            "title": f"测试文章{user_session['user_id'] % 100}",
            "content": self.generate_random_content(100, 300),
            "category": random.choice([6, 7])  # 使用实际存在的分类ID
        }
        
        start_time = time.time()
        try:
            async with session.post(url, json=data, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 201:
                    self.results['successful_requests'] += 1
                    article = await response.json()
                    user_session['created_articles'].append(article['id'])
                    user_session['actions'].append({
                        'action': 'create_article',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': True,
                        'article_id': article['id'],
                        'article_title': article['title']
                    })
                    return article
                else:
                    self.results['failed_requests'] += 1
                    user_session['actions'].append({
                        'action': 'create_article',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': False,
                        'error': response.status
                    })
                    return None
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"创建文章异常: {str(e)}")
            user_session['actions'].append({
                'action': 'create_article',
                'timestamp': time.time(),
                'response_time': time.time() - start_time,
                'success': False,
                'error': str(e)
            })
            return None
    
    async def edit_article(self, session, user_session):
        """编辑文章"""
        if not user_session or not user_session['created_articles']:
            return None
        
        article_id = random.choice(user_session['created_articles'])
        url = f"{self.base_url}/edit/{article_id}/"
        headers = {'Authorization': f'Bearer {user_session["token"]}'}
        data = {
            "title": f"编辑后的文章 {user_session['user_id']} - {self.generate_random_string(8)}",
            "content": self.generate_random_content(100, 300),
            "category": random.choice([1, 2])
        }
        
        start_time = time.time()
        try:
            async with session.put(url, json=data, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 200:
                    self.results['successful_requests'] += 1
                    article = await response.json()
                    user_session['actions'].append({
                        'action': 'edit_article',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': True,
                        'article_id': article_id,
                        'article_title': article['title']
                    })
                    return article
                else:
                    self.results['failed_requests'] += 1
                    user_session['actions'].append({
                        'action': 'edit_article',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': False,
                        'error': response.status
                    })
                    return None
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"编辑文章异常: {str(e)}")
            user_session['actions'].append({
                'action': 'edit_article',
                'timestamp': time.time(),
                'response_time': time.time() - start_time,
                'success': False,
                'error': str(e)
            })
            return None
    
    async def comment_article(self, session, user_session):
        """评论文章"""
        if not user_session:
            return None
        
        # 先获取文章列表
        articles = await self.browse_articles(session, user_session)
        if not articles or not isinstance(articles) or len(articles) == 0:
            return None
        
        article_id = random.choice(articles)['id']
        url = f"{self.base_url}/pubcomments/{article_id}/"
        headers = {'Authorization': f'Bearer {user_session["token"]}'}
        data = {
            "content": f"负载测试评论 {self.generate_random_string(15)}"
        }
        
        start_time = time.time()
        try:
            async with session.post(url, json=data, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 201:
                    self.results['successful_requests'] += 1
                    comment = await response.json()
                    user_session['actions'].append({
                        'action': 'comment_article',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': True,
                        'article_id': article_id,
                        'comment_id': comment['id']
                    })
                    return comment
                else:
                    self.results['failed_requests'] += 1
                    user_session['actions'].append({
                        'action': 'comment_article',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': False,
                        'error': response.status
                    })
                    return None
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"评论文章异常: {str(e)}")
            user_session['actions'].append({
                'action': 'comment_article',
                'timestamp': time.time(),
                'response_time': time.time() - start_time,
                'success': False,
                'error': str(e)
            })
            return None
    
    async def like_article(self, session, user_session):
        """点赞文章"""
        if not user_session:
            return None
        
        # 先获取文章列表
        articles = await self.browse_articles(session, user_session)
        if not articles or not isinstance(articles) or len(articles) == 0:
            return None
        
        article_id = random.choice(articles)['id']
        url = f"{self.base_url}/likes/{article_id}/"
        headers = {'Authorization': f'Bearer {user_session["token"]}'}
        
        start_time = time.time()
        try:
            async with session.post(url, headers=headers) as response:
                response_time = time.time() - start_time
                self.results['response_times'].append(response_time)
                self.results['total_requests'] += 1
                
                if response.status == 201:
                    self.results['successful_requests'] += 1
                    user_session['actions'].append({
                        'action': 'like_article',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': True,
                        'article_id': article_id
                    })
                    return True
                else:
                    self.results['failed_requests'] += 1
                    user_session['actions'].append({
                        'action': 'like_article',
                        'timestamp': time.time(),
                        'response_time': response_time,
                        'success': False,
                        'error': response.status
                    })
                    return None
        except Exception as e:
            self.results['failed_requests'] += 1
            self.results['errors'].append(f"点赞文章异常: {str(e)}")
            user_session['actions'].append({
                'action': 'like_article',
                'timestamp': time.time(),
                'response_time': time.time() - start_time,
                'success': False,
                'error': str(e)
            })
            return None
    
    async def simulate_user_behavior(self, session, user_id):
        """模拟用户行为"""
        # 注册并登录用户
        user_session = await self.register_and_login(session, user_id)
        if not user_session:
            return
        
        self.results['user_sessions'].append(user_session)
        
        start_time = time.time()
        
        # 在测试时间内模拟用户行为
        while time.time() - start_time < self.test_duration:
            # 根据权重选择行为
            actions = []
            for action, weight in self.action_weights.items():
                actions.extend([action] * weight)
            
            selected_action = random.choice(actions)
            
            # 执行选中的行为
            if selected_action == 'browse_articles':
                await self.browse_articles(session, user_session)
            elif selected_action == 'search_articles':
                await self.search_articles(session, user_session)
            elif selected_action == 'read_article':
                await self.read_article(session, user_session)
            elif selected_action == 'create_article':
                await self.create_article(session, user_session)
            elif selected_action == 'edit_article':
                await self.edit_article(session, user_session)
            elif selected_action == 'comment_article':
                await self.comment_article(session, user_session)
            elif selected_action == 'like_article':
                await self.like_article(session, user_session)
            
            # 模拟用户思考时间
            await asyncio.sleep(random.uniform(1, 5))
    
    async def run_load_test(self):
        """运行负载测试"""
        print(f"开始负载测试: {self.concurrent_users} 并发用户，持续 {self.test_duration} 秒")
        print("=" * 60)
        
        # 创建HTTP会话
        connector = aiohttp.TCPConnector(limit=self.concurrent_users * 2)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            start_time = time.time()
            
            # 创建并发用户任务
            tasks = []
            for i in range(self.concurrent_users):
                task = asyncio.create_task(self.simulate_user_behavior(session, i))
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
            print(f"负载测试完成，总耗时: {total_time:.2f} 秒")
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("负载测试报告")
        print("=" * 60)
        
        # 基本统计
        print(f"总请求数: {self.results['total_requests']}")
        print(f"成功请求数: {self.results['successful_requests']}")
        print(f"失败请求数: {self.results['failed_requests']}")
        
        if self.results['total_requests'] > 0:
            success_rate = (self.results['successful_requests'] / self.results['total_requests']) * 100
            print(f"成功率: {success_rate:.2f}%")
        
        # 用户会话统计
        print(f"活跃用户数: {len(self.results['user_sessions'])}")
        
        # 用户行为统计
        action_counts = {}
        for session in self.results['user_sessions']:
            for action in session['actions']:
                action_name = action['action']
                action_counts[action_name] = action_counts.get(action_name, 0) + 1
        
        print(f"\n用户行为统计:")
        for action, count in sorted(action_counts.items()):
            print(f"  {action}: {count} 次")
        
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
            if avg_response_time < 0.2:
                print("响应时间: 优秀 (< 200ms)")
            elif avg_response_time < 0.5:
                print("响应时间: 良好 (200ms - 500ms)")
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
        
        # 保存详细报告
        self.save_detailed_report()
    
    def save_detailed_report(self):
        """保存详细报告到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"load_test_report_{timestamp}.json"
        
        report_data = {
            'test_config': {
                'concurrent_users': self.concurrent_users,
                'test_duration': self.test_duration,
                'base_url': self.base_url,
                'action_weights': self.action_weights,
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
                'rps': self.results['total_requests'] / self.test_duration if self.test_duration > 0 else 0,
                'success_rate': (self.results['successful_requests'] / self.results['total_requests']) * 100 if self.results['total_requests'] > 0 else 0
            }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n详细报告已保存到: {filename}")


async def main():
    """主函数"""
    # 不同负载级别的测试配置
    test_configs = [
        {'concurrent_users': 5, 'test_duration': 60, 'name': '轻负载测试'},
        {'concurrent_users': 10, 'test_duration': 120, 'name': '中负载测试'},
        {'concurrent_users': 20, 'test_duration': 300, 'name': '高负载测试'},
    ]
    
    for config in test_configs:
        print(f"\n开始 {config['name']}")
        load_test = LoadTest(
            concurrent_users=config['concurrent_users'],
            test_duration=config['test_duration']
        )
        
        await load_test.run_load_test()
        load_test.generate_report()
        
        # 测试间隔
        if config != test_configs[-1]:  # 不是最后一个测试
            print("\n等待 30 秒后继续下一个测试...")
            await asyncio.sleep(30)


if __name__ == "__main__":
    print("博客系统负载测试工具")
    print("请确保系统正在运行 (python manage.py runserver)")
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {str(e)}")
