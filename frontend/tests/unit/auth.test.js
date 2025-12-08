/**
 * 前端认证组件测试
 * 测试登录、注册、状态管理等功能
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../../src/stores/auth'

// Mock API服务
vi.mock('../../src/services/api', () => ({
  apiService: {
    getOverview: vi.fn(),
    getExample: vi.fn(),
    login: vi.fn(),
    register: vi.fn(),
    getUserProfile: vi.fn(),
    logout: vi.fn().mockResolvedValue({}),
    refreshToken: vi.fn(),
    getPosts: vi.fn(),
    createPost: vi.fn(),
    updatePost: vi.fn(),
    getPostForEdit: vi.fn(),
    deletePost: vi.fn(),
    getCategories: vi.fn(),
    getTags: vi.fn(),
    getTagsByCategory: vi.fn(),
    createTag: vi.fn(),
    getPostComments: vi.fn(),
    createComment: vi.fn(),
    deleteComment: vi.fn(),
    likePost: vi.fn(),
    unlikePost: vi.fn(),
    dislikePost: vi.fn(),
    undislikePost: vi.fn(),
    getMyPosts: vi.fn(),
    getUserProfileById: vi.fn()
  },
  api: {
    defaults: {
      headers: {
        common: {}
      }
    }
  }
}))

import { apiService, api } from '../../src/services/api'

describe('认证存储测试', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    // 清除所有存储
    localStorage.clear()
    sessionStorage.clear()
    // Mock localStorage和sessionStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: vi.fn(),
        setItem: vi.fn(),
        removeItem: vi.fn(),
        clear: vi.fn()
      },
      writable: true
    })
    Object.defineProperty(window, 'sessionStorage', {
      value: {
        getItem: vi.fn(),
        setItem: vi.fn(),
        removeItem: vi.fn(),
        clear: vi.fn()
      },
      writable: true
    })
  })

  describe('登录功能', () => {
    it('应该成功登录并存储token', async () => {
      const authStore = useAuthStore()
      const mockResponse = {
        access: 'mock-access-token',
        refresh: 'mock-refresh-token',
        user: { id: 1, username: 'testuser', email: 'test@example.com' }
      }
      apiService.login.mockResolvedValue(mockResponse)

      const result = await authStore.login({
        username: 'testuser',
        password: 'password123',
        remember: true
      })

      expect(apiService.login).toHaveBeenCalledWith({
        username: 'testuser',
        password: 'password123',
        remember: true
      })
      expect(authStore.accessToken).toBe('mock-access-token')
      expect(authStore.refreshToken).toBe('mock-refresh-token')
      expect(authStore.user).toEqual(mockResponse.user)
      expect(authStore.isAuthenticated).toBe(true)
      expect(authStore.isLoggedIn).toBe(true)
      expect(localStorage.setItem).toHaveBeenCalledWith('accessToken', 'mock-access-token')
      expect(localStorage.setItem).toHaveBeenCalledWith('refreshToken', 'mock-refresh-token')
      expect(result).toEqual(mockResponse)
    })

    it('登录失败时应该清除认证状态', async () => {
      const authStore = useAuthStore()
      const error = new Error('登录失败')
      apiService.login.mockRejectedValue(error)

      try {
        await authStore.login({
          username: 'testuser',
          password: 'wrongpassword'
        })
      } catch (err) {
        expect(err).toBe(error)
      }

      expect(authStore.isAuthenticated).toBe(false)
      expect(authStore.accessToken).toBeNull()
      expect(authStore.refreshToken).toBeNull()
    })

    it('记住我功能应该正确存储token', async () => {
      const authStore = useAuthStore()
      const mockResponse = {
        access: 'mock-access-token',
        refresh: 'mock-refresh-token',
        user: { id: 1, username: 'testuser', email: 'test@example.com' }
      }
      apiService.login.mockResolvedValue(mockResponse)

      // 测试记住我
      await authStore.login({
        username: 'testuser',
        password: 'password123',
        remember: true
      })

      expect(localStorage.setItem).toHaveBeenCalledWith('accessToken', 'mock-access-token')
      expect(localStorage.setItem).toHaveBeenCalledWith('refreshToken', 'mock-refresh-token')
      expect(sessionStorage.setItem).not.toHaveBeenCalledWith('accessToken', 'mock-access-token')
      expect(sessionStorage.setItem).not.toHaveBeenCalledWith('refreshToken', 'mock-refresh-token')

      // 测试不记住
      vi.clearAllMocks()
      await authStore.login({
        username: 'testuser2',
        password: 'password123',
        remember: false
      })

      expect(sessionStorage.setItem).toHaveBeenCalledWith('accessToken', 'mock-access-token')
      expect(sessionStorage.setItem).toHaveBeenCalledWith('refreshToken', 'mock-refresh-token')
      expect(localStorage.removeItem).toHaveBeenCalledWith('accessToken')
      expect(localStorage.removeItem).toHaveBeenCalledWith('refreshToken')
    })
  })

  describe('注册功能', () => {
    it('应该成功注册用户', async () => {
      const authStore = useAuthStore()
      const userData = {
        username: 'newuser',
        email: 'newuser@example.com',
        password: 'password123',
        password_confirm: 'password123'
      }
      apiService.register.mockResolvedValue({ success: true })

      const result = await authStore.register(userData)

      expect(apiService.register).toHaveBeenCalledWith(userData)
      expect(result).toEqual({ success: true })
    })

    it('注册失败时应该抛出错误', async () => {
      const authStore = useAuthStore()
      const error = new Error('注册失败')
      apiService.register.mockRejectedValue(error)

      try {
        await authStore.register({
          username: 'existinguser',
          email: 'existing@example.com',
          password: 'password123',
          password_confirm: 'password123'
        })
      } catch (err) {
        expect(err).toBe(error)
      }
    })
  })

  describe('令牌刷新功能', () => {
    it('应该成功刷新访问令牌', async () => {
      const authStore = useAuthStore()
      authStore.accessToken = 'old-token'
      authStore.refreshToken = 'refresh-token'
      localStorage.getItem.mockReturnValue('refresh-token')
      const mockResponse = { access: 'new-access-token' }
      apiService.refreshToken.mockResolvedValue(mockResponse)

      const result = await authStore.refreshAccessToken()

      expect(apiService.refreshToken).toHaveBeenCalledWith('refresh-token')
      expect(result).toBe('new-access-token')
      expect(authStore.accessToken).toBe('new-access-token')
    })

    it('刷新失败时应该清除认证状态', async () => {
      const authStore = useAuthStore()
      authStore.accessToken = 'old-token'
      authStore.refreshToken = 'expired-refresh-token'
      localStorage.getItem.mockReturnValue('expired-refresh-token')
      const error = new Error('刷新令牌失败')
      apiService.refreshToken.mockRejectedValue(error)

      try {
        await authStore.refreshAccessToken()
      } catch (err) {
        expect(err).toBe(error)
      }

      expect(authStore.isAuthenticated).toBe(false)
      expect(authStore.accessToken).toBeNull()
      expect(authStore.refreshToken).toBeNull()
    })
  })

  describe('状态初始化', () => {
    it('应该从存储中恢复认证状态', async () => {
      const authStore = useAuthStore()
      
      // 模拟存储中的数据
      localStorage.getItem
        .mockReturnValueOnce('stored-access-token')  // accessToken
        .mockReturnValueOnce('stored-refresh-token') // refreshToken
        .mockReturnValueOnce(JSON.stringify({ id: 1, username: 'testuser' })) // user

      await authStore.initAuth()

      expect(authStore.accessToken).toBe('stored-access-token')
      expect(authStore.refreshToken).toBe('stored-refresh-token')
      expect(authStore.user).toEqual({ id: 1, username: 'testuser' })
      expect(authStore.isAuthenticated).toBe(true)
    })
  })

  describe('Getters', () => {
    it('currentUser应该返回当前用户', () => {
      const authStore = useAuthStore()
      const mockUser = { id: 1, username: 'testuser' }
      authStore.user = mockUser
      
      expect(authStore.currentUser).toStrictEqual(mockUser)
    })

    it('isLoggedIn应该基于token和认证状态返回', () => {
      const authStore = useAuthStore()
      
      // 有token且已认证
      authStore.accessToken = 'mock-token'
      authStore.isAuthenticated = true
      expect(authStore.isLoggedIn).toBe(true)
      
      // 有token但未认证
      authStore.isAuthenticated = false
      expect(authStore.isLoggedIn).toBe(false)
      
      // 无token
      authStore.accessToken = null
      expect(authStore.isLoggedIn).toBe(false)
    })
  })
})