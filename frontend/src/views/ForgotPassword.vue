<template>
  <div class="forgot-password">
    <div class="forgot-password-container">
      <div class="forgot-password-header">
        <h1>忘记密码</h1>
        <p>请输入您的邮箱地址和验证码来重置密码</p>
      </div>

      <form @submit.prevent="handleSubmit" class="forgot-password-form">
        <div class="form-group">
          <label for="email">邮箱地址</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="请输入您的邮箱地址"
            required
            :class="{ 'error': errors.email }"
          />
          <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
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
              :class="{ 'error': errors.captcha }"
            />
            <button
              type="button"
              @click="sendCaptcha"
              :disabled="captchaLoading || countdown > 0"
              class="captcha-btn"
            >
              {{ captchaLoading ? '发送中...' : (countdown > 0 ? `${countdown}秒后重试` : '获取验证码') }}
            </button>
          </div>
          <span v-if="errors.captcha" class="error-message">{{ errors.captcha }}</span>
        </div>

        <div class="form-group">
          <label for="password">新密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="请输入新密码（6-20位）"
            minlength="6"
            maxlength="20"
            required
            :class="{ 'error': errors.password }"
          />
          <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
        </div>

        <div class="form-group">
          <label for="password_confirm">确认新密码</label>
          <input
            id="password_confirm"
            v-model="form.password_confirm"
            type="password"
            placeholder="请再次输入新密码"
            minlength="6"
            maxlength="20"
            required
            :class="{ 'error': errors.password_confirm }"
          />
          <span v-if="errors.password_confirm" class="error-message">{{ errors.password_confirm }}</span>
        </div>

        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <div v-if="errorMessage" class="error-message global-error">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="submit-btn"
        >
          {{ loading ? '重置中...' : '重置密码' }}
        </button>

        <div class="back-to-login">
          <router-link to="/login">返回登录</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '../services/api'

export default {
  name: 'ForgotPassword',
  setup() {
    const router = useRouter()
    
    const form = ref({
      email: '',
      captcha: '',
      password: '',
      password_confirm: ''
    })
    
    const loading = ref(false)
    const captchaLoading = ref(false)
    const countdown = ref(0)
    const errors = ref({})
    const errorMessage = ref('')
    const successMessage = ref('')

    const validateForm = () => {
      errors.value = {}
      
      if (!form.value.email) {
        errors.value.email = '请输入邮箱地址'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
        errors.value.email = '请输入有效的邮箱地址'
      }
      
      if (!form.value.captcha) {
        errors.value.captcha = '请输入验证码'
      } else if (form.value.captcha.length !== 6) {
        errors.value.captcha = '验证码必须是6位数字'
      }
      
      if (!form.value.password) {
        errors.value.password = '请输入新密码'
      } else if (form.value.password.length < 6 || form.value.password.length > 20) {
        errors.value.password = '密码长度必须在6-20位之间'
      }
      
      if (!form.value.password_confirm) {
        errors.value.password_confirm = '请确认新密码'
      } else if (form.value.password !== form.value.password_confirm) {
        errors.value.password_confirm = '两次输入的密码不一致'
      }
      
      return Object.keys(errors.value).length === 0
    }

    const sendCaptcha = async () => {
      if (!form.value.email) {
        errors.value.email = '请先输入邮箱地址'
        return
      }
      
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
        errors.value.email = '请输入有效的邮箱地址'
        return
      }
      
      try {
        captchaLoading.value = true
        errors.value.email = ''
        await apiService.sendCaptcha({ email: form.value.email })
        
        // 开始倒计时
        countdown.value = 60
        const timer = setInterval(() => {
          countdown.value--
          if (countdown.value <= 0) {
            clearInterval(timer)
          }
        }, 1000)
        
        successMessage.value = '验证码已发送到您的邮箱'
        setTimeout(() => {
          successMessage.value = ''
        }, 3000)
      } catch (error) {
        console.error('发送验证码失败:', error)
        errors.value.email = error.response?.data?.errors?.email || '发送验证码失败，请重试'
      } finally {
        captchaLoading.value = false
      }
    }

    const handleSubmit = async () => {
      if (!validateForm()) {
        return
      }
      
      try {
        loading.value = true
        errorMessage.value = ''
        successMessage.value = ''
        
        await apiService.resetPassword({
          email: form.value.email,
          captcha: form.value.captcha,
          password: form.value.password,
          password_confirm: form.value.password_confirm
        })
        
        successMessage.value = '密码重置成功，即将跳转到登录页面'
        
        setTimeout(() => {
          router.push('/login')
        }, 2000)
      } catch (error) {
        console.error('密码重置失败:', error)
        if (error.response?.data?.errors) {
          const serverErrors = error.response.data.errors
          if (typeof serverErrors === 'string') {
            errorMessage.value = serverErrors
          } else {
            Object.keys(serverErrors).forEach(key => {
              errors.value[key] = serverErrors[key][0] || serverErrors[key]
            })
          }
        } else {
          errorMessage.value = '密码重置失败，请重试'
        }
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      captchaLoading,
      countdown,
      errors,
      errorMessage,
      successMessage,
      sendCaptcha,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.forgot-password {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.forgot-password-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.forgot-password-header {
  text-align: center;
  margin-bottom: 2rem;
}

.forgot-password-header h1 {
  color: #333;
  font-size: 24px;
  margin-bottom: 0.5rem;
}

.forgot-password-header p {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.forgot-password-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
  font-size: 14px;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.form-group input.error {
  border-color: #e74c3c;
}

.captcha-group {
  display: flex;
  gap: 0.5rem;
}

.captcha-group input {
  flex: 1;
}

.captcha-btn {
  padding: 0.75rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  white-space: nowrap;
  transition: background-color 0.2s ease;
}

.captcha-btn:hover:not(:disabled) {
  background: #5a6fd8;
}

.captcha-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 0.25rem;
}

.global-error {
  text-align: center;
  padding: 0.75rem;
  background: #fdf2f2;
  border: 1px solid #fecaca;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.success-message {
  color: #27ae60;
  font-size: 14px;
  text-align: center;
  padding: 0.75rem;
  background: #f0f9f0;
  border: 1px solid #c3e6cb;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.submit-btn {
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
  background: #5a6fd8;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.back-to-login {
  text-align: center;
  margin-top: 1rem;
}

.back-to-login a {
  color: #667eea;
  text-decoration: none;
  font-size: 14px;
}

.back-to-login a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .forgot-password-container {
    padding: 1.5rem;
  }
  
  .captcha-group {
    flex-direction: column;
  }
  
  .captcha-btn {
    width: 100%;
  }
}
</style>