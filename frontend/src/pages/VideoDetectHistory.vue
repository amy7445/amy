<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface HistoryItem {
  id: string
  fileName: string
  timestamp: string
  totalFrames: number
  diseaseFrames: number
  detectionRate: number
  categories: Array<{
    name: string
    nameEn: string
    count: number
    frames: number
    percentage: number
    avgConfidence: number
  }>
}

const historyRecords = ref<HistoryItem[]>([
  {
    id: 'VID_20240115_001',
    fileName: 'crop_disease_detection.mp4',
    timestamp: '2024-01-15 15:45:30',
    totalFrames: 1200,
    diseaseFrames: 892,
    detectionRate: 74.3,
    categories: [
      { name: '白粉病', nameEn: 'Powdery Mildew', count: 342, frames: 452, percentage: 37.7, avgConfidence: 0.82 },
      { name: '叶斑病', nameEn: 'Leaf Spot', count: 256, frames: 286, percentage: 23.8, avgConfidence: 0.76 },
      { name: '锈病', nameEn: 'Rust', count: 189, frames: 154, percentage: 12.8, avgConfidence: 0.89 }
    ]
  },
  {
    id: 'VID_20240115_002',
    fileName: 'wheat_field_inspection.mp4',
    timestamp: '2024-01-15 11:20:15',
    totalFrames: 1800,
    diseaseFrames: 324,
    detectionRate: 18.0,
    categories: [
      { name: '白粉病', nameEn: 'Powdery Mildew', count: 156, frames: 198, percentage: 11.0, avgConfidence: 0.85 }
    ]
  },
  {
    id: 'VID_20240114_001',
    fileName: 'tomato_plants.mp4',
    timestamp: '2024-01-14 14:30:00',
    totalFrames: 900,
    diseaseFrames: 693,
    detectionRate: 77.0,
    categories: [
      { name: '早疫病', nameEn: 'Early Blight', count: 234, frames: 342, percentage: 38.0, avgConfidence: 0.91 },
      { name: '叶斑病', nameEn: 'Leaf Spot', count: 189, frames: 225, percentage: 25.0, avgConfidence: 0.78 },
      { name: '白粉病', nameEn: 'Powdery Mildew', count: 123, frames: 126, percentage: 14.0, avgConfidence: 0.83 }
    ]
  },
  {
    id: 'VID_20240113_001',
    fileName: 'rice_field.mp4',
    timestamp: '2024-01-13 09:15:45',
    totalFrames: 2400,
    diseaseFrames: 0,
    detectionRate: 0,
    categories: []
  }
])

function goBack() {
  router.push('/detect/video')
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-800">视频检测历史记录</h2>
      <button
        @click="goBack"
        class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
      >
        返回
      </button>
    </div>

    <div class="space-y-4">
      <div
        v-for="record in historyRecords"
        :key="record.id"
        class="bg-white rounded-xl shadow-md overflow-hidden"
      >
        <div class="p-4 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="font-medium text-gray-800">{{ record.fileName }}</p>
                <p class="text-sm text-gray-500">{{ record.timestamp }} · ID: {{ record.id }}</p>
              </div>
            </div>
            <div class="flex items-center gap-6">
              <div class="text-center">
                <p class="text-xl font-bold text-gray-800">{{ record.totalFrames }}</p>
                <p class="text-xs text-gray-500">总帧数</p>
              </div>
              <div class="text-center">
                <p class="text-xl font-bold" :class="record.diseaseFrames > 0 ? 'text-red-500' : 'text-green-500'">
                  {{ record.diseaseFrames }}
                </p>
                <p class="text-xs text-gray-500">病害帧数</p>
              </div>
              <div class="text-center">
                <p class="text-xl font-bold" :class="record.detectionRate > 50 ? 'text-red-500' : record.detectionRate > 20 ? 'text-yellow-500' : 'text-green-500'">
                  {{ record.detectionRate }}%
                </p>
                <p class="text-xs text-gray-500">检测率</p>
              </div>
            </div>
          </div>
        </div>
        <div v-if="record.categories.length > 0" class="p-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3">类别统计</h4>
          <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-3">
            <div
              v-for="cat in record.categories"
              :key="cat.name"
              class="bg-gray-50 rounded-lg p-3"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-gray-800 text-sm">{{ cat.name }}</span>
                <span class="text-xs text-gray-400">({{ cat.nameEn }})</span>
              </div>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-gray-500">出现:</span>
                  <span class="ml-1 font-medium">{{ cat.count }}次</span>
                </div>
                <div>
                  <span class="text-gray-500">帧数:</span>
                  <span class="ml-1 font-medium">{{ cat.frames }}</span>
                </div>
                <div>
                  <span class="text-gray-500">占比:</span>
                  <span class="ml-1 font-medium">{{ cat.percentage }}%</span>
                </div>
                <div>
                  <span class="text-gray-500">置信度:</span>
                  <span class="ml-1 font-medium">{{ (cat.avgConfidence * 100).toFixed(0) }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="p-4 text-center">
          <span class="text-green-600 font-medium">✓ 视频中未检测到病害</span>
        </div>
      </div>
    </div>

    <div v-if="historyRecords.length === 0" class="bg-white rounded-xl p-12 text-center shadow-md">
      <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-gray-500">暂无检测记录</p>
    </div>
  </div>
</template>
