import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/resume',
      name: 'resume',
      component: () => import('../views/ResumeView.vue')
    },
    {
      path: '/self-intro',
      name: 'selfIntro',
      component: () => import('../views/SelfIntroView.vue')
    },
    {
      path: '/question-bank',
      name: 'questionBank',
      component: () => import('../views/QuestionBankView.vue')
    },
    {
      path: '/mock-interview',
      name: 'mockInterview',
      component: () => import('../views/MockInterviewView.vue')
    },
    {
      path: '/strategy',
      name: 'strategy',
      component: () => import('../views/StrategyView.vue')
    }
  ]
  
})

// 路由守卫：只有首页不需要登录，其他所有页面都需要登录
router.beforeEach((to, from, next) => {
  // 检查是否已登录
  const isLoggedIn = typeof localStorage !== 'undefined' && !!localStorage.getItem('token')
  
  // 登录页面不需要认证
  if (to.name === 'login') {
    if (isLoggedIn) {
      // 已登录，跳转到首页
      next({ name: 'home' })
      return
    }
    next()
    return
  }
  
  // 首页不需要登录
  if (to.name === 'home') {
    next()
    return
  }
  
  // 所有其他页面都需要登录
  if (!isLoggedIn) {
    if (typeof window !== 'undefined') {
      window.alert('请先登录')
    }
    next({ name: 'login' })
    return
  }
  
  // 检查是否需要上传简历（仅针对部分页面）
  const requiresResume = new Set(['selfIntro', 'questionBank', 'mockInterview', 'strategy'])
  if (requiresResume.has(to.name)) {
    let hasResume = false
    try {
      hasResume = typeof localStorage !== 'undefined' && !!localStorage.getItem('resumeId')
    } catch (_) {
      hasResume = false
    }
    if (!hasResume) {
      if (typeof window !== 'undefined') {
        window.alert('请先上传简历')
      }
      next({ name: 'resume' })
      return
    }
  }
  
  next()
})

export default router
