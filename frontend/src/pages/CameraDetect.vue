<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 状态
const isStreaming = ref(false)
const videoRef = ref<HTMLVideoElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const error = ref('')

// 统计数据
const stats = ref({
  fps: 0,
  totalFrames: 0,
  diseaseFrames: 0,
  healthFrames: 0,
  diseaseRate: 0,
  runtime: '00:00:00'
})

// 最近检测记录
const recentRecords = ref<Array<{
  label: string
  confidence: number
  timestamp: string
}>>([])

// 模拟检测结果
const mockDetections = [
  { label: '白粉病 / Powdery Mildew', confidence: 0.92 },
  { label: '叶斑病 / Leaf Spot', confidence: 0.87 },
  { label: '健康 / Healthy', confidence: 0.95 },
  { label: '锈病 / Rust', confidence: 0.78 },
  { label: '白粉病 / Powdery Mildew', confidence: 0.89 },
  { label: '叶斑病 / Leaf Spot', confidence: 0.84 },
  { label: '早疫病 / Early Blight', confidence: 0.81 },
  { label: '健康 / Healthy', confidence: 0.97 }
]

// 计时器
let startTime: Date | null = null
let statsInterval: number | null = null
let detectionInterval: number | null = null
let fpsInterval: number | null = null
let frameCount = 0

// 获取标签颜色
function getLabelColor(label: string): string {
  if (label.includes('白粉病')) return '#ff6b6b'
  if (label.includes('叶斑病')) return '#ffd93d'
  if (label.includes('锈病')) return '#ff8c42'
  if (label.includes('早疫病')) return '#6bcb77'
  return '#2ed573'
}

// 格式化时间
function formatTime(seconds: number): string {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return [hours, minutes, secs]
    .map(v => v.toString().padStart(2, '0'))
    .join(':')
}

// 开始摄像头
async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 1280 },
        height: { ideal: 720 }
      }
    })

    if (videoRef.value) {
      videoRef.value.srcObject = stream
      await videoRef.value.play()
      isStreaming.value = true
      error.value = ''
      startTime = new Date()

      // 开始统计数据更新
      statsInterval = window.setInterval(() => {
        updateStats()
      }, 1000)

      // 开始模拟检测
      detectionInterval = window.setInterval(() => {
        simulateDetection()
      }, 2000)

      // FPS计算
      fpsInterval = window.setInterval(() => {
        stats.value.fps = frameCount
        frameCount = 0
      }, 1000)
    }
  } catch (err: any) {
    error.value = '无法访问摄像头: ' + (err.message || '未知错误')
    console.error('Camera error:', err)
  }
}

// 停止摄像头
function stopCamera() {
  if (videoRef.value && videoRef.value.srcObject) {
    const stream = videoRef.value.srcObject as MediaStream
    stream.getTracks().forEach(track => track.stop())
    videoRef.value.srcObject = null
  }

  isStreaming.value = false

  if (statsInterval) clearInterval(statsInterval)
  if (detectionInterval) clearInterval(detectionInterval)
  if (fpsInterval) clearInterval(fpsInterval)

  // 重置统计
  stats.value = {
    fps: 0,
    totalFrames: 0,
    diseaseFrames: 0,
    healthFrames: 0,
    diseaseRate: 0,
    runtime: '00:00:00'
  }
  recentRecords.value = []
  startTime = null
}

// 更新统计
function updateStats() {
  if (!startTime) return

  const elapsed = Math.floor((Date.now() - startTime.getTime()) / 1000)
  stats.value.runtime = formatTime(elapsed)
}

// 模拟检测
function simulateDetection() {
  if (!isStreaming.value) return

  frameCount++
  stats.value.totalFrames++

  // 随机选择检测结果
  const randomIndex = Math.floor(Math.random() * mockDetections.length)
  const detection = mockDetections[randomIndex]

  // 更新记录
  recentRecords.value.unshift({
    label: detection.label,
    confidence: detection.confidence,
    timestamp: new Date().toLocaleTimeString('zh-CN')
  })

  // 只保留最近10条
  if (recentRecords.value.length > 10) {
    recentRecords.value.pop()
  }

  // 更新统计
  if (detection.label.includes('健康')) {
    stats.value.healthFrames++
  } else {
    stats.value.diseaseFrames++
  }

  // 更新病害率
  stats.value.diseaseRate = stats.value.totalFrames > 0
    ? (stats.value.diseaseFrames / stats.value.totalFrames * 100).toFixed(1) as any
    : 0
}

onMounted(() => {
  // 组件挂载时自动尝试启动摄像头
  startCamera()
})

onUnmounted(() => {
  stopCamera()
})
</script>

<template>
  <div class="space-y-6">
    <!-- 操作按钮 -->
    <div class="flex justify-end">
      <button
        @click="router.push('/detect/camera/history')"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        历史记录
      </button>
    </div>

    <!-- 摄像头预览和统计 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 摄像头画面 -->
      <div class="lg:col-span-2 bg-white rounded-xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-800">摄像头画面</h3>
          <div class="flex items-center gap-2">
            <span
              v-if="isStreaming"
              class="flex items-center gap-2 px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm"
            >
              <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              直播中
            </span>
            <span
              v-else
              class="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm"
            >
              已停止
            </span>
          </div>
        </div>

        <div class="relative bg-black rounded-xl overflow-hidden" style="min-height: 400px;">
          <video
            v-show="isStreaming"
            ref="videoRef"
            class="w-full h-full object-cover"
            playsinline
            muted
          />
          <canvas
            ref="canvasRef"
            class="hidden"
          />

          <!-- 错误提示 -->
          <div v-if="error" class="absolute inset-0 flex items-center justify-center bg-gray-800">
            <div class="text-center text-white p-6">
              <svg class="w-16 h-16 mx-auto mb-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <p class="text-lg">{{ error }}</p>
            </div>
          </div>

          <!-- 未启动提示 -->
          <div v-if="!isStreaming && !error" class="absolute inset-0 flex items-center justify-center bg-gray-700">
            <div class="text-center text-white">
              <svg class="w-20 h-20 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <p class="text-lg mb-4">摄像头未启动</p>
              <button
                @click="startCamera"
                class="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
              >
                启动摄像头
              </button>
            </div>
          </div>
        </div>

        <!-- 控制按钮 -->
        <div class="mt-4 flex gap-4">
          <button
            v-if="!isStreaming"
            @click="startCamera"
            class="flex-1 bg-green-500 text-white py-3 rounded-xl font-bold hover:bg-green-600 transition-colors"
          >
            启动摄像头
          </button>
          <button
            v-else
            @click="stopCamera"
            class="flex-1 bg-red-500 text-white py-3 rounded-xl font-bold hover:bg-red-600 transition-colors"
          >
            停止检测
          </button>
        </div>
      </div>

      <!-- 统计面板 -->
      <div class="space-y-6">
        <!-- 实时统计 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">实时统计</h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <span class="text-gray-600">FPS</span>
              <span class="text-2xl font-bold text-blue-600">{{ stats.fps }}</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span class="text-gray-600">检测帧数</span>
              <span class="text-2xl font-bold text-gray-700">{{ stats.totalFrames }}</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-red-50 rounded-lg">
              <span class="text-gray-600">病害帧数</span>
              <span class="text-2xl font-bold text-red-600">{{ stats.diseaseFrames }}</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <span class="text-gray-600">健康帧数</span>
              <span class="text-2xl font-bold text-green-600">{{ stats.healthFrames }}</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <span class="text-gray-600">病害率</span>
              <span class="text-2xl font-bold text-purple-600">{{ stats.diseaseRate }}%</span>
            </div>
            <div class="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
              <span class="text-gray-600">运行时间</span>
              <span class="text-xl font-mono font-bold text-orange-600">{{ stats.runtime }}</span>
            </div>
          </div>
        </div>

        <!-- 最近检测记录 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">最近检测记录</h3>
          <div v-if="recentRecords.length === 0" class="text-center text-gray-400 py-8">
            <p>暂无检测记录</p>
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="(record, index) in recentRecords"
              :key="index"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div class="flex items-center gap-3">
                <div
                  class="w-10 h-10 rounded-lg flex items-center justify-center"
                  :style="{ backgroundColor: getLabelColor(record.label) + '20' }"
                >
                  <div
                    class="w-3 h-3 rounded-full"
                    :style="{ backgroundColor: getLabelColor(record.label) }"
                  ></div>
                </div>
                <div>
                  <p class="font-medium text-gray-800">{{ record.label.split(' / ')[0] }}</p>
                  <p class="text-xs text-gray-400">{{ record.timestamp }}</p>
                </div>
              </div>
              <span
                class="font-bold"
                :style="{ color: getLabelColor(record.label) }"
              >
                {{ (record.confidence * 100).toFixed(0) }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
