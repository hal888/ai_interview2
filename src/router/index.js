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
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/forgot-password',
      name: 'forgotPassword',
      component: () => import('../views/ForgotPasswordView.vue')
    },
    {
      path: '/reset-password',
      name: 'resetPassword',
      component: () => import('../views/ResetPasswordView.vue')
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

// 路由守卫：公共页面直接放行，保护页面由组件自己处理登录检查
router.beforeEach((to, from, next) => {
  next()
})

export default router
