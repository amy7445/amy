<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import backgroundImage from '@/assets/background.jpg'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const captcha = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')
const captchaUrl = ref('')

function refreshCaptcha() {
  captchaUrl.value = `/api/captcha?timestamp=${Date.now()}`
}

onMounted(() => {
  refreshCaptcha()
})

async function handleLogin() {
    if (!username.value || !password.value || !captcha.value) {
      errorMessage.value = '请输入用户名、密码和验证码'
      return
    }

    isLoading.value = true
    errorMessage.value = ''

    try {
      const result = await authStore.login(username.value, password.value, captcha.value)
      
      // 确保 localStorage 已写入
      await new Promise(resolve => setTimeout(resolve, 100))
      
      // 使用 window.location.href 直接跳转，确保 token 被正确传递
      const redirectPath = result.user.role === 'admin' ? '/admin' : '/'
      window.location.href = redirectPath
    } catch (error: any) {
      errorMessage.value = error.response?.data?.detail || '登录失败，请检查用户名和密码'
      refreshCaptcha()
      captcha.value = ''
    } finally {
      isLoading.value = false
    }
  }

function goToRegister() {
  router.push('/register')
}
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-cover bg-center"
    :style="{ backgroundImage: `url(${backgroundImage})` }"
  >
    <!-- 背景遮罩 -->
    <div class="absolute inset-0 bg-black/10"></div>

    <!-- 登录卡片 -->
    <div class="relative z-10 w-full max-w-md px-6">
      <div class="glass rounded-2xl shadow-2xl p-8 border border-white/20">
        <!-- Logo -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-primary-dark mb-2">智慧农业病虫害检测系统</h1>
        </div>

        <!-- 错误提示 -->
        <div
          v-if="errorMessage"
          class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm"
        >
          {{ errorMessage }}
        </div>

        <!-- 表单 -->
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
            <input
              v-model="username"
              type="text"
              class="input-field"
              placeholder="请输入用户名"
              autocomplete="username"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">密码</label>
            <div class="relative">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="input-field pr-12"
                placeholder="请输入密码"
                autocomplete="current-password"
              />
              <button
                @click="showPassword = !showPassword"
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">验证码</label>
            <div class="flex gap-3">
              <input
                v-model="captcha"
                type="text"
                class="input-field flex-1"
                placeholder="请输入验证码"
                maxlength="4"
              />
              <img
                :src="captchaUrl"
                @click="refreshCaptcha"
                class="w-28 h-10 rounded-lg cursor-pointer border border-gray-200 hover:border-gray-300 transition-colors"
                alt="验证码"
                title="点击刷新"
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="btn-primary w-full flex items-center justify-center gap-2"
          >
            <span v-if="isLoading" class="animate-spin">⏳</span>
            <span>{{ isLoading ? '登录中...' : '登录' }}</span>
          </button>
        </form>

        <!-- 底部链接 -->
        <div class="mt-6 flex items-center justify-between text-sm">
          <button
            @click="goToRegister"
            class="text-primary-dark hover:text-primary-dark/80 transition-colors"
          >
            注册账号
          </button>
          <button class="text-gray-500 hover:text-gray-700 transition-colors">
            忘记密码？
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
