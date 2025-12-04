<template>
  <div class="profile">
    <div class="profile-header">
      <h1>个人中心</h1>
      <p>管理您的个人信息和博客内容</p>
    </div>

    <div class="profile-content">
      <div class="profile-sidebar">
        <nav class="profile-nav">
          <button 
            v-for="tab in tabs" 
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="['nav-btn', { active: activeTab === tab.key }]"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>

      <div class="profile-main">
        <!-- 个人信息 -->
        <div v-if="activeTab === 'info'" class="tab-content">
          <h2>个人信息</h2>
          <form @submit.prevent="updateProfile" class="profile-form">
            <div class="profile-avatar-section">
              <div class="avatar-container">
                <img v-if="profileForm.profile_pic" :src="profileForm.profile_pic" :alt="profileForm.username" class="profile-avatar" />
                <div v-else class="profile-avatar-placeholder">
                  {{ profileForm.username?.charAt(0)?.toUpperCase() || 'U' }}
                </div>
                <input 
                  type="file" 
                  ref="avatarInput" 
                  @change="handleAvatarChange" 
                  accept="image/*" 
                  style="display: none"
                />
                <button 
                  type="button" 
                  @click="$refs.avatarInput.click()" 
                  class="avatar-upload-btn"
                >
                  更换头像
                </button>
              </div>
              <div class="avatar-info">
                <h3>{{ profileForm.username }}</h3>
                <p>更新您的个人资料和头像</p>
              </div>
            </div>
            <div class="form-group">
              <label for="username">用户名</label>
              <input 
                id="username"
                v-model="profileForm.username" 
                type="text" 
                disabled
              />
              <small>用户名无法修改</small>
            </div>
            
            <div class="form-group">
              <label for="introduction">个人简介</label>
              <textarea 
                id="introduction"
                v-model="profileForm.introduction" 
                rows="4"
                maxlength="30"
                placeholder="介绍一下自己（最多30个字符）..."
              ></textarea>
              <small>{{ profileForm.introduction.length }}/30</small>
            </div>
            
            <div class="form-group">
              <label for="birthday">生日</label>
              <input 
                id="birthday"
                v-model="profileForm.birthday" 
                type="date"
              />
            </div>
            
            <div class="form-group">
              <label for="created_at">注册时间</label>
              <input 
                id="created_at"
                :value="formatDate(profileForm.created_at)"
                type="text" 
                disabled
              />
              <small>注册时间无法修改</small>
            </div>
            
            
            
            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="loading"
            >
              {{ loading ? '保存中...' : '保存更改' }}
            </button>
          </form>
        </div>

        <!-- 修改密码 -->
        <div v-if="activeTab === 'password'" class="tab-content">
          <h2>修改密码</h2>
          <form @submit.prevent="changePassword" class="profile-form">
            <div class="form-group">
              <label for="currentPassword">当前密码</label>
              <input 
                id="currentPassword"
                v-model="passwordForm.currentPassword" 
                type="password" 
                required
              />
            </div>
            
            <div class="form-group">
              <label for="newPassword">新密码</label>
              <input 
                id="newPassword"
                v-model="passwordForm.newPassword" 
                type="password" 
                required
                minlength="6"
              />
              <small>密码至少6个字符</small>
            </div>
            
            <div class="form-group">
              <label for="confirmPassword">确认新密码</label>
              <input 
                id="confirmPassword"
                v-model="passwordForm.confirmPassword" 
                type="password" 
                required
              />
              <small v-if="passwordError" class="form-error">{{ passwordError }}</small>
            </div>
            
            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="loading || !passwordFormValid"
            >
              {{ loading ? '修改中...' : '修改密码' }}
            </button>
          </form>
        </div>

        <!-- 我的文章 -->
        <div v-if="activeTab === 'posts'" class="tab-content">
          <div class="tab-header">
            <h2>我的文章</h2>
            <router-link to="/posts/create" class="btn btn-primary">
              写新文章
            </router-link>
          </div>
          
          <div v-if="postsLoading" class="loading">加载中...</div>
          <div v-else-if="myPosts.length === 0" class="empty">
            <p>您还没有发表任何文章</p>
            <router-link to="/posts/create" class="btn btn-primary">
              写第一篇文章
            </router-link>
          </div>
          <div v-else class="posts-list">
            <div v-for="post in myPosts" :key="post.id" class="post-item">
              <div class="post-info">
                <h3>{{ post.title }}</h3>
                <p class="post-meta">
                  发布于 {{ formatDate(post.pub_time) }} · 
                  {{ post.views }} 次浏览 · 
                  {{ post.like_count }} 次点赞 · 
                  {{ post.dislike_count }} 次踩
                </p>
              </div>
              <div class="post-actions">
                <router-link :to="`/posts/${post.id}`" class="btn btn-text">
                  查看
                </router-link>
                <router-link :to="`/posts/${post.id}/edit`" class="btn btn-text">
                  编辑
                </router-link>
                <button @click="deletePost(post)" class="btn btn-text btn-danger">
                  删除
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 退出登录 -->
        <div v-if="activeTab === 'logout'" class="tab-content">
          <h2>退出登录</h2>
          <div class="logout-content">
            <p>确定要退出登录吗？</p>
            <button @click="handleLogout" class="btn btn-danger">
              退出登录
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="success" class="success-message">
      {{ success }}
    </div>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '../services/api'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Profile',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const activeTab = ref('info')
    const loading = ref(false)
    const postsLoading = ref(false)
    const success = ref('')
    const error = ref('')
    const myPosts = ref([])

    const tabs = [
      { key: 'info', label: '个人信息' },
      { key: 'password', label: '修改密码' },
      { key: 'posts', label: '我的文章' },
      { key: 'logout', label: '退出登录' }
    ]

    const profileForm = ref({
      username: '',
      email: '',
      introduction: '',
      birthday: '',
      profile_pic: ''
    })

    const avatarFile = ref(null)

    const passwordForm = ref({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })

    const passwordError = computed(() => {
      if (passwordForm.value.confirmPassword && 
          passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
        return '两次输入的密码不一致'
      }
      return ''
    })

    const passwordFormValid = computed(() => {
      return passwordForm.value.currentPassword &&
             passwordForm.value.newPassword.length >= 6 &&
             passwordForm.value.newPassword === passwordForm.value.confirmPassword
    })

    const fetchProfile = async () => {
      try {
        const response = await apiService.getUserProfile()
        console.log('获取到的用户资料数据:', response)
        
        // 处理不同的数据结构
        let profile = response.profile || response
        
        profileForm.value = {
          username: profile.username || '',
          email: profile.email || '',
          introduction: profile.introduction || '',
          birthday: profile.birthday ? new Date(profile.birthday).toISOString().split('T')[0] : '',
          profile_pic: profile.profile_pic && profile.profile_pic !== 'default.png' ? `http://localhost:8000${profile.profile_pic}` : '',
          created_at: profile.created_at || ''
        }
        
        console.log('设置后的表单数据:', profileForm.value)
      } catch (err) {
        console.error('获取个人信息失败:', err)
        error.value = '获取个人信息失败，请重试'
      }
    }

    const fetchMyPosts = async () => {
      try {
        postsLoading.value = true
        const response = await apiService.getMyPosts()
        myPosts.value = response.results || []
      } catch (err) {
        console.error('获取我的文章失败:', err)
      } finally {
        postsLoading.value = false
      }
    }

    const handleAvatarChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        // 检查文件类型
        if (!file.type.startsWith('image/')) {
          error.value = '请选择图片文件'
          return
        }
        
        // 检查文件大小（限制为5MB）
        if (file.size > 5 * 1024 * 1024) {
          error.value = '图片大小不能超过5MB'
          return
        }
        
        avatarFile.value = file
        
        // 创建预览URL
        const reader = new FileReader()
        reader.onload = (e) => {
          profileForm.value.profile_pic = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }

    const updateProfile = async () => {
      try {
        loading.value = true
        error.value = ''
        success.value = ''
        
        // 创建FormData对象用于文件上传
        const formData = new FormData()
        
        // 添加文本字段
        if (profileForm.value.introduction !== undefined) {
          formData.append('introduction', profileForm.value.introduction)
        }
        if (profileForm.value.birthday) {
          formData.append('birthday', profileForm.value.birthday)
        }
        
        // 添加头像文件
        if (avatarFile.value) {
          formData.append('profile_pic', avatarFile.value)
        }
        
        await apiService.updateProfile(formData)
        success.value = '个人信息更新成功'
        
        // 重新获取用户信息以更新显示
        await fetchProfile()
        
        setTimeout(() => {
          success.value = ''
        }, 3000)
      } catch (err) {
        console.error('更新个人信息失败:', err)
        error.value = err.response?.data?.detail || err.message || '更新失败，请重试'
      } finally {
        loading.value = false
      }
    }

    const changePassword = async () => {
      if (!passwordFormValid.value) return
      
      try {
        loading.value = true
        error.value = ''
        success.value = ''
        
        await apiService.changePassword({
          current_password: passwordForm.value.currentPassword,
          new_password: passwordForm.value.newPassword
        })
        
        success.value = '密码修改成功'
        passwordForm.value = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
        
        setTimeout(() => {
          success.value = ''
        }, 3000)
      } catch (err) {
        error.value = err.message || '密码修改失败，请重试'
      } finally {
        loading.value = false
      }
    }

    const deletePost = async (post) => {
      if (confirm(`确定要删除文章"${post.title}"吗？此操作不可恢复。`)) {
        try {
          await apiService.deletePost(post.id)
          myPosts.value = myPosts.value.filter(p => p.id !== post.id)
          success.value = '文章删除成功'
          
          setTimeout(() => {
            success.value = ''
          }, 3000)
        } catch (err) {
          error.value = '删除文章失败，请重试'
        }
      }
    }

    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }

    
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric'
      }
      return new Date(dateString).toLocaleDateString('zh-CN', options)
    }

    onMounted(() => {
      console.log('Profile组件已挂载，开始获取用户资料')
      fetchProfile()
      if (activeTab.value === 'posts') {
        fetchMyPosts()
      }
    })

    // 监听tab切换
    watch(activeTab, (newValue) => {
      if (newValue === 'posts' && myPosts.value.length === 0) {
        fetchMyPosts()
      }
    })

    return {
      activeTab,
      tabs,
      profileForm,
      passwordForm,
      loading,
      postsLoading,
      success,
      error,
      myPosts,
      passwordError,
      passwordFormValid,
      updateProfile,
      handleAvatarChange,
      changePassword,
      deletePost,
      handleLogout,
      formatDate
    }
  }
}
</script>

<style scoped>
.profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.profile-header {
  text-align: center;
  margin-bottom: 2rem;
}

.profile-header h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.profile-header p {
  color: #666;
}

.profile-content {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
}

.profile-sidebar {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.profile-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-btn {
  background: none;
  border: none;
  padding: 0.75rem 1rem;
  text-align: left;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;
}

.nav-btn:hover {
  background-color: #f8f9fa;
}

.nav-btn.active {
  background-color: #42b983;
  color: white;
}

.profile-main {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.tab-content h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.profile-avatar-section {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.avatar-container {
  position: relative;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #42b983;
}

.profile-avatar-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #42b983;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  border: 3px solid #42b983;
}

.avatar-info h3 {
  margin: 0 0 0.5rem;
  color: #2c3e50;
  font-size: 1.5rem;
}

.avatar-info p {
  margin: 0;
  color: #666;
}

.avatar-upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
}

.avatar-upload-btn:hover {
  background-color: #369870;
}

.profile-form {
  max-width: 500px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #42b983;
}

.form-group input:disabled {
  background-color: #f8f9fa;
  color: #666;
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  color: #666;
  font-size: 12px;
}

.form-error {
  color: #dc3545;
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

.btn-primary:hover:not(:disabled) {
  background-color: #369870;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-text {
  background: none;
  padding: 4px 8px;
  color: #42b983;
}

.btn-text.btn-danger {
  color: #dc3545;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading, .empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-item {
  padding: 1.5rem;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-info h3 {
  margin: 0 0 0.5rem;
  color: #2c3e50;
}

.post-meta {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.post-actions {
  display: flex;
  gap: 0.5rem;
}

.logout-content {
  text-align: center;
  padding: 2rem;
}

.logout-content p {
  margin-bottom: 1.5rem;
  color: #666;
}

.success-message,
.error-message {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 1rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  z-index: 1000;
  max-width: 300px;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

@media (max-width: 768px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
  
  .profile-sidebar {
    order: 2;
  }
  
  .profile-nav {
    flex-direction: row;
    overflow-x: auto;
  }
  
  .profile-main {
    order: 1;
  }
  
  .post-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .post-actions {
    align-self: stretch;
    justify-content: flex-end;
  }
  
  .tab-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
}
</style>