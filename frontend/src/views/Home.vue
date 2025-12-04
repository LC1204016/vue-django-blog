<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <h1>欢迎来到Vue博客</h1>
        <p>一个基于Vue.js和Django的现代化博客系统</p>
        <div class="hero-buttons">
          <router-link to="/posts" class="btn btn-primary">浏览文章</router-link>
          <router-link v-if="isLoggedIn" to="/posts/create" class="btn btn-secondary">发布文章</router-link>
          <router-link v-else to="/register" class="btn btn-secondary">立即注册</router-link>
        </div>
      </div>
    </section>

    <section class="features">
      <h2>功能特点</h2>
      <div class="feature-grid">
        <div class="feature-card">
          <h3>📝 文章管理</h3>
          <p>支持创建、编辑、删除文章，支持Markdown格式</p>
        </div>
        <div class="feature-card">
          <h3>👤 用户系统</h3>
          <p>完整的用户注册、登录、权限管理功能</p>
        </div>
        <div class="feature-card">
          <h3>💬 评论互动</h3>
          <p>支持文章评论和回复，构建活跃社区</p>
        </div>
        <div class="feature-card">
          <h3>📱 响应式设计</h3>
          <p>完美适配各种设备，提供优秀的用户体验</p>
        </div>
      </div>
    </section>

    <section class="recent-posts">
      <h2>最新文章</h2>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="recentPosts.length === 0" class="empty">
        <p>暂无文章，<router-link to="/posts">去看看其他内容</router-link></p>
      </div>
      <div v-else class="post-list">
        <div v-for="post in recentPosts" :key="post.id" class="post-card">
          <h3>{{ post.title }}</h3>
          <p class="post-excerpt">{{ post.excerpt }}</p>
          <div class="post-meta">
            <span>{{ formatDate(post.created_at) }}</span>
            <router-link :to="`/posts/${post.id}`" class="read-more">阅读更多</router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { apiService } from '../services/api'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    const recentPosts = ref([])
    const loading = ref(true)

    const fetchRecentPosts = async () => {
      try {
        const posts = await apiService.getPosts()
        recentPosts.value = posts.slice(0, 3) // 只显示最新3篇
      } catch (error) {
        console.error('获取文章失败:', error)
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric' }
      return new Date(dateString).toLocaleDateString('zh-CN', options)
    }

    const isLoggedIn = computed(() => authStore.isLoggedIn)

    onMounted(() => {
      fetchRecentPosts()
    })

    return {
      recentPosts,
      loading,
      formatDate,
      isLoggedIn
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.hero {
  text-align: center;
  padding: 60px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  margin-bottom: 40px;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 12px 24px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #42b983;
  color: white;
}

.btn-primary:hover {
  background-color: #369870;
}

.btn-secondary {
  background-color: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background-color: white;
  color: #667eea;
}

.features {
  margin-bottom: 40px;
}

.features h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  padding: 2rem;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.recent-posts h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.loading, .empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.post-list {
  display: grid;
  gap: 1.5rem;
}

.post-card {
  padding: 1.5rem;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  transition: box-shadow 0.3s ease;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.post-card h3 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.post-excerpt {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #888;
  font-size: 0.9rem;
}

.read-more {
  color: #42b983;
  text-decoration: none;
  font-weight: 500;
}

.read-more:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>