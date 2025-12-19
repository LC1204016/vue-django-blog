# Vue + Django 前后端分离博客项目

## 项目概述

这是一个基于Vue.js 3和Django 5.2.8的现代化前后端分离博客项目。后端使用Django REST framework提供高性能RESTful API，前端使用Vue.js 3 + Vite + Pinia构建响应式用户界面。项目采用模块化架构设计，后端视图按功能拆分为多个独立模块，前端使用Composition API和组件化开发。

### 核心功能
- **用户系统**：完整的认证系统（注册、登录、JWT令牌）、用户资料管理、邮箱验证码、忘记密码
- **文章管理**：文章CRUD、分类标签、搜索功能、浏览量统计
- **社交互动**：评论系统、点赞踩功能、用户详情页、作者文章列表
- **技术特性**：JWT认证、环境变量管理、Redis缓存支持、完整测试框架

## 快速开始

### 5分钟启动项目

```bash
# 1. 克隆项目（如果还没有）
git clone https://github.com/LC1204016/vue-django-blog.git
cd blog

# 2. 后端设置
# 激活虚拟环境（Windows）
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
copy .env.example .env
# 编辑.env文件，至少配置数据库密码

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动后端服务
python manage.py runserver

# 3. 前端设置（新终端）
cd frontend

# 安装依赖
npm install

# 启动前端服务
npm run dev
```

访问：
- 前端：http://localhost:8080
- 后端API：http://localhost:8000/api
- 管理后台：http://localhost:8000/admin

### 技术栈
- **后端**: Python 3.12, Django 5.2.8, Django REST framework 3.16.1, Django REST framework SimpleJWT 5.5.1, MySQL 8.0, django-cors-headers 4.9.0, Pillow 12.0.0, python-dotenv 1.0.1, aiohttp 3.13.2, asyncio 4.0.0, mysqlclient 2.2.7, PyJWT 2.10.1, asgiref 3.11.0, sqlparse 0.5.4, tzdata 2025.2
- **前端**: Vue.js 3.4.0, Vite 5.0.0, @vitejs/plugin-vue 5.0.0, Vue Router 4.2.0, Pinia 2.1.0, Axios 1.6.0, ESLint 8.45.0, eslint-plugin-vue 9.15.0, Vitest 0.34.6, @vitest/ui 0.34.7, jsdom 22.1.0
- **测试**: Django TestCase, REST Framework APITestCase, Vitest, jsdom 22.1.0
- **通信**: RESTful API, CORS, JWT认证
- **邮件服务**: QQ邮箱SMTP服务（用于验证码发送）
- **缓存**: Redis缓存支持（可选，需安装django-redis）

### 项目结构
```
D:\dev\blog\
├───manage.py              # Django管理脚本
├───blog\                  # Django项目配置目录
│   ├───__init__.py
│   ├───asgi.py           # ASGI配置
│   ├───settings.py       # 项目设置（支持环境变量）
│   ├───urls.py           # URL路由配置
│   └───wsgi.py           # WSGI配置
├───backend\              # Django后端API应用
│   ├───__init__.py
│   ├───admin.py
│   ├───apps.py
│   ├───authentication.py # 自定义认证后端
│   ├───migrations\        # 数据库迁移文件
│   │   ├───0001_initial.py
│   │   ├───0002_remove_userprofile_birthday.py
│   │   ├───0003_category_alter_userprofile_introduction_article.py
│   │   ├───0004_userprofile_birthday.py
│   │   ├───0005_article_likes_article_views_comment.py
│   │   ├───0006_comment_author.py
│   │   ├───0007_comment_pub_time.py
│   │   ├───0008_rename_likes_article_like_count_like.py
│   │   ├───0009_article_dislike_count_dislike.py
│   │   ├───0010_article_updated_time.py
│   │   ├───0011_userprofile_profile_pic.py
│   │   ├───0012_tag_article_tags.py
│   │   ├───0013_captcha.py
│   │   ├───0014_remove_article_summary.py
│   │   ├───0015_category_tag.py
│   │   └───0016_alter_captcha_created_at.py
│   ├───models.py         # 数据模型
│   ├───permissions.py    # 权限和认证类
│   ├───serializers.py    # API序列化器
│   ├───test_framework.py # 后端测试框架
│   ├───urls.py           # API路由配置
│   ├───views.py          # API视图（模块化视图导入）
│   ├───article_views.py  # 文章相关视图
│   ├───auth_views.py     # 认证相关视图
│   ├───category_views.py # 分类和标签视图
│   ├───comment_views.py  # 评论相关视图
│   ├───interaction_views.py # 互动功能视图
│   ├───profile_views.py  # 用户资料视图
│   └───management\       # 管理命令
│       └───commands\     # 自定义命令
│           ├───create_category_tags.py
│           └───fix_tag_model.py
├───frontend\             # Vue.js前端项目
│   ├───.env.development  # 开发环境变量
│   ├───.env.production   # 生产环境变量
│   ├───index.html
│   ├───package.json
│   ├───package-lock.json
│   ├───vite.config.js    # Vite配置（支持开发和生产环境）
│   └───src\
│       ├───App.vue
│       ├───main.js
│       ├───style.css
│       ├───assets\        # 静态资源
│       ├───components\    # 组件
│       │   ├───Footer.vue
│       │   └───Header.vue
│       ├───router\        # 路由配置
│       │   └───index.js
│       ├───services\      # API服务
│       │   └───api.js     # API服务封装（支持JWT自动刷新）
│       ├───stores\        # Pinia状态管理
│       │   ├───auth.js
│       │   ├───index.js
│       │   └───posts.js
│       ├───tests\         # 前端测试目录
│       │   ├───basic.test.js
│       │   └───setup.js
│       │   └───unit\       # 单元测试
│       │       ├───auth.test.js
│       │       └───posts.test.js
│       ├───utils\         # 工具函数
│       └───views\         # 页面组件
│           ├───CreatePost.vue
│           ├───EditPost.vue # 文章编辑页面
│           ├───ForgotPassword.vue # 忘记密码页面
│           ├───Home.vue
│           ├───Login.vue
│           ├───NotFound.vue
│           ├───PostDetail.vue
│           ├───Posts.vue
│           ├───Profile.vue
│           ├───Register.vue
│           └───UserProfile.vue # 用户详情页面（支持分页）
├───api\                  # 额外的API应用
│   ├───__init__.py
│   ├───admin.py
│   ├───apps.py
│   ├───models.py
│   ├───tests.py
│   ├───views.py
│   └───migrations\
│       └───__init__.py
├───test\                 # 测试和压力测试脚本
│   ├───load_test.py      # 负载测试
│   ├───run_tests.py      # 测试运行器
│   ├───simple_load_test.py
│   ├───simple_load_test2.py
│   ├───stress_test.py    # 压力测试
│   ├───test_connection.py
│   ├───test_api.py       # API测试
│   ├───test_comment.py   # 评论测试
│   ├───check_categories.py
│   ├───debug_test.py
│   ├───simple_test.py
│   └───TESTING.md        # 测试指南文档
├───media\                # 媒体文件目录
│   └───profile_pics\     # 用户头像目录
├───static\               # 静态文件目录（用于收集静态文件）
├───.venv\               # Python虚拟环境
├───.idea\               # IDE配置目录
├───.git\                # Git版本控制
├───.env.example         # 环境变量示例文件
├───requirements.txt     # Python依赖列表
```

## 构建和运行

### 环境准备
1. 确保Python 3.12和Node.js已安装
2. 激活Python虚拟环境：
   ```bash
   .venv\Scripts\activate
   ```

### 环境变量配置
1. 复制环境变量示例文件：
   ```bash
   copy .env.example .env
   ```
2. 根据实际情况修改`.env`文件中的配置，包括：
   - Django配置（SECRET_KEY, DEBUG, ALLOWED_HOSTS）
   - 数据库配置（MYSQL_PASSWORD, DB_NAME, DB_USER, DB_HOST, DB_PORT）
   - 邮件配置（DEFAULT_FROM_EMAIL, QQ_EMAIL_HOST_PASSWORD）
   - 静态文件和媒体文件路径（STATIC_ROOT, MEDIA_ROOT）
   - 日志配置（LOG_LEVEL, LOG_FILE）
   - CORS配置（CORS_ALLOWED_ORIGINS）

### 前端环境变量配置
前端支持环境变量配置：
- 开发环境：`frontend/.env.development`

配置示例：
```bash
# 开发环境
VITE_APP_ENV=development
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_TITLE=Vue+Django博客系统(开发版)
```

**注意**: 
- Vite环境变量必须以 `VITE_` 前缀开头才能在客户端代码中访问
- 在代码中通过 `import.meta.env.VITE_变量名` 访问环境变量

### 数据库配置
项目使用MySQL 8.0数据库，确保已安装MySQL服务并创建`blog`数据库。

### Redis缓存配置（可选）
项目已配置Redis缓存支持，如需启用：
```bash
pip install django-redis
```
确保Redis服务运行在 `127.0.0.1:6379`，或修改 `blog/settings.py` 中的 `CACHES` 配置。

### 后端运行

#### 数据库迁移
```bash
.venv\Scripts\python.exe manage.py makemigrations
.venv\Scripts\python.exe manage.py migrate
```

#### 创建超级用户
```bash
.venv\Scripts\python.exe manage.py createsuperuser
```

#### 创建分类和标签关联数据
```bash
.venv\Scripts\python.exe manage.py create_category_tags
```

#### 修复标签模型（如需要）
```bash
.venv\Scripts\python.exe manage.py fix_tag_model
```

#### 启动Django开发服务器
```bash
.venv\Scripts\python.exe manage.py runserver
```
后端API将在 http://localhost:8000 运行

### 前端运行

#### 安装依赖
```bash
cd frontend
npm install
```

#### 启动Vue开发服务器
```bash
npm run dev
```
前端应用将在 http://localhost:8080 运行

#### 构建生产版本
```bash
npm run build
```

#### 预览生产版本
```bash
npm run preview
```

#### 代码检查
```bash
npm run lint
```

#### 前端测试
```bash
# 运行测试
npm run test

# 运行测试并查看UI界面
npm run test:ui

# 运行测试并监视文件变化
npm run test:watch
```

## 测试

### 后端测试

#### 运行单元测试
```bash
# 激活虚拟环境
.venv\Scripts\activate

# 运行所有后端测试
python manage.py test backend.test_framework --verbosity=2

# 运行特定测试类
python manage.py test backend.test_framework.AuthenticationTestCase --verbosity=2
```

#### 运行性能测试
```bash
# 运行压力测试
python test/stress_test.py

# 运行负载测试
python test/load_test.py

# 运行简单连接测试
python test/test_connection.py
```

### 前端测试

#### 运行单元测试
```bash
# 进入前端目录
cd frontend

# 运行测试
npm run test

# 运行测试并查看UI界面
npm run test:ui

# 运行测试并监视文件变化
npm run test:watch
```

### 运行完整测试套件
```bash
# 运行所有测试
python test/run_tests.py

# 运行包含压力测试的完整测试
python test/run_tests.py --include-stress

# 运行包含负载测试的完整测试
python test/run_tests.py --include-load

# 运行所有测试（包括性能测试）
python test/run_tests.py --include-stress --include-load

# 只运行单元测试
python test/run_tests.py --unit-only

# 只运行前端测试
python test/run_tests.py --frontend-only

# 只运行后端测试
python test/run_tests.py --backend-only
```

## API端点

### 认证相关
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/register/` - 用户注册
- `POST /api/captcha/` - 发送邮箱验证码
- `POST /api/password/reset/` - 重置密码（通过邮箱验证码）
- `POST /api/token/refresh/` - 刷新JWT令牌

### 文章相关（RESTful API）
- `GET /api/articles/` - 获取文章列表（支持分页，默认每页16条）
- `POST /api/articles/` - 创建文章（需要认证）
- `GET /api/articles/<int:pk>/` - 获取文章详情
- `PUT /api/articles/<int:pk>/` - 更新文章（需要认证）
- `PATCH /api/articles/<int:pk>/` - 部分更新文章（需要认证）
- `DELETE /api/articles/<int:pk>/` - 删除文章（需要认证）

### 分类和标签相关
- `GET /api/categories/` - 获取所有分类
- `GET /api/tags/<category>/` - 获取指定分类下的所有标签

### 评论相关
- `GET /api/articles/<article_id>/comments/` - 获取文章评论
- `POST /api/articles/<article_id>/comments/` - 发表评论（需要认证）

### 互动功能
- `POST /api/articles/<int:article_id>/likes/` - 点赞文章（需要认证）
- `DELETE /api/articles/<int:article_id>/likes/` - 取消点赞（需要认证）
- `POST /api/articles/<int:article_id>/dislikes/` - 踩文章（需要认证）
- `DELETE /api/articles/<int:article_id>/dislikes/` - 取消踩（需要认证）

### 用户资料相关
- `GET /api/users/profile/` - 获取当前用户资料（需要认证）
- `PUT /api/users/profile/` - 更新当前用户资料（需要认证）
- `PATCH /api/users/profile/` - 部分更新当前用户资料（需要认证）
- `GET /api/users/<int:user_id>/profile/` - 获取指定用户资料和文章列表（支持分页）

## 数据模型

### 用户相关
- `User` - Django内置用户模型
- `UserProfile` - 用户扩展资料，包含个人简介、生日、头像和注册时间

### 文章相关
- `Article` - 文章模型，包含标题、内容、作者、分类、标签、发布时间、更新时间、浏览量、点赞数和踩数
- `Category` - 文章分类模型，包含分类描述
- `Tag` - 文章标签模型
- `CategoryTag` - 分类-标签关联模型，建立分类和标签的多对多关系

### 互动相关
- `Like` - 点赞记录模型
- `Dislike` - 踩记录模型
- `Comment` - 评论模型，包含文章、作者、内容和发布时间

### 验证相关
- `Captcha` - 邮箱验证码模型，包含邮箱、验证码和创建时间（auto_now=True）

## 开发工作流程

### 新功能开发流程
1. **创建功能分支**：从develop分支创建新的功能分支
2. **后端开发**：
   - 在`backend/models.py`中定义数据模型
   - 创建数据库迁移：`python manage.py makemigrations`
   - 应用迁移：`python manage.py migrate`
   - 在对应的视图模块中实现API（如`article_views.py`）
   - 在`backend/serializers.py`中添加序列化器
   - 在`backend/urls.py`中配置路由
   - 编写测试用例
3. **前端开发**：
   - 在`frontend/src/services/api.js`中添加API调用方法
   - 在`frontend/src/views/`中创建或修改页面组件
   - 在`frontend/src/router/index.js`中配置路由
   - 更新Pinia store（如需要）
   - 编写组件测试
4. **测试验证**：
   - 运行后端测试：`python manage.py test`
   - 运行前端测试：`npm run test`
   - 手动测试功能
5. **代码审查**：提交Pull Request，等待代码审查
6. **合并代码**：审查通过后合并到develop分支

### 常见开发任务

#### 添加新的API端点
```python
# 1. 在对应的视图模块中添加视图类或函数
# backend/article_views.py
from rest_framework.views import APIView

class NewFeatureView(APIView):
    def get(self, request):
        # 实现逻辑
        pass

# 2. 在urls.py中注册路由
# backend/urls.py
path('new-feature/', views.NewFeatureView.as_view(), name='new-feature'),
```

#### 添加新的前端页面
```javascript
// 1. 创建页面组件
// frontend/src/views/NewPage.vue

// 2. 在路由中注册
// frontend/src/router/index.js
{
  path: '/new-page',
  name: 'NewPage',
  component: () => import('../views/NewPage.vue'),
  meta: { requiresAuth: true, title: '新页面' }
}
```

#### 数据库模型变更
```bash
# 1. 修改models.py
# 2. 创建迁移文件
python manage.py makemigrations

# 3. 查看迁移SQL（可选）
python manage.py sqlmigrate backend 0017

# 4. 应用迁移
python manage.py migrate

# 5. 如果需要回滚
python manage.py migrate backend 0016
```

## 开发约定

### 后端设置配置
- 开发环境：`DEBUG = False`（默认，通过环境变量控制）
- 数据库：MySQL 8.0 (`blog`)，配置通过环境变量管理
- API框架：Django REST framework
- JWT认证：使用Django REST framework SimpleJWT
- JWT配置：访问令牌有效期60分钟，刷新令牌有效期7天
- CORS配置：通过环境变量 `CORS_ALLOWED_ORIGINS` 控制，默认允许 `http://localhost:8080` 和 `http://127.0.0.1:8080`
- 自定义认证后端：支持邮箱和用户名登录
- 中间件：已启用CSRF保护（`django.middleware.csrf.CsrfViewMiddleware`）
- 媒体文件：支持用户头像上传，存储在 `media/` 目录
- 邮件服务：使用QQ邮箱SMTP服务发送验证码
- 环境变量：完整的环境变量管理，支持数据库、邮件、缓存、日志等配置
- 解析器：支持JSON、MultiPart和Form解析器
- 渲染器：使用JSON渲染器
- 权限类：默认允许所有访问（开发环境）
- 缓存配置：支持Redis缓存（需安装django-redis），默认配置为 `redis://127.0.0.1:6379/1`
- 日志配置：支持文件和控制台日志输出，通过 `LOG_LEVEL` 和 `LOG_FILE` 环境变量控制
- CORS配置：通过 `CORS_ALLOWED_ORIGINS` 环境变量控制允许的跨域源，多个源用逗号分隔
- 异步支持：添加了aiohttp和asyncio依赖，提供异步处理能力

### 前端开发约定
- 构建工具：Vite 5.0.0，优化构建性能
- 端口：8080
- API代理：`/api` 请求代理到 `http://localhost:8000`
- HTTP客户端：Axios 1.6.0，封装完整的API服务，支持JWT自动刷新
- 状态管理：Pinia 2.1.0，包含auth和posts状态管理
- 路由：Vue Router 4.2.0，实现动态路由懒加载，支持路由守卫
- 代码规范：ESLint 8.45.0, eslint-plugin-vue 9.15.0
- 认证状态：支持"记住我"功能，Token可存储在localStorage或sessionStorage
- 路由守卫：实现权限控制，需要登录的页面会自动跳转到登录页
- 分页设置：文章列表默认每页显示16条，用户文章列表支持分页
- 请求拦截器：自动添加Token到请求头
- 响应拦截器：统一处理错误状态码和Token自动刷新
- 动态路由：使用动态导入实现路由懒加载（CreatePost.vue, EditPost.vue, UserProfile.vue, ForgotPassword.vue）
- 页面标题：通过路由meta自动设置页面标题
- 环境变量：支持环境变量配置（`.env.development`）
- 构建优化：支持代码压缩、资源分离、Tree Shaking等优化
- 测试框架：使用Vitest进行单元测试，支持测试UI和监视模式
- 测试环境：使用jsdom模拟浏览器环境进行测试
- 别名配置：使用`@`别名指向`src`目录，简化导入路径
- 路由配置：包含首页、文章列表、文章详情、登录注册、个人中心、用户详情、忘记密码等完整路由
- **Vite配置**：支持代码分割、懒加载、资源优化和测试集成
- **构建目标**：ES2015，支持现代浏览器
- **资源管理**：自动分割CSS和JavaScript资源
- **API环境配置**：支持通过VITE_API_BASE_URL环境变量配置API基础URL
- **代码分割**：自动分割Vue相关库和第三方依赖，优化加载性能
- **资源优化**：支持压缩、去重和Tree Shaking，减小打包体积
- **测试配置**：完整的Vitest测试环境配置，包含全局测试设置和Mock对象
- **依赖优化**：自动检测和优化依赖，包含Vitest集成配置
- **别名配置详解**：`@` 别名指向 `src` 目录，使用 `path.resolve` 确保跨平台兼容
- **代理配置**：开发环境下 `/api` 请求自动代理到 `http://localhost:8000`
- **构建输出**：生产构建输出到 `dist` 目录，资源分类存储在 `assets` 子目录
- **代码分割策略**：Vue相关库（vue, vue-router, pinia）和第三方库（axios）分别打包
- **测试环境**：集成jsdom环境，支持组件测试和单元测试

### 测试约定
- 后端测试：使用Django TestCase和REST Framework APITestCase
- 前端测试：使用Vitest进行单元测试，jsdom作为测试环境
- 性能测试：包含压力测试和负载测试脚本
- 测试报告：生成JSON和HTML格式的测试报告
- 测试覆盖率：支持代码覆盖率分析
- 测试自动化：提供完整的测试运行器，支持单元测试、集成测试和性能测试
- 测试分类：分为单元测试、集成测试、压力测试和负载测试四大类
- 测试超时：单元测试5分钟超时，压力测试10分钟超时，负载测试15分钟超时
- 测试文档：完整的测试指南和最佳实践文档（test/TESTING.md）
- 测试脚本：包含API测试、评论测试、分类检查等多种专项测试脚本
- 测试目录：所有测试脚本位于 `test/` 目录下
- **测试运行器**：`test/run_tests.py` 提供统一的测试运行和报告生成功能
- **测试报告**：自动生成可视化HTML报告和JSON格式报告，包含测试统计和图表
- **测试环境隔离**：前端和后端测试环境完全独立，确保测试结果准确性
- **测试超时机制**：为不同类型的测试设置合理的超时时间，防止测试卡死
- **测试结果分析**：提供详细的测试失败原因分析和错误输出
- **性能测试指标**：包含响应时间、成功率、每秒请求数(RPS)等关键性能指标
- **前端测试配置**：完整的Vitest测试环境设置，包含localStorage/sessionStorage Mock和TextEncoder兼容性处理
- **后端测试框架**：模块化测试类设计，包含认证、文章、评论、互动、用户资料、边界条件和错误处理测试
- **测试基类**：提供通用测试工具和方法，简化测试用例编写
- **测试数据管理**：自动化测试数据创建和清理，确保测试环境一致性

### 安全注意事项
- **密钥管理**：开发环境应使用安全的`SECRET_KEY`
- **调试模式**：开发环境可设置`DEBUG = True`便于调试
- **主机白名单**：配置`ALLOWED_HOSTS`限制允许访问的域名
- **CORS配置**：通过`CORS_ALLOWED_ORIGINS`环境变量限制跨域源
- **验证码安全**：邮箱验证码10分钟内有效，防止暴力破解
- **JWT令牌**：访问令牌60分钟有效期，刷新令牌7天有效期，支持令牌轮换
- **敏感信息**：数据库密码、邮件服务密码等通过环境变量管理，不在代码中硬编码
- **CSRF保护**：已启用CSRF中间件，增强表单提交安全性
- **环境变量文件**：`.env`文件不应提交到版本控制，使用`.env.example`作为模板
- **依赖安全**：定期更新依赖包，关注安全漏洞公告

### 国际化
- 语言代码：`zh-hans`（简体中文）
- 时区：`Asia/shanghai`
- 未启用时区支持（USE_TZ = False）

## 故障排查

### 常见问题及解决方案

#### 后端问题

**问题1：数据库连接失败**
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```
解决方案：
- 检查MySQL服务是否运行
- 验证`.env`文件中的数据库配置
- 确认数据库用户权限
- 检查防火墙设置

**问题2：迁移冲突**
```
django.db.migrations.exceptions.InconsistentMigrationHistory
```
解决方案：
```bash
# 查看迁移状态
python manage.py showmigrations

# 回滚到特定迁移
python manage.py migrate backend 0016

# 重新应用迁移
python manage.py migrate
```

**问题3：静态文件404**
解决方案：
```bash
# 收集静态文件
python manage.py collectstatic --noinput

# 检查STATIC_ROOT和STATIC_URL配置
```

**问题4：CORS错误**
```
Access to XMLHttpRequest has been blocked by CORS policy
```
解决方案：
- 检查`CORS_ALLOWED_ORIGINS`环境变量
- 确认前端URL在允许列表中
- 验证`django-cors-headers`已安装并配置

#### 前端问题

**问题1：API请求失败**
```
Network Error / Request failed with status code 500
```
解决方案：
- 检查后端服务是否运行（http://localhost:8000）
- 查看浏览器开发者工具的Network标签
- 检查API端点URL是否正确
- 验证JWT令牌是否有效

**问题2：路由404**
```
Cannot GET /some-route
```
解决方案：
- 检查`router/index.js`中的路由配置
- 确认组件路径正确
- 验证路由懒加载语法

**问题3：Vite构建失败**
```
Failed to resolve import
```
解决方案：
```bash
# 清除node_modules和重新安装
rm -rf node_modules package-lock.json
npm install

# 清除Vite缓存
rm -rf node_modules/.vite
```

**问题4：环境变量未生效**
解决方案：
- 确认环境变量以`VITE_`前缀开头
- 重启开发服务器
- 检查`.env.development`或`.env.production`文件

#### 测试问题

**问题1：测试数据库错误**
解决方案：
```bash
# 使用--keepdb保留测试数据库
python manage.py test --keepdb

# 强制重建测试数据库
python manage.py test --keepdb=false
```

**问题2：前端测试失败**
解决方案：
```bash
# 清除测试缓存
npm run test -- --clearCache

# 更新测试快照
npm run test -- -u
```

### 日志查看

#### 后端日志
```bash
# 查看Django日志
tail -f django.log
```

#### 前端日志
- 浏览器开发者工具 Console 标签
- Network 标签查看API请求详情

### 性能优化建议

1. **数据库优化**
   - 添加索引到常查询字段
   - 使用`select_related()`和`prefetch_related()`减少查询次数
   - 启用数据库查询日志分析慢查询

2. **缓存优化**
   - 安装并启用Redis缓存
   - 缓存频繁访问的数据
   - 使用HTTP缓存头

3. **前端优化**
   - 使用代码分割和懒加载
   - 优化图片大小和格式
   - 启用Gzip压缩

## 项目状态

当前项目是一个功能完整的前后端分离博客系统，包含：

### 后端功能
- Django REST framework API
- 用户认证系统（注册、登录、资料管理）
- 邮箱验证码功能
- 忘记密码功能
- 文章CRUD功能
- 文章分类系统
- 文章标签系统
- 评论系统
- 点赞/踩互动功能
- 文章浏览量统计
- 自定义认证后端（支持邮箱/用户名登录）
- CORS支持
- MySQL数据库集成
- JWT认证系统（已配置完整实现）
- 分页支持
- 获取用户文章功能
- 用户头像上传功能
- 文章更新时间记录
- 分类-标签关联管理命令
- 文章搜索功能（支持关键词、分类和排序）
- 环境变量管理
- Redis缓存支持
- 日志系统
- 完整的测试框架（单元测试、集成测试、性能测试）
- 异步处理支持（aiohttp, asyncio）
- **模块化视图架构**：将视图按功能拆分为多个模块化文件
  - `article_views.py` - 文章CRUD操作（ArticleList, ArticleDetail）
  - `auth_views.py` - 用户认证（登录、注册、验证码、密码重置）
  - `category_views.py` - 分类和标签管理
  - `comment_views.py` - 评论功能
  - `interaction_views.py` - 点赞和踩功能
  - `profile_views.py` - 用户资料管理
- **RESTful API设计**：符合REST规范的API端点设计，支持GET、POST、PUT、PATCH、DELETE方法
- **统一响应格式**：API返回统一的JSON格式，便于前端处理
- **错误处理**：完善的错误处理机制，返回清晰的错误信息和状态码

### 前端功能
- Vue.js 3.4.0 + Composition API
- 完整的路由系统（首页、文章列表、文章详情、登录、注册、个人中心、文章编辑、用户详情、忘记密码）
- 用户认证状态管理（Pinia）
- API服务封装
- 响应式设计
- 路由守卫（权限控制）
- "记住我"登录功能
- 文章发布和编辑界面
- 请求/响应拦截器
- 错误处理和状态反馈
- 文章搜索功能（支持关键词、分类和排序）
- 分页导航
- 评论展示
- 点赞/踩交互
- 个人中心页面（个人信息、修改密码、我的文章管理）
- 用户头像上传和显示
- 邮箱验证码功能
- 文章标签选择和管理
- 用户详情页面（展示用户资料和其发布的文章，支持分页）
- JWT令牌自动刷新机制
- 环境变量配置
- 前端单元测试框架（Vitest）
- 测试UI界面支持
- 路径别名配置（@指向src目录）
- **Vite构建优化**：支持代码分割、懒加载、资源优化
- **组件化设计**：Header、Footer等公共组件复用
- **状态持久化**：支持用户登录状态持久化（localStorage/sessionStorage）
- **路由元信息**：支持页面标题、权限控制等元信息配置
- **测试集成**：Vitest测试框架，支持UI测试和监视模式
- **开发体验**：热重载、代码检查、自动化测试
- **分页功能**：用户文章列表和个人中心支持分页显示
- **忘记密码功能**：完整的忘记密码流程，包含邮箱验证码验证

### 已实现的新功能
1. 文章标签系统 - 完整的标签模型和管理功能，支持多标签关联
2. 邮箱验证码系统 - 使用QQ邮箱SMTP服务发送验证码，支持注册验证
3. 文章编辑功能 - 完整的文章编辑界面，支持标题、内容、分类和标签修改
4. 用户头像系统 - 支持用户头像上传和显示，包含默认头像
5. 文章更新时间记录 - 自动记录文章最后更新时间
6. 媒体文件管理 - 建立了完整的媒体文件存储结构
7. JWT认证系统 - 完整实现Django REST framework SimpleJWT，包含令牌刷新机制
8. 请求/响应拦截器 - 统一处理API请求、错误和令牌自动刷新
9. 验证码模型 - 完整的验证码存储和验证机制
10. 文章摘要移除 - 移除了文章摘要字段，简化了文章结构
11. 分类-标签关联系统 - 实现CategoryTag模型，建立分类和标签的多对多关系
12. 分类描述功能 - 为Category模型添加描述字段
13. 分类标签管理命令 - create_category_tags命令创建分类和标签关联关系
14. 标签模型修复命令 - fix_tag_model命令用于修复标签模型结构
15. 用户详情页面 - 新增UserProfile.vue组件，展示用户资料和其发布的文章列表
16. 作者链接功能 - 在文章详情页面添加点击作者名称跳转到用户详情页面的功能
17. 文章搜索功能 - 实现了基于关键词、分类和排序的文章搜索API，支持多关键词搜索
18. CSRF保护 - 已启用CSRF中间件，增强安全性
19. 令牌自动刷新 - 前端实现JWT令牌自动刷新机制，提升用户体验
20. 环境变量管理 - 支持通过.env文件管理配置
21. Redis缓存支持 - 已配置Redis缓存框架（需安装django-redis），可选启用以提升性能
22. 日志系统 - 完整的日志配置，支持文件和控制台输出
23. 后端测试框架 - 完整的单元测试、集成测试和性能测试框架
24. 前端测试框架 - 集成Vitest测试框架，支持单元测试和UI测试
25. 测试自动化脚本 - 提供完整的测试运行器和报告生成
26. 性能测试工具 - 包含压力测试和负载测试脚本，评估系统性能
27. 测试文档 - 详细的测试指南和最佳实践文档（test/TESTING.md）
28. 异步处理支持 - 添加aiohttp和asyncio依赖，提供异步处理能力
29. 前端测试UI - 支持可视化测试界面，提升测试体验
30. 路径别名配置 - 简化前端导入路径，提高开发效率
31. 测试分类优化 - 将测试分为单元测试、集成测试、压力测试和负载测试四大类
32. 测试超时机制 - 为不同类型的测试设置合理的超时时间
33. 测试报告增强 - 生成JSON和HTML格式的详细测试报告
34. **后端模块化架构** - 将视图按功能拆分为多个模块化文件，提高代码可维护性
35. **Vite构建优化** - 支持代码分割、懒加载和Tree Shaking
36. **API端点优化** - 完整的RESTful API设计，支持文章删除功能
37. **分页功能增强** - 用户文章列表和个人中心支持分页显示，提升用户体验
38. **API环境配置** - 前端支持通过环境变量配置API基础URL
39. **忘记密码功能** - 完整的忘记密码流程，包含邮箱验证码验证和密码重置
40. **验证码模型优化** - 更新验证码模型的created_at字段为auto_now=True，确保时间戳准确性

### 项目特色亮点
- **现代化架构**：采用Vue 3 Composition API和Django 5.2.8最新技术栈
- **完整测试体系**：包含单元测试、集成测试、性能测试和详细测试文档（test/TESTING.md）
- **高性能优化**：Redis缓存支持（可选）、异步处理、代码分离和Tree Shaking
- **安全防护**：JWT认证、CSRF保护、环境变量管理
- **开发友好**：热重载、代码检查、自动化测试和详细文档
- **模块化设计**：后端视图模块化，前端组件化，提高代码复用性和可维护性
- **API设计**：RESTful API设计，支持JWT认证和令牌自动刷新
- **前端优化**：Vite构建优化，支持代码分割和懒加载
- **测试自动化**：完整的测试运行器，支持多种测试类型和报告生成
- **用户体验**：分页功能、响应式设计和流畅的交互体验
- **密码管理**：完整的忘记密码和重置密码功能，提升用户账户安全性
- **环境配置**：完整的环境变量管理
- **测试报告**：可视化HTML测试报告，包含图表和进度条，便于测试结果分析
- **性能监控**：压力测试和负载测试工具，评估系统性能和稳定性
- **测试框架升级**：模块化测试基类设计，支持边界条件和错误处理测试
- **依赖管理**：精确的版本控制，包含asgiref、sqlparse、tzdata等核心依赖

### 下一步开发建议
1. 将django-redis添加到requirements.txt，完善Redis缓存依赖管理
2. 实现用户权限管理（管理员/普通用户）
3. 添加文章收藏功能
4. 添加网站统计和分析
5. 添加富文本编辑器
6. 实现文章草稿功能
7. 添加图片上传功能（到文章内容中）
8. 实现用户关注系统
9. 优化文章搜索功能（添加全文搜索、高亮显示等）
10. 实现评论回复功能
11. 添加消息通知系统
12. 实现文章导出功能
13. 添加文章阅读进度记录
14. 完善用户社交功能（用户互相关注、动态推送）
15. 添加API文档（Swagger/OpenAPI）
16. 实现数据备份和恢复功能
17. 添加多语言支持
18. 实现文章定时发布功能
19. 添加文章访问统计和热门推荐
20. 实现邮件订阅功能
21. 优化前端性能（实现SSR或SSG）
22. 添加文件上传进度显示
23. 实现文章版本历史功能
24. 添加文章分享功能
25. 实现评论点赞功能
26. 添加用户活动时间线
27. 实现文章审核工作流
28. 优化SEO（Meta标签、结构化数据）
29. 添加网站地图生成
30. 实现RSS订阅功能
31. 增加测试覆盖率，添加更多边界测试和异常处理测试
32. 实现WebSocket支持，添加实时功能
33. 添加全文搜索引擎（如Elasticsearch）

## 贡献指南

### 如何贡献

我们欢迎所有形式的贡献，包括但不限于：
- 🐛 报告Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复或新功能

### 贡献流程

1. **Fork项目**
   ```bash
   # 在GitHub上Fork项目到你的账号
   ```

2. **克隆到本地**
   ```bash
   git clone https://github.com/你的用户名/vue-django-blog.git
   cd blog
   ```

3. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

4. **进行开发**
   - 遵循项目的代码规范
   - 编写清晰的提交信息
   - 添加必要的测试
   - 更新相关文档

5. **提交代码**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   # 或
   git commit -m "fix: 修复Bug描述"
   ```

6. **推送到远程**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建Pull Request**
   - 在GitHub上创建PR
   - 填写PR模板，描述你的改动
   - 等待代码审查

### 提交信息规范

使用约定式提交（Conventional Commits）：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

类型：
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(article): 添加文章导出功能

添加了将文章导出为PDF和Markdown格式的功能。

Closes #123
```

### 代码规范

#### Python/Django
- 遵循PEP 8规范
- 使用有意义的变量名和函数名
- 添加必要的文档字符串
- 单元测试覆盖核心功能

#### JavaScript/Vue
- 遵循ESLint配置
- 使用Vue 3 Composition API
- 组件名使用PascalCase
- 保持组件单一职责

### 测试要求

提交代码前请确保：
```bash
# 后端测试通过
python manage.py test

# 前端测试通过
cd frontend
npm run test

# 代码规范检查通过
npm run lint
```

### 问题报告

报告Bug时请提供：
1. 问题描述
2. 复现步骤
3. 期望行为
4. 实际行为
5. 环境信息（操作系统、Python版本、Node版本等）
6. 相关日志或截图

### 功能建议

提出新功能时请说明：
1. 功能描述
2. 使用场景
3. 预期效果
4. 可能的实现方案

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 联系方式

- GitHub Issues: https://github.com/LC1204016/vue-django-blog/issues
- 项目维护者: LC1204016

## 致谢

感谢所有为本项目做出贡献的开发者！

---

**最后更新**: 2025年12月19日
