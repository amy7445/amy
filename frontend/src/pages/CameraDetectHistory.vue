<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface HistoryItem {
  id: string
  timestamp: string
  duration: string
  totalFrames: number
  diseaseFrames: number
  totalDetections: number
  avgFps: number
  detections: Array<{
    className: string
    classNameEn: string
    confidence: number
    time: string
  }>
}

const historyRecords = ref<HistoryItem[]>([
  {
    id: 'CAM_20240115_001',
    timestamp: '2024-01-15 16:30:00',
    duration: '15:32',
    totalFrames: 23040,
    diseaseFrames: 892,
    totalDetections: 1247,
    avgFps: 25,
    detections: [
      { className: '白粉病', classNameEn: 'Powdery Mildew', confidence: 0.87, time: '00:02:15' },
      { className: '叶斑病', classNameEn: 'Leaf Spot', confidence: 0.72, time: '00:05:33' },
      { className: '白粉病', classNameEn: 'Powdery Mildew', confidence: 0.91, time: '00:08:47' },
      { className: '锈病', classNameEn: 'Rust', confidence: 0.85, time: '00:12:18' }
    ]
  },
  {
    id: 'CAM_20240115_002',
    timestamp: '2024-01-15 08:00:00',
    duration: '30:15',
    totalFrames: 45225,
    diseaseFrames: 1567,
    totalDetections: 2341,
    avgFps: 24.9,
    detections: [
      { className: '早疫病', classNameEn: 'Early Blight', confidence: 0.93, time: '00:03:22' },
      { className: '白粉病', classNameEn: 'Powdery Mildew', confidence: 0.88, time: '00:10:15' },
      { className: '叶斑病', classNameEn: 'Leaf Spot', confidence: 0.76, time: '00:18:44' },
      { className: '早疫病', classNameEn: 'Early Blight', confidence: 0.91, time: '00:25:30' }
    ]
  },
  {
    id: 'CAM_20240114_001',
    timestamp: '2024-01-14 14:20:00',
    duration: '20:00',
    totalFrames: 30000,
    diseaseFrames: 0,
    totalDetections: 0,
    avgFps: 25,
    detections: []
  },
  {
    id: 'CAM_20240113_001',
    timestamp: '2024-01-13 09:00:00',
    duration: '45:00',
    totalFrames: 67500,
    diseaseFrames: 3421,
    totalDetections: 5123,
    avgFps: 24.8,
    detections: [
      { className: '白粉病', classNameEn: 'Powdery Mildew', confidence: 0.82, time: '00:05:10' },
      { className: '锈病', classNameEn: 'Rust', confidence: 0.89, time: '00:12:35' },
      { className: '白粉病', classNameEn: 'Powdery Mildew', confidence: 0.77, time: '00:20:18' },
      { className: '叶斑病', classNameEn: 'Leaf Spot', confidence: 0.84, time: '00:33:42' }
    ]
  }
])

function goBack() {
  router.push('/detect/camera')
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-800">实时检测历史记录</h2>
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
              <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <div>
                <p class="font-medium text-gray-800">检测记录 {{ record.id }}</p>
                <p class="text-sm text-gray-500">{{ record.timestamp }} · 时长: {{ record.duration }}</p>
              </div>
            </div>
            <div class="flex items-center gap-6">
              <div class="text-center">
                <p class="text-xl font-bold text-gray-800">{{ record.avgFps }}</p>
                <p class="text-xs text-gray-500">平均FPS</p>
              </div>
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
                <p class="text-xl font-bold text-gray-800">{{ record.totalDetections }}</p>
                <p class="text-xs text-gray-500">总检测数</p>
              </div>
            </div>
          </div>
        </div>
        <div v-if="record.detections.length > 0" class="p-4">
          <h4 class="text-sm font-medium text-gray-700 mb-3">检测记录（最近4条）</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            <div
              v-for="(det, index) in record.detections"
              :key="index"
              class="bg-gray-50 rounded-lg p-3"
            >
              <div class="flex items-center justify-between mb-1">
                <span class="font-medium text-gray-800 text-sm">{{ det.className }}</span>
                <span class="text-xs text-gray-400">({{ det.classNameEn }})</span>
              </div>
              <div class="flex items-center justify-between text-xs">
                <span class="text-gray-500">时间: {{ det.time }}</span>
                <span :class="[
                  'px-2 py-0.5 rounded font-medium',
                  det.confidence >= 0.8 ? 'bg-green-100 text-green-700' :
                  det.confidence >= 0.5 ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'
                ]">
                  {{ (det.confidence * 100).toFixed(0) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="p-4 text-center">
          <span class="text-green-600 font-medium">✓ 检测期间未发现病害</span>
        </div>
      </div>
    </div>

    <div v-if="historyRecords.length === 0" class="bg-white rounded-xl p-12 text-center shadow-md">
      <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
      </svg>
      <p class="text-gray-500">暂无检测记录</p>
    </div>
  </div>
</template>
