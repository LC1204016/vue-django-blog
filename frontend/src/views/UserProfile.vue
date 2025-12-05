<template>
  <div class="user-profile">
    <div class="profile-header">
      <h1>用户资料</h1>
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
        <h3>用户文章</h3>
        <div v-if="postsLoading" class="loading">
          加载文章中...
        </div>
        <div v-else-if="posts.length === 0" class="no-posts">
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
            <p class="post-summary">{{ truncateContent(post.content) }}</p>
            <div class="post-meta">
              <span class="post-date">{{ formatDate(post.pub_time) }}</span>
              <span class="post-views">{{ post.views }} 浏览</span>
            </div>
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
    
    const user = ref({})
    const posts = ref([])
    const loading = ref(true)
    const postsLoading = ref(false)
    const error = ref('')
    
    const userId = route.params.id
    
    const fetchUserProfile = async () => {
      try {
        const response = await apiService.getUserProfileById(userId)
        user.value = response.user
        await fetchUserPosts()
      } catch (err) {
        error.value = '获取用户资料失败'
        console.error('获取用户资料错误:', err)
      } finally {
        loading.value = false
      }
    }
    
    const fetchUserPosts = async () => {
      postsLoading.value = true
      try {
        // 使用author_id参数获取指定用户的文章
        const response = await apiService.getPosts({ author_id: userId })
        posts.value = response.results || response
      } catch (err) {
        console.error('获取用户文章错误:', err)
      } finally {
        postsLoading.value = false
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    }
    
    const truncateContent = (content) => {
      if (!content) return ''
      return content.length > 100 ? content.substring(0, 100) + '...' : content
    }
    
    const goToPost = (postId) => {
      router.push(`/posts/${postId}`)
    }
    
    onMounted(() => {
      fetchUserProfile()
    })
    
    return {
      user,
      posts,
      loading,
      postsLoading,
      error,
      formatDate,
      truncateContent,
      goToPost
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

.user-posts h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.5rem;
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