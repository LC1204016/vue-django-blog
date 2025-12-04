<template>
  <header class="header">
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-name">Vue博客</span>
        </router-link>
      </div>
      
      <div class="nav-menu" :class="{ active: menuOpen }">
        <router-link to="/" class="nav-link" @click="closeMenu">首页</router-link>
        <router-link to="/posts" class="nav-link" @click="closeMenu">文章</router-link>
        
        <div v-if="isLoggedIn" class="auth-logged-in">
          <router-link to="/posts/create" class="nav-link create-btn" @click="closeMenu">
            发布文章
          </router-link>
          <div class="user-menu">
          <div class="dropdown" @click="toggleDropdown">
            <button class="dropdown-toggle">
              <div class="user-avatar">
                <img v-if="currentUser?.profile_pic" :src="currentUser.profile_pic.startsWith('http') ? currentUser.profile_pic : `http://localhost:8000${currentUser.profile_pic}`" :alt="currentUser.username" />
                <span v-else class="avatar-placeholder">{{ currentUser?.username?.charAt(0)?.toUpperCase() || 'U' }}</span>
              </div>
              {{ currentUser?.username || '用户' }}
              <span class="dropdown-arrow">▼</span>
            </button>
            <div class="dropdown-menu" :class="{ show: dropdownOpen }">
              <router-link to="/profile" class="dropdown-item" @click="closeMenus">
                个人中心
              </router-link>
              <button @click="handleLogout" class="dropdown-item logout-btn">
                退出登录
              </button>
            </div>
          </div>
          </div>
        </div>
        
        <div v-else class="auth-menu">
          <router-link to="/login" class="nav-link login-btn" @click="closeMenu">
            登录
          </router-link>
          <router-link to="/register" class="nav-link register-btn" @click="closeMenu">
            注册
          </router-link>
        </div>
      </div>
      
      <button class="mobile-menu-toggle" @click="toggleMenu">
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </button>
    </nav>
  </header>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Header',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const menuOpen = ref(false)
    const dropdownOpen = ref(false)

    const isLoggedIn = computed(() => authStore.isLoggedIn)
    const currentUser = computed(() => authStore.currentUser)

    const toggleMenu = () => {
      menuOpen.value = !menuOpen.value
      if (menuOpen.value) {
        dropdownOpen.value = false
      }
    }

    const closeMenu = () => {
      menuOpen.value = false
    }

    const toggleDropdown = (event) => {
      event.stopPropagation()
      dropdownOpen.value = !dropdownOpen.value
    }

    const closeDropdown = () => {
      dropdownOpen.value = false
    }

    const closeMenus = () => {
      closeMenu()
      closeDropdown()
    }

    const handleLogout = () => {
      authStore.logout()
      closeMenus()
      router.push('/login')
    }

    // 点击外部关闭下拉菜单
    const handleClickOutside = (event) => {
      if (!event.target.closest('.dropdown')) {
        closeDropdown()
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      menuOpen,
      dropdownOpen,
      isLoggedIn,
      currentUser,
      toggleMenu,
      closeMenu,
      toggleDropdown,
      closeMenus,
      handleLogout
    }
  }
}
</script>

<style scoped>
.header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.nav-brand {
  flex-shrink: 0;
}

.brand-link {
  text-decoration: none;
  color: #42b983;
  font-weight: bold;
  font-size: 1.5rem;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #2c3e50;
  font-weight: 500;
  padding: 0.5rem 0;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #42b983;
  border-bottom-color: #42b983;
}

.user-menu {
  position: relative;
}

.dropdown {
  position: relative;
}

.dropdown-toggle {
  background: none;
  border: none;
  color: #2c3e50;
  font-weight: 500;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border: 2px solid #e9ecef;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #42b983;
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.dropdown-toggle:hover {
  background-color: #f8f9fa;
}

.dropdown-arrow {
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border: 1px solid #e1e8ed;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 150px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  z-index: 1000;
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  display: block;
  padding: 0.75rem 1rem;
  color: #2c3e50;
  text-decoration: none;
  border-bottom: 1px solid #f8f9fa;
  transition: background-color 0.3s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.logout-btn {
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  color: #dc3545;
}

.logout-btn:hover {
  background-color: #f8d7da;
}

.auth-menu {
  display: flex;
  gap: 1rem;
}

.login-btn {
  color: #42b983 !important;
}

.register-btn {
  background-color: #42b983;
  color: white !important;
  padding: 0.5rem 1rem;
  border-radius: 6px;
}

.register-btn:hover {
  background-color: #369870;
  border-bottom-color: transparent;
}

.auth-logged-in {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.create-btn {
  background-color: #42b983 !important;
  color: white !important;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border-bottom-color: transparent !important;
}

.create-btn:hover {
  background-color: #369870 !important;
  border-bottom-color: transparent !important;
}

.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.hamburger-line {
  width: 25px;
  height: 3px;
  background-color: #2c3e50;
  margin: 2px 0;
  transition: all 0.3s ease;
}

@media (max-width: 768px) {
  .navbar {
    padding: 0 15px;
  }
  
  .mobile-menu-toggle {
    display: flex;
  }
  
  .nav-menu {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    background-color: white;
    flex-direction: column;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    gap: 1rem;
  }
  
  .nav-menu.active {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }
  
  .nav-link {
    padding: 0.75rem 0;
    border-bottom: 1px solid #f8f9fa;
    width: 100%;
  }
  
  .nav-link:last-child {
    border-bottom: none;
  }
  
  .auth-menu {
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
  }
  
  .login-btn,
  .register-btn {
    text-align: center;
    padding: 0.75rem 0;
    width: 100%;
  }
  
  .dropdown-menu {
    position: static;
    box-shadow: none;
    border: 1px solid #e1e8ed;
    margin-top: 0.5rem;
    opacity: 1;
    visibility: visible;
    transform: none;
    display: none;
  }
  
  .dropdown-menu.show {
    display: block;
  }
}
</style>