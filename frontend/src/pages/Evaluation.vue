<script setup lang="ts">
import { ref } from 'vue'

// 评估记录
const evaluationRecords = ref([
  {
    id: 1,
    treatmentDate: '2024-03-01',
    disease: '白粉病',
    beforeCount: 15,
    afterCount: 3,
    effectiveness: 80,
    medicine: '多菌灵',
    status: '有效'
  },
  {
    id: 2,
    treatmentDate: '2024-02-25',
    disease: '叶斑病',
    beforeCount: 8,
    afterCount: 5,
    effectiveness: 37.5,
    medicine: '代森锰锌',
    status: '待观察'
  },
  {
    id: 3,
    treatmentDate: '2024-02-20',
    disease: '锈病',
    beforeCount: 20,
    afterCount: 2,
    effectiveness: 90,
    medicine: '百菌清',
    status: '非常有效'
  }
])

// 新评估表单
const newEvaluation = ref({
  disease: '',
  medicine: '',
  beforeImage: null as File | null,
  afterImage: null as File | null,
  beforeImageUrl: '',
  afterImageUrl: ''
})

// 提交评估
function submitEvaluation() {
  if (!newEvaluation.value.disease || !newEvaluation.value.medicine) {
    alert('请填写所有必填字段')
    return
  }

  // 模拟提交
  alert('评估提交成功！系统将自动分析防治效果。')

  // 重置表单
  newEvaluation.value = {
    disease: '',
    medicine: '',
    beforeImage: null,
    afterImage: null,
    beforeImageUrl: '',
    afterImageUrl: ''
  }
}

// 处理图片上传
function handleBeforeImageUpload(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    newEvaluation.value.beforeImage = target.files[0]
    newEvaluation.value.beforeImageUrl = URL.createObjectURL(target.files[0])
  }
}

function handleAfterImageUpload(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    newEvaluation.value.afterImage = target.files[0]
    newEvaluation.value.afterImageUrl = URL.createObjectURL(target.files[0])
  }
}

// 获取状态颜色
function getStatusColor(status: string): string {
  switch (status) {
    case '非常有效': return 'bg-green-100 text-green-700'
    case '有效': return 'bg-blue-100 text-blue-700'
    case '待观察': return 'bg-yellow-100 text-yellow-700'
    case '无效': return 'bg-red-100 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
}

// 获取效果条颜色
function getEffectivenessColor(percentage: number): string {
  if (percentage >= 70) return 'bg-green-500'
  if (percentage >= 40) return 'bg-yellow-500'
  return 'bg-red-500'
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
      <!-- 评估表单 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">提交新的评估</h3>

        <div class="space-y-6">
          <!-- 病害类型 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              病害类型 <span class="text-red-500">*</span>
            </label>
            <select
              v-model="newEvaluation.disease"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
            >
              <option value="">请选择病害类型</option>
              <option value="powdery_mildew">白粉病 / Powdery Mildew</option>
              <option value="leaf_spot">叶斑病 / Leaf Spot</option>
              <option value="rust">锈病 / Rust</option>
              <option value="early_blight">早疫病 / Early Blight</option>
            </select>
          </div>

          <!-- 使用药剂 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              使用药剂 <span class="text-red-500">*</span>
            </label>
            <input
              v-model="newEvaluation.medicine"
              type="text"
              placeholder="请输入使用的药剂名称"
              class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
            />
          </div>

          <!-- 施药前图片 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              施药前图片 <span class="text-red-500">*</span>
            </label>
            <div
              class="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center cursor-pointer hover:border-green-500 transition-colors"
              @click="($refs.beforeInput as HTMLInputElement).click()"
            >
              <input
                ref="beforeInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleBeforeImageUpload"
              />
              <div v-if="newEvaluation.beforeImageUrl" class="relative">
                <img
                  :src="newEvaluation.beforeImageUrl"
                  alt="施药前"
                  class="max-h-48 mx-auto rounded-lg"
                />
                <p class="text-sm text-green-600 mt-2">已上传施药前图片</p>
              </div>
              <div v-else>
                <svg class="w-12 h-12 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="text-gray-500">点击上传施药前图片</p>
              </div>
            </div>
          </div>

          <!-- 施药后图片 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              施药后图片 <span class="text-red-500">*</span>
            </label>
            <div
              class="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center cursor-pointer hover:border-green-500 transition-colors"
              @click="($refs.afterInput as HTMLInputElement).click()"
            >
              <input
                ref="afterInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleAfterImageUpload"
              />
              <div v-if="newEvaluation.afterImageUrl" class="relative">
                <img
                  :src="newEvaluation.afterImageUrl"
                  alt="施药后"
                  class="max-h-48 mx-auto rounded-lg"
                />
                <p class="text-sm text-green-600 mt-2">已上传施药后图片</p>
              </div>
              <div v-else>
                <svg class="w-12 h-12 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="text-gray-500">点击上传施药后图片</p>
              </div>
            </div>
          </div>

          <!-- 提交按钮 -->
          <button
            @click="submitEvaluation"
            class="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-3 rounded-lg font-bold hover:from-green-600 hover:to-green-700 transition-all"
          >
            提交评估
          </button>
        </div>
      </div>

      <!-- 历史评估记录 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">评估历史</h3>

        <div class="space-y-4">
          <div
            v-for="record in evaluationRecords"
            :key="record.id"
            class="border border-gray-200 rounded-xl p-4 hover:border-green-300 transition-colors"
          >
            <div class="flex items-center justify-between mb-3">
              <div>
                <span class="font-bold text-gray-800">{{ record.disease }}</span>
                <span class="ml-2 px-2 py-0.5 rounded text-xs" :class="getStatusColor(record.status)">
                  {{ record.status }}
                </span>
              </div>
              <span class="text-sm text-gray-500">{{ record.treatmentDate }}</span>
            </div>

            <div class="grid grid-cols-3 gap-4 mb-3">
              <div class="text-center">
                <p class="text-sm text-gray-500">施药前</p>
                <p class="text-xl font-bold text-red-600">{{ record.beforeCount }}</p>
              </div>
              <div class="text-center">
                <p class="text-sm text-gray-500">施药后</p>
                <p class="text-xl font-bold text-green-600">{{ record.afterCount }}</p>
              </div>
              <div class="text-center">
                <p class="text-sm text-gray-500">使用药剂</p>
                <p class="text-sm font-medium text-blue-600">{{ record.medicine }}</p>
              </div>
            </div>

            <div>
              <div class="flex items-center justify-between text-sm mb-1">
                <span class="text-gray-600">防治效果</span>
                <span class="font-bold" :class="record.effectiveness >= 70 ? 'text-green-600' : record.effectiveness >= 40 ? 'text-yellow-600' : 'text-red-600'">
                  {{ record.effectiveness }}%
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div
                  class="h-2 rounded-full transition-all"
                  :class="getEffectivenessColor(record.effectiveness)"
                  :style="{ width: record.effectiveness + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 效果评估标准 -->
    <div class="bg-white rounded-xl p-6 shadow-md">
      <h3 class="text-lg font-bold text-gray-800 mb-4">效果评估标准</h3>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="text-center p-4 bg-green-50 rounded-xl">
          <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-2">
            <span class="text-white font-bold">90%+</span>
          </div>
          <p class="font-medium text-gray-800">非常有效</p>
          <p class="text-sm text-gray-500">病害基本消除</p>
        </div>
        <div class="text-center p-4 bg-blue-50 rounded-xl">
          <div class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-2">
            <span class="text-white font-bold">70%+</span>
          </div>
          <p class="font-medium text-gray-800">有效</p>
          <p class="text-sm text-gray-500">病害明显减少</p>
        </div>
        <div class="text-center p-4 bg-yellow-50 rounded-xl">
          <div class="w-12 h-12 bg-yellow-500 rounded-full flex items-center justify-center mx-auto mb-2">
            <span class="text-white font-bold">40%+</span>
          </div>
          <p class="font-medium text-gray-800">待观察</p>
          <p class="text-sm text-gray-500">效果不明显</p>
        </div>
        <div class="text-center p-4 bg-red-50 rounded-xl">
          <div class="w-12 h-12 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-2">
            <span class="text-white font-bold">&lt;40%</span>
          </div>
          <p class="font-medium text-gray-800">无效</p>
          <p class="text-sm text-gray-500">需更换方案</p>
        </div>
      </div>
    </div>
  </div>
</template>
