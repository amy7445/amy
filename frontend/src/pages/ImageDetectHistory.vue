<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDetectionStore, type DetectionRecord } from '@/stores/detection'

const router = useRouter()
const detectionStore = useDetectionStore()

const historyRecords = ref<DetectionRecord[]>([])
const isLoading = ref(true)

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

const formattedRecords = ref<HistoryItem[]>([])

function formatRecords(records: DetectionRecord[]) {
  return records.map(record => {
    const diseaseCount = record.detections.filter(d => d.label !== 'healthy').length
    const healthCount = record.detections.filter(d => d.label === 'healthy').length
    const avgConfidence = record.detections.length > 0
      ? record.detections.reduce((sum, d) => sum + d.confidence, 0) / record.detections.length
      : 1.0

    return {
      id: record.id,
      imageUrl: record.result_image || '',
      timestamp: record.created_at,
      diseaseCount,
      healthCount,
      confidence: avgConfidence,
      detections: record.detections.filter(d => d.label !== 'healthy').map(d => ({
        className: d.label,
        classNameEn: d.label_en,
        confidence: d.confidence
      }))
    }
  })
}

async function loadHistory() {
  isLoading.value = true
  try {
    await detectionStore.fetchHistory(1, 100)
    historyRecords.value = detectionStore.history
    formattedRecords.value = formatRecords(detectionStore.history)
  } catch (error) {
    console.error('加载历史记录失败:', error)
    formattedRecords.value = []
  } finally {
    isLoading.value = false
  }
}

function goBack() {
  router.push('/detect/image')
}

onMounted(() => {
  loadHistory()
})
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

    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin w-12 h-12 border-4 border-green-500 border-t-transparent rounded-full"></div>
    </div>

    <div v-else-if="formattedRecords.length === 0" class="bg-white rounded-xl p-12 text-center shadow-md">
      <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="text-gray-500">暂无检测记录</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="record in formattedRecords"
        :key="record.id"
        class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow"
      >
        <div class="relative">
          <img
            v-if="record.imageUrl"
            :src="record.imageUrl"
            :alt="'检测记录 ' + record.id"
            class="w-full h-48 object-cover"
          />
          <div v-else class="w-full h-48 bg-gray-100 flex items-center justify-center">
            <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
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
  </div>
</template>