import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 优先从sessionStorage获取token（不记住我），再从localStorage获取（记住我）
    const token = sessionStorage.getItem('token') || localStorage.getItem('token')
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
  error => {
    // 对响应错误做点什么
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token')
          // 这里可以添加路由跳转逻辑
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
  
  // 博客相关API
  getPosts(params = {}) {
    return api.get('/getposts', { params })
  },
  
  getPost(id) {
    return api.get(`/posts/${id}/`)
  },
  
  createPost(data) {
    return api.post('/pubposts/', data)
  },
  
  updatePost(id, data) {
    return api.put(`/edit/${id}/`, data)
  },
  
  getPostForEdit(id) {
    return api.get(`/edit/${id}/`)
  },
  
  deletePost(id) {
    return api.delete(`/posts/${id}/`)
  },
  
  // 用户认证API（待后端实现）
  login(credentials) {
    return api.post('/auth/login/', credentials)
  },
  
  logout() {
    return api.post('/auth/logout/')
  },
  
  register(userData) {
    return api.post('/auth/register/', userData)
  },
  
  getUserProfile() {
    return api.get('/profile/')
  },
  
  updateProfile(data) {
    // 如果是FormData，设置正确的Content-Type
    if (data instanceof FormData) {
      return api.put('/profile/', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    }
    return api.put('/profile/', data)
  },
  
  getCategories() {
    return api.get('/categories/')
  },
  
  getTags() {
    return api.get('/tags/')
  },
  
  createTag(tagName) {
    return api.post('/tags/', { tag: tagName })
  },
  
  // 评论相关API
  getPostComments(postId) {
    return api.get(`/comments/${postId}/`)
  },
  
  createComment(postId, data) {
    return api.post(`/pubcomments/${postId}/`, data)
  },
  
  deleteComment(commentId) {
    return api.delete(`/comments/${commentId}/`)
  },
  
  // 点赞相关API
  likePost(postId) {
    return api.post(`/likes/${postId}/`)
  },
  
  unlikePost(postId) {
    return api.delete(`/likes/${postId}/`)
  },
  
  dislikePost(postId) {
    return api.post(`/dislikes/${postId}/`)
  },
  
  undislikePost(postId) {
    return api.delete(`/dislikes/${postId}/`)
  },
  
  // 获取我的文章
  getMyPosts(params = {}) {
    return api.get('/getmyposts/', { params })
  }
}

export { api }
export default api