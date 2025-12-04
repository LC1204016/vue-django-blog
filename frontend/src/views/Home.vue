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

    <section class="recent-posts">
      <h2>最新文章</h2>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="recentPosts.length === 0" class="empty">
        <p>暂无文章，<router-link to="/posts">去看看其他内容</router-link></p>
      </div>
      <div v-else class="articles-list">
        <div 
          v-for="post in recentPosts" 
          :key="post.id" 
          class="article-item"
        >
          <div class="article-avatar">
            <img v-if="post.profile_pic" :src="post.profile_pic.startsWith('http') ? post.profile_pic : `http://localhost:8000${post.profile_pic}`" :alt="post.author" />
            <span v-else class="avatar-placeholder">{{ post.author.charAt(0).toUpperCase() }}</span>
          </div>
          <div class="article-content">
            <router-link :to="`/posts/${post.id}`" class="article-title">
              {{ post.title }}
            </router-link>
            <p class="article-summary">{{ post.content.substring(0, 120) }}{{ post.content.length > 120 ? '...' : '' }}</p>
            <div class="article-meta">
              <span class="author-name">{{ post.author }}</span>
              <span class="publish-time">{{ formatDateTime(post.pub_time) }}</span>
              <span v-if="post.updated_time && post.updated_time !== post.pub_time" class="update-time">
                更新于 {{ formatDateTime(post.updated_time) }}
              </span>
            </div>
            <div class="article-tags">
              <span class="category-tag">{{ post.category }}</span>
              <span 
                v-for="tag in post.tags.slice(0, 3)" 
                :key="tag" 
                class="tag-item"
              >
                #{{ tag }}
              </span>
            </div>
            <div class="article-interaction">
            <div class="interaction-item">
              <span class="icon">💬</span>
              <span class="count">{{ post.comments_count || 0 }}</span>
            </div>
            <div class="interaction-item">
              <span class="icon">👍</span>
              <span class="count">{{ post.like_count }}</span>
            </div>
            <div class="interaction-item">
              <span class="icon">👎</span>
              <span class="count">{{ post.dislike_count }}</span>
            </div>
            <div class="interaction-item">
              <span class="icon">👁️</span>
              <span class="count">{{ post.views }}</span>
            </div>
          </div>
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
        const response = await apiService.getPosts()
        recentPosts.value = response.results.slice(0, 8) // 显示最新8篇文章
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

    const formatDateTime = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diff = now - date
      
      // 如果是今天
      if (diff < 24 * 60 * 60 * 1000 && date.getDate() === now.getDate()) {
        return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      }
      
      // 如果是昨天
      const yesterday = new Date(now)
      yesterday.setDate(yesterday.getDate() - 1)
      if (date.getDate() === yesterday.getDate() && date.getMonth() === yesterday.getMonth() && date.getFullYear() === yesterday.getFullYear()) {
        return '昨天 ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      }
      
      // 其他情况显示日期
      return date.toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' }) + ' ' + 
             date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    }

    const isLoggedIn = computed(() => authStore.isLoggedIn)

    onMounted(() => {
      fetchRecentPosts()
    })

    return {
      recentPosts,
      loading,
      formatDate,
      formatDateTime,
      isLoggedIn
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 10px;
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

.recent-posts h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
  font-size: 24px;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
}

.loading, .empty {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.articles-list {
  margin-bottom: 2rem;
}

.article-item {
  padding: 16px 0;
  border-bottom: 1px solid #eee;
  display: flex;
  gap: 12px;
}

.article-item:last-child {
  border-bottom: none;
}

.article-avatar {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  overflow: hidden;
  flex-shrink: 0;
}

.article-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 16px;
}

.article-content {
  flex: 1;
  min-width: 0;
}

.article-title {
  font-size: 16px;
  font-weight: bold;
  color: #0066CC;
  text-decoration: none;
  display: block;
  margin-bottom: 8px;
  line-height: 1.4;
}

.article-title:hover {
  color: #0055AA;
  text-decoration: underline;
}

.article-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin: 0 0 8px 0;
}

.article-meta {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.author-name {
  font-size: 13px;
  color: #333;
  font-weight: 500;
}

.publish-time, .update-time {
  font-size: 13px;
  color: #999;
}

.update-time {
  color: #0066CC;
}

.article-tags {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.category-tag {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.tag-item {
  background-color: #f5f5f5;
  color: #666;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.article-interaction {
  display: flex;
  gap: 16px;
  align-items: center;
}

.interaction-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.interaction-item .icon {
  font-size: 14px;
  color: #999;
}

.interaction-item .count {
  font-size: 13px;
  color: #333;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .article-item {
    padding: 12px 0;
  }
  
  .article-title {
    font-size: 15px;
  }
  
  .article-summary {
    font-size: 13px;
  }
  
  .article-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .article-interaction {
    gap: 12px;
  }
}

@media (max-width: 1200px) {
  .home {
    max-width: 100%;
    padding: 0 15px;
  }
}
</style>