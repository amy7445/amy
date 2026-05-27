<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 状态
const isDragging = ref(false)
const selectedFile = ref<File | null>(null)
const imageUrl = ref<string | null>(null)
const isLoading = ref(false)
const result = ref<any>(null)

// 检测结果（用于显示检测框）
const detectionResults = computed(() => {
  if (!result.value) return []
  return result.value.detections || []
})

// 处理拖拽
function handleDragOver(e: DragEvent) {
  e.preventDefault()
  isDragging.value = true
}

function handleDragLeave() {
  isDragging.value = false
}

function handleDrop(e: DragEvent) {
  e.preventDefault()
  isDragging.value = false
  const files = e.dataTransfer?.files
  if (files && files[0]) {
    handleFileSelect(files[0])
  }
}

// 处理文件选择
function handleFileInput(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    handleFileSelect(target.files[0])
  }
}

function handleFileSelect(file: File) {
  if (!file.type.match(/^image\/(jpeg|png|jpg)$/)) {
    alert('请上传 JPG 或 PNG 格式的图片')
    return
  }
  selectedFile.value = file
  imageUrl.value = URL.createObjectURL(file)
  result.value = null
}

// 重置
function resetDetection() {
  selectedFile.value = null
  if (imageUrl.value) {
    URL.revokeObjectURL(imageUrl.value)
  }
  imageUrl.value = null
  result.value = null
}

// 开始检测
async function startDetection() {
  if (!selectedFile.value) return

  isLoading.value = true

  // 模拟检测过程
  await new Promise(resolve => setTimeout(resolve, 2000))

  // 模拟检测结果
  result.value = {
    image_id: 'IMG_' + Date.now(),
    timestamp: new Date().toLocaleString('zh-CN'),
    total_detections: 3,
    disease_count: 2,
    health_count: 1,
    detections: [
      {
        class: 'powdery_mildew',
        label: '白粉病 / Powdery Mildew',
        confidence: 0.92,
        bbox: { x: 120, y: 80, width: 150, height: 120 }
      },
      {
        class: 'leaf_spot',
        label: '叶斑病 / Leaf Spot',
        confidence: 0.87,
        bbox: { x: 350, y: 200, width: 180, height: 140 }
      },
      {
        class: 'healthy',
        label: '健康 / Healthy',
        confidence: 0.95,
        bbox: { x: 500, y: 100, width: 100, height: 100 }
      }
    ],
    summary: {
      main_disease: '白粉病',
      severity: '中等',
      recommendation: '建议使用多菌灵或百菌清进行防治'
    }
  }

  isLoading.value = false
}

// 获取边框颜色
function getBoxColor(diseaseClass: string): string {
  const colors: Record<string, string> = {
    'powdery_mildew': '#ff6b6b',
    'leaf_spot': '#ffd93d',
    'rust': '#ff8c42',
    'early_blight': '#6bcb77',
    'late_blight': '#4d96ff',
    'healthy': '#2ed573'
  }
  return colors[diseaseClass] || '#333'
}
</script>

<template>
  <div class="space-y-6">
    <!-- 操作按钮 -->
    <div class="flex justify-end">
      <button
        @click="router.push('/detect/image/history')"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        历史记录
      </button>
    </div>

    <!-- 上传区域 -->
    <div v-if="!selectedFile" class="bg-white rounded-xl p-12 shadow-md">
      <div
        @dragover="handleDragOver"
        @dragleave="handleDragLeave"
        @drop="handleDrop"
        :class="[
          'border-3 border-dashed rounded-2xl p-12 text-center transition-all duration-300 cursor-pointer',
          isDragging 
            ? 'border-green-500 bg-green-50' 
            : 'border-gray-300 hover:border-green-500 hover:bg-gray-50'
        ]"
      >
        <div class="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <p class="text-2xl text-gray-700 mb-2 font-medium">拖拽图片到这里</p>
        <p class="text-gray-500 mb-6">支持 JPG、PNG 格式</p>
        <label class="inline-block">
          <span class="inline-block bg-green-500 text-white px-8 py-3 rounded-lg font-medium cursor-pointer hover:bg-green-600 transition-colors">
            选择图片
          </span>
          <input
            type="file"
            accept="image/jpeg,image/png,image/jpg"
            class="hidden"
            @change="handleFileInput"
          />
        </label>
      </div>
    </div>

    <!-- 已选择图片并检测 -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 图片预览和检测框 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-800">检测结果可视化</h3>
          <button
            @click="resetDetection"
            class="text-gray-500 hover:text-gray-700 transition-colors"
          >
            重新上传
          </button>
        </div>

        <div class="relative bg-gray-100 rounded-xl overflow-hidden" style="min-height: 400px;">
          <img
            :src="imageUrl!"
            alt="待检测图片"
            class="w-full h-auto"
            style="max-height: 500px; object-fit: contain;"
          />
          
          <!-- 检测框 -->
          <div
            v-for="(det, index) in detectionResults"
            :key="index"
            class="absolute border-3 rounded-lg flex items-center justify-center"
            :style="{
              left: det.bbox.x + 'px',
              top: det.bbox.y + 'px',
              width: det.bbox.width + 'px',
              height: det.bbox.height + 'px',
              borderColor: getBoxColor(det.class),
              backgroundColor: 'rgba(255,255,255,0.1)'
            }"
          >
            <!-- 标签 -->
            <div
              class="absolute -top-8 left-0 px-2 py-1 rounded-t-lg text-xs font-bold text-white whitespace-nowrap"
              :style="{ backgroundColor: getBoxColor(det.class) }"
            >
              {{ det.label.split(' / ')[0] }} {{ (det.confidence * 100).toFixed(0) }}%
            </div>
          </div>

          <!-- 加载动画 -->
          <div
            v-if="isLoading"
            class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center"
          >
            <div class="text-center text-white">
              <div class="animate-spin w-16 h-16 border-4 border-white border-t-transparent rounded-full mx-auto mb-4"></div>
              <p class="text-xl font-medium">正在检测中...</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 检测结果详情 -->
      <div class="space-y-6">
        <!-- 检测统计 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">检测统计</h3>
          <div v-if="!result" class="text-center text-gray-400 py-8">
            <p>点击"开始检测"按钮进行分析</p>
          </div>
          <div v-else class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-blue-50 rounded-lg p-4 text-center">
                <p class="text-3xl font-bold text-blue-600">{{ result.total_detections }}</p>
                <p class="text-sm text-gray-500">检测总数</p>
              </div>
              <div class="bg-green-50 rounded-lg p-4 text-center">
                <p class="text-3xl font-bold text-green-600">{{ result.health_count }}</p>
                <p class="text-sm text-gray-500">健康区域</p>
              </div>
              <div class="bg-red-50 rounded-lg p-4 text-center">
                <p class="text-3xl font-bold text-red-600">{{ result.disease_count }}</p>
                <p class="text-sm text-gray-500">病害区域</p>
              </div>
              <div class="bg-orange-50 rounded-lg p-4 text-center">
                <p class="text-lg font-bold text-orange-600">{{ result.summary.severity }}</p>
                <p class="text-sm text-gray-500">严重程度</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 检测详情列表 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">检测详情</h3>
          <div v-if="!result" class="text-center text-gray-400 py-8">
            <p>暂无检测数据</p>
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="(det, index) in result.detections"
              :key="index"
              class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg"
            >
              <div
                class="w-12 h-12 rounded-lg flex items-center justify-center"
                :style="{ backgroundColor: getBoxColor(det.class) + '20' }"
              >
                <div
                  class="w-4 h-4 rounded-full"
                  :style="{ backgroundColor: getBoxColor(det.class) }"
                ></div>
              </div>
              <div class="flex-1">
                <p class="font-bold text-gray-800">{{ det.label.split(' / ')[0] }}</p>
                <p class="text-sm text-gray-500">{{ det.label.split(' / ')[1] }}</p>
              </div>
              <div class="text-right">
                <p class="text-2xl font-bold" :style="{ color: getBoxColor(det.class) }">
                  {{ (det.confidence * 100).toFixed(0) }}%
                </p>
                <p class="text-xs text-gray-400">置信度</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 建议 -->
        <div v-if="result" class="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg">
          <h3 class="text-lg font-bold mb-3">防治建议</h3>
          <p class="text-green-100">{{ result.summary.recommendation }}</p>
        </div>

        <!-- 开始检测按钮 -->
        <button
          v-if="!result"
          @click="startDetection"
          :disabled="isLoading"
          class="w-full bg-green-500 text-white py-4 rounded-xl font-bold text-lg hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isLoading ? '检测中...' : '开始检测' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.border-3 {
  border-width: 3px;
}
</style>
