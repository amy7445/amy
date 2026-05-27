<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 用户信息
const userInfo = ref({
  username: authStore.user?.username || '用户名',
  email: authStore.user?.email || '',
  phone: authStore.user?.phone || '',
  role: authStore.user?.role || 'user',
  avatar: '',
  joinDate: '2024-01-15',
  lastLogin: '2024-03-15 14:30'
})

// 检测统计
const detectionStats = ref({
  totalDetections: 256,
  imageDetections: 189,
  videoDetections: 45,
  cameraDetections: 22
})

// 修改密码表单
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 安全设置
const securitySettings = ref({
  emailNotification: true,
  smsNotification: false,
  wechatNotification: true
})

// 修改个人信息
function updateProfile() {
  alert('个人信息更新成功！')
}

// 修改密码
function changePassword() {
  if (!passwordForm.value.oldPassword) {
    alert('请输入原密码')
    return
  }
  if (!passwordForm.value.newPassword) {
    alert('请输入新密码')
    return
  }
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }

  alert('密码修改成功！')
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
}

// 保存安全设置
function saveSecuritySettings() {
  alert('安全设置已保存！')
}
</script>

<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左侧用户信息卡片 -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-xl p-6 shadow-md">
          <div class="text-center mb-6">
            <div class="w-24 h-24 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-4xl font-bold text-white">
                {{ userInfo.username[0].toUpperCase() }}
              </span>
            </div>
            <h2 class="text-xl font-bold text-gray-800">{{ userInfo.username }}</h2>
            <p class="text-sm text-gray-500 mt-1">
              {{ userInfo.role === 'admin' ? '管理员' : '普通用户' }}
            </p>
            <p class="text-xs text-gray-400 mt-2">
              注册时间：{{ userInfo.joinDate }}
            </p>
          </div>

          <div class="space-y-4">
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span class="text-gray-600">检测总数</span>
              <span class="font-bold text-green-600">{{ detectionStats.totalDetections }}</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span class="text-gray-600">图片检测</span>
              <span class="font-bold text-blue-600">{{ detectionStats.imageDetections }}</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span class="text-gray-600">视频检测</span>
              <span class="font-bold text-purple-600">{{ detectionStats.videoDetections }}</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span class="text-gray-600">实时监测</span>
              <span class="font-bold text-orange-600">{{ detectionStats.cameraDetections }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧设置区域 -->
      <div class="lg:col-span-2 space-y-6">
        <!-- 基本信息 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">基本信息</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
              <input
                v-model="userInfo.username"
                type="text"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
              <input
                v-model="userInfo.email"
                type="email"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">手机号</label>
              <input
                v-model="userInfo.phone"
                type="tel"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">上次登录</label>
              <input
                :value="userInfo.lastLogin"
                type="text"
                disabled
                class="w-full px-4 py-3 rounded-lg border border-gray-200 bg-gray-50 text-gray-500"
              />
            </div>
          </div>
          <button
            @click="updateProfile"
            class="mt-6 px-6 py-3 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600 transition-colors"
          >
            保存修改
          </button>
        </div>

        <!-- 修改密码 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">修改密码</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">原密码</label>
              <input
                v-model="passwordForm.oldPassword"
                type="password"
                placeholder="请输入原密码"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">新密码</label>
              <input
                v-model="passwordForm.newPassword"
                type="password"
                placeholder="请输入新密码"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">确认新密码</label>
              <input
                v-model="passwordForm.confirmPassword"
                type="password"
                placeholder="请再次输入新密码"
                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
              />
            </div>
          </div>
          <button
            @click="changePassword"
            class="mt-6 px-6 py-3 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
          >
            修改密码
          </button>
        </div>

        <!-- 安全设置 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">通知设置</h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <p class="font-medium text-gray-800">邮件通知</p>
                <p class="text-sm text-gray-500">接收检测结果和系统通知</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input
                  v-model="securitySettings.emailNotification"
                  type="checkbox"
                  class="sr-only peer"
                />
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
              </label>
            </div>

            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <p class="font-medium text-gray-800">短信通知</p>
                <p class="text-sm text-gray-500">接收重要预警短信</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input
                  v-model="securitySettings.smsNotification"
                  type="checkbox"
                  class="sr-only peer"
                />
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
              </label>
            </div>

            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <p class="font-medium text-gray-800">微信通知</p>
                <p class="text-sm text-gray-500">接收微信推送通知</p>
              </div>
              <label class="relative inline-flex items-center cursor-pointer">
                <input
                  v-model="securitySettings.wechatNotification"
                  type="checkbox"
                  class="sr-only peer"
                />
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
              </label>
            </div>
          </div>
          <button
            @click="saveSecuritySettings"
            class="mt-6 px-6 py-3 bg-purple-500 text-white rounded-lg font-medium hover:bg-purple-600 transition-colors"
          >
            保存设置
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
