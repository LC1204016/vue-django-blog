import { defineStore } from 'pinia'
import { apiService, api } from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: sessionStorage.getItem('accessToken') || localStorage.getItem('accessToken') || null,
    refreshToken: sessionStorage.getItem('refreshToken') || localStorage.getItem('refreshToken') || null,
    isAuthenticated: false
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => !!state.accessToken && state.isAuthenticated
  },

  actions: {
    async login(credentials) {
      try {
        const response = await apiService.login(credentials)
        
        this.accessToken = response.access
        this.refreshToken = response.refresh
        this.user = response.user
        this.isAuthenticated = true
        
        // 根据记住我选择存储token
        if (credentials.remember) {
          // 记住我：存储到localStorage（长期有效）
          localStorage.setItem('accessToken', this.accessToken)
          localStorage.setItem('refreshToken', this.refreshToken)
          localStorage.setItem('user', JSON.stringify(response.user)) // 存储用户信息
        } else {
          // 不记住：存储到sessionStorage（浏览器关闭时清除）
          sessionStorage.setItem('accessToken', this.accessToken)
          sessionStorage.setItem('refreshToken', this.refreshToken)
          sessionStorage.setItem('user', JSON.stringify(response.user)) // 存储用户信息
          localStorage.removeItem('accessToken') // 清除localStorage中的token
          localStorage.removeItem('refreshToken')
          localStorage.removeItem('user') // 清除localStorage中的用户信息
        }
        
        // 设置axios默认header
        api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
        
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
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false
      
      // 清除所有存储
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
      sessionStorage.removeItem('accessToken')
      sessionStorage.removeItem('refreshToken')
      sessionStorage.removeItem('user')
      
      // 清除axios header
      delete api.defaults.headers.common['Authorization']
      
      // 调用后端logout API（可选）
      apiService.logout().catch(() => {
        // 忽略logout API错误
      })
    },

    // 刷新访问令牌
    async refreshAccessToken() {
      try {
        // 获取刷新令牌
        const refreshToken = sessionStorage.getItem('refreshToken') || localStorage.getItem('refreshToken')
        
        if (!refreshToken) {
          throw new Error('没有刷新令牌')
        }
        
        const response = await apiService.refreshToken(refreshToken)
        
        this.accessToken = response.access
        
        // 更新存储的访问令牌
        if (localStorage.getItem('refreshToken')) {
          localStorage.setItem('accessToken', this.accessToken)
        } else {
          sessionStorage.setItem('accessToken', this.accessToken)
        }
        
        // 更新axios header
        api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
        
        return response.access
      } catch (error) {
        // 刷新失败，清除认证状态
        this.logout()
        throw error
      }
    },

    // 初始化认证状态
    async initAuth() {
      // 优先从sessionStorage获取token（不记住我）
      let accessToken = sessionStorage.getItem('accessToken') || localStorage.getItem('accessToken')
      let refreshToken = sessionStorage.getItem('refreshToken') || localStorage.getItem('refreshToken')
      
      if (accessToken && refreshToken) {
        // 设置认证状态
        this.accessToken = accessToken
        this.refreshToken = refreshToken
        this.isAuthenticated = true
        
        // 设置axios header
        api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
        
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