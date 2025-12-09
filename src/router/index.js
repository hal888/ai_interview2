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

export default router