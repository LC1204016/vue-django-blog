<template>
  <div class="user-profile">
    <div class="profile-header">
      <h1>{{ isOwnProfile ? '我的资料' : '用户资料' }}</h1>
    </div>

    <div v-if="loading" class="loading">
      加载中...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="profile-content">
      <div class="profile-card">
        <div class="avatar-section">
          <img 
            :src="(user.profile_pic && user.profile_pic.startsWith('http')) ? user.profile_pic : (user.profile_pic ? `http://localhost:8000${user.profile_pic}` : '/default.png')" 
            :alt="user.username"
            class="avatar"
          >
        </div>
        
        <div class="user-info">
          <h2 class="username">{{ user.username }}</h2>
          
          <div class="info-item">
            <span class="label">个人简介：</span>
            <span class="value">{{ user.introduction || '暂无简介' }}</span>
          </div>
          
          <div class="info-item" v-if="user.birthday">
            <span class="label">生日：</span>
            <span class="value">{{ formatDate(user.birthday) }}</span>
          </div>
          
          <div class="info-item" v-if="user.created_at">
            <span class="label">注册时间：</span>
            <span class="value">{{ formatDate(user.created_at) }}</span>
          </div>
        </div>
      </div>
      
      <div class="user-posts">
        <div class="posts-header">
          <h3>{{ isOwnProfile ? '我的文章' : '用户文章' }}</h3>
          <router-link v-if="isOwnProfile" to="/posts/create" class="btn btn-primary">
            写新文章
          </router-link>
        </div>
        <div v-if="posts.length === 0" class="no-posts">
          该用户暂无发布的文章
        </div>
        <div v-else class="posts-list">
          <div 
            v-for="post in posts" 
            :key="post.id"
            class="post-item"
            @click="goToPost(post.id)"
          >
            <h4 class="post-title">{{ post.title }}</h4>
            <div class="post-meta">
              <span class="post-date">{{ formatDate(post.pub_time) }}</span>
              <span class="post-views">{{ post.views }} 浏览</span>
              <span class="post-likes">{{ post.like_count }} 点赞</span>
            </div>
          </div>
          
          <!-- 分页组件 -->
          <div v-if="pagination.total_pages > 1" class="pagination">
            <button 
              @click="changePage(pagination.page - 1)"
              :disabled="pagination.page <= 1"
              class="pagination-btn"
            >
              上一页
            </button>
            
            <span class="pagination-info">
              第 {{ pagination.page }} 页，共 {{ pagination.total_pages }} 页
            </span>
            
            <button 
              @click="changePage(pagination.page + 1)"
              :disabled="pagination.page >= pagination.total_pages"
              class="pagination-btn"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiService } from '../services/api'

export default {
  name: 'UserProfile',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const user = ref(null)
    const posts = ref([])
    const loading = ref(true)
    const error = ref(null)
    const currentPage = ref(1)
    const totalPages = ref(1)
    const isOwnProfile = ref(false)
    const pagination = ref({
      count: 0,
      page: 1,
      page_size: 12,
      total_pages: 0
    })
    
    const userId = route.params.id
    
    const fetchUserProfile = async () => {
      try {
        loading.value = true
        console.log('获取用户资料，userId:', userId, '页码:', currentPage.value)
        const response = await apiService.getUserProfile(userId, {
          page: currentPage.value,
          page_size: 12
        })
        console.log('API响应:', response)
        user.value = response.profile
        posts.value = response.results || []
        totalPages.value = response.total_pages || 1
        pagination.value = {
          count: response.count || 0,
          page: response.page || currentPage.value,
          page_size: response.page_size || 12,
          total_pages: response.total_pages || 1
        }
        isOwnProfile.value = response.profile.is_owner || false
        console.log('用户资料设置完成:', user.value)
      } catch (error) {
        console.error('获取用户资料失败:', error)
        if (error.response?.status === 404) {
          error.value = '用户不存在'
        } else {
          error.value = '获取用户资料失败'
        }
      } finally {
        loading.value = false
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    }
    
    const goToPost = (postId) => {
      router.push(`/posts/${postId}`)
    }

    const changePage = (page) => {
      currentPage.value = page
      fetchUserProfile()
    }
    
    onMounted(() => {
      fetchUserProfile()
    })
    
    return {
      user,
      posts,
      loading,
      error,
      currentPage,
      totalPages,
      isOwnProfile,
      pagination,
      formatDate,
      goToPost,
      changePage
    }
  }
}
</script>

<style scoped>
.user-profile {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  text-align: center;
  margin-bottom: 30px;
}

.profile-header h1 {
  color: #333;
  font-size: 2rem;
  margin-bottom: 10px;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  font-size: 1.1rem;
}

.error {
  color: #e74c3c;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.profile-card {
  background: #fff;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.avatar-section {
  flex-shrink: 0;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f0f0f0;
}

.user-info {
  flex: 1;
}

.username {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
}

.info-item {
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start;
}

.label {
  font-weight: bold;
  color: #666;
  margin-right: 10px;
  min-width: 80px;
}

.value {
  color: #333;
  word-break: break-word;
}

.user-posts {
  background: #fff;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.posts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.user-posts h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.no-posts {
  text-align: center;
  color: #666;
  padding: 20px;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.post-item {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.post-item:hover {
  border-color: #3498db;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2);
}

.post-title {
  color: #333;
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.post-summary {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.5;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  color: #999;
  font-size: 0.9rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  color: #42b983;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #f8f9fa;
  border-color: #42b983;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  color: #999;
}

.pagination-info {
  color: #666;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .profile-card {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .info-item {
    flex-direction: column;
    align-items: center;
  }
  
  .label {
    margin-right: 0;
    margin-bottom: 5px;
  }
}
</style>