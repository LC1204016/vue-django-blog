<template>
  <div class="login">
    <div class="login-container">
      <div class="login-form">
        <h1>登录</h1>
        <p class="login-subtitle">欢迎回来！请登录您的账户</p>
        
        <form @submit.prevent="handleLogin">
          <div class="form-group">
              <label for="email">邮箱</label>
              <input 
                id="email"
                v-model="form.email" 
                type="email" 
                placeholder="请输入邮箱"
                required
              />
            </div>
          
          <div class="form-group">
            <label for="password">密码</label>
            <input 
              id="password"
              v-model="form.password" 
              type="password" 
              placeholder="请输入密码"
              required
            />
          </div>
          
          <div class="form-options">
            <label class="checkbox-label">
              <input v-model="form.remember" type="checkbox" />
              记住我
            </label>
            <router-link to="/forgot-password" class="forgot-password">忘记密码？</router-link>
          </div>
          
          <button 
            type="submit" 
            class="btn btn-primary" 
            :disabled="loading"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </form>
        
        <div class="login-footer">
          <p>还没有账户？ <router-link to="/register">立即注册</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    
    const form = ref({
      email: '',
      password: '',
      remember: false
    })
    
    const loading = ref(false)
    const error = ref('')

    const handleLogin = async () => {
      try {
        loading.value = true
        error.value = ''
        
        await authStore.login({
          email: form.value.email,
          password: form.value.password,
          remember: form.value.remember
        })
        
        // 登录成功后跳转
        const redirect = route.query.redirect || '/'
        router.push(redirect)
        
      } catch (err) {
        error.value = err.message || '登录失败，请检查用户名和密码'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      error,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-form {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.login-form h1 {
  text-align: center;
  margin: 0 0 0.5rem;
  color: #2c3e50;
  font-size: 2rem;
}

.login-subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
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

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #42b983;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  color: #666;
  font-size: 14px;
}

.checkbox-label input {
  margin-right: 0.5rem;
}

.forgot-password {
  color: #42b983;
  text-decoration: none;
  font-size: 14px;
}

.forgot-password:hover {
  text-decoration: underline;
}

.btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #42b983;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #369870;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #f8d7da;
  color: #721c24;
  border-radius: 4px;
  font-size: 14px;
}

.login-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.login-footer a {
  color: #42b983;
  text-decoration: none;
  font-weight: 500;
}

.login-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-container {
    max-width: 100%;
  }
  
  .login-form {
    padding: 2rem 1.5rem;
  }
}
</style>