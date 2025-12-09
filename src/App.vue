<script setup>
// App.vue - Main application component with navigation
</script>

<template>
  <div class="app-container">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-container">
        <div class="navbar-brand">
          <router-link to="/" class="brand-link">
            <div class="brand-icon">🤖</div>
            <span class="brand-name">AI智能面试宝典</span>
          </router-link>
        </div>
        
        <div class="navbar-menu">
          <router-link to="/" class="nav-link" exact-active-class="active">首页</router-link>
          <router-link to="/resume" class="nav-link" exact-active-class="active">简历优化</router-link>
          <router-link to="/self-intro" class="nav-link" exact-active-class="active">自我介绍</router-link>
          <router-link to="/question-bank" class="nav-link" exact-active-class="active">智能题库</router-link>
          <router-link to="/mock-interview" class="nav-link" exact-active-class="active">模拟面试</router-link>
          <router-link to="/strategy" class="nav-link" exact-active-class="active">面试策略</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-container">
        <p>&copy; 2025 AI智能面试宝典. 保留所有权利.</p>
      </div>
    </footer>
  </div>
</template>

<style>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f5f7fa;
  color: #333;
  line-height: 1.6;
}

/* App Container */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Navigation Bar - 全局一致样式 */
.navbar {
  background-color: #ffffff !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
  position: sticky !important;
  top: 0 !important;
  z-index: 1000 !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
}

.navbar-container {
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 0 20px !important;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  height: 70px !important;
  background-color: transparent !important;
}

.navbar-brand {
  display: flex !important;
  align-items: center !important;
  background-color: transparent !important;
}

.brand-link {
  display: flex !important;
  align-items: center !important;
  gap: 15px !important;
  text-decoration: none !important;
  color: #333 !important;
  font-weight: bold !important;
  background-color: transparent !important;
}

.brand-link:hover {
  color: #333 !important;
  text-decoration: none !important;
  background-color: transparent !important;
}

.brand-icon {
  font-size: 2rem !important;
  background-color: transparent !important;
}

.brand-name {
  font-size: 1.5rem !important;
  color: #667eea !important;
  background-color: transparent !important;
}

.navbar-menu {
  display: flex !important;
  gap: 30px !important;
  align-items: center !important;
  background-color: transparent !important;
}

.nav-link {
  text-decoration: none !important;
  color: #333 !important;
  font-weight: 500 !important;
  font-size: 1rem !important;
  transition: color 0.3s ease !important;
  position: relative !important;
  background-color: transparent !important;
}

.nav-link:hover {
  color: #667eea !important;
  text-decoration: none !important;
  background-color: transparent !important;
}

.nav-link.active {
  color: #667eea !important;
  background-color: transparent !important;
}

.nav-link.active::after {
  content: '' !important;
  position: absolute !important;
  bottom: -8px !important;
  left: 0 !important;
  width: 100% !important;
  height: 2px !important;
  background-color: #667eea !important;
  border-radius: 2px !important;
  background-color: transparent !important;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 30px 20px;
}

/* Footer */
.footer {
  background-color: #333;
  color: white;
  padding: 20px;
  text-align: center;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    height: auto;
    padding: 15px 20px;
    gap: 15px;
  }
  
  .navbar-menu {
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
  }
  
  .nav-link {
    font-size: 0.9rem;
  }
  
  .main-content {
    padding: 20px 10px;
  }
}
</style>
