<template>
  <div class="edit-post">
    <div class="edit-post-header">
      <h1>编辑文章</h1>
      <p>修改您的文章内容</p>
    </div>

    <div v-if="loading" class="loading">
      加载中...
    </div>

    <div v-else class="edit-post-content">
      <form @submit.prevent="handleSubmit" class="post-form">
        <div class="form-group">
          <label for="title">标题</label>
          <input 
            id="title"
            v-model="form.title" 
            type="text" 
            required
            minlength="5"
            maxlength="30"
            placeholder="请输入文章标题（5-30个字符）"
          />
          <small>{{ form.title.length }}/30</small>
        </div>

        <div class="form-group">
          <label for="category">分类</label>
          <select 
            id="category"
            v-model="form.category" 
            required
          >
            <option value="">请选择分类</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>

        

        <div class="form-group">
          <label for="tags">标签</label>
          <div class="tags-container">
            <div class="available-tags">
              <div 
                v-for="tag in availableTags" 
                :key="tag.tag_id"
                :class="['tag-item', { selected: isTagSelected(tag.tag_id) }]"
                @click="toggleTag(tag)"
              >
                {{ tag.tag }}
              </div>
            </div>
            <small class="form-help">点击选择标签，可多选</small>
            <div v-if="form.tags.length > 0" class="selected-tags">
              <span>已选择的标签：</span>
              <span v-for="(tag, index) in form.tags" :key="`selected-${tag.tag_id}-${index}`" class="tag">
                {{ tag.tag }}
                <button type="button" @click="removeTag(tag.tag_id)" class="tag-remove">×</button>
              </span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="content">内容</label>
          <textarea 
            id="content"
            v-model="form.content" 
            rows="15"
            required
            minlength="5"
            placeholder="请输入文章内容（至少5个字符）"
          ></textarea>
          <small>{{ form.content.length }} 个字符</small>
        </div>

        <div class="form-actions">
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="submitting"
          >
            {{ submitting ? '保存中...' : '保存修改' }}
          </button>
          <router-link :to="`/posts/${postId}`" class="btn btn-text">
            取消
          </router-link>
        </div>
      </form>
    </div>

    <div v-if="success" class="success-message">
      {{ success }}
    </div>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiService } from '../services/api'

export default {
  name: 'EditPost',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const postId = route.params.id
    
    const loading = ref(true)
    const submitting = ref(false)
    const success = ref('')
    const error = ref('')
    const categories = ref([])
    
    const form = ref({
      title: '',
      category: '',
      content: '',
      tags: [],
      tag_ids: []
    })
    
    const availableTags = ref([])

    const fetchPost = async () => {
      try {
        const post = await apiService.getPostForEdit(postId)
        
        // 处理标签数据 - API返回的是标签名称数组，需要转换为对象数组
        const tagNames = post.tags || []
        const tags = tagNames.map(tagName => ({
          tag_id: null, // 暂时没有标签ID，如果需要可以后续添加
          tag: tagName
        }))
        
        form.value = {
          title: post.title,
          category: post.category,
          content: post.content,
          tags: tags,
          tag_ids: [] // 暂时为空数组
        }
      } catch (err) {
        error.value = err.response?.data?.errors || '获取文章失败'
        console.error('获取文章失败:', err)
      } finally {
        loading.value = false
      }
    }

    const fetchCategories = async () => {
      try {
        const response = await apiService.getCategories()
        categories.value = response.map(cat => cat.name)
        return response
      } catch (err) {
        console.error('获取分类失败:', err)
        return []
      }
    }

    const fetchTags = async () => {
      try {
        const response = await apiService.getTags()
        availableTags.value = response.tags || []
        return response.tags || []
      } catch (err) {
        console.error('获取标签失败:', err)
        return []
      }
    }

    const fetchTagsByCategory = async (categoryName) => {
      if (!categoryName) {
        availableTags.value = []
        return
      }
      
      try {
        const response = await apiService.getTagsByCategory(categoryName)
        availableTags.value = response.tags || []
      } catch (error) {
        console.error('获取分类标签失败:', error)
        availableTags.value = []
      }
    }

    const isTagSelected = (tagId) => {
      return form.value.tag_ids.includes(tagId)
    }

    const toggleTag = (tag) => {
      const index = form.value.tag_ids.indexOf(tag.tag_id)
      if (index === -1) {
        // 添加标签
        form.value.tag_ids.push(tag.tag_id)
        form.value.tags.push(tag)
      } else {
        // 移除标签
        form.value.tag_ids.splice(index, 1)
        form.value.tags = form.value.tags.filter(t => t.tag_id !== tag.tag_id)
      }
    }

    const removeTag = (tagId) => {
      const index = form.value.tag_ids.indexOf(tagId)
      if (index !== -1) {
        form.value.tag_ids.splice(index, 1)
        form.value.tags = form.value.tags.filter(t => t.tag_id !== tagId)
      }
    }

    const handleSubmit = async () => {
      try {
        submitting.value = true
        error.value = ''
        success.value = ''
        
        await apiService.updatePost(postId, form.value)
        success.value = '文章修改成功'
        
        setTimeout(() => {
          router.push(`/posts/${postId}`)
        }, 1500)
      } catch (err) {
        if (err.response?.data) {
          const errors = err.response.data
          if (typeof errors === 'string') {
            error.value = errors
          } else if (errors.errors) {
            error.value = errors.errors
          } else {
            // 处理字段级别的错误
            const errorMessages = []
            Object.keys(errors).forEach(key => {
              if (Array.isArray(errors[key])) {
                errorMessages.push(`${key}: ${errors[key].join(', ')}`)
              } else {
                errorMessages.push(`${key}: ${errors[key]}`)
              }
            })
            error.value = errorMessages.join('; ')
          }
        } else {
          error.value = '修改失败，请重试'
        }
        console.error('修改文章失败:', err)
      } finally {
        submitting.value = false
      }
    }

    // 监听分类变化
    watch(() => form.value.category, (newCategory) => {
      // 获取新分类的标签
      fetchTagsByCategory(newCategory)
    })

    onMounted(async () => {
      // 先获取分类数据，再获取文章数据
      await fetchCategories()
      await fetchPost()
      // 根据文章的分类获取对应的标签
      if (form.value.category) {
        await fetchTagsByCategory(form.value.category)
      }
    })

    return {
      postId,
      form,
      categories,
      availableTags,
      loading,
      submitting,
      success,
      error,
      isTagSelected,
      toggleTag,
      removeTag,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.edit-post {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.edit-post-header {
  text-align: center;
  margin-bottom: 2rem;
}

.edit-post-header h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.edit-post-header p {
  color: #666;
}

.loading {
  text-align: center;
  padding: 4rem;
  color: #666;
}

.edit-post-content {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-form {
  max-width: 100%;
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

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  font-family: inherit;
  resize: vertical;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #42b983;
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  color: #666;
  font-size: 12px;
  text-align: right;
}

.tags-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.available-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  max-height: 120px;
  overflow-y: auto;
  padding: 0.5rem;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  background-color: #f8f9fa;
}

.tag-item {
  background-color: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.tag-item:hover {
  background-color: #dee2e6;
  transform: translateY(-1px);
}

.tag-item.selected {
  background-color: #42b983;
  color: white;
  border-color: #369870;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  margin-top: 0.5rem;
}

.selected-tags span:first-child {
  color: #666;
  font-size: 0.9rem;
  margin-right: 0.5rem;
}

.tag {
  background-color: #42b983;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.tag-remove {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 12px;
  padding: 0;
  margin-left: 0.25rem;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tag-remove:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn {
  padding: 10px 20px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  font-size: 16px;
}

.btn-primary {
  background-color: #42b983;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #369870;
}

.btn-text {
  background: none;
  color: #666;
  border: 1px solid #ddd;
}

.btn-text:hover {
  background-color: #f8f9fa;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success-message,
.error-message {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 1rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  z-index: 1000;
  max-width: 300px;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

@media (max-width: 768px) {
  .edit-post {
    padding: 0 10px;
  }
  
  .edit-post-content {
    padding: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    text-align: center;
  }
}
</style>