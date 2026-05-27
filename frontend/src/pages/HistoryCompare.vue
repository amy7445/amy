<script setup lang="ts">
import { ref } from 'vue'

// 历史记录列表
const historyRecords = ref([
  {
    id: 1,
    date: '2024-03-15',
    type: '图片',
    image: 'https://via.placeholder.com/150',
    result: '白粉病',
    count: 5,
    severity: '中等'
  },
  {
    id: 2,
    date: '2024-03-10',
    type: '图片',
    image: 'https://via.placeholder.com/150',
    result: '叶斑病',
    count: 3,
    severity: '轻度'
  },
  {
    id: 3,
    date: '2024-03-05',
    type: '视频',
    image: 'https://via.placeholder.com/150',
    result: '锈病',
    count: 12,
    severity: '严重'
  },
  {
    id: 4,
    date: '2024-02-28',
    type: '图片',
    image: 'https://via.placeholder.com/150',
    result: '健康',
    count: 0,
    severity: '-'
  }
])

// 选中的记录进行对比
const selectedRecords = ref<number[]>([])
const comparisonResult = ref<any>(null)

// 选择记录
function toggleSelect(id: number) {
  const index = selectedRecords.value.indexOf(id)
  if (index > -1) {
    selectedRecords.value.splice(index, 1)
  } else if (selectedRecords.value.length < 2) {
    selectedRecords.value.push(id)
  }
}

// 进行对比
function compareRecords() {
  if (selectedRecords.value.length !== 2) {
    alert('请选择两条记录进行对比')
    return
  }

  const record1 = historyRecords.value.find(r => r.id === selectedRecords.value[0])
  const record2 = historyRecords.value.find(r => r.id === selectedRecords.value[1])

  if (!record1 || !record2) return

  // 模拟对比结果
  comparisonResult.value = {
    record1: {
      date: record1.date,
      type: record1.type,
      result: record1.result,
      count: record1.count,
      severity: record1.severity
    },
    record2: {
      date: record2.date,
      type: record2.type,
      result: record2.result,
      count: record2.count,
      severity: record2.severity
    },
    changes: {
      countChange: record2.count - record1.count,
      countChangePercent: record1.count > 0 ? ((record2.count - record1.count) / record1.count * 100).toFixed(1) : '0',
      effectiveness: record1.count > 0 && record2.count < record1.count ? '有效' : '待观察'
    }
  }
}

// 清除选择
function clearSelection() {
  selectedRecords.value = []
  comparisonResult.value = null
}

// 获取严重程度颜色
function getSeverityColor(severity: string): string {
  switch (severity) {
    case '严重': return 'text-red-600 bg-red-100'
    case '中等': return 'text-orange-600 bg-orange-100'
    case '轻度': return 'text-yellow-600 bg-yellow-100'
    default: return 'text-green-600 bg-green-100'
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="bg-yellow-50 border border-yellow-200 rounded-xl p-4 flex items-center gap-3">
      <svg class="w-5 h-5 text-yellow-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span class="text-yellow-800 text-sm">
        <strong>注意：</strong>当前显示的是模拟数据，实际数据将在连接真实后端后自动更新。
      </span>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 历史记录列表 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-gray-800">历史检测记录</h3>
          <span class="text-sm text-gray-500">
            已选择 {{ selectedRecords.length }}/2 条
          </span>
        </div>

        <div class="space-y-4">
          <div
            v-for="record in historyRecords"
            :key="record.id"
            @click="toggleSelect(record.id)"
            :class="[
              'p-4 rounded-xl border-2 cursor-pointer transition-all',
              selectedRecords.includes(record.id)
                ? 'border-green-500 bg-green-50'
                : 'border-gray-200 hover:border-gray-300'
            ]"
          >
            <div class="flex items-center gap-4">
              <div class="relative">
                <img
                  :src="record.image"
                  alt="检测图片"
                  class="w-20 h-20 rounded-lg object-cover"
                />
                <div
                  v-if="selectedRecords.includes(record.id)"
                  class="absolute -top-2 -right-2 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center"
                >
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </div>
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <span class="font-medium text-gray-800">{{ record.result }}</span>
                  <span :class="['px-2 py-0.5 rounded text-xs font-medium', getSeverityColor(record.severity)]">
                    {{ record.severity }}
                  </span>
                </div>
                <p class="text-sm text-gray-500">
                  {{ record.type }} · {{ record.date }}
                </p>
                <p class="text-sm text-gray-600 mt-1">
                  检测数量：<span class="font-bold">{{ record.count }}</span>
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="mt-6 flex gap-4">
          <button
            @click="compareRecords"
            :disabled="selectedRecords.length !== 2"
            class="flex-1 bg-green-500 text-white py-3 rounded-lg font-bold hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            对比分析
          </button>
          <button
            @click="clearSelection"
            class="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
          >
            清除选择
          </button>
        </div>
      </div>

      <!-- 对比结果 -->
      <div class="space-y-6">
        <!-- 对比结果展示 -->
        <div v-if="comparisonResult" class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">对比结果</h3>

          <!-- 两条记录对比 -->
          <div class="grid grid-cols-2 gap-4 mb-6">
            <!-- 记录1 -->
            <div class="bg-blue-50 rounded-xl p-4">
              <div class="text-sm text-blue-600 mb-2">记录 1</div>
              <p class="font-bold text-gray-800">{{ comparisonResult.record1.result }}</p>
              <p class="text-sm text-gray-500">{{ comparisonResult.record1.date }}</p>
              <p class="text-2xl font-bold text-blue-600 mt-2">
                {{ comparisonResult.record1.count }}
                <span class="text-sm font-normal text-gray-500">检测数量</span>
              </p>
            </div>

            <!-- 记录2 -->
            <div class="bg-green-50 rounded-xl p-4">
              <div class="text-sm text-green-600 mb-2">记录 2</div>
              <p class="font-bold text-gray-800">{{ comparisonResult.record2.result }}</p>
              <p class="text-sm text-gray-500">{{ comparisonResult.record2.date }}</p>
              <p class="text-2xl font-bold text-green-600 mt-2">
                {{ comparisonResult.record2.count }}
                <span class="text-sm font-normal text-gray-500">检测数量</span>
              </p>
            </div>
          </div>

          <!-- 变化统计 -->
          <div class="bg-gray-50 rounded-xl p-4">
            <h4 class="font-medium text-gray-800 mb-3">变化分析</h4>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-gray-600">数量变化</span>
                <span
                  :class="[
                    'font-bold',
                    comparisonResult.changes.countChange > 0 ? 'text-red-600' :
                    comparisonResult.changes.countChange < 0 ? 'text-green-600' : 'text-gray-600'
                  ]"
                >
                  {{ comparisonResult.changes.countChange > 0 ? '+' : '' }}{{ comparisonResult.changes.countChange }}
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-600">变化百分比</span>
                <span
                  :class="[
                    'font-bold',
                    parseFloat(comparisonResult.changes.countChangePercent) > 0 ? 'text-red-600' :
                    parseFloat(comparisonResult.changes.countChangePercent) < 0 ? 'text-green-600' : 'text-gray-600'
                  ]"
                >
                  {{ parseFloat(comparisonResult.changes.countChangePercent) > 0 ? '+' : '' }}{{ comparisonResult.changes.countChangePercent }}%
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-600">防治效果</span>
                <span
                  :class="[
                    'px-3 py-1 rounded-full text-sm font-bold',
                    comparisonResult.changes.effectiveness === '有效' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                  ]"
                >
                  {{ comparisonResult.changes.effectiveness }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="bg-white rounded-xl p-12 shadow-md text-center">
          <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <p class="text-gray-500">请从左侧选择两条历史记录进行对比</p>
        </div>

        <!-- 使用说明 -->
        <div class="bg-blue-50 rounded-xl p-6 border-l-4 border-blue-500">
          <h4 class="font-bold text-gray-800 mb-2">使用说明</h4>
          <ul class="text-sm text-gray-600 space-y-1">
            <li>1. 从左侧列表中选择两条历史检测记录</li>
            <li>2. 点击"对比分析"按钮查看对比结果</li>
            <li>3. 对比结果包括数量变化、百分比变化和效果评估</li>
            <li>4. 负数表示数量减少，正数表示数量增加</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
