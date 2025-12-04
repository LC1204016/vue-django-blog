import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './stores'
import { useAuthStore } from './stores'
import './style.css'

const app = createApp(App)

app.use(router)
app.use(pinia)

// 初始化认证状态
const authStore = useAuthStore()
authStore.initAuth().catch(error => {
  console.error('认证初始化失败:', error)
})

app.mount('#app')