<script setup lang="ts">
import { ref } from 'vue'

// 表单数据
const formData = ref({
  disease: '',
  severity: '',
  crop: ''
})

// 生成结果
const result = ref<any>(null)
const isGenerating = ref(false)

// 选项
const diseaseOptions = [
  { value: 'powdery_mildew', label: '白粉病 / Powdery Mildew' },
  { value: 'leaf_spot', label: '叶斑病 / Leaf Spot' },
  { value: 'rust', label: '锈病 / Rust' },
  { value: 'early_blight', label: '早疫病 / Early Blight' },
  { value: 'late_blight', label: '晚疫病 / Late Blight' }
]

const severityOptions = [
  { value: 'light', label: '轻度 / Light' },
  { value: 'medium', label: '中度 / Medium' },
  { value: 'severe', label: '重度 / Severe' }
]

const cropOptions = [
  { value: 'tomato', label: '番茄 / Tomato' },
  { value: 'potato', label: '土豆 / Potato' },
  { value: 'wheat', label: '小麦 / Wheat' },
  { value: 'corn', label: '玉米 / Corn' },
  { value: 'rice', label: '水稻 / Rice' }
]

// 生成方案
async function generateTreatment() {
  if (!formData.value.disease || !formData.value.severity || !formData.value.crop) {
    alert('请填写所有字段')
    return
  }

  isGenerating.value = true

  // 模拟LLM生成
  await new Promise(resolve => setTimeout(resolve, 2000))

  // 模拟生成的防治方案
  const disease = diseaseOptions.find(d => d.value === formData.value.disease)
  const severity = severityOptions.find(s => s.value === formData.value.severity)
  const crop = cropOptions.find(c => c.value === formData.value.crop)

  result.value = {
    disease: disease?.label || '',
    severity: severity?.label || '',
    crop: crop?.label || '',
    timestamp: new Date().toLocaleString('zh-CN'),
    medicines: [
      {
        name: '多菌灵悬浮剂',
        usage: '叶面喷施',
        dosage: '稀释1000-1500倍',
        frequency: '每7-10天一次',
        precautions: '避免在高温时段使用，建议早晨或傍晚施药'
      },
      {
        name: '百菌清可湿性粉剂',
        usage: '叶面喷施',
        dosage: '稀释600-800倍',
        frequency: '每10-15天一次',
        precautions: '与其他农药混用需先进行试验'
      },
      {
        name: '代森锰锌可湿性粉剂',
        usage: '叶面喷施',
        dosage: '稀释500-700倍',
        frequency: '每7-10天一次',
        precautions: '不能与铜制剂或碱性农药混用'
      }
    ],
    farmingAdvice: [
      {
        title: '及时清除病叶',
        description: '发现病叶立即摘除，带出田外销毁，减少病原传播',
        icon: 'leaf'
      },
      {
        title: '加强通风透光',
        description: '合理密植，保持田间通风透光，降低田间湿度',
        icon: 'sun'
      },
      {
        title: '控制灌溉',
        description: '避免大水漫灌，采用滴灌或渗灌方式，保持土壤适度干燥',
        icon: 'water'
      },
      {
        title: '增施有机肥',
        description: '适当增施磷钾肥，提高植株抗病能力，避免偏施氮肥',
        icon: 'fertilizer'
      }
    ],
    prevention: [
      '选择抗病品种种植',
      '实行轮作制度，避免连作',
      '种子消毒处理',
      '加强田间管理，及时清除杂草',
      '关注天气预报，提前预防'
    ]
  }

  isGenerating.value = false
}

// 重置表单
function resetForm() {
  formData.value = {
    disease: '',
    severity: '',
    crop: ''
  }
  result.value = null
}
</script>

<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 输入表单 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">输入信息</h3>

        <div class="space-y-6">
          <!-- 病害类型 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              病害类型 <span class="text-red-500">*</span>
            </label>
            <select
              v-model="formData.disease"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
            >
              <option value="">请选择病害类型</option>
              <option
                v-for="option in diseaseOptions"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </div>

          <!-- 严重程度 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              严重程度 <span class="text-red-500">*</span>
            </label>
            <select
              v-model="formData.severity"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
            >
              <option value="">请选择严重程度</option>
              <option
                v-for="option in severityOptions"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </div>

          <!-- 作物种类 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              作物种类 <span class="text-red-500">*</span>
            </label>
            <select
              v-model="formData.crop"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
            >
              <option value="">请选择作物种类</option>
              <option
                v-for="option in cropOptions"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </div>

          <!-- 操作按钮 -->
          <div class="flex gap-4">
            <button
              @click="generateTreatment"
              :disabled="isGenerating"
              class="flex-1 bg-gradient-to-r from-green-500 to-green-600 text-white py-3 rounded-lg font-bold hover:from-green-600 hover:to-green-700 transition-all disabled:opacity-50"
            >
              {{ isGenerating ? '生成中...' : '生成防治方案' }}
            </button>
            <button
              @click="resetForm"
              class="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
            >
              重置
            </button>
          </div>
        </div>
      </div>

      <!-- 生成的方案 -->
      <div class="space-y-6">
        <!-- 加载状态 -->
        <div v-if="isGenerating" class="bg-white rounded-xl p-12 shadow-md text-center">
          <div class="animate-spin w-16 h-16 border-4 border-green-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p class="text-gray-600">正在基于LLM生成个性化防治方案...</p>
        </div>

        <!-- 结果 -->
        <div v-else-if="result" class="space-y-6">
          <!-- 基本信息 -->
          <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg">
            <h3 class="text-lg font-bold mb-3">生成的防治方案</h3>
            <div class="grid grid-cols-3 gap-4 text-center">
              <div>
                <p class="text-green-100 text-sm">病害类型</p>
                <p class="font-bold">{{ result.disease.split(' / ')[0] }}</p>
              </div>
              <div>
                <p class="text-green-100 text-sm">严重程度</p>
                <p class="font-bold">{{ result.severity.split(' / ')[0] }}</p>
              </div>
              <div>
                <p class="text-green-100 text-sm">作物种类</p>
                <p class="font-bold">{{ result.crop.split(' / ')[0] }}</p>
              </div>
            </div>
          </div>

          <!-- 推荐药剂 -->
          <div class="bg-white rounded-xl p-6 shadow-md">
            <h3 class="text-lg font-bold text-gray-800 mb-4">推荐药剂</h3>
            <div class="space-y-4">
              <div
                v-for="(medicine, index) in result.medicines"
                :key="index"
                class="border border-gray-200 rounded-lg p-4 hover:border-green-300 transition-colors"
              >
                <div class="flex items-center justify-between mb-2">
                  <h4 class="font-bold text-gray-800">{{ medicine.name }}</h4>
                  <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                    {{ medicine.usage }}
                  </span>
                </div>
                <div class="grid grid-cols-2 gap-4 text-sm text-gray-600">
                  <div>
                    <span class="text-gray-500">用量：</span>
                    {{ medicine.dosage }}
                  </div>
                  <div>
                    <span class="text-gray-500">频率：</span>
                    {{ medicine.frequency }}
                  </div>
                </div>
                <p class="mt-2 text-sm text-orange-600">
                  <span class="font-medium">注意事项：</span>{{ medicine.precautions }}
                </p>
              </div>
            </div>
          </div>

          <!-- 农事建议 -->
          <div class="bg-white rounded-xl p-6 shadow-md">
            <h3 class="text-lg font-bold text-gray-800 mb-4">农事管理建议</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div
                v-for="(advice, index) in result.farmingAdvice"
                :key="index"
                class="flex items-start gap-3 p-4 bg-green-50 rounded-lg"
              >
                <div class="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg v-if="advice.icon === 'leaf'" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                  </svg>
                  <svg v-else-if="advice.icon === 'sun'" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                  <svg v-else-if="advice.icon === 'water'" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                  </svg>
                  <svg v-else class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064" />
                  </svg>
                </div>
                <div>
                  <h4 class="font-medium text-gray-800 mb-1">{{ advice.title }}</h4>
                  <p class="text-sm text-gray-600">{{ advice.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 预防措施 -->
          <div class="bg-white rounded-xl p-6 shadow-md">
            <h3 class="text-lg font-bold text-gray-800 mb-4">预防为主</h3>
            <ul class="space-y-2">
              <li
                v-for="(item, index) in result.prevention"
                :key="index"
                class="flex items-center gap-2 text-gray-600"
              >
                <svg class="w-5 h-5 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ item }}
              </li>
            </ul>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="bg-white rounded-xl p-12 shadow-md text-center">
          <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <p class="text-gray-500">请填写病害信息，系统将为您生成个性化的防治方案</p>
        </div>
      </div>
    </div>
  </div>
</template>
