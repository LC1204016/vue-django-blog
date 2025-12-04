# Vue + Django 前后端分离博客项目

## 项目概述

这是一个基于Vue.js 3和Django 5.2.8的前后端分离博客项目。后端使用Django REST framework提供API，前端使用Vue.js 3 + Vite + Pinia构建用户界面，实现了完整的用户认证、文章发布、编辑、评论互动、点赞功能和文章标签系统。

### 技术栈
- **后端**: Python 3.12, Django 5.2.8, Django REST framework, MySQL, django-cors-headers, Pillow
- **前端**: Vue.js 3.4.0, Vite 5.0.0, Vue Router 4.2.0, Pinia 2.1.0, Axios 1.6.0, ESLint 8.45.0
- **通信**: RESTful API, CORS, 自定义Token认证
- **邮件服务**: QQ邮箱SMTP服务（用于验证码发送）

### 项目结构
```
D:\dev\blog\
├───manage.py              # Django管理脚本
├───test_email.py          # 邮件测试脚本
├───blog\                  # Django项目配置目录
│   ├───__init__.py
│   ├───asgi.py           # ASGI配置
│   ├───settings.py       # 项目设置
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
│   │   └───0014_remove_article_summary.py
│   ├───models.py         # 数据模型
│   ├───permissions.py    # 权限和认证类
│   ├───serializers.py    # API序列化器
│   ├───tests.py
│   ├───urls.py           # API路由配置
│   ├───views.py          # API视图
│   └───management\       # 管理命令
│       └───commands\     # 自定义命令
│           ├───create_test_posts.py
│           └───create_tags.py
├───frontend\             # Vue.js前端项目
│   ├───index.html
│   ├───package.json
│   ├───vite.config.js
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
│       │   └───api.js
│       ├───stores\        # Pinia状态管理
│       │   ├───auth.js
│       │   ├───index.js
│       │   └───posts.js
│       ├───utils\         # 工具函数
│       └───views\         # 页面组件
│           ├───CreatePost.vue
│           ├───EditPost.vue # 文章编辑页面
│           ├───Home.vue
│           ├───Login.vue
│           ├───NotFound.vue
│           ├───PostDetail.vue
│           ├───Posts.vue
│           ├───Profile.vue
│           └───Register.vue
├───api\                  # 额外的API应用
│   ├───__init__.py
│   ├───admin.py
│   ├───apps.py
│   ├───models.py
│   ├───tests.py
│   ├───views.py
│   └───migrations\
│       └───__init__.py
├───media\                # 媒体文件目录
│   ├───default.png       # 默认头像
│   └───profile_pics\     # 用户头像目录
├───templates\            # Django模板目录（当前为空）
├───.venv\               # Python虚拟环境
├───.idea\               # IDE配置目录
└───.git\                # Git版本控制
```

## 构建和运行

### 环境准备
1. 确保Python 3.12和Node.js已安装
2. 激活Python虚拟环境：
   ```bash
   .venv\Scripts\activate
   ```

### 数据库配置
项目使用MySQL数据库，确保已安装MySQL服务并创建`blog`数据库。

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

#### 创建初始标签数据
```bash
.venv\Scripts\python.exe manage.py create_tags
```

#### 创建测试文章数据
```bash
.venv\Scripts\python.exe manage.py create_test_posts
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

## API端点

### 认证相关
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/register/` - 用户注册
- `POST /api/captcha/` - 发送邮箱验证码

### 文章相关
- `GET /api/getposts` - 获取文章列表（支持分页，默认每页12条）
- `POST /api/pubposts/` - 创建文章（需要认证）
- `GET /api/posts/<id>/` - 获取文章详情
- `GET /api/getmyposts/` - 获取当前用户的文章（需要认证）
- `PUT /api/edit/<post_id>/` - 更新文章（需要认证）
- `GET /api/edit/<post_id>/` - 获取文章详情用于编辑（需要认证）
- `GET /api/categories/` - 获取所有分类

### 标签相关
- `GET /api/tags/` - 获取所有标签
- `POST /api/tags/` - 创建新标签（需要认证）

### 评论相关
- `GET /api/comments/<post_id>/` - 获取文章评论
- `POST /api/pubcomments/<post_id>/` - 发表评论（需要认证）

### 互动功能
- `POST /api/likes/<post_id>/` - 点赞文章（需要认证）
- `DELETE /api/likes/<post_id>/` - 取消点赞（需要认证）
- `POST /api/dislikes/<post_id>/` - 踩文章（需要认证）
- `DELETE /api/dislikes/<post_id>/` - 取消踩（需要认证）

### 用户相关
- `GET /api/profile/` - 获取当前用户资料（需要认证）
- `PUT /api/profile/` - 更新当前用户资料（需要认证）

### 其他
- `GET /api/` - API概览
- `GET /api/example/` - 示例API端点

## 数据模型

### 用户相关
- `User` - Django内置用户模型
- `UserProfile` - 用户扩展资料，包含个人简介、生日和头像

### 文章相关
- `Article` - 文章模型，包含标题、内容、作者、分类、标签、发布时间、更新时间、浏览量、点赞数和踩数
- `Category` - 文章分类模型
- `Tag` - 文章标签模型

### 互动相关
- `Like` - 点赞记录模型
- `Dislike` - 踩记录模型
- `Comment` - 评论模型，包含文章、作者、内容和发布时间

### 验证相关
- `Captcha` - 邮箱验证码模型，包含邮箱、验证码和创建时间

## 开发约定

### 后端设置配置
- 开发环境：`DEBUG = True`
- 数据库：MySQL (`blog`)
- API框架：Django REST framework
- CORS配置：允许 `http://localhost:8080` 和 `http://127.0.0.1:8080`
- 认证方式：自定义Token认证（SimpleTokenAuthentication）
- 自定义认证后端：支持邮箱和用户名登录
- 中间件：暂时禁用CSRF，便于API开发
- 媒体文件：支持用户头像上传，存储在 `media/` 目录
- 邮件服务：使用QQ邮箱SMTP服务发送验证码

### 前端开发约定
- 构建工具：Vite 5.0.0
- 端口：8080
- API代理：`/api` 请求代理到 `http://localhost:8000`
- HTTP客户端：Axios 1.6.0
- 状态管理：Pinia 2.1.0
- 路由：Vue Router 4.2.0
- 代码规范：ESLint 8.45.0
- 认证状态：支持"记住我"功能，Token可存储在localStorage或sessionStorage
- 路由守卫：实现权限控制，需要登录的页面会自动跳转到登录页
- 分页设置：文章列表默认每页显示12条
- 请求拦截器：自动添加Token到请求头
- 响应拦截器：统一处理错误状态码

### 安全注意事项
- 生产环境需要更改`SECRET_KEY`
- 生产环境需要设置`DEBUG = False`
- 需要配置`ALLOWED_HOSTS`
- 生产环境需要限制CORS源
- 生产环境需要启用CSRF保护
- 验证码10分钟内有效，防止滥用

### 国际化
- 语言代码：`zh-hans`（简体中文）
- 时区：`Asia/shanghai`
- 未启用时区支持（USE_TZ = False）

## 项目状态

当前项目是一个功能完整的前后端分离博客系统，包含：

### 后端功能
- Django REST framework API
- 用户认证系统（注册、登录、资料管理）
- 邮箱验证码功能
- 文章CRUD功能
- 文章分类系统
- 文章标签系统
- 评论系统
- 点赞/踩互动功能
- 文章浏览量统计
- 自定义认证后端（支持邮箱/用户名登录）
- CORS支持
- MySQL数据库集成
- 简化的Token认证系统
- 分页支持
- 获取用户文章功能
- 测试数据创建命令
- 用户头像上传功能
- 文章更新时间记录
- 标签管理命令

### 前端功能
- Vue.js 3.4.0 + Composition API
- 完整的路由系统（首页、文章列表、文章详情、登录、注册、个人中心、文章编辑）
- 用户认证状态管理（Pinia）
- API服务封装
- 响应式设计
- 路由守卫（权限控制）
- "记住我"登录功能
- 文章发布和编辑界面
- 请求/响应拦截器
- 错误处理和状态反馈
- 文章搜索功能
- 分页导航
- 评论展示
- 点赞/踩交互
- 个人中心页面（个人信息、修改密码、我的文章管理）
- 用户头像上传和显示
- 邮箱验证码功能
- 文章标签选择和管理

### 已实现的新功能
1. 文章标签系统 - 完整的标签模型和管理功能，支持多标签关联
2. 邮箱验证码系统 - 使用QQ邮箱SMTP服务发送验证码，支持注册验证
3. 文章编辑功能 - 完整的文章编辑界面，支持标题、内容、分类和标签修改
4. 用户头像系统 - 支持用户头像上传和显示，包含默认头像
5. 文章更新时间记录 - 自动记录文章最后更新时间
6. 媒体文件管理 - 建立了完整的媒体文件存储结构
7. 自定义Token认证 - 实现了SimpleTokenAuthentication类
8. 请求/响应拦截器 - 统一处理API请求和错误
9. 标签管理命令 - 创建初始标签数据的管理命令
10. 验证码模型 - 完整的验证码存储和验证机制
11. 文章摘要移除 - 移除了文章摘要字段，简化了文章结构

### 下一步开发建议
1. 实现用户权限管理（管理员/普通用户）
2. 添加文章收藏功能
3. 添加网站统计和分析
4. 部署配置（Docker、Nginx等）
5. 添加单元测试和集成测试
6. 实现JWT认证替代简化Token
7. 添加富文本编辑器
8. 实现文章草稿功能
9. 添加图片上传功能（到文章内容中）
10. 实现用户关注系统
11. 添加文章搜索优化
12. 实现评论回复功能
13. 添加消息通知系统
14. 实现文章导出功能
15. 添加文章阅读进度记录