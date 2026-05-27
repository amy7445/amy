<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface HistoryItem {
  id: string
  imageUrl: string
  timestamp: string
  diseaseCount: number
  healthCount: number
  confidence: number
  detections: Array<{
    className: string
    classNameEn: string
    confidence: number
  }>
}

const historyRecords = ref<HistoryItem[]>([
  {
    id: 'IMG_20240115_001',
    imageUrl: 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=agricultural%20crop%20leaf%20with%20disease%20symptoms%20white%20mold%20on%20green%20leaf&image_size=square',
    timestamp: '2024-01-15 14:30:25',
    diseaseCount: 2,
    healthCount: 1,
    confidence: 0.87,
    detections: [
      { className: '白粉病', classNameEn: 'Powdery Mildew', confidence: 0.87 },
      { className: '叶斑病', classNameEn: 'Leaf Spot', confidence: 0.72 }
    ]
  },
  {
    id: 'IMG_20240115_002',
    imageUrl: 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=corn%20plant%20leaf%20with%20rust%20disease%20orange%20spots&image_size=square',
    timestamp: '2024-01-15 10:22:18',
    diseaseCount: 1,
    healthCount: 3,
    confidence: 0.91,
    detections: [
      { className: '锈病', classNameEn: 'Rust', confidence: 0.91 }
    ]
  },
  {
    id: 'IMG_20240114_001',
    imageUrl: 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=tomato%20plant%20leaf%20with%20early%20blight%20disease%20dark%20brown%20spots&image_size=square',
    timestamp: '2024-01-14 16:45:33',
    diseaseCount: 1,
    healthCount: 2,
    confidence: 0.85,
    detections: [
      { className: '早疫病', classNameEn: 'Early Blight', confidence: 0.85 }
    ]
  },
  {
    id: 'IMG_20240114_002',
    imageUrl: 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=healthy%20green%20rice%20leaves%20agricultural%20field&image_size=square',
    timestamp: '2024-01-14 09:15:42',
    diseaseCount: 0,
    healthCount: 4,
    confidence: 1.0,
    detections: []
  },
  {
    id: 'IMG_20240113_001',
    imageUrl: 'https://neeko-copilot.bytedance.net/api/text_to_image?prompt=wheat%20plant%20with%20powdery%20mildew%20white%20fungal%20growth&image_size=square',
    timestamp: '2024-01-13 11:30:55',
    diseaseCount: 3,
    healthCount: 0,
    confidence: 0.78,
    detections: [
      { className: '白粉病', classNameEn: 'Powdery Mildew', confidence: 0.78 }
    ]
  }
])

function goBack() {
  router.push('/detect/image')
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-800">图片检测历史记录</h2>
      <button
        @click="goBack"
        class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
      >
        返回
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="record in historyRecords"
        :key="record.id"
        class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow"
      >
        <div class="relative">
          <img
            :src="record.imageUrl"
            :alt="'检测记录 ' + record.id"
            class="w-full h-48 object-cover"
          />
          <div
            :class="[
              'absolute top-2 right-2 px-2 py-1 rounded text-xs font-medium',
              record.diseaseCount > 0 ? 'bg-red-500 text-white' : 'bg-green-500 text-white'
            ]"
          >
            {{ record.diseaseCount > 0 ? '检测到病害' : '健康' }}
          </div>
        </div>
        <div class="p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-gray-500">{{ record.timestamp }}</span>
            <span class="text-sm font-medium text-gray-700">ID: {{ record.id }}</span>
          </div>
          <div class="flex items-center gap-4 text-sm text-gray-600 mb-3">
            <span>病害: {{ record.diseaseCount }}</span>
            <span>健康: {{ record.healthCount }}</span>
          </div>
          <div v-if="record.detections.length > 0" class="space-y-2">
            <div
              v-for="(det, index) in record.detections"
              :key="index"
              class="flex items-center justify-between text-sm"
            >
              <div>
                <span class="font-medium text-gray-800">{{ det.className }}</span>
                <span class="text-gray-400 ml-1">({{ det.classNameEn }})</span>
              </div>
              <span :class="[
                'px-2 py-0.5 rounded text-xs font-medium',
                det.confidence >= 0.8 ? 'bg-green-100 text-green-700' :
                det.confidence >= 0.5 ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'
              ]">
                {{ (det.confidence * 100).toFixed(0) }}%
              </span>
            </div>
          </div>
          <div v-else class="text-sm text-green-600 font-medium">
            ✓ 未检测到病害
          </div>
        </div>
      </div>
    </div>

    <div v-if="historyRecords.length === 0" class="bg-white rounded-xl p-12 text-center shadow-md">
      <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="text-gray-500">暂无检测记录</p>
    </div>
  </div>
</template>
