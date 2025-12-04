import { defineStore } from 'pinia'
import { apiService, api } from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: sessionStorage.getItem('token') || localStorage.getItem('token') || null,
    isAuthenticated: false
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => !!state.token && state.isAuthenticated
  },

  actions: {
    async login(credentials) {
      try {
        const response = await apiService.login(credentials)
        
        this.token = response.token
        this.user = response.user
        this.isAuthenticated = true
        
        // 根据记住我选择存储token
        if (credentials.remember) {
          // 记住我：存储14天
          localStorage.setItem('token', this.token)
          localStorage.setItem('tokenExpiry', new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString())
          localStorage.setItem('user', JSON.stringify(response.user)) // 存储用户信息
        } else {
          // 不记住：存储到sessionStorage（浏览器关闭时清除）
          sessionStorage.setItem('token', this.token)
          sessionStorage.setItem('user', JSON.stringify(response.user)) // 存储用户信息
          localStorage.removeItem('token') // 清除localStorage中的token
          localStorage.removeItem('tokenExpiry')
          localStorage.removeItem('user') // 清除localStorage中的用户信息
        }
        
        // 设置axios默认header
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        
        return response
      } catch (error) {
        this.logout()
        throw error
      }
    },

    async register(userData) {
      try {
        const response = await apiService.register(userData)
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchProfile() {
      try {
        const profile = await apiService.getUserProfile()
        this.user = profile
        this.isAuthenticated = true
        return profile
      } catch (error) {
        this.logout()
        throw error
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      
      // 清除所有存储
      localStorage.removeItem('token')
      localStorage.removeItem('tokenExpiry')
      localStorage.removeItem('user')
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('user')
      
      // 清除axios header
      delete api.defaults.headers.common['Authorization']
      
      // 调用后端logout API（可选）
      apiService.logout().catch(() => {
        // 忽略logout API错误
      })
    },

    // 初始化认证状态
    async initAuth() {
      // 优先从sessionStorage获取token（不记住我）
      let token = sessionStorage.getItem('token') || localStorage.getItem('token')
      
      if (token) {
        // 检查token是否过期
        const expiry = localStorage.getItem('tokenExpiry')
        if (expiry && new Date() > new Date(expiry)) {
          this.logout()
          return
        }
        
        // 设置认证状态
        this.token = token
        this.isAuthenticated = true
        
        // 设置axios header
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        
        // 从登录时存储的用户信息中恢复（如果有）
        const storedUser = sessionStorage.getItem('user') || localStorage.getItem('user')
        if (storedUser) {
          try {
            this.user = JSON.parse(storedUser)
          } catch (error) {
            console.error('解析用户信息失败:', error)
          }
        }
      }
    }
  }
})