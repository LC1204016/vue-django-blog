import { defineStore } from 'pinia'
import { apiService } from '../services/api'

export const usePostsStore = defineStore('posts', {
  state: () => ({
    posts: [],
    currentPost: null,
    loading: false,
    error: null,
    pagination: {
      currentPage: 1,
      totalPages: 1,
      totalCount: 0,
      pageSize: 10
    },
    filters: {
      search: '',
      category: '',
      tags: [],
      author: ''
    }
  }),

  getters: {
    filteredPosts: (state) => {
      let filtered = [...state.posts]
      
      if (state.filters.search) {
        const searchLower = state.filters.search.toLowerCase()
        filtered = filtered.filter(post => 
          post.title.toLowerCase().includes(searchLower) ||
          post.excerpt.toLowerCase().includes(searchLower) ||
          post.content.toLowerCase().includes(searchLower)
        )
      }
      
      if (state.filters.category) {
        filtered = filtered.filter(post => post.category === state.filters.category)
      }
      
      if (state.filters.tags.length > 0) {
        filtered = filtered.filter(post => 
          state.filters.tags.some(tag => post.tags.includes(tag))
        )
      }
      
      if (state.filters.author) {
        filtered = filtered.filter(post => post.author === state.filters.author)
      }
      
      return filtered
    },

    getPostById: (state) => (id) => {
      return state.posts.find(post => post.id === parseInt(id))
    },

    getRecentPosts: (state) => (limit = 3) => {
      return [...state.posts]
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, limit)
    }
  },

  actions: {
    async fetchPosts(page = 1, filters = {}) {
      try {
        this.loading = true
        this.error = null
        
        const params = {
          page,
          ...filters
        }
        
        const response = await apiService.getPosts(params)
        
        if (response.results) {
          // 分页响应格式
          this.posts = response.results
          this.pagination = {
            currentPage: page,
            totalPages: response.total_pages || Math.ceil(response.count / this.pagination.pageSize),
            totalCount: response.count,
            pageSize: this.pagination.pageSize
          }
        } else {
          // 非分页响应格式
          this.posts = response
        }
        
        return response
      } catch (error) {
        this.error = error.message || '获取文章失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchPost(id) {
      try {
        this.loading = true
        this.error = null
        
        const post = await apiService.getPost(id)
        this.currentPost = post
        
        // 更新posts列表中的对应文章
        const index = this.posts.findIndex(p => p.id === parseInt(id))
        if (index !== -1) {
          this.posts[index] = post
        }
        
        return post
      } catch (error) {
        this.error = error.message || '获取文章详情失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    async createPost(postData) {
      try {
        this.loading = true
        this.error = null
        
        const post = await apiService.createPost(postData)
        this.posts.unshift(post)
        
        return post
      } catch (error) {
        this.error = error.message || '创建文章失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updatePost(id, postData) {
      try {
        this.loading = true
        this.error = null
        
        const post = await apiService.updatePost(id, postData)
        
        // 更新posts列表中的对应文章
        const index = this.posts.findIndex(p => p.id === parseInt(id))
        if (index !== -1) {
          this.posts[index] = post
        }
        
        // 更新currentPost
        if (this.currentPost && this.currentPost.id === parseInt(id)) {
          this.currentPost = post
        }
        
        return post
      } catch (error) {
        this.error = error.message || '更新文章失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deletePost(id) {
      try {
        this.loading = true
        this.error = null
        
        await apiService.deletePost(id)
        
        // 从posts列表中移除
        this.posts = this.posts.filter(post => post.id !== parseInt(id))
        
        // 清除currentPost
        if (this.currentPost && this.currentPost.id === parseInt(id)) {
          this.currentPost = null
        }
        
        return true
      } catch (error) {
        this.error = error.message || '删除文章失败'
        throw error
      } finally {
        this.loading = false
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },

    clearFilters() {
      this.filters = {
        search: '',
        category: '',
        tags: [],
        author: ''
      }
    },

    clearError() {
      this.error = null
    },

    clearCurrentPost() {
      this.currentPost = null
    }
  }
})