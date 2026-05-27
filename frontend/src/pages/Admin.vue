<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'

const route = useRoute()

// 当前激活的标签页
const activeTab = ref('dashboard')

// 根据路由设置初始标签
function setTabFromRoute() {
  const path = route.path
  if (path === '/admin/users') {
    activeTab.value = 'users'
  } else if (path === '/admin/model') {
    activeTab.value = 'model'
  } else if (path === '/admin/logs') {
    activeTab.value = 'logs'
  } else if (path === '/admin/config') {
    activeTab.value = 'config'
  } else if (path === '/admin/announcements') {
    activeTab.value = 'announcements'
  } else {
    activeTab.value = 'dashboard'
  }
}

// 监听路由变化
watch(() => route.path, () => {
  setTabFromRoute()
})

// 用户列表
const users = ref([
  { id: 1, username: 'admin', role: 'admin', email: 'admin@example.com', status: 'active', lastLogin: '2024-03-15 14:30', detections: 156 },
  { id: 2, username: 'zhangsan', role: 'user', email: 'zhangsan@example.com', status: 'active', lastLogin: '2024-03-15 10:20', detections: 45 },
  { id: 3, username: 'lisi', role: 'user', email: 'lisi@example.com', status: 'inactive', lastLogin: '2024-03-10 08:15', detections: 23 },
  { id: 4, username: 'wangwu', role: 'user', email: 'wangwu@example.com', status: 'active', lastLogin: '2024-03-15 09:45', detections: 67 },
  { id: 5, username: 'zhaoliu', role: 'user', email: 'zhaoliu@example.com', status: 'active', lastLogin: '2024-03-14 16:20', detections: 34 }
])

// 系统配置
const systemConfig = ref({
  detectionThreshold: 0.5,
  maxConcurrent: 10,
  logRetention: 30,
  modelVersion: 'YOLOv11',
  autoUpdate: true,
  emailNotification: true
})

// 检测日志
const detectionLogs = ref([
  { id: 1, userId: 2, username: 'zhangsan', type: '图片检测', result: '白粉病', confidence: 0.92, time: '2024-03-15 14:28' },
  { id: 2, userId: 4, username: 'wangwu', type: '视频检测', result: '叶斑病', confidence: 0.87, time: '2024-03-15 14:25' },
  { id: 3, userId: 1, username: 'admin', type: '实时监测', result: '健康', confidence: 0.95, time: '2024-03-15 14:20' },
  { id: 4, userId: 5, username: 'zhaoliu', type: '图片检测', result: '锈病', confidence: 0.78, time: '2024-03-15 14:15' },
  { id: 5, userId: 2, username: 'zhangsan', type: '图片检测', result: '健康', confidence: 0.97, time: '2024-03-15 14:10' }
])

// 系统公告
const announcements = ref([
  { id: 1, title: '系统升级通知', content: '系统将于本周日凌晨2:00-6:00进行升级维护，届时系统将暂停服务。', date: '2024-03-14', status: 'active' },
  { id: 2, title: '新模型上线', content: 'YOLOv11模型已正式上线，检测准确率提升15%，欢迎体验。', date: '2024-03-10', status: 'active' },
  { id: 3, title: '功能更新', content: '新增历史数据对比功能，方便用户对比分析防治效果。', date: '2024-03-05', status: 'active' }
])

// 统计数据
const stats = ref({
  totalUsers: 156,
  activeUsers: 89,
  totalDetections: 12580,
  todayDetections: 234,
  modelAccuracy: 94.5,
  avgResponseTime: 1.2
})

// 图表
let userChart: echarts.ECharts | null = null
let detectionChart: echarts.ECharts | null = null
const userChartRef = ref<HTMLDivElement | null>(null)
const detectionChartRef = ref<HTMLDivElement | null>(null)

function initUserChart() {
  if (!userChartRef.value) return

  userChart = echarts.init(userChartRef.value)
  userChart.setOption({
    tooltip: { trigger: 'item', backgroundColor: 'rgba(255,255,255,0.95)', borderColor: '#A3E4A3' },
    series: [{
      name: '用户统计',
      type: 'pie',
      radius: ['50%', '80%'],
      center: ['50%', '50%'],
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { label: { show: true, fontSize: 16, fontWeight: 'bold' } },
      data: [
        { value: stats.value.activeUsers, name: '活跃用户', itemStyle: { color: '#4CAF50' } },
        { value: stats.value.totalUsers - stats.value.activeUsers, name: '非活跃用户', itemStyle: { color: '#E0E0E0' } }
      ]
    }]
  })
}

function initDetectionChart() {
  if (!detectionChartRef.value) return

  detectionChart = echarts.init(detectionChartRef.value)
  detectionChart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(255,255,255,0.95)', borderColor: '#A3E4A3' },
    grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
    xAxis: { type: 'category', data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'], axisLine: { lineStyle: { color: '#A3E4A3' } } },
    yAxis: { type: 'value', axisLine: { show: false }, splitLine: { lineStyle: { color: '#f0f0f0' } } },
    series: [{
      name: '检测次数',
      type: 'bar',
      data: [120, 145, 132, 168, 156, 189, 174],
      itemStyle: { color: '#4CAF50' },
      barWidth: '50%'
    }]
  })
}

function handleResize() {
  userChart?.resize()
  detectionChart?.resize()
}

onMounted(() => {
  setTabFromRoute()
  setTimeout(() => {
    initUserChart()
    initDetectionChart()
  }, 100)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  userChart?.dispose()
  detectionChart?.dispose()
})

// 用户操作
function toggleUserStatus(userId: number) {
  const user = users.value.find(u => u.id === userId)
  if (user) {
    user.status = user.status === 'active' ? 'inactive' : 'active'
  }
}

function deleteUser(userId: number) {
  if (confirm('确定要删除该用户吗？')) {
    users.value = users.value.filter(u => u.id !== userId)
  }
}

// 保存配置
function saveConfig() {
  alert('系统配置已保存！')
}

// 添加公告
function addAnnouncement() {
  alert('公告发布功能')
}


</script>

<template>
  <div class="space-y-6">
    <!-- 系统概览 -->
    <div v-if="activeTab === 'dashboard'" class="bg-white rounded-xl shadow-md p-6">
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
          <div class="bg-blue-50 rounded-xl p-4 text-center">
            <p class="text-sm text-gray-500 mb-1">总用户数</p>
            <p class="text-2xl font-bold text-blue-600">{{ stats.totalUsers }}</p>
          </div>
          <div class="bg-green-50 rounded-xl p-4 text-center">
            <p class="text-sm text-gray-500 mb-1">活跃用户</p>
            <p class="text-2xl font-bold text-green-600">{{ stats.activeUsers }}</p>
          </div>
          <div class="bg-purple-50 rounded-xl p-4 text-center">
            <p class="text-sm text-gray-500 mb-1">总检测数</p>
            <p class="text-2xl font-bold text-purple-600">{{ stats.totalDetections.toLocaleString() }}</p>
          </div>
          <div class="bg-orange-50 rounded-xl p-4 text-center">
            <p class="text-sm text-gray-500 mb-1">今日检测</p>
            <p class="text-2xl font-bold text-orange-600">{{ stats.todayDetections }}</p>
          </div>
          <div class="bg-red-50 rounded-xl p-4 text-center">
            <p class="text-sm text-gray-500 mb-1">模型准确率</p>
            <p class="text-2xl font-bold text-red-600">{{ stats.modelAccuracy }}%</p>
          </div>
          <div class="bg-teal-50 rounded-xl p-4 text-center">
            <p class="text-sm text-gray-500 mb-1">平均响应(秒)</p>
            <p class="text-2xl font-bold text-teal-600">{{ stats.avgResponseTime }}</p>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-gray-50 rounded-xl p-4">
            <h3 class="font-medium text-gray-800 mb-3">用户分布</h3>
            <div ref="userChartRef" class="h-64"></div>
          </div>
          <div class="bg-gray-50 rounded-xl p-4">
            <h3 class="font-medium text-gray-800 mb-3">本周检测趋势</h3>
            <div ref="detectionChartRef" class="h-64"></div>
          </div>
        </div>
      </div>

      <!-- 用户管理 -->
      <div v-if="activeTab === 'users'" class="bg-white rounded-xl shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-medium text-gray-800">用户列表</h3>
          <button class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors">
            添加用户
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="bg-gray-50">
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">用户名</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">角色</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">邮箱</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">状态</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">检测次数</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">最后登录</th>
                <th class="px-4 py-3 text-left text-sm font-medium text-gray-700">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="px-4 py-3">
                  <div class="flex items-center gap-2">
                    <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <span class="text-sm font-bold text-green-600">{{ user.username[0].toUpperCase() }}</span>
                    </div>
                    <span class="font-medium text-gray-800">{{ user.username }}</span>
                  </div>
                </td>
                <td class="px-4 py-3">
                  <span :class="[
                    'px-2 py-1 rounded text-xs font-medium',
                    user.role === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
                  ]">
                    {{ user.role === 'admin' ? '管理员' : '普通用户' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-gray-600">{{ user.email }}</td>
                <td class="px-4 py-3">
                  <button
                    @click="toggleUserStatus(user.id)"
                    :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      user.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                    ]"
                  >
                    {{ user.status === 'active' ? '活跃' : '停用' }}
                  </button>
                </td>
                <td class="px-4 py-3 text-gray-600">{{ user.detections }}</td>
                <td class="px-4 py-3 text-gray-600">{{ user.lastLogin }}</td>
                <td class="px-4 py-3">
                  <div class="flex gap-2">
                    <button class="px-3 py-1 bg-blue-100 text-blue-700 rounded text-sm hover:bg-blue-200">编辑</button>
                    <button
                      v-if="user.role !== 'admin'"
                      @click="deleteUser(user.id)"
                      class="px-3 py-1 bg-red-100 text-red-700 rounded text-sm hover:bg-red-200"
                    >删除</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 检测日志 -->
      <div v-if="activeTab === 'logs'" class="bg-white rounded-xl shadow-md p-6">
        <h3 class="font-medium text-gray-800 mb-4">检测日志</h3>
        <div class="space-y-3">
          <div
            v-for="log in detectionLogs"
            :key="log.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div class="flex items-center gap-3">
              <div :class="[
                'w-10 h-10 rounded-lg flex items-center justify-center',
                log.type === '图片检测' ? 'bg-green-100' :
                log.type === '视频检测' ? 'bg-blue-100' : 'bg-orange-100'
              ]">
                <span class="text-xs font-bold" :class="log.type === '图片检测' ? 'text-green-600' : log.type === '视频检测' ? 'text-blue-600' : 'text-orange-600'">
                  {{ log.type.slice(0, 2) }}
                </span>
              </div>
              <div>
                <p class="font-medium text-gray-800">{{ log.username }} · {{ log.type }}</p>
                <p class="text-sm text-gray-500">结果: {{ log.result }} · 置信度: {{ (log.confidence * 100).toFixed(0) }}%</p>
              </div>
            </div>
            <span class="text-sm text-gray-400">{{ log.time }}</span>
          </div>
        </div>
      </div>

      <!-- 模型设置 -->
      <div v-if="activeTab === 'model'" class="bg-white rounded-xl shadow-md p-6">
        <h3 class="font-medium text-gray-800 mb-4">模型设置</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="bg-gray-50 rounded-xl p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div>
                <p class="font-bold text-gray-800">当前模型</p>
                <p class="text-sm text-gray-500">{{ systemConfig.modelVersion }}</p>
              </div>
            </div>
            <p class="text-sm text-gray-600">准确率: {{ stats.modelAccuracy }}%</p>
            <button class="mt-4 w-full py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors">
              检查更新
            </button>
          </div>
          <div class="bg-gray-50 rounded-xl p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
              <div>
                <p class="font-bold text-gray-800">模型训练</p>
                <p class="text-sm text-gray-500">管理训练任务</p>
              </div>
            </div>
            <button class="mt-4 w-full py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
              开始训练
            </button>
          </div>
          <div class="bg-gray-50 rounded-xl p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
              <div>
                <p class="font-bold text-gray-800">模型导出</p>
                <p class="text-sm text-gray-500">导出训练好的模型</p>
              </div>
            </div>
            <button class="mt-4 w-full py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors">
              导出模型
            </button>
          </div>
        </div>
        <div class="mt-6 bg-white rounded-xl p-6 border border-gray-200">
          <h4 class="font-bold text-gray-800 mb-4">模型参数配置</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">输入尺寸</label>
              <select class="w-full px-4 py-3 rounded-lg border border-gray-300">
                <option>416x416</option>
                <option>640x640</option>
                <option>800x800</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">置信度阈值</label>
              <input
                type="number"
                step="0.05"
                min="0"
                max="1"
                value="0.5"
                class="w-full px-4 py-3 rounded-lg border border-gray-300"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">NMS阈值</label>
              <input
                type="number"
                step="0.05"
                min="0"
                max="1"
                value="0.45"
                class="w-full px-4 py-3 rounded-lg border border-gray-300"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">最大检测数</label>
              <input
                type="number"
                min="1"
                max="100"
                value="50"
                class="w-full px-4 py-3 rounded-lg border border-gray-300"
              />
            </div>
          </div>
          <button class="mt-6 px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors">
            保存配置
          </button>
        </div>
      </div>

      <!-- 系统配置 -->
      <div v-if="activeTab === 'config'" class="bg-white rounded-xl shadow-md p-6">
        <h3 class="font-medium text-gray-800 mb-4">系统配置</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">检测置信度阈值</label>
            <input
              v-model.number="systemConfig.detectionThreshold"
              type="number"
              step="0.1"
              min="0"
              max="1"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">最大并发检测数</label>
            <input
              v-model.number="systemConfig.maxConcurrent"
              type="number"
              min="1"
              max="100"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">日志保留天数</label>
            <input
              v-model.number="systemConfig.logRetention"
              type="number"
              min="7"
              max="365"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">当前模型版本</label>
            <input
              :value="systemConfig.modelVersion"
              disabled
              class="w-full px-4 py-3 rounded-lg border border-gray-200 bg-gray-50 text-gray-500"
            />
          </div>
          <div>
            <label class="flex items-center gap-2 cursor-pointer">
              <input v-model="systemConfig.autoUpdate" type="checkbox" class="w-4 h-4 text-green-600" />
              <span class="text-sm text-gray-700">自动更新模型</span>
            </label>
          </div>
          <div>
            <label class="flex items-center gap-2 cursor-pointer">
              <input v-model="systemConfig.emailNotification" type="checkbox" class="w-4 h-4 text-green-600" />
              <span class="text-sm text-gray-700">发送邮件通知</span>
            </label>
          </div>
        </div>
        <button
          @click="saveConfig"
          class="mt-6 px-6 py-3 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
        >
          保存配置
        </button>
      </div>

      <!-- 公告管理 -->
      <div v-if="activeTab === 'announcements'" class="bg-white rounded-xl shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-medium text-gray-800">系统公告</h3>
          <button @click="addAnnouncement" class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors">
            发布公告
          </button>
        </div>
        <div class="space-y-4">
          <div
            v-for="announcement in announcements"
            :key="announcement.id"
            class="p-4 bg-gray-50 rounded-lg"
          >
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-medium text-gray-800">{{ announcement.title }}</h4>
              <span class="text-sm text-gray-400">{{ announcement.date }}</span>
            </div>
            <p class="text-gray-600">{{ announcement.content }}</p>
            <div class="flex gap-2 mt-3">
              <button class="px-3 py-1 bg-blue-100 text-blue-700 rounded text-sm">编辑</button>
              <button class="px-3 py-1 bg-red-100 text-red-700 rounded text-sm">删除</button>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>
