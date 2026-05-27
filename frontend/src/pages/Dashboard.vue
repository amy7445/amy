<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import * as echarts from 'echarts'

const authStore = useAuthStore()

const currentTime = ref(new Date().toLocaleString('zh-CN'))
let timeInterval: number | null = null

// 统计数据
const stats = ref({
  todayCount: 156,
  weekCount: 892,
  totalCount: 12580,
  diseaseRate: 0.342,
  activeCameras: 4,
  alertCount: 3
})

// 实时检测记录
const recentDetections = ref([
  { id: 1, type: '图片', result: '白粉病', confidence: 0.92, time: '刚刚' },
  { id: 2, type: '视频', result: '叶斑病', confidence: 0.87, time: '3分钟前' },
  { id: 3, type: '摄像头', result: '健康', confidence: 0.95, time: '5分钟前' },
  { id: 4, type: '图片', result: '锈病', confidence: 0.78, time: '8分钟前' },
  { id: 5, type: '视频', result: '白粉病', confidence: 0.91, time: '12分钟前' }
])

// 病害分布
const diseaseDistribution = ref([
  { name: '白粉病', count: 423, percentage: 35.2 },
  { name: '叶斑病', count: 312, percentage: 26.0 },
  { name: '锈病', count: 245, percentage: 20.4 },
  { name: '早疫病', count: 156, percentage: 13.0 },
  { name: '其他', count: 66, percentage: 5.4 }
])

// 图表实例
let trendChart: echarts.ECharts | null = null
let pieChart: echarts.ECharts | null = null
const trendChartRef = ref<HTMLDivElement | null>(null)
const pieChartRef = ref<HTMLDivElement | null>(null)

// 7天趋势数据
const weekTrend = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const weekValues = [128, 145, 132, 168, 156, 189, 174]

function initTrendChart() {
  if (!trendChartRef.value) return
  
  trendChart = echarts.init(trendChartRef.value)
  trendChart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#A3E4A3',
      borderWidth: 1,
      textStyle: { color: '#1A1A1A' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: weekTrend,
      axisLine: { lineStyle: { color: '#A3E4A3' } },
      axisLabel: { color: '#666' }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: '#f0f0f0' } },
      axisLabel: { color: '#666' }
    },
    series: [{
      name: '检测次数',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 10,
      itemStyle: {
        color: '#2D5016',
        borderColor: '#fff',
        borderWidth: 3
      },
      lineStyle: { color: '#2D5016', width: 4 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(45,80,22,0.4)' },
          { offset: 1, color: 'rgba(45,80,22,0.05)' }
        ])
      },
      data: weekValues
    }]
  })
}

function initPieChart() {
  if (!pieChartRef.value) return
  
  pieChart = echarts.init(pieChartRef.value)
  pieChart.setOption({
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#A3E4A3',
      textStyle: { color: '#1A1A1A' },
      formatter: '{b}: {c}次 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: '#666' }
    },
    series: [{
      name: '病害分布',
      type: 'pie',
      radius: ['35%', '70%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#fff',
        borderWidth: 3
      },
      label: { show: false },
      emphasis: {
        label: {
          show: true,
          fontSize: 18,
          fontWeight: 'bold'
        }
      },
      labelLine: { show: false },
      data: diseaseDistribution.value.map((item, index) => ({
        value: item.count,
        name: item.name,
        itemStyle: {
          color: ['#2D5016', '#4CAF50', '#8BC34A', '#C6F7D0', '#A3E4A3'][index]
        }
      }))
    }]
  })
}

function handleResize() {
  trendChart?.resize()
  pieChart?.resize()
}

onMounted(() => {
  // 更新时间
  timeInterval = window.setInterval(() => {
    currentTime.value = new Date().toLocaleString('zh-CN')
  }, 1000)

  // 初始化图表
  setTimeout(() => {
    initTrendChart()
    initPieChart()
  }, 100)

  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
  window.removeEventListener('resize', handleResize)
  trendChart?.dispose()
  pieChart?.dispose()
})
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
    
    <!-- 欢迎横幅 -->
    <div class="bg-gradient-to-r from-green-600 to-green-500 rounded-2xl p-6 text-white shadow-lg">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold mb-2">欢迎回来，{{ authStore.user?.username }}</h1>
          <p class="text-green-100 text-lg">智慧农业病虫害检测系统 - 守护作物健康</p>
        </div>
        <div class="text-right">
          <div class="text-2xl font-bold">{{ currentTime }}</div>
          <div class="text-green-100 text-sm mt-1">
            今日检测: {{ stats.todayCount }} 次
          </div>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- 总检测数 -->
      <div class="bg-white rounded-xl p-6 shadow-md border-l-4 border-green-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm mb-1">总检测次数</p>
            <p class="text-3xl font-bold text-gray-800">{{ stats.totalCount.toLocaleString() }}</p>
          </div>
          <div class="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center">
            <svg class="w-7 h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
        </div>
        <p class="text-green-600 text-sm mt-3">↑ 12.5% 较上周</p>
      </div>

      <!-- 病害检出率 -->
      <div class="bg-white rounded-xl p-6 shadow-md border-l-4 border-orange-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm mb-1">病害检出率</p>
            <p class="text-3xl font-bold text-gray-800">{{ (stats.diseaseRate * 100).toFixed(1) }}%</p>
          </div>
          <div class="w-14 h-14 bg-orange-100 rounded-full flex items-center justify-center">
            <svg class="w-7 h-7 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
        </div>
        <p class="text-red-500 text-sm mt-3">↓ 3.2% 较上周</p>
      </div>

      <!-- 活跃摄像头 -->
      <div class="bg-white rounded-xl p-6 shadow-md border-l-4 border-blue-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm mb-1">活跃摄像头</p>
            <p class="text-3xl font-bold text-gray-800">{{ stats.activeCameras }}</p>
          </div>
          <div class="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center">
            <svg class="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
        <p class="text-blue-600 text-sm mt-3">实时监控中</p>
      </div>

      <!-- 预警数量 -->
      <div class="bg-white rounded-xl p-6 shadow-md border-l-4 border-red-500">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm mb-1">待处理预警</p>
            <p class="text-3xl font-bold text-gray-800">{{ stats.alertCount }}</p>
          </div>
          <div class="w-14 h-14 bg-red-100 rounded-full flex items-center justify-center">
            <svg class="w-7 h-7 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </div>
        </div>
        <p class="text-red-600 text-sm mt-3">需要关注</p>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 趋势图 -->
      <div class="lg:col-span-2 bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">近7天检测趋势</h3>
        <div ref="trendChartRef" class="h-80"></div>
      </div>

      <!-- 病害分布 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">病害类型分布</h3>
        <div ref="pieChartRef" class="h-80"></div>
      </div>
    </div>

    <!-- 快捷入口和最近检测 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 快捷入口 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">快捷入口</h3>
        <div class="grid grid-cols-2 gap-4">
          <router-link to="/detect/image" class="flex items-center gap-3 p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
            <div class="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <p class="font-medium text-gray-800">图片检测</p>
              <p class="text-sm text-gray-500">上传图片分析</p>
            </div>
          </router-link>

          <router-link to="/detect/video" class="flex items-center gap-3 p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
            <div class="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <p class="font-medium text-gray-800">视频检测</p>
              <p class="text-sm text-gray-500">逐帧分析视频</p>
            </div>
          </router-link>

          <router-link to="/detect/camera" class="flex items-center gap-3 p-4 bg-orange-50 rounded-lg hover:bg-orange-100 transition-colors">
            <div class="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div>
              <p class="font-medium text-gray-800">实时监测</p>
              <p class="text-sm text-gray-500">摄像头监控</p>
            </div>
          </router-link>

          <router-link to="/knowledge" class="flex items-center gap-3 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
            <div class="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <div>
              <p class="font-medium text-gray-800">知识库</p>
              <p class="text-sm text-gray-500">查看病害信息</p>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 最近检测 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">最近检测记录</h3>
        <div class="space-y-3">
          <div
            v-for="record in recentDetections"
            :key="record.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div class="flex items-center gap-3">
              <div :class="[
                'w-10 h-10 rounded-lg flex items-center justify-center',
                record.type === '图片' ? 'bg-green-100' :
                record.type === '视频' ? 'bg-blue-100' : 'bg-orange-100'
              ]">
                <svg v-if="record.type === '图片'" class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <svg v-else-if="record.type === '视频'" class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                <svg v-else class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                </svg>
              </div>
              <div>
                <p class="font-medium text-gray-800">{{ record.result }}</p>
                <p class="text-sm text-gray-500">{{ record.type }} · {{ record.time }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="font-bold text-green-600">{{ (record.confidence * 100).toFixed(0) }}%</p>
              <p class="text-xs text-gray-400">置信度</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
