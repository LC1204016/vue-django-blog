<template>
  <div class="register">
    <div class="register-container">
      <div class="register-form">
        <h1>注册</h1>
        <p class="register-subtitle">创建您的账户，开始博客之旅</p>
        
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="username">用户名</label>
            <input 
              id="username"
              v-model="form.username" 
              type="text" 
              placeholder="请输入用户名"
              required
              minlength="3"
            />
            <small class="form-help">用户名至少3个字符</small>
          </div>
          
          <div class="form-group">
            <label for="email">邮箱</label>
            <input 
              id="email"
              v-model="form.email" 
              type="email" 
              placeholder="请输入邮箱地址"
              required
              @blur="validateEmail"
            />
          </div>
          
          <div class="form-group">
            <label for="captcha">验证码</label>
            <div class="captcha-group">
              <input 
                id="captcha"
                v-model="form.captcha" 
                type="text" 
                placeholder="请输入6位验证码"
                maxlength="6"
                required
              />
              <button 
                type="button" 
                @click="sendCaptcha" 
                :disabled="!canSendCaptcha || captchaLoading"
                class="btn-captcha"
              >
                {{ captchaButtonText }}
              </button>
            </div>
            <small class="form-help">验证码10分钟内有效</small>
          </div>
          
          <div class="form-group">
            <label for="password">密码</label>
            <input 
              id="password"
              v-model="form.password" 
              type="password" 
              placeholder="请输入密码"
              required
              minlength="6"
            />
            <small class="form-help">密码至少6个字符</small>
          </div>
          
          <div class="form-group">
            <label for="confirmPassword">确认密码</label>
            <input 
              id="confirmPassword"
              v-model="form.confirmPassword" 
              type="password" 
              placeholder="请再次输入密码"
              required
            />
            <small v-if="passwordError" class="form-error">{{ passwordError }}</small>
          </div>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input v-model="form.agree" type="checkbox" required />
              我同意 <a href="#" class="terms-link">服务条款</a> 和 <a href="#" class="terms-link">隐私政策</a>
            </label>
          </div>
          
          <button 
            type="submit" 
            class="btn btn-primary" 
            :disabled="loading || !formValid"
          >
            {{ loading ? '注册中...' : '注册' }}
          </button>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </form>
        
        <div class="register-footer">
          <p>已有账户？ <router-link to="/login">立即登录</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = ref({
      username: '',
      email: '',
      captcha: '',
      password: '',
      confirmPassword: '',
      agree: false
    })
    
    const loading = ref(false)
    const error = ref('')
    const captchaLoading = ref(false)
    const countdown = ref(0)
    const emailValid = ref(false)

    const passwordError = computed(() => {
      if (form.value.confirmPassword && form.value.password !== form.value.confirmPassword) {
        return '两次输入的密码不一致'
      }
      return ''
    })

    const canSendCaptcha = computed(() => {
      return form.value.email && emailValid.value && countdown.value === 0
    })

    const captchaButtonText = computed(() => {
      if (countdown.value > 0) {
        return `${countdown.value}秒后重试`
      }
      return captchaLoading.value ? '发送中...' : '获取验证码'
    })

    const formValid = computed(() => {
      return form.value.username.length >= 3 &&
             form.value.email &&
             emailValid.value &&
             form.value.captcha.length === 6 &&
             form.value.password.length >= 6 &&
             form.value.password === form.value.confirmPassword &&
             form.value.agree
    })

    const validateEmail = () => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      emailValid.value = emailRegex.test(form.value.email)
    }

    const sendCaptcha = async () => {
      if (!canSendCaptcha.value) return
      
      try {
        captchaLoading.value = true
        error.value = ''
        
        // 调用API发送验证码
        const response = await fetch('/api/captcha/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: form.value.email
          })
        })
        
        const data = await response.json()
        
        if (response.ok) {
          // 开始倒计时
          countdown.value = 60
          const timer = setInterval(() => {
            countdown.value--
            if (countdown.value <= 0) {
              clearInterval(timer)
            }
          }, 1000)
          
          // 显示成功消息
          error.value = ''
          alert('验证码已发送到您的邮箱，请查收')
        } else {
          error.value = data.errors || '发送验证码失败'
        }
        
      } catch (err) {
        error.value = '网络错误，请稍后重试'
      } finally {
        captchaLoading.value = false
      }
    }

    const handleRegister = async () => {
      if (!formValid.value) return
      
      try {
        loading.value = true
        error.value = ''
        
        await authStore.register({
          username: form.value.username,
          email: form.value.email,
          password: form.value.password,
          password_confirm: form.value.confirmPassword,
          captcha: form.value.captcha
        })
        
        // 注册成功后跳转到登录页
        router.push({
          name: 'Login',
          query: { message: '注册成功，请登录' }
        })
        
      } catch (err) {
        error.value = err.message || '注册失败，请稍后重试'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      error,
      passwordError,
      captchaLoading,
      countdown,
      canSendCaptcha,
      captchaButtonText,
      formValid,
      validateEmail,
      sendCaptcha,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 400px;
}

.register-form {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.register-form h1 {
  text-align: center;
  margin: 0 0 0.5rem;
  color: #2c3e50;
  font-size: 2rem;
}

.register-subtitle {
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

.captcha-group {
  display: flex;
  gap: 0.5rem;
}

.captcha-group input {
  flex: 1;
}

.btn-captcha {
  padding: 12px 16px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 100px;
}

.btn-captcha:hover:not(:disabled) {
  background-color: #5a6268;
}

.btn-captcha:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-help {
  display: block;
  margin-top: 0.25rem;
  color: #666;
  font-size: 12px;
}

.form-error {
  display: block;
  margin-top: 0.25rem;
  color: #dc3545;
  font-size: 12px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

.checkbox-label input {
  margin-right: 0.5rem;
  margin-top: 2px;
  width: auto;
}

.terms-link {
  color: #42b983;
  text-decoration: none;
}

.terms-link:hover {
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

.register-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.register-footer a {
  color: #42b983;
  text-decoration: none;
  font-weight: 500;
}

.register-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .register-container {
    max-width: 100%;
  }
  
  .register-form {
    padding: 2rem 1.5rem;
  }
  
  .captcha-group {
    flex-direction: column;
  }
  
  .btn-captcha {
    width: 100%;
  }
}
</style>