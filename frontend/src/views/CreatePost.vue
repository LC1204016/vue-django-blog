<template>
  <div class="create-post">
    <div class="create-post-container">
      <h1>发布文章</h1>
      
      <form @submit.prevent="handleSubmit" class="post-form">
        <div class="form-group">
          <label for="title">文章标题 *</label>
          <input 
            id="title"
            v-model="form.title" 
            type="text" 
            placeholder="请输入文章标题"
            required
            maxlength="200"
          />
          <small class="form-help">{{ form.title.length }}/200</small>
        </div>
        
        
        
        <div class="form-group">
          <label for="category">分类 *</label>
          <select id="category" v-model="form.category" required>
            <option value="">请选择分类</option>
            <option v-for="category in categories" :key="category.id" :value="category.name">
              {{ category.name }}
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
              <span v-for="tag in form.tags" :key="tag.tag_id" class="tag">
                {{ tag.tag }}
                <button type="button" @click="removeTag(tag.tag_id)" class="tag-remove">×</button>
              </span>
            </div>
          </div>
        </div>
        
        <div class="form-group">
          <label for="content">文章内容 *</label>
          <div class="editor-tabs">
            <button 
              type="button" 
              :class="['tab-btn', { active: editorMode === 'write' }]"
              @click="editorMode = 'write'"
            >
              写作
            </button>
            <button 
              type="button" 
              :class="['tab-btn', { active: editorMode === 'preview' }]"
              @click="editorMode = 'preview'"
            >
              预览
            </button>
          </div>
          
          <div v-if="editorMode === 'write'" class="editor-write">
            <textarea 
              id="content"
              v-model="form.content" 
              placeholder="请输入文章内容，支持Markdown格式"
              required
              rows="15"
            ></textarea>
            <div class="editor-toolbar">
              <small>支持Markdown语法</small>
            </div>
          </div>
          
          <div v-else class="editor-preview">
            <div class="preview-content" v-html="previewContent"></div>
          </div>
        </div>
        
        <div class="form-actions">
          <button 
            type="button" 
            @click="saveDraft" 
            class="btn btn-secondary"
            :disabled="loading"
          >
            保存草稿
          </button>
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="loading || !formValid"
          >
            {{ loading ? '发布中...' : '发布文章' }}
          </button>
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
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '../services/api'

export default {
  name: 'CreatePost',
  setup() {
    const router = useRouter()
    
    const form = ref({
      title: '',
      content: '',
      category: '',
      tags: [],
      tag_ids: []
    })
    
    const tagsInput = ref('')
    const editorMode = ref('write')
    const loading = ref(false)
    const success = ref('')
    const error = ref('')
    const categories = ref([])
    const availableTags = ref([])
    
    const formValid = computed(() => {
      return form.value.title.trim() &&
             form.value.content.trim() &&
             form.value.category
    })
    
    const previewContent = computed(() => {
      // 简单的Markdown预览（实际项目中应该使用专业的Markdown解析库）
      return form.value.content
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*)\*/gim, '<em>$1</em>')
        .replace(/!\[([^\]]*)\]\(([^)]*)\)/gim, '<img src="$2" alt="$1" />')
        .replace(/\[([^\]]*)\]\(([^)]*)\)/gim, '<a href="$2">$1</a>')
        .replace(/\n/gim, '<br>')
    })
    
    // 监听标签输入
    watch(tagsInput, (newValue) => {
      const tags = newValue
        .split(',')
        .map(tag => tag.trim())
        .filter(tag => tag.length > 0)
      form.value.tags = tags
    })
    
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

    const fetchCategories = async () => {
      try {
        const data = await apiService.getCategories()
        categories.value = data
      } catch (error) {
        console.error('获取分类失败:', error)
      }
    }

    const fetchTags = async () => {
      try {
        const response = await apiService.getTags()
        availableTags.value = response.tags || []
      } catch (error) {
        console.error('获取标签失败:', error)
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

    // 监听分类变化
    watch(() => form.value.category, (newCategory) => {
      // 清空已选择的标签
      form.value.tags = []
      form.value.tag_ids = []
      
      // 获取新分类的标签
      fetchTagsByCategory(newCategory)
    })

    onMounted(() => {
      fetchCategories()
      // 不在初始化时获取所有标签，而是等待用户选择分类
    })
    
    const handleSubmit = async () => {
      if (!formValid.value) return
      
      try {
        loading.value = true
        error.value = ''
        success.value = ''
        
        const postData = {
          title: form.value.title,
          content: form.value.content,
          category: form.value.category,
          tag_ids: form.value.tag_ids,  // 添加标签ID列表
          status: 'published'
        }
        
        const response = await apiService.createPost(postData)
        success.value = '文章发布成功！'
        
        // 获取文章ID并跳转到文章详情页
        const postId = response.article?.id || response.id
        if (postId) {
          setTimeout(() => {
            router.push(`/posts/${postId}`)
          }, 1000)
        } else {
          error.value = '发布成功但无法获取文章ID，请手动查看文章列表'
        }
        
      } catch (err) {
        error.value = err.message || '发布失败，请重试'
      } finally {
        loading.value = false
      }
    }
    
    const saveDraft = async () => {
      try {
        loading.value = true
        error.value = ''
        
        const draftData = {
          title: form.value.title,
          content: form.value.content,
          category: form.value.category,
          tag_ids: form.value.tag_ids,  // 添加标签ID列表
          status: 'draft'
        }
        
        const response = await apiService.createPost(draftData)
        success.value = '草稿保存成功！'
        
        // 获取文章ID，如果成功保存也提供跳转选项
        const postId = response.article?.id || response.id
        if (postId) {
          setTimeout(() => {
            if (confirm('草稿保存成功！是否查看文章详情？')) {
              router.push(`/posts/${postId}`)
            } else {
              success.value = ''
            }
          }, 1000)
        } else {
          setTimeout(() => {
            success.value = ''
          }, 3000)
        }
        
      } catch (err) {
        error.value = err.message || '保存草稿失败，请重试'
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      tagsInput,
      editorMode,
      loading,
      success,
      error,
      categories,
      availableTags,
      formValid,
      previewContent,
      isTagSelected,
      toggleTag,
      removeTag,
      handleSubmit,
      saveDraft
    }
  }
}
</script>

<style scoped>
.create-post {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 20px;
}

.create-post-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 2.5rem;
}

.create-post-container h1 {
  margin: 0 0 2rem;
  color: #2c3e50;
  text-align: center;
}

.post-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  font-family: inherit;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #42b983;
}

.form-help {
  margin-top: 0.25rem;
  color: #666;
  font-size: 12px;
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

.editor-tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 0;
}

.tab-btn {
  background: none;
  border: none;
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.tab-btn.active {
  color: #42b983;
  border-bottom-color: #42b983;
}

.editor-write textarea {
  min-height: 300px;
  resize: vertical;
}

.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.editor-preview {
  min-height: 300px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 0 0 6px 6px;
  background-color: #f8f9fa;
}

.preview-content {
  line-height: 1.6;
  color: #333;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn {
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #42b983;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #369870;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #5a6268;
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
  .create-post {
    padding: 1rem 10px;
  }
  
  .create-post-container {
    padding: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>