<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 状态
const isDragging = ref(false)
const selectedFile = ref<File | null>(null)
const videoUrl = ref<string | null>(null)
const isLoading = ref(false)
const result = ref<any>(null)
const uploadProgress = ref(0)

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
  if (!file.type.match(/^video\//)) {
    alert('请上传视频文件')
    return
  }
  selectedFile.value = file
  videoUrl.value = URL.createObjectURL(file)
  result.value = null
}

// 重置
function resetDetection() {
  selectedFile.value = null
  if (videoUrl.value) {
    URL.revokeObjectURL(videoUrl.value)
  }
  videoUrl.value = null
  result.value = null
  uploadProgress.value = 0
}

// 开始检测
async function startDetection() {
  if (!selectedFile.value) return

  isLoading.value = true
  uploadProgress.value = 0

  // 模拟上传和检测进度
  for (let i = 0; i <= 100; i += 5) {
    await new Promise(resolve => setTimeout(resolve, 100))
    uploadProgress.value = i
  }

  // 模拟检测结果
  result.value = {
    total_frames: 480,
    disease_frames: 370,
    health_frames: 110,
    disease_rate: 0.771,
    categories: [
      {
        name: '白粉病 / Powdery Mildew',
        count: 198,
        frame_count: 198,
        percentage: 0.535,
        avg_confidence: 0.89
      },
      {
        name: '叶斑病 / Leaf Spot',
        count: 124,
        frame_count: 124,
        percentage: 0.335,
        avg_confidence: 0.84
      },
      {
        name: '锈病 / Rust',
        count: 48,
        frame_count: 48,
        percentage: 0.130,
        avg_confidence: 0.78
      }
    ],
    top_frames: [
      { frame_id: 15, label: '白粉病 / Powdery Mildew', confidence: 0.94, timestamp: '00:00:15' },
      { frame_id: 32, label: '叶斑病 / Leaf Spot', confidence: 0.91, timestamp: '00:00:32' },
      { frame_id: 48, label: '白粉病 / Powdery Mildew', confidence: 0.93, timestamp: '00:00:48' },
      { frame_id: 67, label: '叶斑病 / Leaf Spot', confidence: 0.88, timestamp: '00:01:07' },
      { frame_id: 89, label: '白粉病 / Powdery Mildew', confidence: 0.92, timestamp: '00:01:29' },
      { frame_id: 112, label: '锈病 / Rust', confidence: 0.85, timestamp: '00:01:52' },
      { frame_id: 135, label: '白粉病 / Powdery Mildew', confidence: 0.90, timestamp: '00:02:15' },
      { frame_id: 158, label: '叶斑病 / Leaf Spot', confidence: 0.87, timestamp: '00:02:38' },
      { frame_id: 181, label: '白粉病 / Powdery Mildew', confidence: 0.91, timestamp: '00:03:01' },
      { frame_id: 204, label: '叶斑病 / Leaf Spot', confidence: 0.86, timestamp: '00:03:24' },
      { frame_id: 227, label: '锈病 / Rust', confidence: 0.82, timestamp: '00:03:47' },
      { frame_id: 250, label: '白粉病 / Powdery Mildew', confidence: 0.89, timestamp: '00:04:10' }
    ]
  }

  isLoading.value = false
}

// 获取标签颜色
function getLabelColor(label: string): string {
  if (label.includes('白粉病')) return '#ff6b6b'
  if (label.includes('叶斑病')) return '#ffd93d'
  if (label.includes('锈病')) return '#ff8c42'
  if (label.includes('早疫病')) return '#6bcb77'
  return '#2ed573'
}
</script>

<template>
  <div class="space-y-6">
    <!-- 操作按钮 -->
    <div class="flex justify-end">
      <button
        @click="router.push('/detect/video/history')"
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
        <div class="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </div>
        <p class="text-2xl text-gray-700 mb-2 font-medium">拖拽视频到这里</p>
        <p class="text-gray-500 mb-6">支持 MP4、AVI、MOV 等格式</p>
        <label class="inline-block">
          <span class="inline-block bg-blue-500 text-white px-8 py-3 rounded-lg font-medium cursor-pointer hover:bg-blue-600 transition-colors">
            选择视频
          </span>
          <input
            type="file"
            accept="video/*"
            class="hidden"
            @change="handleFileInput"
          />
        </label>
      </div>
    </div>

    <!-- 已选择视频 -->
    <div v-else class="space-y-6">
      <!-- 视频预览 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-800">视频预览</h3>
          <button
            @click="resetDetection"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            重新选择
          </button>
        </div>

        <div class="flex items-center gap-4 mb-4">
          <div class="w-16 h-16 bg-blue-100 rounded-xl flex items-center justify-center">
            <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
          <div class="flex-1">
            <p class="font-medium text-gray-800">{{ selectedFile.name }}</p>
            <p class="text-sm text-gray-500">
              {{ (selectedFile.size / 1024 / 1024).toFixed(2) }} MB
            </p>
          </div>
        </div>

        <div v-if="videoUrl" class="rounded-xl overflow-hidden bg-black">
          <video
            :src="videoUrl"
            class="w-full"
            style="max-height: 400px;"
            controls
          />
        </div>
      </div>

      <!-- 上传进度 -->
      <div v-if="isLoading" class="bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">检测进度</h3>
        <div class="mb-2">
          <div class="flex items-center justify-between text-sm text-gray-600 mb-2">
            <span>正在处理视频...</span>
            <span class="font-mono font-bold text-green-600">{{ uploadProgress }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-3">
            <div
              class="bg-gradient-to-r from-green-500 to-green-600 h-3 rounded-full transition-all duration-300"
              :style="{ width: uploadProgress + '%' }"
            ></div>
          </div>
        </div>
        <p class="text-center text-gray-500 text-sm mt-4">正在进行逐帧检测，请稍候...</p>
      </div>

      <!-- 开始检测按钮 -->
      <button
        v-if="!result && !isLoading"
        @click="startDetection"
        class="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:from-blue-600 hover:to-blue-700 transition-all shadow-lg"
      >
        开始逐帧检测
      </button>

      <!-- 检测结果 -->
      <div v-if="result" class="space-y-6">
        <!-- 统计概览 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-blue-100 text-sm mb-1">总帧数</p>
                <p class="text-4xl font-bold">{{ result.total_frames }}</p>
              </div>
              <div class="w-16 h-16 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-gradient-to-br from-red-500 to-red-600 rounded-xl p-6 text-white shadow-lg">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-red-100 text-sm mb-1">病害帧数</p>
                <p class="text-4xl font-bold">{{ result.disease_frames }}</p>
              </div>
              <div class="w-16 h-16 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-green-100 text-sm mb-1">帧检测率</p>
                <p class="text-4xl font-bold">{{ (result.disease_rate * 100).toFixed(1) }}%</p>
              </div>
              <div class="w-16 h-16 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- 各类别统计 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">各类别统计</h3>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-gray-200">
                  <th class="text-left py-3 px-4 text-sm font-semibold text-gray-700">病害类别</th>
                  <th class="text-center py-3 px-4 text-sm font-semibold text-gray-700">出现次数</th>
                  <th class="text-center py-3 px-4 text-sm font-semibold text-gray-700">帧数</th>
                  <th class="text-center py-3 px-4 text-sm font-semibold text-gray-700">占比</th>
                  <th class="text-center py-3 px-4 text-sm font-semibold text-gray-700">平均置信度</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(cat, index) in result.categories"
                  :key="index"
                  class="border-b border-gray-100 hover:bg-gray-50 transition-colors"
                >
                  <td class="py-3 px-4">
                    <div class="flex items-center gap-2">
                      <div
                        class="w-3 h-3 rounded-full"
                        :style="{ backgroundColor: getLabelColor(cat.name) }"
                      ></div>
                      <span class="font-medium text-gray-800">{{ cat.name }}</span>
                    </div>
                  </td>
                  <td class="text-center py-3 px-4 font-mono text-gray-600">{{ cat.count }}</td>
                  <td class="text-center py-3 px-4 font-mono text-gray-600">{{ cat.frame_count }}</td>
                  <td class="text-center py-3 px-4">
                    <div class="flex items-center justify-center gap-2">
                      <div class="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          class="h-2 rounded-full"
                          :style="{
                            width: (cat.percentage * 100) + '%',
                            backgroundColor: getLabelColor(cat.name)
                          }"
                        ></div>
                      </div>
                      <span class="font-mono text-sm text-gray-600">{{ (cat.percentage * 100).toFixed(1) }}%</span>
                    </div>
                  </td>
                  <td class="text-center py-3 px-4">
                    <span class="font-mono font-bold" :style="{ color: getLabelColor(cat.name) }">
                      {{ (cat.avg_confidence * 100).toFixed(0) }}%
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 前N帧详情 -->
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">前 {{ result.top_frames.length }} 帧详情</h3>
          <div class="space-y-3">
            <div
              v-for="(frame, index) in result.top_frames"
              :key="index"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors"
            >
              <div class="flex items-center gap-4">
                <div
                  class="w-14 h-14 rounded-xl flex items-center justify-center font-bold text-white"
                  :style="{ backgroundColor: getLabelColor(frame.label) }"
                >
                  #{{ frame.frame_id }}
                </div>
                <div>
                  <p class="font-bold text-gray-800">{{ frame.label.split(' / ')[0] }}</p>
                  <p class="text-sm text-gray-500">{{ frame.label.split(' / ')[1] }} · {{ frame.timestamp }}</p>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <div class="w-32 bg-gray-200 rounded-full h-2">
                  <div
                    class="h-2 rounded-full"
                    :style="{
                      width: (frame.confidence * 100) + '%',
                      backgroundColor: getLabelColor(frame.label)
                    }"
                  ></div>
                </div>
                <span class="font-mono font-bold text-lg" :style="{ color: getLabelColor(frame.label) }">
                  {{ (frame.confidence * 100).toFixed(0) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.border-3 {
  border-width: 3px;
}
</style>
