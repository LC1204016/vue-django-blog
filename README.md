# Vue + Django 前后端分离博客系统

[![Django](https://img.shields.io/badge/Django-5.2.8-brightgreen.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.4.0-brightgreen.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

一个基于Vue.js 3和Django 5.2.8的现代化前后端分离博客系统，采用RESTful API设计，支持用户认证、文章发布、评论互动等功能。

## 👥 团队

- **后端开发**: 项目所有者
- **前端开发**: AI助手
- **文档撰写**: AI助手
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

## 🧪 测试

### 后端测试
```bash
# 运行所有测试
python manage.py test

# 运行特定测试
python manage.py test backend.test_framework
```

### 前端测试
```bash
cd frontend

# 运行单元测试
npm run test

# 运行测试并生成覆盖率报告
npm run test:coverage
```

### 性能测试
```bash
# 运行压力测试
python test/stress_test.py

# 运行负载测试
python test/load_test.py
```

## 📚 开发指南

### 代码贡献规范

#### 🤖 AI完成部分
- **前端开发**: 所有Vue.js组件、页面、样式和交互逻辑
- **文档撰写**: 项目文档、API文档、README、部署指南
- **测试编写**: 前端单元测试、集成测试
- **UI/UX设计**: 界面设计、用户体验优化

#### 👨‍💻 开发者完成部分
- **后端开发**: Django模型、视图、序列化器、URL路由
- **数据库设计**: 数据模型设计、数据库优化
- **业务逻辑**: 核心业务逻辑实现
- **API设计**: RESTful API设计和实现

#### 🤝 AI辅助部分
- **代码审查**: 代码质量检查、最佳实践建议
- **性能优化**: 查询优化、缓存策略建议
- **安全加固**: 安全漏洞检查、修复建议
- **部署支持**: 部署脚本、CI/CD配置

### 开发流程
1. 创建功能分支
2. 后端开发者实现API接口
3. AI开发前端界面和交互
4. AI编写测试用例
5. 代码审查和优化
6. 合并到主分支


## 📊 项目状态

- ✅ 用户认证系统
- ✅ 文章管理功能
- ✅ 评论系统
- ✅ 搜索功能
- ✅ 响应式设计
- ✅ 测试框架
- 🔄 富文本编辑器（开发中）
- 🔄 实时通知（计划中）
- 🔄 文件上传（计划中）

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。


## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和AI助手！

---

⭐ 如果这个项目对你有帮助，请给它一个星标！