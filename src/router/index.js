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

// 访问受限页面前检查是否已上传简历
const protectedRoutes = new Set(['selfIntro', 'questionBank', 'mockInterview', 'strategy'])
router.beforeEach((to, from, next) => {
  if (protectedRoutes.has(to.name)) {
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
