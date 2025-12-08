/**
 * 前端文章功能测试
 * 测试文章列表、详情、创建、编辑等功能
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { usePostsStore } from '../../src/stores/posts'

// Mock API服务
vi.mock('../../src/services/api', () => ({
  apiService: {
    getPosts: vi.fn(),
    getPost: vi.fn(),
    createPost: vi.fn(),
    updatePost: vi.fn(),
    getPostForEdit: vi.fn(),
    deletePost: vi.fn(),
    getCategories: vi.fn(),
    getMyPosts: vi.fn()
  }
}))

import { apiService } from '../../src/services/api'

describe('文章存储测试', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('获取文章列表', () => {
    it('应该成功获取文章列表', async () => {
      const mockPosts = [
        { id: 1, title: '文章1', author: '用户1' },
        { id: 2, title: '文章2', author: '用户2' }
      ]
      apiService.getPosts.mockResolvedValue(mockPosts)

      const postsStore = usePostsStore()
      const result = await postsStore.fetchPosts()

      expect(apiService.getPosts).toHaveBeenCalledWith({ page: 1 })
      expect(postsStore.posts).toEqual(mockPosts)
      expect(result).toEqual(mockPosts)
    })

    it('应该支持分页参数', async () => {
      const params = { limit: 10 }
      apiService.getPosts.mockResolvedValue([])

      const postsStore = usePostsStore()
      await postsStore.fetchPosts(2, params)

      expect(apiService.getPosts).toHaveBeenCalledWith({ page: 2, limit: 10 })
    })

    it('应该正确设置加载状态', async () => {
      const postsStore = usePostsStore()
      
      // 开始加载
      const promise = postsStore.fetchPosts()
      expect(postsStore.loading).toBe(true)
      
      // 完成加载
      await promise
      expect(postsStore.loading).toBe(false)
    })
  })

  describe('获取文章详情', () => {
    it('应该成功获取文章详情', async () => {
      const mockPost = { id: 1, title: '测试文章', content: '测试内容' }
      apiService.getPost.mockResolvedValue(mockPost)

      const postsStore = usePostsStore()
      const result = await postsStore.fetchPost(1)

      expect(apiService.getPost).toHaveBeenCalledWith(1)
      expect(result).toEqual(mockPost)
    })

    it('应该处理文章不存在的情况', async () => {
      const error = new Error('文章不存在')
      apiService.getPost.mockRejectedValue(error)

      const postsStore = usePostsStore()
      
      try {
        await postsStore.fetchPost(999)
      } catch (err) {
        expect(err).toBe(error)
      }
    })
  })

  describe('创建文章', () => {
    it('应该成功创建文章', async () => {
      const newPost = {
        title: '新文章',
        content: '新文章内容',
        category: 1
      }
      const createdPost = { id: 1, ...newPost }
      apiService.createPost.mockResolvedValue(createdPost)

      const postsStore = usePostsStore()
      const result = await postsStore.createPost(newPost)

      expect(apiService.createPost).toHaveBeenCalledWith(newPost)
      expect(result).toEqual(createdPost)
    })

    it('创建失败时应该抛出错误', async () => {
      const error = new Error('创建失败')
      apiService.createPost.mockRejectedValue(error)

      const postsStore = usePostsStore()
      
      try {
        await postsStore.createPost({
          title: '',
          content: '',
          category: 1
        })
      } catch (err) {
        expect(err).toBe(error)
      }
    })
  })

  describe('更新文章', () => {
    it('应该成功更新文章', async () => {
      const postId = 1
      const updateData = {
        title: '更新的标题',
        content: '更新的内容'
      }
      const updatedPost = { id: postId, ...updateData }
      apiService.updatePost.mockResolvedValue(updatedPost)

      const postsStore = usePostsStore()
      const result = await postsStore.updatePost(postId, updateData)

      expect(apiService.updatePost).toHaveBeenCalledWith(postId, updateData)
      expect(result).toEqual(updatedPost)
    })

    it('更新不存在的文章应该抛出错误', async () => {
      const error = new Error('文章不存在')
      apiService.updatePost.mockRejectedValue(error)

      const postsStore = usePostsStore()
      
      try {
        await postsStore.updatePost(999, { title: '新标题' })
      } catch (err) {
        expect(err).toBe(error)
      }
    })
  })

  describe('删除文章', () => {
    it('应该成功删除文章', async () => {
      apiService.deletePost.mockResolvedValue({ success: true })

      const postsStore = usePostsStore()
      const result = await postsStore.deletePost(1)

      expect(apiService.deletePost).toHaveBeenCalledWith(1)
      expect(result).toBe(true)
    })

    it('删除不存在的文章应该抛出错误', async () => {
      const error = new Error('文章不存在')
      apiService.deletePost.mockRejectedValue(error)

      const postsStore = usePostsStore()
      
      try {
        await postsStore.deletePost(999)
      } catch (err) {
        expect(err).toBe(error)
      }
    })
  })

  describe('状态管理', () => {
    it('应该正确初始化状态', () => {
      const postsStore = usePostsStore()
      
      expect(postsStore.posts).toEqual([])
      expect(postsStore.currentPost).toBeNull()
      expect(postsStore.loading).toBe(false)
      expect(postsStore.error).toBeNull()
    })

    it('应该正确设置加载状态', async () => {
      const postsStore = usePostsStore()
      
      // 开始加载
      const promise = postsStore.fetchPosts()
      expect(postsStore.loading).toBe(true)
      
      // 完成加载
      await promise
      expect(postsStore.loading).toBe(false)
    })

    it('应该正确处理错误', async () => {
      const error = new Error('测试错误')
      apiService.getPosts.mockRejectedValue(error)

      const postsStore = usePostsStore()
      
      try {
        await postsStore.fetchPosts()
      } catch (err) {
        expect(postsStore.error).toBe('测试错误')
      }
    })
  })

  describe('筛选功能', () => {
    it('应该正确设置筛选条件', () => {
      const postsStore = usePostsStore()
      const filters = {
        search: 'Vue',
        category: '技术',
        tags: ['前端'],
        author: '测试作者'
      }
      
      postsStore.setFilters(filters)
      
      expect(postsStore.filters.search).toBe('Vue')
      expect(postsStore.filters.category).toBe('技术')
      expect(postsStore.filters.tags).toEqual(['前端'])
      expect(postsStore.filters.author).toBe('测试作者')
    })

    it('应该正确清除筛选条件', () => {
      const postsStore = usePostsStore()
      // 先设置一些筛选条件
      postsStore.setFilters({ search: 'Vue', category: '技术' })
      
      // 清除筛选条件
      postsStore.clearFilters()
      
      expect(postsStore.filters.search).toBe('')
      expect(postsStore.filters.category).toBe('')
      expect(postsStore.filters.tags).toEqual([])
      expect(postsStore.filters.author).toBe('')
    })

    it('应该正确清除错误', () => {
      const postsStore = usePostsStore()
      postsStore.error = '测试错误'
      
      postsStore.clearError()
      
      expect(postsStore.error).toBeNull()
    })

    it('应该正确清除当前文章', () => {
      const postsStore = usePostsStore()
      postsStore.currentPost = { id: 1, title: '测试文章' }
      
      postsStore.clearCurrentPost()
      
      expect(postsStore.currentPost).toBeNull()
    })
  })

  describe('计算属性', () => {
    it('filteredPosts应该根据搜索条件筛选文章', () => {
      const postsStore = usePostsStore()
      postsStore.posts = [
        { id: 1, title: 'Vue教程', excerpt: '学习Vue框架', content: 'Vue是流行的前端框架', tags: ['前端'], category: '技术', author: '作者1' },
        { id: 2, title: 'React教程', excerpt: '学习React框架', content: 'React是流行的前端框架', tags: ['前端'], category: '技术', author: '作者2' },
        { id: 3, title: '生活随笔', excerpt: '日常生活', content: '今天天气很好', tags: ['生活'], category: '生活', author: '作者3' }
      ]
      
      // 测试搜索
      postsStore.setFilters({ search: 'Vue' })
      const searchResults = postsStore.filteredPosts
      expect(searchResults).toHaveLength(1)
      expect(searchResults[0].title).toBe('Vue教程')
      
      // 测试分类筛选
      postsStore.setFilters({ search: '', category: '生活' })
      const categoryResults = postsStore.filteredPosts
      expect(categoryResults).toHaveLength(1)
      expect(categoryResults[0].title).toBe('生活随笔')
      
      // 测试标签筛选
      postsStore.setFilters({ search: '', category: '', tags: ['前端'] })
      const tagResults = postsStore.filteredPosts
      expect(tagResults).toHaveLength(2)
      
      // 测试作者筛选
      postsStore.setFilters({ search: '', category: '', tags: [], author: '作者1' })
      const authorResults = postsStore.filteredPosts
      expect(authorResults).toHaveLength(1)
      expect(authorResults[0].title).toBe('Vue教程')
    })

    it('getPostById应该根据ID获取文章', () => {
      const postsStore = usePostsStore()
      postsStore.posts = [
        { id: 1, title: '文章1' },
        { id: 2, title: '文章2' }
      ]
      
      const post = postsStore.getPostById(1)
      expect(post.title).toBe('文章1')
      
      const nonExistentPost = postsStore.getPostById(999)
      expect(nonExistentPost).toBeUndefined()
    })

    it('getRecentPosts应该获取最新文章', () => {
      const postsStore = usePostsStore()
      postsStore.posts = [
        { id: 1, title: '旧文章', created_at: '2023-01-01' },
        { id: 2, title: '新文章', created_at: '2023-12-01' },
        { id: 3, title: '最新文章', created_at: '2023-12-31' }
      ]
      
      const recentPosts = postsStore.getRecentPosts(2)
      expect(recentPosts).toHaveLength(2)
      expect(recentPosts[0].title).toBe('最新文章')
      expect(recentPosts[1].title).toBe('新文章')
    })
  })
})