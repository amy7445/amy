<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDetectionStore } from '@/stores/detection'

const router = useRouter()
const detectionStore = useDetectionStore()

const isDragging = ref(false)
const selectedFile = ref<File | null>(null)
const imageUrl = ref<string | null>(null)
const result = ref<any>(null)
const selectedDetectionIndex = ref<number>(-1)
const showDetailModal = ref(false)

interface DiseaseInfo {
  description: string
  symptoms: string[]
  causes: string
  recommendations: string[]
}

const diseaseDatabase: Record<string, DiseaseInfo> = {
  'powdery_mildew': {
    description: '白粉病是由真菌引起的常见植物病害，主要影响叶片、茎和花。',
    symptoms: [
      '叶片表面出现白色粉状斑点',
      '斑点逐渐扩大并覆盖整个叶片',
      '叶片变黄、卷曲甚至枯萎',
      '严重时导致植株生长受阻'
    ],
    causes: '高湿度、通风不良、光照不足等环境因素容易诱发白粉病。',
    recommendations: [
      '保持植株间距，确保通风良好',
      '及时摘除并销毁病叶',
      '使用多菌灵、百菌清等杀菌剂',
      '增加光照，避免过度浇水'
    ]
  },
  'leaf_spot': {
    description: '叶斑病是一类常见的植物病害，由多种真菌或细菌引起。',
    symptoms: [
      '叶片上出现圆形或不规则形斑点',
      '斑点颜色从褐色到黑色不等',
      '斑点中心可能出现灰白色霉层',
      '严重时叶片脱落'
    ],
    causes: '温暖潮湿的环境、植株过密、通风不良等条件容易导致叶斑病爆发。',
    recommendations: [
      '清除并销毁病叶',
      '避免叶片积水',
      '使用代森锰锌、甲基硫菌灵等药剂',
      '保持植株通风透光'
    ]
  },
  'rust': {
    description: '锈病是由锈菌引起的植物病害，能在叶片上形成锈色孢子堆。',
    symptoms: [
      '叶片背面出现黄色或橙色锈斑',
      '后期病斑变为深褐色',
      '叶片提前脱落',
      '植株生长衰弱'
    ],
    causes: '温暖潮湿的气候条件有利于锈病的发生和传播。',
    recommendations: [
      '选用抗病品种',
      '及时清除病株残体',
      '使用三唑酮、戊唑醇等杀菌剂',
      '合理施肥，增强植株抗性'
    ]
  },
  'early_blight': {
    description: '早疫病又称轮纹病，主要危害番茄、马铃薯等作物。',
    symptoms: [
      '叶片上出现同心轮纹状褐色病斑',
      '病斑周围有黄色晕圈',
      '下部叶片先发病，逐渐向上蔓延',
      '严重时全株叶片枯死'
    ],
    causes: '高温高湿环境、连作种植、植株长势弱等因素易诱发早疫病。',
    recommendations: [
      '实行轮作，避免连作',
      '及时摘除下部病叶',
      '使用代森锌、百菌清等药剂',
      '加强田间管理，增强植株长势'
    ]
  },
  'late_blight': {
    description: '晚疫病是一种毁灭性病害，曾导致历史上著名的爱尔兰马铃薯饥荒。',
    symptoms: [
      '叶片出现暗绿色水渍状病斑',
      '病斑迅速扩大变为褐色',
      '叶背出现白色霉层',
      '果实出现褐色硬斑'
    ],
    causes: '低温高湿环境是晚疫病爆发的主要条件。',
    recommendations: [
      '选用抗病品种',
      '及时清除病株',
      '使用甲霜灵锰锌、霜霉威等药剂',
      '加强通风，降低湿度'
    ]
  },
  'healthy': {
    description: '植株生长健康，未检测到明显的病害症状。',
    symptoms: [
      '叶片颜色正常，无斑点',
      '植株生长旺盛',
      '叶片形态正常'
    ],
    causes: '良好的种植管理和适宜的生长环境。',
    recommendations: [
      '继续保持良好的田间管理',
      '定期检查植株健康状况',
      '合理施肥浇水',
      '注意通风透光'
    ]
  }
}

const detectionResults = computed(() => {
  if (!result.value) return []
  return result.value.detections || []
})

const getDiseaseInfo = (diseaseClass: string): DiseaseInfo => {
  return diseaseDatabase[diseaseClass] || diseaseDatabase['healthy']
}

const calculateSeverity = () => {
  if (!result.value || result.value.disease_count === 0) return '健康'
  
  const diseaseRatio = result.value.disease_count / result.value.total_detections
  if (diseaseRatio > 0.6) return '严重'
  if (diseaseRatio > 0.3) return '中等'
  return '轻微'
}

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = false
  const files = e.dataTransfer?.files
  if (files && files[0]) {
    handleFileSelect(files[0])
  }
}

const handleFileInput = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    handleFileSelect(target.files[0])
  }
}

const handleFileSelect = (file: File) => {
  if (!file.type.match(/^image\/(jpeg|png|jpg)$/)) {
    alert('请上传 JPG 或 PNG 格式的图片')
    return
  }
  selectedFile.value = file
  imageUrl.value = URL.createObjectURL(file)
  result.value = null
}

const resetDetection = () => {
  selectedFile.value = null
  if (imageUrl.value) {
    URL.revokeObjectURL(imageUrl.value)
  }
  imageUrl.value = null
  result.value = null
  selectedDetectionIndex.value = -1
}

const showDetectionDetail = (index: number) => {
  selectedDetectionIndex.value = index
  showDetailModal.value = true
}

const exportReport = () => {
  if (!result.value) return
  
  const reportData = {
    检测编号: result.value.image_id,
    检测时间: result.value.timestamp,
    检测总数: result.value.total_detections,
    健康区域: result.value.health_count,
    病害区域: result.value.disease_count,
    严重程度: calculateSeverity(),
    检测结果: result.value.detections.map((det: any) => ({
      病害名称: det.label.split(' / ')[0],
      英文名称: det.label.split(' / ')[1],
      置信度: `${(det.confidence * 100).toFixed(1)}%`,
      位置: `X: ${det.bbox.x.toFixed(0)}, Y: ${det.bbox.y.toFixed(0)}, 宽: ${det.bbox.width.toFixed(0)}, 高: ${det.bbox.height.toFixed(0)}`
    })),
    防治建议: result.value.summary.recommendation
  }
  
  const reportText = JSON.stringify(reportData, null, 2)
  const blob = new Blob([reportText], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `检测报告_${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)
}

const startDetection = async () => {
  if (!selectedFile.value) return

  try {
    const response = await detectionStore.detectImage(selectedFile.value)
    
    const detections = response.detections.map((d: any) => ({
      class: d.label_en.toLowerCase().replace(/\s+/g, '_'),
      label: `${d.label} / ${d.label_en}`,
      confidence: d.confidence,
      bbox: { 
        x: d.bbox[0], 
        y: d.bbox[1], 
        width: d.bbox[2] - d.bbox[0], 
        height: d.bbox[3] - d.bbox[1] 
      },
      info: getDiseaseInfo(d.label_en.toLowerCase().replace(/\s+/g, '_'))
    }))
    
    const mainDisease = detections.length > 0 
      ? detections.sort((a: any, b: any) => b.confidence - a.confidence)[0] 
      : null
    
    const severity = calculateSeverity()
    const mainDiseaseInfo = mainDisease ? getDiseaseInfo(mainDisease.class) : diseaseDatabase['healthy']
    
    result.value = {
      image_id: response.id,
      timestamp: new Date().toLocaleString('zh-CN'),
      file_name: selectedFile.value.name,
      file_size: (selectedFile.value.size / 1024).toFixed(2) + ' KB',
      detection_time: response.detection_time ? `${response.detection_time.toFixed(2)}ms` : '未知',
      total_detections: detections.length,
      disease_count: detections.filter((d: any) => d.class !== 'healthy').length,
      health_count: detections.filter((d: any) => d.class === 'healthy').length,
      severity,
      main_disease: mainDisease ? mainDisease.label.split(' / ')[0] : '健康',
      detections,
      summary: {
        main_disease: mainDisease ? mainDisease.label.split(' / ')[0] : '健康',
        severity,
        recommendation: mainDiseaseInfo.recommendations[0] || '建议定期检查植株健康状况'
      }
    }
  } catch (error) {
    console.error('检测失败:', error)
    alert('检测失败，请重试')
  }
}

const getBoxColor = (diseaseClass: string): string => {
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

const getSeverityColor = (severity: string): string => {
  const colors: Record<string, string> = {
    '健康': '#2ed573',
    '轻微': '#fbbf24',
    '中等': '#f97316',
    '严重': '#ef4444'
  }
  return colors[severity] || '#6b7280'
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">图片病害检测</h2>
      <div class="flex gap-3">
        <button
          v-if="result"
          @click="exportReport"
          class="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors"
        >
          <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          导出报告
        </button>
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
    </div>

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

    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
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

        <div v-if="selectedFile" class="mb-4 p-3 bg-gray-50 rounded-lg">
          <p class="text-sm text-gray-600">
            <strong>文件名:</strong> {{ selectedFile.name }}
          </p>
          <p class="text-sm text-gray-500">
            <strong>大小:</strong> {{ (selectedFile.size / 1024).toFixed(2) }} KB
          </p>
        </div>

        <div class="relative bg-gray-100 rounded-xl overflow-hidden" style="min-height: 400px;">
          <img
            :src="imageUrl!"
            alt="待检测图片"
            class="w-full h-auto"
            style="max-height: 500px; object-fit: contain;"
          />
          
          <div
            v-for="(det, index) in detectionResults"
            :key="index"
            @click="showDetectionDetail(index)"
            class="absolute border-3 rounded-lg cursor-pointer transition-all duration-200 hover:border-white hover:shadow-lg"
            :class="{
              'ring-2 ring-white': selectedDetectionIndex === index
            }"
            :style="{
              left: det.bbox.x + 'px',
              top: det.bbox.y + 'px',
              width: det.bbox.width + 'px',
              height: det.bbox.height + 'px',
              borderColor: getBoxColor(det.class),
              backgroundColor: getBoxColor(det.class) + '15'
            }"
          >
            <div
              class="absolute -top-8 left-0 px-2 py-1 rounded-t-lg text-xs font-bold text-white whitespace-nowrap"
              :style="{ backgroundColor: getBoxColor(det.class) }"
            >
              {{ det.label.split(' / ')[0] }} {{ (det.confidence * 100).toFixed(0) }}%
            </div>
          </div>

          <div
            v-if="detectionStore.isLoading"
            class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center"
          >
            <div class="text-center text-white">
              <div class="animate-spin w-16 h-16 border-4 border-white border-t-transparent rounded-full mx-auto mb-4"></div>
              <p class="text-xl font-medium">正在检测中...</p>
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">检测统计</h3>
          <div v-if="!result" class="text-center text-gray-400 py-8">
            <p>点击"开始检测"按钮进行分析</p>
          </div>
          <div v-else>
            <div class="grid grid-cols-2 gap-4 mb-4">
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
                <p class="text-lg font-bold" :style="{ color: getSeverityColor(result.severity) }">{{ result.severity }}</p>
                <p class="text-sm text-gray-500">严重程度</p>
              </div>
            </div>
            
            <div class="border-t pt-4 space-y-2">
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">检测编号</span>
                <span class="text-sm font-mono">{{ result.image_id }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">检测时间</span>
                <span class="text-sm">{{ result.timestamp }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">文件名称</span>
                <span class="text-sm">{{ result.file_name }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">文件大小</span>
                <span class="text-sm">{{ result.file_size }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">处理耗时</span>
                <span class="text-sm">{{ result.detection_time }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">检测详情</h3>
          <div v-if="!result" class="text-center text-gray-400 py-8">
            <p>暂无检测数据</p>
          </div>
          <div v-else class="space-y-3 max-h-64 overflow-y-auto">
            <div
              v-for="(det, index) in result.detections"
              :key="index"
              @click="showDetectionDetail(index)"
              class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
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
                <p class="text-xs text-gray-400 mt-1">
                  位置: ({{ det.bbox.x.toFixed(0) }}, {{ det.bbox.y.toFixed(0) }})
                </p>
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

        <div v-if="result" class="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg">
          <h3 class="text-lg font-bold mb-3">防治建议</h3>
          <p class="text-green-100 mb-4">{{ result.summary.recommendation }}</p>
          <div class="text-sm text-green-100">
            <p class="mb-2">💡 主要提示:</p>
            <ul class="list-disc list-inside space-y-1">
              <li>定期检查植株健康状况</li>
              <li>保持良好的通风和光照</li>
              <li>及时清除病叶，防止扩散</li>
            </ul>
          </div>
        </div>

        <button
          v-if="!result"
          @click="startDetection"
          :disabled="detectionStore.isLoading"
          class="w-full bg-green-500 text-white py-4 rounded-xl font-bold text-lg hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ detectionStore.isLoading ? '检测中...' : '开始检测' }}
        </button>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <div v-if="showDetailModal && selectedDetectionIndex >= 0 && result" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-start mb-6">
            <div>
              <h3 class="text-xl font-bold text-gray-800">
                {{ result.detections[selectedDetectionIndex].label.split(' / ')[0] }}
              </h3>
              <p class="text-sm text-gray-500">{{ result.detections[selectedDetectionIndex].label.split(' / ')[1] }}</p>
            </div>
            <button @click="showDetailModal = false" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="mb-4">
            <div class="flex items-center gap-3 mb-4">
              <div
                class="w-10 h-10 rounded-full flex items-center justify-center"
                :style="{ backgroundColor: getBoxColor(result.detections[selectedDetectionIndex].class) + '20' }"
              >
                <div
                  class="w-5 h-5 rounded-full"
                  :style="{ backgroundColor: getBoxColor(result.detections[selectedDetectionIndex].class) }"
                ></div>
              </div>
              <div>
                <p class="text-3xl font-bold" :style="{ color: getBoxColor(result.detections[selectedDetectionIndex].class) }">
                  {{ (result.detections[selectedDetectionIndex].confidence * 100).toFixed(1) }}%
                </p>
                <p class="text-xs text-gray-400">置信度</p>
              </div>
              <div class="ml-auto text-right">
                <p class="text-sm text-gray-600">
                  位置: ({{ result.detections[selectedDetectionIndex].bbox.x.toFixed(0) }}, {{ result.detections[selectedDetectionIndex].bbox.y.toFixed(0) }})
                </p>
                <p class="text-sm text-gray-600">
                  大小: {{ result.detections[selectedDetectionIndex].bbox.width.toFixed(0) }} x {{ result.detections[selectedDetectionIndex].bbox.height.toFixed(0) }}
                </p>
              </div>
            </div>
          </div>

          <div class="space-y-4">
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="font-bold text-gray-800 mb-2">📋 病害描述</h4>
              <p class="text-gray-600">{{ result.detections[selectedDetectionIndex].info.description }}</p>
            </div>

            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="font-bold text-gray-800 mb-2">🔍 症状表现</h4>
              <ul class="list-disc list-inside space-y-1">
                <li v-for="(symptom, idx) in result.detections[selectedDetectionIndex].info.symptoms" :key="idx" class="text-gray-600">
                  {{ symptom }}
                </li>
              </ul>
            </div>

            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="font-bold text-gray-800 mb-2">🌱 诱因分析</h4>
              <p class="text-gray-600">{{ result.detections[selectedDetectionIndex].info.causes }}</p>
            </div>

            <div class="bg-gradient-to-r from-green-50 to-green-100 rounded-lg p-4">
              <h4 class="font-bold text-green-800 mb-2">💊 防治建议</h4>
              <ul class="list-disc list-inside space-y-1">
                <li v-for="(rec, idx) in result.detections[selectedDetectionIndex].info.recommendations" :key="idx" class="text-green-700">
                  {{ rec }}
                </li>
              </ul>
            </div>
          </div>

          <div class="mt-6 flex justify-end">
            <button
              @click="showDetailModal = false"
              class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              关闭
            </button>
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