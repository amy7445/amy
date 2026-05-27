import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/pages/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/pages/Dashboard.vue'),
        meta: { title: '数据看板', roles: ['user', 'admin'] }
      },
      {
        path: 'detect/image',
        name: 'ImageDetect',
        component: () => import('@/pages/ImageDetect.vue'),
        meta: { title: '图片检测', roles: ['user', 'admin'] }
      },
      {
        path: 'detect/image/history',
        name: 'ImageDetectHistory',
        component: () => import('@/pages/ImageDetectHistory.vue'),
        meta: { title: '图片检测历史', roles: ['user', 'admin'] }
      },
      {
        path: 'detect/video',
        name: 'VideoDetect',
        component: () => import('@/pages/VideoDetect.vue'),
        meta: { title: '视频检测', roles: ['user', 'admin'] }
      },
      {
        path: 'detect/video/history',
        name: 'VideoDetectHistory',
        component: () => import('@/pages/VideoDetectHistory.vue'),
        meta: { title: '视频检测历史', roles: ['user', 'admin'] }
      },
      {
        path: 'detect/camera',
        name: 'CameraDetect',
        component: () => import('@/pages/CameraDetect.vue'),
        meta: { title: '实时摄像头', roles: ['user', 'admin'] }
      },
      {
        path: 'detect/camera/history',
        name: 'CameraDetectHistory',
        component: () => import('@/pages/CameraDetectHistory.vue'),
        meta: { title: '实时检测历史', roles: ['user', 'admin'] }
      },
      {
        path: 'predict',
        name: 'TrendPredict',
        component: () => import('@/pages/TrendPredict.vue'),
        meta: { title: '趋势预测', roles: ['user', 'admin'] }
      },
      {
        path: 'treatment',
        name: 'Treatment',
        component: () => import('@/pages/Treatment.vue'),
        meta: { title: '防治方案', roles: ['user', 'admin'] }
      },
      {
        path: 'evaluation',
        name: 'Evaluation',
        component: () => import('@/pages/Evaluation.vue'),
        meta: { title: '效果评估', roles: ['user', 'admin'] }
      },
      {
        path: 'compare',
        name: 'HistoryCompare',
        component: () => import('@/pages/HistoryCompare.vue'),
        meta: { title: '历史对比', roles: ['user', 'admin'] }
      },
      {
        path: 'knowledge',
        name: 'Knowledge',
        component: () => import('@/pages/Knowledge.vue'),
        meta: { title: '知识库', roles: ['user', 'admin'] }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/pages/Profile.vue'),
        meta: { title: '个人中心', roles: ['user'] }
      },
      {
        path: 'admin',
        name: 'Admin',
        component: () => import('@/pages/Admin.vue'),
        meta: { title: '系统概览', roles: ['admin'] }
      },
      {
        path: 'admin/users',
        name: 'AdminUsers',
        component: () => import('@/pages/Admin.vue'),
        meta: { title: '用户管理', roles: ['admin'] }
      },
      {
        path: 'admin/model',
        name: 'AdminModel',
        component: () => import('@/pages/Admin.vue'),
        meta: { title: '模型设置', roles: ['admin'] }
      },
      {
        path: 'admin/logs',
        name: 'AdminLogs',
        component: () => import('@/pages/Admin.vue'),
        meta: { title: '检测日志', roles: ['admin'] }
      },
      {
        path: 'admin/config',
        name: 'AdminConfig',
        component: () => import('@/pages/Admin.vue'),
        meta: { title: '系统设置', roles: ['admin'] }
      },
      {
        path: 'admin/announcements',
        name: 'AdminAnnouncements',
        component: () => import('@/pages/Admin.vue'),
        meta: { title: '公告管理', roles: ['admin'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const token = localStorage.getItem('token')
  
  console.log('[ROUTER] ==========================')
  console.log('[ROUTER] From:', _from.path, 'To:', to.path)
  console.log('[ROUTER] requiresAuth:', requiresAuth)
  console.log('[ROUTER] localStorage token exists:', !!token)
  console.log('[ROUTER] authStore.token:', authStore.token)
  console.log('[ROUTER] authStore.user:', authStore.user)
  
  // 首先检查是否需要认证，检查 localStorage 中的 token
  if (requiresAuth && !token) {
    console.log('[ROUTER] No token found, redirecting to login')
    next('/login')
    return
  }
  
  // 如果已经登录，但是访问登录/注册页面，重定向到首页
  if ((to.path === '/login' || to.path === '/register') && token) {
    // 如果用户信息已加载，根据角色跳转
    if (authStore.user?.role === 'admin') {
      next('/admin')
    } else {
      next('/')
    }
    return
  }

  // 检查用户角色权限（仅当用户信息已加载时）
  const requiredRoles = to.meta.roles as string[] | undefined
  if (requiredRoles && authStore.user) {
    const hasPermission = requiredRoles.includes(authStore.user.role)
    if (!hasPermission) {
      if (authStore.user.role === 'admin') {
        next('/admin')
      } else {
        next('/')
      }
      return
    }
  }

  // 如果有token但没有用户信息（刚登录），允许访问，让页面自己加载用户信息
  if (token && !authStore.user && requiresAuth) {
    next()
    return
  }

  next()
})

export default router
