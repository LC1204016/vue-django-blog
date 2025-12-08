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
                <img 
                  v-if="profileForm.profile_pic && profileForm.profile_pic !== ''" 
                  :src="profileForm.profile_pic.startsWith('http') ? profileForm.profile_pic : `http://localhost:8000${profileForm.profile_pic}`" 
                  :alt="profileForm.username" 
                  class="profile-avatar" 
                />
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
          <p class="password-info">
            修改密码需要通过邮箱验证码验证身份。请输入您的邮箱地址并获取验证码。
          </p>
          
          <!-- 邮箱和验证码输入界面 -->
          <form @submit.prevent="resetPassword" class="profile-form">
            <div class="form-group">
              <label for="email">邮箱地址</label>
              <input 
                id="email"
                v-model="captchaForm.email" 
                type="email" 
                placeholder="请输入您的邮箱地址"
                required
              />
              <small>请输入您注册时使用的邮箱地址</small>
            </div>
            
            <div class="form-group">
              <label for="captcha">验证码</label>
              <div class="captcha-input-group">
                <input 
                  id="captcha"
                  v-model="captchaForm.captcha" 
                  type="text" 
                  placeholder="请输入6位验证码"
                  maxlength="6"
                  required
                />
                <button 
                  type="button"
                  @click="sendCaptcha"
                  :disabled="countdown > 0 || captchaLoading || !captchaForm.email"
                  class="btn btn-secondary"
                >
                  {{ captchaLoading ? '发送中...' : (countdown > 0 ? `${countdown}秒后重试` : '获取验证码') }}
                </button>
              </div>
              <small v-if="!captchaForm.email" class="text-muted">请先输入邮箱地址</small>
              <small v-else-if="countdown > 0" class="text-info">{{ countdown }}秒后可重新发送</small>
            </div>
            
            <div class="form-group">
              <label for="newPassword">新密码</label>
              <input 
                id="newPassword"
                v-model="passwordForm.newPassword" 
                type="password" 
                placeholder="请输入新密码（6-20位）"
                required
                minlength="6"
                maxlength="20"
              />
              <small>密码长度6-20个字符</small>
            </div>
            
            <div class="form-group">
              <label for="confirmPassword">确认新密码</label>
              <input 
                id="confirmPassword"
                v-model="passwordForm.confirmPassword" 
                type="password" 
                placeholder="请再次输入新密码"
                required
                minlength="6"
                maxlength="20"
              />
              <small v-if="passwordError" class="error-text">{{ passwordError }}</small>
            </div>
            
            <div v-if="successMessage" class="success-message">
              {{ successMessage }}
            </div>
            
            <div v-if="errorMessage" class="error-message">
              {{ errorMessage }}
            </div>
            
            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="loading || !passwordFormValid || !captchaForm.captcha || !captchaSent"
            >
              {{ loading ? '重置中...' : '确认修改' }}
            </button>
            <small v-if="!captchaSent" class="text-muted">请先获取验证码</small>
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
    const successMessage = ref('')
    const error = ref('')
    const errorMessage = ref('')
    const myPosts = ref([])
    const isLoggedIn = computed(() => authStore.isAuthenticated)
    const pagination = ref({
      count: 0,
      page: 1,
      page_size: 12,
      total_pages: 0
    })

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
      const isValid = passwordForm.value.newPassword.length >= 6 &&
             passwordForm.value.newPassword.length <= 20 &&
             passwordForm.value.newPassword === passwordForm.value.confirmPassword
      
      console.log('passwordFormValid 重新计算:', {
        newPassword: passwordForm.value.newPassword,
        confirmPassword: passwordForm.value.confirmPassword,
        newPasswordLength: passwordForm.value.newPassword.length,
        passwordsMatch: passwordForm.value.newPassword === passwordForm.value.confirmPassword,
        isValid: isValid
      })
      
      return isValid
    })

    const fetchProfile = async () => {
      try {
        const response = await apiService.getUserProfile(null)
        if (response.profile) {
          profileForm.value = {
            username: response.profile.username || '',
            introduction: response.profile.introduction || '',
            birthday: response.profile.birthday || '',
            profile_pic: response.profile.profile_pic || '',
            created_at: response.profile.created_at || ''
          }
        }
      } catch (error) {
        console.error('获取用户资料失败:', error)
        errorMessage.value = '获取用户资料失败'
      }
    }

    const fetchMyPosts = async () => {
      try {
        postsLoading.value = true
        console.log('获取我的文章，页码:', pagination.value.page)
        const response = await apiService.getUserProfile(null, {
          page: pagination.value.page,
          page_size: pagination.value.page_size
        })
        console.log('我的文章API响应:', response)
        myPosts.value = response.results || []
        pagination.value = {
          count: response.count || 0,
          page: response.page || 1,
          page_size: response.page_size || 12,
          total_pages: response.total_pages || 1
        }
      } catch (error) {
        console.error('获取我的文章失败:', error)
        error.value = '获取我的文章失败'
      } finally {
        postsLoading.value = false
      }
    }

    const changePage = (page) => {
      pagination.value.page = page
      fetchMyPosts()
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
        successMessage.value = '个人信息更新成功'
        
        // 重新获取用户信息以更新显示
        await fetchProfile()
        
        setTimeout(() => {
          success.value = ''
          successMessage.value = ''
        }, 3000)
      } catch (err) {
        console.error('更新个人信息失败:', err)
        error.value = err.response?.data?.detail || err.message || '更新失败，请重试'
      } finally {
        loading.value = false
      }
    }

    // 添加验证码相关的响应式变量
    const captchaForm = ref({
      email: '',
      captcha: ''
    })
    const captchaSent = ref(false)
    const countdown = ref(0)
    const captchaLoading = ref(false)
    
    const sendCaptcha = async () => {
      if (!captchaForm.value.email) {
        errorMessage.value = '请先输入邮箱地址'
        return
      }
      
      // 验证邮箱格式
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(captchaForm.value.email)) {
        errorMessage.value = '请输入有效的邮箱地址'
        return
      }
      
      try {
        captchaLoading.value = true
        errorMessage.value = ''
        
        await apiService.sendCaptcha({ email: captchaForm.value.email })
        
        captchaSent.value = true
        countdown.value = 60
        const timer = setInterval(() => {
          countdown.value--
          if (countdown.value <= 0) {
            clearInterval(timer)
          }
        }, 1000)
        
        success.value = '验证码已发送到您的邮箱'
        successMessage.value = '验证码已发送到您的邮箱'
        setTimeout(() => {
          success.value = ''
          successMessage.value = ''
        }, 3000)
      } catch (err) {
        console.error('发送验证码失败:', err)
        errorMessage.value = err.response?.data?.errors?.email || '发送验证码失败，请重试'
      } finally {
        captchaLoading.value = false
      }
    }
    
    const resetPassword = async () => {
      if (!captchaForm.value.captcha || captchaForm.value.captcha.length !== 6) {
        errorMessage.value = '请输入6位验证码'
        return
      }
      
      if (!passwordFormValid.value) {
        errorMessage.value = '请正确填写密码信息'
        return
      }
      
      try {
        loading.value = true
        errorMessage.value = ''
        success.value = ''
        
        await apiService.resetPassword({
          email: captchaForm.value.email,
          captcha: captchaForm.value.captcha,
          password: passwordForm.value.newPassword,
          password_confirm: passwordForm.value.confirmPassword
        })
        
        success.value = '密码修改成功'
        successMessage.value = '密码修改成功'
        passwordForm.value = {
          newPassword: '',
          confirmPassword: ''
        }
        captchaForm.value = {
          email: captchaForm.value.email,
          captcha: ''
        }
        captchaSent.value = false
        
        setTimeout(() => {
          success.value = ''
          successMessage.value = ''
        }, 3000)
      } catch (err) {
        console.error('密码修改失败:', err)
        if (err.response?.data?.errors) {
          const serverErrors = err.response.data.errors
          if (typeof serverErrors === 'string') {
            errorMessage.value = serverErrors
          } else {
            errorMessage.value = Object.values(serverErrors)[0][0] || '密码修改失败，请重试'
          }
        } else {
          errorMessage.value = err.message || '密码修改失败，请重试'
        }
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
          successMessage.value = '文章删除成功'
          
          setTimeout(() => {
            success.value = ''
            successMessage.value = ''
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

    
    
    const setActiveTab = (tabKey) => {
      activeTab.value = tabKey
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
      fetchProfile()
      fetchMyPosts()
    })
    
    // 监听tab切换，重置密码修改相关状态
    watch(activeTab, (newTab, oldTab) => {
      if (oldTab === 'password' && newTab !== 'password') {
        // 从密码修改标签切换出去时，重置状态
        captchaForm.value = {
          email: '',
          captcha: ''
        }
        captchaSent.value = false
        countdown.value = 0
        errorMessage.value = ''
        success.value = ''
        successMessage.value = ''
      }
    })

    // 监听tab切换 - 不再需要单独获取文章，因为fetchProfile已经获取了
    watch(activeTab, (newValue) => {
      // 文章数据已经在fetchProfile中获取，不需要额外请求
    })

    return {
      tabs,
      activeTab,
      profileForm,
      passwordForm,
      passwordError,
      passwordFormValid,
      loading,
      postsLoading,
      myPosts,
      pagination,
      avatarFile,
      error,
      success,
      successMessage,
      errorMessage,
      isLoggedIn,
      captchaForm,
      captchaSent,
      countdown,
      captchaLoading,
      updateProfile,
      sendCaptcha,
      resetPassword,
      deletePost,
      handleLogout,
      handleAvatarChange,
      formatDate,
      setActiveTab,
      changePage
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

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e1e8ed;
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

.password-info {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  color: #6c757d;
  font-size: 14px;
  line-height: 1.5;
}

.captcha-section {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1rem;
}

.captcha-input-group {
  display: flex;
  gap: 0.5rem;
}

.captcha-input-group input {
  flex: 1;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #5a6268;
}

.btn-secondary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.text-muted {
  color: #6c757d;
  font-size: 12px;
  margin-top: 0.25rem;
}

.text-info {
  color: #17a2b8;
  font-size: 12px;
  margin-top: 0.25rem;
}

.error-text {
  color: #dc3545;
  font-size: 12px;
  margin-top: 0.25rem;
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