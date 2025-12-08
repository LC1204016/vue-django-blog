import axios from 'axios'

// 根据环境变量设置API基础URL
const getApiBaseURL = () => {
  // 优先使用环境变量，否则使用默认值
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }
  return '/api' // 默认值，适用于生产环境
}

// 创建axios实例
const api = axios.create({
  baseURL: getApiBaseURL(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 优先从sessionStorage获取accessToken（不记住我），再从localStorage获取（记住我）
    const token = sessionStorage.getItem('accessToken') || localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    return response.data
  },
  async error => {
    // 对响应错误做点什么
    const originalRequest = error.config
    
    if (error.response) {
      // 如果是401错误且不是刷新令牌的请求，尝试刷新令牌
      if (error.response.status === 401 && !originalRequest._retry && !originalRequest.url.includes('/token/refresh/')) {
        originalRequest._retry = true
        
        try {
          // 获取刷新令牌
          const refreshToken = sessionStorage.getItem('refreshToken') || localStorage.getItem('refreshToken')
          
          if (refreshToken) {
            // 调用刷新令牌API
            const response = await api.post('/token/refresh/', { refresh: refreshToken })
            const newAccessToken = response.access
            
            // 更新存储的访问令牌
            if (localStorage.getItem('refreshToken')) {
              localStorage.setItem('accessToken', newAccessToken)
            } else {
              sessionStorage.setItem('accessToken', newAccessToken)
            }
            
            // 更新请求头
            api.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
            
            // 重试原始请求
            return api(originalRequest)
          }
        } catch (refreshError) {
          // 刷新令牌失败，清除所有令牌
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          localStorage.removeItem('user')
          sessionStorage.removeItem('accessToken')
          sessionStorage.removeItem('refreshToken')
          sessionStorage.removeItem('user')
          
          // 可以在这里添加路由跳转到登录页的逻辑
          console.error('刷新令牌失败，需要重新登录')
          
          return Promise.reject(refreshError)
        }
      }
      
      switch (error.response.status) {
        case 401:
          // 未授权
          console.error('未授权访问')
          break
        case 403:
          // 权限不足
          console.error('权限不足')
          break
        case 404:
          // 资源不存在
          console.error('资源不存在')
          break
        case 500:
          // 服务器错误
          console.error('服务器错误')
          break
      }
    }
    return Promise.reject(error)
  }
)

// API方法
export const apiService = {
  // 获取API概览
  getOverview() {
    return api.get('/')
  },
  
  // 示例API
  getExample() {
    return api.get('/example/')
  },
  
  // 博客相关API - RESTful版本
  getPosts(params = {}) {
    // 统一使用/articles/端点，支持搜索、筛选、分页
    console.log('API调用 - 参数:', params)
    return api.get('/articles/', { params })
  },
  
  getPost(id) {
    return api.get(`/articles/${id}/`)
  },
  
  createPost(data) {
    return api.post('/articles/', data)
  },
  
  updatePost(id, data) {
    return api.put(`/articles/${id}/`, data)
  },
  
  getPostForEdit(id) {
    return api.get(`/articles/${id}/`)
  },
  
  deletePost(id) {
    return api.delete(`/articles/${id}/`)
  },
  
  // 用户认证API
  login(credentials) {
    return api.post('/auth/login/', credentials)
  },
  
  logout() {
    return api.post('/auth/logout/')
  },
  
  register(userData) {
    return api.post('/auth/register/', userData)
  },
  
  // 发送验证码
  sendCaptcha(data) {
    return api.post('/captcha/', data)
  },
  
  // 刷新令牌
  refreshToken(refreshToken) {
    return api.post('/token/refresh/', { refresh: refreshToken })
  },
  
  // 密码重置
  resetPassword(data) {
    return api.put('/password/reset/', data)
  },
  
  getUserProfile(params = {}) {
    return api.get('/profile/me/', { params })
  },
  
  updateProfile(data) {
    // 如果是FormData，设置正确的Content-Type
    if (data instanceof FormData) {
      return api.post('/profile/me/', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    }
    return api.post('/profile/me/', data)
  },
  
  getCategories() {
    return api.get('/categories/')
  },
  
  getTags() {
    return api.get('/tags/')
  },
  
  getTagsByCategory(categoryName) {
    return api.get(`/tags/${categoryName}/`)
  },
  
  createTag(tagName) {
    return api.post('/tags/', { tag: tagName })
  },
  
  // 评论相关API - RESTful版本
  getPostComments(postId) {
    return api.get(`/articles/${postId}/comments/`)
  },
  
  createComment(postId, data) {
    return api.post(`/articles/${postId}/comments/`, data)
  },
  
  deleteComment(commentId) {
    return api.delete(`/comments/${commentId}/`)
  },
  
  // 点赞相关API - RESTful版本
  likePost(postId) {
    return api.post(`/articles/${postId}/likes/`)
  },
  
  unlikePost(postId) {
    return api.delete(`/articles/${postId}/likes/`)
  },
  
  dislikePost(postId) {
    return api.post(`/articles/${postId}/dislikes/`)
  },
  
  undislikePost(postId) {
    return api.delete(`/articles/${postId}/dislikes/`)
  },
  
  // 获取我的文章 - RESTful版本
  getMyPosts(params = {}) {
    return api.get('/getmyposts/', { params })
  },
  
  // 统一的用户资料API
  getUserProfile(userId = null, params = {}) {
    // 如果没有userId，获取当前用户资料
    if (userId === null) {
      return api.get('/users/profile/', { params })
    }
    // 获取指定用户资料
    return api.get(`/users/${userId}/profile/`, { params })
  },
  
  // 更新用户资料
  updateProfile(data) {
    // 如果是FormData，设置正确的Content-Type
    if (data instanceof FormData) {
      return api.put('/users/profile/', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    }
    return api.put('/users/profile/', data)
  }
}

export { api }
export default api