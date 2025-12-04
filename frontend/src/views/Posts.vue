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
    <div v-else class="posts-grid">
      <router-link 
        v-for="post in filteredPosts" 
        :key="post.id" 
        :to="`/posts/${post.id}`" 
        class="post-card-link"
      >
        <article class="post-card">
        <div class="post-header">
          <h2>{{ post.title }}</h2>
          <div class="post-meta">
            <div class="author-info">
              <div class="author-avatar">
                <img v-if="post.profile_pic" :src="post.profile_pic.startsWith('http') ? post.profile_pic : `http://localhost:8000${post.profile_pic}`" :alt="post.author" />
                <span v-else>{{ post.author.charAt(0).toUpperCase() }}</span>
              </div>
              <span class="author">作者: {{ post.author }}</span>
            </div>
            <div class="post-meta-info">
              <div class="post-category">
                <span class="category-text">{{ post.category }}</span>
              </div>
              <div class="post-dates-inline">
                <div class="post-date">
                  <span class="date-text">发布: {{ formatDate(post.pub_time) }}</span>
                </div>
                <div v-if="post.updated_time && post.updated_time !== post.pub_time" class="post-updated">
                  <span class="update-text">更新: {{ formatDate(post.updated_time) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="post-content">
          <p class="post-excerpt">{{ post.content.substring(0, 150) }}{{ post.content.length > 150 ? '...' : '' }}</p>
        </div>
        
        <!-- 标签显示 -->
        <div v-if="post.tags && post.tags.length > 0" class="post-tags">
          <span 
            v-for="tag in post.tags" 
            :key="tag" 
            class="tag"
          >
            {{ tag }}
          </span>
        </div>
        
        <div class="post-footer">
          <div class="post-stats">
            <span>👁️ {{ post.views }} 次浏览</span>
            <span>❤️ {{ post.like_count }} 次点赞</span>
            <span>👎 {{ post.dislike_count }} 次踩</span>
          </div>
        </div>
      </article>
      </router-link>
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
          page_size: 12  // 修改为每页显示12个文章
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
      formatDate
    }
  }
}
</script>

<style scoped>
.posts {
  max-width: 1200px;
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
}

.posts-header h1 {
  color: #2c3e50;
  margin: 0;
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
  border-color: #42b983;
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
  background-color: #42b983;
  color: white;
}

.btn-primary:hover {
  background-color: #369870;
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

.btn-text {
  color: #42b983;
  background: none;
  padding: 4px 8px;
}

.btn-text:hover {
  text-decoration: underline;
}

.loading, .empty {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.post-card {
  border: 1px solid #e1e8ed;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f8f9ff 0%, #f5f7fa 100%);
  cursor: pointer;
}

.post-header {
  padding: 1.5rem 1.5rem 0;
}

.post-header h2 {
  margin: 0 0 0.5rem;
  color: #2c3e50;
  font-size: 1.5rem;
}

.post-meta {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
  overflow: hidden;
}

.author-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-meta-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.post-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.post-card-link:hover .post-card {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
}

.post-category {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #5e72e4 0%, #825ee4 100%);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 600;
  box-shadow: 0 3px 6px rgba(94, 114, 228, 0.3);
  transition: all 0.3s ease;
}

.post-category:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(94, 114, 228, 0.4);
}

.post-dates-inline {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.post-date, .post-updated {
  display: inline-block;
  font-size: 0.75rem;
  color: #6c757d;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 0.3rem 0.6rem;
  border-radius: 10px;
  transition: all 0.2s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.post-updated {
  color: #007bff;
  background-color: rgba(0, 123, 255, 0.1);
  border: 1px solid rgba(0, 123, 255, 0.2);
  font-weight: 500;
}

.post-date:hover, .post-updated:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.08);
}

.category {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.post-content {
  padding: 0 1.5rem;
}

.post-excerpt {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.post-tags {
  padding: 0.75rem 1.5rem 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.post-tags .tag {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.post-tags .tag:hover {
  background-color: #bbdefb;
  transform: translateY(-1px);
}

.post-footer {
  padding: 1rem 1.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-stats {
  display: flex;
  gap: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.post-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  background-color: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-info {
  color: #666;
}

@media (max-width: 768px) {
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
  
  .posts-grid {
    grid-template-columns: 1fr;
  }
  
  .post-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .post-meta-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .post-dates-inline {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .post-dates {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style>