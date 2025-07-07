import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/account'
// 임포트가 너무 많아서 화살표 방식으로 임포트 수정했음! 
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Start',
      component: () => import('@/views/StartPageView.vue'),
    },
    {
      path: '/main',
      name: 'main',
      component: () => import('@/views/MainPageView.vue'),
    },
    {
      path: '/books/book_list',
      name: 'BookList',
      component: () => import('@/views/BookListView.vue'),
    },
    {
      path: '/books/book_detail/:id',
      name: 'BookDetail',
      component: () => import('@/components/BookDetail.vue'),
    },
    {
      path: '/books/bookcard',
      name: 'BookCard',
      component: () => import('@/components/BookCard.vue'),
    },
    {
      path: '/books/cardgame',
      name: 'CardGame',
      component: () => import('@/components/CardGame.vue'),
    },
    {
      path: '/books/search_book/',
      name: 'BookSearch',
      component: () => import('@/views/BookSearch.vue'),
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: () => import('@/views/SignUpView.vue'),
    },
    {
      path: '/login',
      name: 'LogInView',
      component: () => import('@/views/LogInView.vue'),
    },
    {
      path: '/accounts/password/change',
      name: 'ChangePassword',
      component: () => import('@/components/ChangePassword.vue'),
    },
    {
      path: '/accounts/user',
      name: 'MyPageView',
      component: () => import('@/views/MypageView.vue'),
    },
    {
      path: '/accounts/user_profile/:id',
      name: 'UserDetail',
      component: () => import('@/components/UserDetail.vue'),
    },
    {
      path: '/community',
      children: [
        {
          path: '',
          name: 'CommunityView',
          component: () => import('@/views/CommunityView.vue'),
        },
        {
          path: 'detail/:id',
          name: 'ThreadDetail',
          component: () => import('@/components/ThreadDetail.vue'),
          children: [
            {
              path: 'comment/:commentId',
              name: 'CommentDetail',
              component: () => import('@/components/CommentDetail.vue'),
            },
          ],
        },
        {
          path: 'create_thread/:id',
          name: 'CreateThread',
          component: () => import('@/views/CreateThread.vue'),
        },
       
      ],
    },
    {
      path: '/activity/aks_gpt',
      name: 'AskGptView',
      component: () => import('@/views/AskGptView.vue'),
    },
    {
      path: '/activity/quize_gpt',
      name: 'QuizGptView',
      component: () => import('@/views/QuizGptView.vue'),
    },
    {
      path: '/activity/debate_gpt',
      name: 'DebateGptView',
      component: () => import('@/views/DebateGptView.vue'),
    },
  ],
})

router.beforeEach((to) => {
  const store = useAccountStore()
  console.log('isLogIned:', store.isLogIned, 'to:', to.name)
  if (!store.isLogIned && to.name !== 'main' && to.name !== 'SignUpView' && to.name !== 'LogInView' && to.name !== 'Start') {
    return { name: 'LogInView' }
  }
  if (store.isLogIned && (to.name === 'SignUpView' || to.name === 'LogInView')) {
    return { name: 'main' }
  }
})

export default router
