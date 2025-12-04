<template>
  <div class="post-detail">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <router-link to="/posts" class="btn btn-primary">返回文章列表</router-link>
    </div>
    <article v-else-if="post" class="post-article">
      <header class="post-header">
        <h1>{{ post.title }}</h1>
        <div class="post-meta">
          <div class="author-info">
            <div class="author-avatar">
              <img v-if="post.profile_pic" :src="post.profile_pic.startsWith('http') ? post.profile_pic : `http://localhost:8000${post.profile_pic}`" :alt="post.author" />
              <span v-else>{{ post.author.charAt(0).toUpperCase() }}</span>
            </div>
            <span class="author">作者: {{ post.author }}</span>
          </div>
          <div class="post-dates">
            <span class="date">发布时间: {{ formatDate(post.created_at) }}</span>
            <span v-if="post.updated_time" class="updated-time">更新时间: {{ formatDate(post.updated_time) }}</span>
          </div>
          <span class="category">分类: {{ post.category }}</span>
        </div>
        <div class="post-tags">
          <span v-for="tag in post.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </header>

      

      <div class="post-content" v-html="post.content"></div>

      <footer class="post-footer">
        <div class="post-actions">
          <button v-if="isAuthor" @click="editPost" class="btn btn-secondary">
            编辑
          </button>
          <button v-if="isAuthor" @click="deletePost" class="btn btn-danger">
            删除
          </button>
        </div>
        <div class="post-stats">
          <span>👁️ {{ post.views }} 次浏览</span>
          <span>💬 {{ post.comments_count }} 条评论</span>
          <div class="like-dislike-buttons">
            <button 
              @click="toggleLike" 
              :class="['like-button', { 'liked': post.liked, 'loading': likeLoading }]"
              :disabled="likeLoading"
            >
              <span class="like-icon">{{ post.liked ? '❤️' : '🤍' }}</span>
              <span class="like-count">{{ post.likes }}</span>
            </button>
            <button 
              @click="toggleDislike" 
              :class="['dislike-button', { 'disliked': post.disliked, 'loading': dislikeLoading }]"
              :disabled="dislikeLoading"
            >
              <span class="dislike-icon">{{ post.disliked ? '👎' : '👎🏻' }}</span>
              <span class="dislike-count">{{ post.dislikes }}</span>
            </button>
          </div>
        </div>
      </footer>
    </article>

    <!-- 评论区 -->
    <section class="comments-section">
      <h2>评论 ({{ comments.length }})</h2>
      
      <!-- 发表评论表单 -->
      <div v-if="isLoggedIn" class="comment-form">
        <h3>发表评论</h3>
        <form @submit.prevent="submitComment">
          <div class="form-group">
            <textarea 
              v-model="newComment" 
              placeholder="写下你的评论..." 
              required
              rows="4"
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary">发表评论</button>
        </form>
      </div>
      <div v-else class="login-prompt">
        <p>请 <router-link to="/login">登录</router-link> 后发表评论</p>
      </div>

      <!-- 评论列表 -->
      <div v-if="comments.length === 0" class="empty-comments">
        <p>暂无评论，快来发表第一条评论吧！</p>
      </div>
      <div v-else class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment">
          <div class="comment-header">
            <div class="comment-author-info">
              <div class="comment-avatar">
                <img v-if="comment.profile_pic" :src="comment.profile_pic.startsWith('http') ? comment.profile_pic : `http://localhost:8000${comment.profile_pic}`" :alt="comment.author" />
                <span v-else>{{ comment.author.charAt(0).toUpperCase() }}</span>
              </div>
              <span class="comment-author">{{ comment.author }}</span>
            </div>
            <span class="comment-date">{{ formatDate(comment.created_at || comment.pub_time) }}</span>
          </div>
          <div class="comment-content">{{ comment.content }}</div>
          <div v-if="isCommentAuthor(comment)" class="comment-actions">
            <button @click="deleteComment(comment.id)" class="btn btn-text btn-danger">
              删除
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiService } from '../services/api'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'PostDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    const post = ref(null)
    const comments = ref([])
    const loading = ref(true)
    const error = ref('')
    const newComment = ref('')
    const likeLoading = ref(false)
    const dislikeLoading = ref(false)

    const isLoggedIn = computed(() => authStore.isAuthenticated)
    const currentUser = computed(() => authStore.user)

    const isAuthor = computed(() => {
      return currentUser.value && post.value && 
             currentUser.value.username === post.value.author
    })

    const fetchPost = async () => {
      try {
        loading.value = true
        const postId = route.params.id
        const postData = await apiService.getPost(postId)
        
        // 处理后端返回的数据格式
        post.value = {
          ...postData,
          id: postId, // 添加文章ID
          created_at: postData.pub_time, // 映射pub_time到created_at
          updated_time: postData.updated_time, // 添加更新时间
          profile_pic: postData.profile_pic, // 添加作者头像
          views: postData.views || 0,
          likes: postData.like_count || 0, // 映射like_count到likes
          dislikes: postData.dislike_count || 0, // 添加dislikes字段
          comments_count: 0, // 将在获取评论后更新
          tags: postData.tags || []
        }
        
        // 获取评论
        const commentsData = await apiService.getPostComments(postId)
        console.log('获取到的评论数据:', commentsData) // 调试输出
        // 为评论添加id字段（使用索引作为临时id）
        comments.value = commentsData.map((comment, index) => ({
          ...comment,
          id: comment.id || `temp-${index}`, // 如果后端没有返回id，使用临时id
          created_at: comment.pub_time // 统一时间字段名
        }))
        post.value.comments_count = comments.value.length
        
        // 点赞状态已在get_post接口中返回，无需额外请求
      } catch (err) {
        error.value = '文章不存在或加载失败'
        console.error('获取文章失败:', err)
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return '未知时间'
      
      try {
        const date = new Date(dateString)
        if (isNaN(date.getTime())) return '时间格式错误'
        
        const options = { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }
        return date.toLocaleDateString('zh-CN', options)
      } catch (error) {
        console.error('时间格式化错误:', error, dateString)
        return '时间格式错误'
      }
    }

    const isCommentAuthor = (comment) => {
      return currentUser.value && currentUser.value.username === comment.author
    }

    const submitComment = async () => {
      try {
        const comment = await apiService.createComment(post.value.id, {
          content: newComment.value
        })
        // 发表成功后刷新页面
        window.location.reload()
      } catch (err) {
        console.error('发表评论失败:', err)
        alert('发表评论失败，请重试')
      }
    }

    const deleteComment = async (commentId) => {
      if (confirm('确定要删除这条评论吗？')) {
        try {
          await apiService.deleteComment(commentId)
          comments.value = comments.value.filter(c => c.id !== commentId)
          post.value.comments_count--
        } catch (err) {
          console.error('删除评论失败:', err)
          alert('删除评论失败，请重试')
        }
      }
    }

    const editPost = () => {
      router.push(`/posts/${post.value.id}/edit`)
    }

    const deletePost = async () => {
      if (confirm('确定要删除这篇文章吗？此操作不可恢复。')) {
        try {
          await apiService.deletePost(post.value.id)
          router.push('/posts')
        } catch (err) {
          console.error('删除文章失败:', err)
          alert('删除文章失败，请重试')
        }
      }
    }

    const toggleLike = async () => {
      if (!isLoggedIn.value) {
        alert('请先登录后再点赞')
        return
      }
      
      if (likeLoading.value) return
      
      try {
        likeLoading.value = true
        
        if (post.value.liked) {
          await apiService.unlikePost(post.value.id)
          post.value.likes--
          post.value.liked = false
        } else {
          // 如果之前点过踩，先取消踩
          if (post.value.disliked) {
            await apiService.undislikePost(post.value.id)
            post.value.dislikes--
            post.value.disliked = false
          }
          
          await apiService.likePost(post.value.id)
          post.value.likes++
          post.value.liked = true
        }
      } catch (err) {
        console.error('点赞操作失败:', err)
        alert('点赞操作失败，请重试')
      } finally {
        likeLoading.value = false
      }
    }

    const toggleDislike = async () => {
      if (!isLoggedIn.value) {
        alert('请先登录后再点赞')
        return
      }
      
      if (dislikeLoading.value) return
      
      try {
        dislikeLoading.value = true
        
        if (post.value.disliked) {
          await apiService.undislikePost(post.value.id)
          post.value.dislikes--
          post.value.disliked = false
        } else {
          // 如果之前点过赞，先取消赞
          if (post.value.liked) {
            await apiService.unlikePost(post.value.id)
            post.value.likes--
            post.value.liked = false
          }
          
          await apiService.dislikePost(post.value.id)
          post.value.dislikes++
          post.value.disliked = true
        }
      } catch (err) {
        console.error('点踩操作失败:', err)
        alert('点踩操作失败，请重试')
      } finally {
        dislikeLoading.value = false
      }
    }

    onMounted(() => {
      fetchPost()
    })

    return {
      post,
      comments,
      loading,
      error,
      newComment,
      likeLoading,
      dislikeLoading,
      isLoggedIn,
      isAuthor,
      formatDate,
      isCommentAuthor,
      submitComment,
      deleteComment,
      editPost,
      deletePost,
      toggleLike,
      toggleDislike
    }
  }
}
</script>

<style scoped>
.post-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.loading, .error {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.error {
  color: #dc3545;
}

.post-article {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 2rem;
}

.post-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid #e1e8ed;
}

.post-header h1 {
  margin: 0 0 1rem;
  color: #2c3e50;
  font-size: 2rem;
}

.post-meta {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1rem;
  overflow: hidden;
}

.author-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-dates {
  display: flex;
  gap: 1.5rem;
}

.updated-time {
  color: #6c757d;
  font-style: italic;
}

.post-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  background-color: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}



.post-content {
  padding: 2rem;
  line-height: 1.8;
  color: #333;
}

.post-content :deep(h2),
.post-content :deep(h3),
.post-content :deep(h4) {
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.post-content :deep(p) {
  margin-bottom: 1rem;
}

.post-content :deep(pre) {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  margin: 1rem 0;
}

.post-footer {
  padding: 1rem 2rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #e1e8ed;
}

.post-actions {
  display: flex;
  gap: 0.5rem;
}

.post-stats {
  display: flex;
  gap: 1rem;
  color: #666;
  font-size: 0.9rem;
  align-items: center;
}

.like-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;
  font-size: 0.9rem;
}

.like-button:hover {
  background-color: #f8f9fa;
  border-color: #adb5bd;
}

.like-button.liked {
  background-color: #fff5f5;
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.like-button.liked:hover {
  background-color: #ffe3e3;
}

.like-button.loading {
  opacity: 0.6;
  cursor: not-allowed;
}

.like-icon {
  font-size: 1.1rem;
  transition: transform 0.3s ease;
}

.like-button:hover .like-icon {
  transform: scale(1.2);
}

.like-button.liked .like-icon {
  animation: heartbeat 0.6s ease;
}

.like-dislike-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.like-button, .dislike-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;
  font-size: 0.9rem;
}

.like-button:hover, .dislike-button:hover {
  background-color: #f8f9fa;
  border-color: #adb5bd;
}

.like-button.liked {
  background-color: #fff5f5;
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.like-button.liked:hover {
  background-color: #ffe3e3;
}

.dislike-button.disliked {
  background-color: #f0f0f0;
  border-color: #6c757d;
  color: #6c757d;
}

.dislike-button.disliked:hover {
  background-color: #e9ecef;
}

.like-button.loading, .dislike-button.loading {
  opacity: 0.6;
  cursor: not-allowed;
}

.like-icon, .dislike-icon {
  font-size: 1.1rem;
  transition: transform 0.3s ease;
}

.like-button:hover .like-icon, .dislike-button:hover .dislike-icon {
  transform: scale(1.2);
}

.like-button.liked .like-icon {
  animation: heartbeat 0.6s ease;
}

@keyframes heartbeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background-color: #42b983;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-text {
  background: none;
  padding: 4px 8px;
}

.btn-text.btn-danger {
  color: #dc3545;
}

.comments-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.comments-section h2 {
  margin-top: 0;
  color: #2c3e50;
}

.comment-form {
  margin-bottom: 2rem;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.comment-form h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.comment-form h3::before {
  content: "💬";
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  font-size: 1rem;
  line-height: 1.5;
  transition: all 0.3s ease;
  min-height: 120px;
}

.form-group textarea:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.1);
}

.form-group textarea::placeholder {
  color: #6c757d;
}

.login-prompt {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  margin-bottom: 2rem;
  border: 1px solid #dee2e6;
}

.login-prompt p {
  margin: 0;
  font-size: 1.1rem;
  color: #495057;
}

.login-prompt a {
  color: #42b983;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.login-prompt a:hover {
  color: #369870;
  text-decoration: underline;
}

.empty-comments {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comment {
  padding: 1.5rem;
  border: 1px solid #e1e8ed;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.comment:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.comment-author-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1rem;
  overflow: hidden;
}

.comment-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.comment-author {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1rem;
}

.comment-date {
  color: #6c757d;
  font-size: 0.85rem;
  background: #f8f9fa;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
}

.comment-content {
  line-height: 1.6;
  color: #333;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #42b983;
}

.comment-actions {
  text-align: right;
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .post-header {
    padding: 1.5rem 1.5rem 1rem;
  }
  
  .post-header h1 {
    font-size: 1.5rem;
  }
  
  .post-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .post-dates {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .post-content {
    padding: 1.5rem;
  }
  
  .post-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .comments-section {
    padding: 1.5rem;
  }
}
</style>