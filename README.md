# Vue + Django 前后端分离博客系统

[![Django](https://img.shields.io/badge/Django-5.2.8-brightgreen.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.4.0-brightgreen.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

一个基于Vue.js 3和Django 5.2.8的现代化前后端分离博客系统，采用RESTful API设计，支持用户认证、文章发布、评论互动等功能。

## 👥 团队

- **后端开发**: 项目所有者
- **前端开发**: AI助手
- **测试**: AI助手 + 后端开发者

## 🌟 项目特性

### 核心功能
- 🔐 完整的用户认证系统（注册、登录、密码重置）
- 📝 文章发布、编辑、删除功能
- 🏷️ 文章分类和标签系统
- 💬 评论互动功能
- 👍👎 点赞/踩互动功能
- 🔍 文章搜索功能
- 👤 用户资料管理
- 📧 邮箱验证码支持

### 技术特性
- 🚀 现代化技术栈（Vue 3 + Django 5.2.8）
- 🔄 RESTful API设计
- 📱 响应式设计，支持移动端
- 🎨 现代化UI界面
- ⚡ 高性能缓存（Redis）
- 🛡️ JWT认证系统

## 🛠️ 技术栈

### 后端技术
- **框架**: Django 5.2.8
- **API**: Django REST Framework 3.16.1
- **认证**: Django REST Framework SimpleJWT 5.5.1
- **数据库**: MySQL 8.0
- **缓存**: Redis

### 前端技术
- **框架**: Vue.js 3.4.0
- **构建工具**: Vite 5.0.0
- **路由**: Vue Router 4.2.0
- **状态管理**: Pinia 2.1.0
- **HTTP客户端**: Axios 1.6.0
- **UI组件**: 自定义组件 + CSS3

### 开发工具
- **代码质量**: ESLint, Prettier
- **测试**: Vitest, Django TestCase
- **版本控制**: Git

## 📁 项目结构

```
D:\dev\blog\
├───backend\              # Django后端应用
│   ├───models.py         # 数据模型
│   ├───views.py          # API视图
│   ├───serializers.py    # 序列化器
│   └───urls.py           # 路由配置
├───frontend\             # Vue.js前端应用
│   ├───src\
│   │   ├───components\   # 组件
│   │   ├───views\        # 页面
│   │   ├───stores\       # 状态管理
│   │   └───services\     # API服务
│   └───dist\             # 构建输出
├───blog\                 # Django项目配置
├───media\                # 媒体文件
├───static\               # 静态文件
├───test\                 # 测试文件
└───requirements.txt      # Python依赖
```

## 🚀 快速开始

### 环境要求
- Python 3.12+
- Node.js 16+
- MySQL 8.0+
- Redis 6.0+

### 后端设置

1. **克隆项目**
```bash
git clone https://github.com/LC1204016/vue-django-blog.git
cd vue-django-blog
```

2. **创建虚拟环境**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# 或
source .venv/bin/activate  # Linux/Mac
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
copy .env.example .env
# 编辑 .env 文件，配置数据库和其他设置
```

5. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **创建超级用户**
```bash
python manage.py createsuperuser
```

7. **启动后端服务**
```bash
python manage.py runserver
```

### 前端设置

1. **安装依赖**
```bash
cd frontend
npm install
```

2. **启动开发服务器**
```bash
npm run dev
```


## 📖 API文档

后端API文档可通过以下方式访问：
- 开发环境：http://localhost:8000/api/docs/
- 生产环境：https://your-domain.com/api/docs/

主要API端点：
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/register/` - 用户注册
- `GET /api/articles/` - 获取文章列表
- `POST /api/articles/` - 创建文章
- `GET /api/articles/<id>/` - 获取文章详情
- `POST /api/articles/<id>/comments/` - 发表评论

