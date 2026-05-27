<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

// 预测数据
const predictionData = ref({
  currentWeek: {
    powdery_mildew: 156,
    leaf_spot: 89,
    rust: 45,
    early_blight: 32,
    healthy: 178
  },
  nextWeek: {
    powdery_mildew: 182,
    leaf_spot: 95,
    rust: 52,
    early_blight: 38,
    healthy: 165
  },
  changeRate: {
    powdery_mildew: 16.7,
    leaf_spot: 6.7,
    rust: 15.6,
    early_blight: 18.8,
    healthy: -7.3
  }
})

// 预警信息
const alerts = ref([
  {
    level: 'warning',
    disease: '白粉病',
    message: '未来7天白粉病发病风险较高，建议提前预防',
    time: '高风险'
  },
  {
    level: 'info',
    disease: '叶斑病',
    message: '叶斑病发病率将略有上升，注意田间管理',
    time: '中风险'
  }
])

// 图表
let trendChart: echarts.ECharts | null = null
let comparisonChart: echarts.ECharts | null = null
const trendChartRef = ref<HTMLDivElement | null>(null)
const comparisonChartRef = ref<HTMLDivElement | null>(null)

// 月份数据
const months = ['1月', '2月', '3月', '4月', '5月', '6月']
const diseaseData = {
  powdery_mildew: [45, 52, 78, 125, 168, 156],
  leaf_spot: [28, 35, 52, 68, 82, 89],
  rust: [12, 18, 28, 35, 42, 45],
  early_blight: [8, 12, 18, 25, 30, 32]
}

function initTrendChart() {
  if (!trendChartRef.value) return

  trendChart = echarts.init(trendChartRef.value)
  trendChart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#A3E4A3',
      textStyle: { color: '#1A1A1A' }
    },
    legend: {
      data: ['白粉病', '叶斑病', '锈病', '早疫病'],
      bottom: 0,
      textStyle: { color: '#666' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: months,
      axisLine: { lineStyle: { color: '#A3E4A3' } },
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: '#f0f0f0' } },
      axisLabel: { color: '#666' }
    },
    series: [
      {
        name: '白粉病',
        type: 'line',
        smooth: true,
        data: diseaseData.powdery_mildew,
        itemStyle: { color: '#ff6b6b' },
        lineStyle: { width: 3 }
      },
      {
        name: '叶斑病',
        type: 'line',
        smooth: true,
        data: diseaseData.leaf_spot,
        itemStyle: { color: '#ffd93d' },
        lineStyle: { width: 3 }
      },
      {
        name: '锈病',
        type: 'line',
        smooth: true,
        data: diseaseData.rust,
        itemStyle: { color: '#ff8c42' },
        lineStyle: { width: 3 }
      },
      {
        name: '早疫病',
        type: 'line',
        smooth: true,
        data: diseaseData.early_blight,
        itemStyle: { color: '#6bcb77' },
        lineStyle: { width: 3 }
      }
    ]
  })
}

function initComparisonChart() {
  if (!comparisonChartRef.value) return

  comparisonChart = echarts.init(comparisonChartRef.value)
  comparisonChart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#A3E4A3',
      textStyle: { color: '#1A1A1A' },
      axisPointer: { type: 'shadow' }
    },
    legend: {
      data: ['本周', '下周预测'],
      bottom: 0,
      textStyle: { color: '#666' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['白粉病', '叶斑病', '锈病', '早疫病', '健康'],
      axisLine: { lineStyle: { color: '#A3E4A3' } },
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: '#f0f0f0' } },
      axisLabel: { color: '#666' }
    },
    series: [
      {
        name: '本周',
        type: 'bar',
        data: [
          predictionData.value.currentWeek.powdery_mildew,
          predictionData.value.currentWeek.leaf_spot,
          predictionData.value.currentWeek.rust,
          predictionData.value.currentWeek.early_blight,
          predictionData.value.currentWeek.healthy
        ],
        itemStyle: { color: '#4CAF50' },
        barWidth: '30%'
      },
      {
        name: '下周预测',
        type: 'bar',
        data: [
          predictionData.value.nextWeek.powdery_mildew,
          predictionData.value.nextWeek.leaf_spot,
          predictionData.value.nextWeek.rust,
          predictionData.value.nextWeek.early_blight,
          predictionData.value.nextWeek.healthy
        ],
        itemStyle: { color: '#ff9800' },
        barWidth: '30%'
      }
    ]
  })
}

function handleResize() {
  trendChart?.resize()
  comparisonChart?.resize()
}

onMounted(() => {
  setTimeout(() => {
    initTrendChart()
    initComparisonChart()
  }, 100)

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  trendChart?.dispose()
  comparisonChart?.dispose()
})

// 获取变化颜色
function getChangeColor(rate: number): string {
  if (rate > 0) return 'text-red-600'
  if (rate < 0) return 'text-green-600'
  return 'text-gray-600'
}

function getChangeIcon(rate: number): string {
  if (rate > 0) return '↑'
  if (rate < 0) return '↓'
  return '→'
}
</script>

<template>
  <div class="space-y-6">
    <!-- 预警信息 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="(alert, index) in alerts"
        :key="index"
        :class="[
          'rounded-xl p-6 shadow-md border-l-4',
          alert.level === 'warning' ? 'bg-orange-50 border-orange-500' : 'bg-blue-50 border-blue-500'
        ]"
      >
        <div class="flex items-start gap-4">
          <div :class="[
            'w-12 h-12 rounded-full flex items-center justify-center',
            alert.level === 'warning' ? 'bg-orange-100' : 'bg-blue-100'
          ]">
            <svg v-if="alert.level === 'warning'" class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <svg v-else class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="flex-1">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-bold text-gray-800">{{ alert.disease }}预警</h3>
              <span :class="[
                'px-3 py-1 rounded-full text-sm font-medium',
                alert.level === 'warning' ? 'bg-orange-200 text-orange-800' : 'bg-blue-200 text-blue-800'
              ]">
                {{ alert.time }}
              </span>
            </div>
            <p class="text-gray-600">{{ alert.message }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 趋势图表 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 历史趋势 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">近6个月发病趋势</h3>
        <div ref="trendChartRef" class="h-80"></div>
      </div>

      <!-- 周对比预测 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">本周 vs 下周预测</h3>
        <div ref="comparisonChartRef" class="h-80"></div>
      </div>
    </div>

    <!-- 预测统计 -->
    <div class="bg-white rounded-xl p-6 shadow-md">
      <h3 class="text-lg font-bold text-gray-800 mb-4">下周预测详情</h3>
      <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div class="bg-red-50 rounded-xl p-4 text-center">
          <p class="text-sm text-gray-500 mb-2">白粉病</p>
          <p class="text-2xl font-bold text-red-600">{{ predictionData.nextWeek.powdery_mildew }}</p>
          <p class="text-sm mt-1" :class="getChangeColor(predictionData.changeRate.powdery_mildew)">
            {{ getChangeIcon(predictionData.changeRate.powdery_mildew) }}
            {{ Math.abs(predictionData.changeRate.powdery_mildew) }}%
          </p>
        </div>
        <div class="bg-yellow-50 rounded-xl p-4 text-center">
          <p class="text-sm text-gray-500 mb-2">叶斑病</p>
          <p class="text-2xl font-bold text-yellow-600">{{ predictionData.nextWeek.leaf_spot }}</p>
          <p class="text-sm mt-1" :class="getChangeColor(predictionData.changeRate.leaf_spot)">
            {{ getChangeIcon(predictionData.changeRate.leaf_spot) }}
            {{ Math.abs(predictionData.changeRate.leaf_spot) }}%
          </p>
        </div>
        <div class="bg-orange-50 rounded-xl p-4 text-center">
          <p class="text-sm text-gray-500 mb-2">锈病</p>
          <p class="text-2xl font-bold text-orange-600">{{ predictionData.nextWeek.rust }}</p>
          <p class="text-sm mt-1" :class="getChangeColor(predictionData.changeRate.rust)">
            {{ getChangeIcon(predictionData.changeRate.rust) }}
            {{ Math.abs(predictionData.changeRate.rust) }}%
          </p>
        </div>
        <div class="bg-green-50 rounded-xl p-4 text-center">
          <p class="text-sm text-gray-500 mb-2">早疫病</p>
          <p class="text-2xl font-bold text-green-600">{{ predictionData.nextWeek.early_blight }}</p>
          <p class="text-sm mt-1" :class="getChangeColor(predictionData.changeRate.early_blight)">
            {{ getChangeIcon(predictionData.changeRate.early_blight) }}
            {{ Math.abs(predictionData.changeRate.early_blight) }}%
          </p>
        </div>
        <div class="bg-blue-50 rounded-xl p-4 text-center">
          <p class="text-sm text-gray-500 mb-2">健康</p>
          <p class="text-2xl font-bold text-blue-600">{{ predictionData.nextWeek.healthy }}</p>
          <p class="text-sm mt-1" :class="getChangeColor(predictionData.changeRate.healthy)">
            {{ getChangeIcon(predictionData.changeRate.healthy) }}
            {{ Math.abs(predictionData.changeRate.healthy) }}%
          </p>
        </div>
      </div>
    </div>

    <!-- 防治建议 -->
    <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg">
      <h3 class="text-lg font-bold mb-4">智能防治建议</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-white bg-opacity-20 rounded-lg p-4">
          <h4 class="font-bold mb-2">白粉病预防</h4>
          <p class="text-green-100 text-sm">保持田间通风，及时清除病叶，喷施多菌灵或百菌清</p>
        </div>
        <div class="bg-white bg-opacity-20 rounded-lg p-4">
          <h4 class="font-bold mb-2">叶斑病预防</h4>
          <p class="text-green-100 text-sm">加强排水，避免过度灌溉，发病初期使用代森锰锌</p>
        </div>
        <div class="bg-white bg-opacity-20 rounded-lg p-4">
          <h4 class="font-bold mb-2">锈病预防</h4>
          <p class="text-green-100 text-sm">增施磷钾肥，提高植株抗病性，发现病株立即清除</p>
        </div>
      </div>
    </div>
  </div>
</template>
