<script setup>
// App.vue - Main application component with navigation
import { ref, onMounted, onUnmounted, computed } from 'vue'

// 导航栏显示状态
const navbarVisible = ref(true)
// 上次滚动位置
const lastScrollY = ref(0)
// 滚动阈值，避免微小滚动触发
const scrollThreshold = 10
// 距离顶部阈值
const topThreshold = 50
// 防抖动计时器
let debounceTimer = null
// 移动设备宽度阈值
const mobileThreshold = 768
// 窗口宽度
const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)

// 计算是否为移动设备视图
const isMobileView = computed(() => {
  return windowWidth.value < mobileThreshold
})

// 滚动事件处理函数
const handleScroll = () => {
  const currentScrollY = typeof window !== 'undefined' ? window.scrollY || 0 : 0
  const scrollDifference = Math.abs(currentScrollY - lastScrollY.value)
  
  // 如果滚动距离小于阈值，不触发状态变化
  if (scrollDifference < scrollThreshold) {
    return
  }
  
  // 清除之前的计时器
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  // 防抖动处理，避免快速连续滚动
  debounceTimer = setTimeout(() => {
    // 页面已处于顶部位置，保持显示
    if (currentScrollY <= topThreshold) {
      navbarVisible.value = true
    } else {
      // 向下滚动时隐藏，向上滚动时显示
      navbarVisible.value = currentScrollY < lastScrollY.value
    }
    
    // 更新上次滚动位置
    lastScrollY.value = currentScrollY
  }, 50)
}

// 窗口大小变化事件处理
const handleResize = () => {
  windowWidth.value = typeof window !== 'undefined' ? window.innerWidth : windowWidth.value
}

// 计算用户是否已登录
const isUserLoggedIn = computed(() => {
  return !!localStorage.getItem('token') || !!sessionStorage.getItem('token')
})

// 组件挂载时添加事件监听
onMounted(() => {
  // 确保页面加载时导航栏显示
  navbarVisible.value = true
  lastScrollY.value = typeof window !== 'undefined' ? window.scrollY || 0 : 0
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', handleResize)
})

// 退出登录处理
const handleLogout = () => {
  // 清除本地存储的令牌和用户信息
  localStorage.removeItem('token')
  localStorage.removeItem('userId')
  localStorage.removeItem('email')
  localStorage.removeItem('resumeId')
  
  // 清除会话存储的令牌和用户信息
  sessionStorage.removeItem('token')
  sessionStorage.removeItem('userId')
  sessionStorage.removeItem('email')
  
  // 跳转到登录页
  window.location.href = '/login'
}

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', handleResize)
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
})
</script>

<template>
  <div class="app-container">
    <!-- Desktop Navigation Bar -->
    <nav class="navbar desktop-navbar" :class="{ 
      'navbar-hidden': !navbarVisible && lastScrollY > topThreshold 
    }">
      <div class="navbar-container">
        <div class="navbar-header">
          <div class="navbar-brand">
            <router-link to="/" class="brand-link">
              <img src="/logo.svg" alt="AI智能面试宝典" class="brand-icon" />
              <span class="brand-name">AI智能面试宝典</span>
            </router-link>
          </div>
        </div>
        
        <div class="navbar-menu">
          <router-link to="/" class="nav-link" exact-active-class="active">首页</router-link>
          <router-link to="/resume" class="nav-link" exact-active-class="active">简历优化</router-link>
          <router-link to="/self-intro" class="nav-link" exact-active-class="active">自我介绍</router-link>
          <router-link to="/question-bank" class="nav-link" exact-active-class="active">智能题库</router-link>
          <router-link to="/mock-interview" class="nav-link" exact-active-class="active">模拟面试</router-link>
          <router-link to="/strategy" class="nav-link" exact-active-class="active">面试策略</router-link>
          <template v-if="isUserLoggedIn">
            <button class="nav-link logout-btn" @click="handleLogout">退出登录</button>
          </template>
          <!-- <template v-else>
            <router-link to="/login" class="nav-link login-btn" exact-active-class="active">登录</router-link>
            <router-link to="/register" class="nav-link register-btn" exact-active-class="active">注册</router-link>
          </template> -->
        </div>
      </div>
    </nav>

    <!-- Mobile Top Brand -->
    <div class="mobile-top-brand">
      <div class="brand-content">
        <router-link to="/" class="brand-link">
          <img src="/logo.svg" alt="AI智能面试宝典" class="brand-icon" />
          <span class="brand-name">AI智能面试宝典</span>
        </router-link>
      </div>
    </div>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>

    <nav class="mobile-navbar">
      <div class="mobile-nav-container">
        <router-link to="/" class="nav-link" exact-active-class="active">首页</router-link>
        <router-link to="/resume" class="nav-link" exact-active-class="active">简历优化</router-link>
        <router-link to="/self-intro" class="nav-link" exact-active-class="active">自我介绍</router-link>
        <router-link to="/question-bank" class="nav-link" exact-active-class="active">智能题库</router-link>
        <router-link to="/mock-interview" class="nav-link" exact-active-class="active">模拟面试</router-link>
        <router-link to="/strategy" class="nav-link" exact-active-class="active">面试策略</router-link>
        <template v-if="isUserLoggedIn">
          <button class="nav-link logout-btn" @click="handleLogout">退出登录</button>
        </template>
        <!-- <template v-else>
          <router-link to="/login" class="nav-link login-btn" exact-active-class="active">登录</router-link>
          <router-link to="/register" class="nav-link register-btn" exact-active-class="active">注册</router-link>
        </template> -->
      </div>
    </nav>
  </div>
</template>

<style scoped>
/* App Container */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Navigation Bar - 全局一致样式 */
.navbar {
  background-color: var(--color-bg) !important;
  box-shadow: 0 2px 20px rgba(102, 126, 234, 0.15) !important;
  position: sticky !important;
  top: 0 !important;
  z-index: 1000 !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  transition: all 0.3s ease !important;
  transform: translateY(0);
  backdrop-filter: blur(15px) saturate(110%);
  background-color: rgba(255, 255, 255, 0.98) !important;
  /* 确保导航栏层级正确 */
  will-change: transform;
  overflow: visible !important;
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

/* 导航栏隐藏状态 */
.navbar.navbar-hidden {
  transform: translateY(-100%);
}

/* 导航栏容器 */
.navbar-container {
  max-width: var(--content-max) !important;
  margin: 0 auto !important;
  padding: 0 25px !important;
  display: flex !important;
  flex-direction: column !important;
  background-color: transparent !important;
  box-sizing: border-box !important;
  transition: all 0.3s ease !important;
  width: 100% !important;
}

/* 导航栏头部 - 包含品牌和切换按钮 */
.navbar-header {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  padding: 15px 0 !important;
  background-color: transparent !important;
}

/* 移动端折叠按钮 */
.navbar-toggle {
  background: none !important;
  border: none !important;
  cursor: pointer !important;
  padding: 8px !important;
  font-size: 1.5rem !important;
  color: var(--color-primary) !important;
  transition: all 0.3s ease !important;
  display: none !important;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex !important;
  align-items: center;
  justify-content: center;
}

/* 折叠按钮图标 */
.navbar-toggle-icon {
  display: block !important;
  background-color: transparent !important;
}

/* 折叠按钮悬停效果 */
.navbar-toggle:hover {
  background-color: rgba(102, 126, 234, 0.1);
  transform: rotate(90deg);
}

/* 导航菜单 */
.navbar-menu {
  display: flex !important;
  gap: 30px !important;
  align-items: center !important;
  background-color: transparent !important;
  transition: all 0.3s ease !important;
  flex: 1 !important;
  justify-content: center !important;
  max-height: 500px !important;
  flex-wrap: nowrap !important;
  overflow: visible !important;
}

/* 折叠状态下的菜单 */
.navbar-collapsed .navbar-menu {
  max-height: 0 !important;
  opacity: 0 !important;
  visibility: hidden !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* 展开状态下的菜单 */
.menu-expanded {
  max-height: 500px !important;
  opacity: 1 !important;
  visibility: visible !important;
  padding: 10px 0 !important;
}

/* 桌面端导航样式 */
.desktop-navbar {
  display: block;
}

/* 移动端顶部品牌 */
.mobile-top-brand {
  display: none;
  background-color: rgba(255, 255, 255, 0.98);
  box-shadow: 0 2px 20px rgba(102, 126, 234, 0.15);
  padding: 15px 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
  padding-top: env(safe-area-inset-top);
  backdrop-filter: blur(15px) saturate(110%);
  border-bottom: 1px solid rgba(102, 126, 234, 0.1);
}

/* 品牌内容容器 */
.brand-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

/* 移动端底部导航在桌面端默认隐藏 */
.mobile-navbar {
  display: none;
}

/* 确保在桌面端不应用隐藏效果 */
@media (min-width: 769px) {
  .navbar.navbar-hidden {
    transform: translateY(0);
  }
  
  .navbar-container {
    flex-direction: row !important;
    align-items: center !important;
    flex-wrap: nowrap !important;
    justify-content: space-between !important;
  }
  
  .navbar-header {
    flex: 0 0 auto !important;
  }
  
  .navbar-menu {
    flex: 1 !important;
    flex-wrap: nowrap !important;
    justify-content: flex-end !important;
    gap: 20px !important;
    overflow: visible !important;
  }
  
  .navbar-toggle {
    display: none !important;
  }
  /* 桌面端隐藏底部导航栏 */
  .mobile-navbar {
    display: none !important;
  }
}

/* 移动端样式 */
@media (max-width: 768px) {
  /* 隐藏桌面端导航 */
  .desktop-navbar {
    display: none;
  }
  
  /* 显示移动端顶部品牌 */
  .mobile-top-brand {
    display: block;
  }
  
  /* 移除移动端底部导航样式 */
  .mobile-navbar {
    display: block;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: var(--color-bg);
    box-shadow: 0 -2px 10px var(--color-shadow);
    z-index: 1000;
    padding: 10px 0;
    padding-bottom: env(safe-area-inset-bottom);
  }
  
  /* 移动端导航容器 */
  .mobile-nav-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    max-width: var(--content-max);
    margin: 0 auto;
    padding: 0 5px;
    gap: 5px;
  }
  
  /* 移动端导航链接 */
  .mobile-navbar .nav-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    padding: 12px 8px;
    text-align: center;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    min-width: 0;
    border: none !important;
    gap: 6px;
    color: var(--color-text-secondary) !important;
    transition: all 0.3s ease !important;
    border-radius: 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    background-color: transparent;
    position: relative;
  }
  
  /* 移动端导航链接悬停效果 */
  .mobile-navbar .nav-link:hover {
    background-color: rgba(102, 126, 234, 0.08) !important;
    color: var(--color-primary) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15) !important;
  }
  
  /* 移动端导航链接激活状态 */
  .mobile-navbar .nav-link.active {
    color: var(--color-primary) !important;
    font-weight: 600 !important;
    background-color: rgba(102, 126, 234, 0.1) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15) !important;
  }
  
  /* 移除旧的下划线样式 */
  .mobile-navbar .nav-link.active::after {
    content: none !important;
  }
  
  /* 移动端导航链接顶部装饰条 */
  .mobile-navbar .nav-link::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 0 !important;
    height: 3px !important;
    background-color: var(--color-primary) !important;
    border-radius: 3px !important;
    transition: all 0.3s ease !important;
  }
  
  /* 移动端导航链接悬停和激活状态的顶部装饰条 */
  .mobile-navbar .nav-link:hover::before,
  .mobile-navbar .nav-link.active::before {
    width: 60% !important;
  }
  
  /* 调整主内容区，避免被底部导航遮挡 */
  .main-content {
    padding-bottom: 85px;
  }
  
  /* 调整移动端footer */
  .footer {
    margin-bottom: 65px;
  }
  
  /* 小屏幕手机优化 */
  @media (max-width: 375px) {
    .mobile-navbar .nav-link {
      font-size: 0.75rem !important;
      padding: 8px 2px;
    }
    
    .mobile-navbar {
      padding: 8px 0;
    }
  }
}

.navbar-brand {
  display: flex !important;
  align-items: center !important;
  background-color: transparent !important;
  flex-shrink: 0;
}

.brand-link {
  display: flex !important;
  align-items: center !important;
  gap: 15px !important;
  text-decoration: none !important;
  color: var(--color-text) !important;
  font-weight: bold !important;
  background-color: transparent !important;
  flex-shrink: 0;
  transition: all 0.3s ease !important;
  padding: 8px 12px !important;
  border-radius: 12px !important;
  position: relative;
  overflow: hidden;
}

.brand-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.brand-link:hover {
  color: var(--color-primary) !important;
  text-decoration: none !important;
  background-color: transparent !important;
  transform: translateY(-2px) scale(1.02) !important;
}

.brand-link:hover::before {
  opacity: 1;
}

.brand-link:hover .brand-name {
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-link:hover .brand-icon {
  transform: scale(1.1) rotate(5deg);
}

.brand-icon {
  width: 40px !important;
  height: 40px !important;
  background-color: transparent !important;
  object-fit: contain;
  transition: all 0.3s ease !important;
  position: relative;
  z-index: 1;
}

.brand-name {
  font-size: 1.5rem !important;
  color: var(--color-primary) !important;
  background-color: transparent !important;
  white-space: nowrap;
  overflow: visible;
  text-overflow: clip;
  max-width: none;
  flex-shrink: 0;
  font-weight: 700 !important;
  transition: all 0.3s ease !important;
  position: relative;
  z-index: 1;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 4px rgba(102, 126, 234, 0.1);
}

.navbar-menu {
  display: flex !important;
  gap: 30px !important;
  align-items: center !important;
  background-color: transparent !important;
  flex-wrap: nowrap;
  justify-content: flex-end;
}

.nav-link {
  text-decoration: none !important;
  color: var(--color-text-secondary) !important;
  font-weight: 500 !important;
  font-size: 1rem !important;
  transition: all 0.3s ease !important;
  position: relative !important;
  background-color: transparent !important;
  display: inline-block;
  padding: 12px 16px !important;
  min-width: 90px;
  text-align: center;
  border-radius: 8px;
  border: 2px solid transparent;
}

.nav-link:hover {
  color: var(--color-primary) !important;
  text-decoration: none !important;
  background-color: rgba(102, 126, 234, 0.08) !important;
  border-color: rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.nav-link.active {
  color: var(--color-primary) !important;
  background-color: rgba(102, 126, 234, 0.1) !important;
  border-color: var(--color-primary);
  font-weight: 600 !important;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
}

/* 移除旧的下划线样式，使用边框和背景色替代 */
.nav-link.active::after {
  content: none !important;
}

/* 为导航链接添加顶部装饰条作为视觉指示器 */
.nav-link::before {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  width: 0 !important;
  height: 3px !important;
  background-color: var(--color-primary) !important;
  border-radius: 3px !important;
  transition: all 0.3s ease !important;
}

.nav-link:hover::before,
.nav-link.active::before {
  width: 80% !important;
}

/* 登录、注册、退出按钮样式 */
.nav-link.login-btn {
  background-color: rgba(102, 126, 234, 0.1) !important;
  border-color: var(--color-primary) !important;
  color: var(--color-primary) !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.nav-link.login-btn:hover {
  background-color: rgba(102, 126, 234, 0.2) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
}

.nav-link.register-btn {
  background-color: var(--color-primary) !important;
  border-color: var(--color-primary) !important;
  color: white !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.nav-link.register-btn:hover {
  background-color: var(--color-secondary) !important;
  border-color: var(--color-secondary) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
}

.nav-link.logout-btn {
  background-color: rgba(231, 76, 60, 0.1) !important;
  border-color: #e74c3c !important;
  color: #e74c3c !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: all 0.3s ease !important;
}

.nav-link.logout-btn:hover {
  background-color: rgba(231, 76, 60, 0.2) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.2) !important;
}

/* 移除登录、注册、退出按钮的顶部装饰条 */
.nav-link.login-btn::before,
.nav-link.register-btn::before,
.nav-link.logout-btn::before {
  content: none !important;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 30px 20px;
  max-width: var(--content-max);
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}


/* Responsive Design */
/* 平板设备优化 */
@media (min-width: 769px) and (max-width: 1024px) {
  .navbar-container {
    padding: 0 15px !important;
    flex-wrap: nowrap !important;
  }
  
  .navbar-menu {
    gap: 15px !important;
    flex-wrap: nowrap !important;
    overflow: visible !important;
  }
  
  .nav-link {
    padding: 10px 12px !important;
    font-size: 0.9rem !important;
  }
  
  .main-content {
    padding: 25px 15px;
  }
}

/* 移动设备优化 */
@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    padding: 15px 10px !important;
    gap: 15px;
    align-items: stretch;
  }
  
  .navbar-brand {
    justify-content: center;
  }
  
  .brand-link {
    justify-content: center;
  }
  
  .brand-name {
    font-size: 1.3rem !important;
    max-width: none;
    overflow: visible;
    text-overflow: clip;
  }
  
  .brand-icon {
    font-size: 1.8rem !important;
  }
  
  .navbar-menu {
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px !important;
    padding: 10px 0;
  }
  
  .nav-link {
    font-size: 0.85rem;
    padding: 8px 12px;
    min-width: 70px;
    flex: 1;
    max-width: 120px;
  }
  
  .nav-link.active::after {
    bottom: -6px !important;
    height: 1.5px !important;
  }
  
  .main-content {
    padding: 20px 10px;
  }
}

/* 小屏幕手机优化 */
  @media (max-width: 375px) {
    .brand-name {
      font-size: 1.1rem !important;
      max-width: none;
      overflow: visible;
      text-overflow: clip;
    }
  
  .brand-icon {
    font-size: 1.5rem !important;
  }
  
  .navbar-menu {
    gap: 8px !important;
  }
  
  .nav-link {
    font-size: 0.8rem;
    padding: 6px 10px;
    min-width: 65px;
    max-width: 100px;
  }
  
  .brand-link {
    gap: 10px !important;
  }
}
</style>
