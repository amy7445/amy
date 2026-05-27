<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const menuItems = [
  { path: '/', label: '数据看板', roles: ['user'] },
  { path: '/detect/image', label: '图片检测', roles: ['user'] },
  { path: '/detect/video', label: '视频检测', roles: ['user'] },
  { path: '/detect/camera', label: '实时摄像头', roles: ['user'] },
  { path: '/predict', label: '趋势预测', roles: ['user'] },
  { path: '/treatment', label: '防治方案', roles: ['user'] },
  { path: '/evaluation', label: '效果评估', roles: ['user'] },
  { path: '/compare', label: '历史对比', roles: ['user'] },
  { path: '/knowledge', label: '知识库', roles: ['user'] },
  { path: '/profile', label: '个人中心', roles: ['user'] },
  { path: '/admin', label: '系统概览', roles: ['admin'] },
  { path: '/admin/users', label: '用户管理', roles: ['admin'] },
  { path: '/admin/model', label: '模型设置', roles: ['admin'] },
  { path: '/admin/logs', label: '检测日志', roles: ['admin'] },
  { path: '/admin/config', label: '系统设置', roles: ['admin'] },
  { path: '/admin/announcements', label: '公告管理', roles: ['admin'] }
]

const currentPath = computed(() => route.path)

// 根据用户角色过滤菜单
const visibleMenuItems = computed(() => {
  const userRole = authStore.user?.role || 'user'
  return menuItems.filter(item => item.roles.includes(userRole))
})

// 面包屑导航数据
const breadcrumbs = computed(() => {
  const pathMap: Record<string, { label: string; path: string }[]> = {
    '/': [{ label: '数据看板', path: '/' }],
    '/detect/image': [{ label: '图片检测', path: '/detect/image' }],
    '/detect/image/history': [
      { label: '图片检测', path: '/detect/image' },
      { label: '历史记录', path: '/detect/image/history' }
    ],
    '/detect/video': [{ label: '视频检测', path: '/detect/video' }],
    '/detect/video/history': [
      { label: '视频检测', path: '/detect/video' },
      { label: '历史记录', path: '/detect/video/history' }
    ],
    '/detect/camera': [{ label: '实时摄像头', path: '/detect/camera' }],
    '/detect/camera/history': [
      { label: '实时摄像头', path: '/detect/camera' },
      { label: '历史记录', path: '/detect/camera/history' }
    ],
    '/predict': [{ label: '趋势预测', path: '/predict' }],
    '/treatment': [{ label: '防治方案', path: '/treatment' }],
    '/evaluation': [{ label: '效果评估', path: '/evaluation' }],
    '/compare': [{ label: '历史对比', path: '/compare' }],
    '/knowledge': [{ label: '知识库', path: '/knowledge' }],
    '/profile': [{ label: '个人中心', path: '/profile' }],
    '/admin': [{ label: '系统概览', path: '/admin' }],
    '/admin/users': [
      { label: '系统管理', path: '/admin' },
      { label: '用户管理', path: '/admin/users' }
    ],
    '/admin/model': [
      { label: '系统管理', path: '/admin' },
      { label: '模型设置', path: '/admin/model' }
    ],
    '/admin/logs': [
      { label: '系统管理', path: '/admin' },
      { label: '检测日志', path: '/admin/logs' }
    ],
    '/admin/config': [
      { label: '系统管理', path: '/admin' },
      { label: '系统设置', path: '/admin/config' }
    ],
    '/admin/announcements': [
      { label: '系统管理', path: '/admin' },
      { label: '公告管理', path: '/admin/announcements' }
    ]
  }
  return pathMap[route.path] || [{ label: '数据看板', path: '/' }]
})

function navigateTo(path: string) {
  router.push(path)
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="flex min-h-screen">
    <!-- 侧边栏 -->
    <aside class="sidebar flex flex-col">
      <!-- Logo区域 -->
      <div class="p-4 border-b" style="border-color: rgba(0,0,0,0.08);">
        <div class="text-center">
          <h1 class="text-lg font-bold" style="color: var(--color-primary-dark);">
            智慧农业病虫害检测系统
          </h1>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="flex-1 py-3 overflow-y-auto">
        <ul class="space-y-0">
          <li v-for="item in visibleMenuItems" :key="item.path">
            <button
              @click="navigateTo(item.path)"
              :class="[
                'sidebar-menu-item',
                currentPath === item.path ? 'active' : ''
              ]"
            >
              {{ item.label }}
            </button>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- 主内容区 -->
    <div class="content-area flex-1 flex flex-col">
      <!-- 顶部导航栏 -->
      <header class="top-navbar">
        <div class="flex items-center gap-2">
          <!-- 面包屑导航 -->
          <nav class="breadcrumb-nav">
            <span v-for="(crumb, index) in breadcrumbs" :key="crumb.path" class="breadcrumb-item">
              <span
                v-if="index < breadcrumbs.length - 1"
                class="breadcrumb-link"
                @click="navigateTo(crumb.path)"
              >
                {{ crumb.label }}
              </span>
              <span v-else class="breadcrumb-current">
                {{ crumb.label }}
              </span>
              <span v-if="index < breadcrumbs.length - 1" class="breadcrumb-separator">/</span>
            </span>
          </nav>
        </div>
        
        <div class="flex items-center gap-4">
          <!-- 功能图标区 -->
          <div class="flex items-center gap-3">
            <button class="nav-icon-btn" title="翻译">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
              </svg>
            </button>
            <button class="nav-icon-btn" title="全屏">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
              </svg>
            </button>
            <button class="nav-icon-btn" title="通知">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </button>
          </div>
          
          <!-- 用户区 -->
          <div class="flex items-center gap-3 ml-2">
            <div class="user-avatar">
              <span class="font-medium">{{ authStore.user?.username ? authStore.user.username[0].toUpperCase() : 'U' }}</span>
            </div>
            <span class="text-sm font-medium" style="color: var(--color-text);">
              {{ authStore.user?.username }}
            </span>
            <button
              @click="handleLogout"
              class="text-sm px-3 py-1.5 rounded-lg transition-colors hover:bg-red-50 hover:text-red-600 border border-gray-200"
              style="color: var(--color-text-secondary);"
            >
              退出登录
            </button>
          </div>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="flex-1 p-6" style="background-color: var(--color-bg-light);">
        <router-view />
      </main>
    </div>
  </div>
</template>
