<template>
  <div class="posts">
    <div class="posts-header">
      <h1>文章列表</h1>
      <div class="posts-actions">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="搜索文章..." 
          class="search-input"
        />
        <router-link v-if="isLoggedIn" to="/posts/create" class="btn btn-primary">
          写文章
        </router-link>
      </div>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="filteredPosts.length === 0" class="empty">
      <p>{{ searchQuery ? '没有找到匹配的文章' : '暂无文章' }}</p>
      <router-link v-if="isLoggedIn" to="/posts/create" class="btn btn-primary">
        写第一篇文章
      </router-link>
    </div>
    <div v-else class="articles-list">
      <div 
        v-for="post in filteredPosts" 
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

    <div v-if="totalPages > 1" class="pagination">
      <button 
        @click="currentPage > 1 && currentPage--" 
        :disabled="currentPage === 1"
        class="btn btn-secondary"
      >
        上一页
      </button>
      <span class="page-info">
        第 {{ currentPage }} 页，共 {{ totalPages }} 页
      </span>
      <button 
        @click="currentPage < totalPages && currentPage++" 
        :disabled="currentPage === totalPages"
        class="btn btn-secondary"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { apiService } from '../services/api'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Posts',
  setup() {
    const posts = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const currentPage = ref(1)
    const totalPages = ref(1)
    const authStore = useAuthStore()

    const isLoggedIn = computed(() => authStore.isAuthenticated)

    const filteredPosts = computed(() => {
      if (!searchQuery.value) return posts.value
      return posts.value.filter(post => 
        post.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        post.excerpt.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        post.tags.some(tag => tag.toLowerCase().includes(searchQuery.value.toLowerCase()))
      )
    })

    const fetchPosts = async () => {
      try {
        loading.value = true
        const response = await apiService.getPosts({
          page: currentPage.value,
          page_size: 16  // 修改为每页显示16个文章
        })
        posts.value = response.results || []
        totalPages.value = response.total_pages || 1
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

    // 后端已经截断内容，无需前端再次截断

    // 监听搜索和页码变化
    watch([searchQuery, currentPage], () => {
      fetchPosts()
    })

    onMounted(() => {
      fetchPosts()
    })

    return {
      posts,
      loading,
      searchQuery,
      currentPage,
      totalPages,
      isLoggedIn,
      filteredPosts,
      formatDate,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.posts {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.posts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
}

.posts-header h1 {
  color: #333;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.posts-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  width: 200px;
}

.search-input:focus {
  outline: none;
  border-color: #0066CC;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background-color: #0066CC;
  color: white;
}

.btn-primary:hover {
  background-color: #0055AA;
}

.btn-secondary {
  background-color: #f8f9fa;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.btn-secondary:hover {
  background-color: #e9ecef;
}

.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.page-info {
  color: #666;
  font-size: 14px;
}

@media (max-width: 768px) {
  .posts {
    padding: 0 15px;
  }
  
  .posts-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .posts-actions {
    justify-content: space-between;
  }
  
  .search-input {
    flex: 1;
    max-width: 200px;
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
  .posts {
    max-width: 100%;
    padding: 0 15px;
  }
}
</style>