<script setup lang="ts">
import { ref } from 'vue'

// 知识库分类
const categories = ref([
  { id: 1, name: '常见病害', icon: 'disease', count: 5 },
  { id: 2, name: '防治技术', icon: 'technology', count: 8 },
  { id: 3, name: '农药知识', icon: 'pesticide', count: 6 },
  { id: 4, name: '农事管理', icon: 'farming', count: 10 }
])

// 知识文章
const articles = ref([
  {
    id: 1,
    title: '白粉病的识别与防治',
    category: '常见病害',
    author: '农业专家',
    date: '2024-03-15',
    views: 1256,
    summary: '白粉病是作物常见的真菌性病害，主要危害叶片、茎秆和果实表面，形成白色粉状物。本文详细介绍白粉病的识别方法和防治措施。',
    tags: ['白粉病', '真菌病害', '防治']
  },
  {
    id: 2,
    title: '如何正确使用多菌灵',
    category: '农药知识',
    author: '农药专家',
    date: '2024-03-12',
    views: 892,
    summary: '多菌灵是一种广谱性杀菌剂，对多种作物病害有良好的防治效果。本文介绍多菌灵的使用方法、注意事项和最佳使用时机。',
    tags: ['多菌灵', '杀菌剂', '使用方法']
  },
  {
    id: 3,
    title: '叶斑病的综合防治策略',
    category: '防治技术',
    author: '植保专家',
    date: '2024-03-10',
    views: 756,
    summary: '叶斑病是一类引起叶片出现斑点、坏死的病害总称。本文提出一套综合防治策略，包括农业防治、生物防治和化学防治相结合的方法。',
    tags: ['叶斑病', '综合防治', '植保']
  },
  {
    id: 4,
    title: '春季农事管理要点',
    category: '农事管理',
    author: '农艺师',
    date: '2024-03-08',
    views: 1432,
    summary: '春季是农作物生长的关键时期，也是病虫害高发期。本文总结春季农事管理的要点，帮助农户做好春耕工作。',
    tags: ['春季', '农事管理', '春耕']
  },
  {
    id: 5,
    title: '锈病的识别与防治',
    category: '常见病害',
    author: '农业专家',
    date: '2024-03-05',
    views: 654,
    summary: '锈病主要危害作物的叶片和茎秆，表现为出现铁锈色的孢子堆。本文介绍锈病的识别特征和防治方法。',
    tags: ['锈病', '真菌病害', '防治']
  },
  {
    id: 6,
    title: '生物防治技术概述',
    category: '防治技术',
    author: '生物防治专家',
    date: '2024-03-03',
    views: 1087,
    summary: '生物防治是利用有益生物或其代谢产物来控制病虫害的方法，具有环保、可持续等优点。本文概述生物防治的主要技术和应用。',
    tags: ['生物防治', '绿色防控', '可持续']
  }
])

// 社区问答
const questions = ref([
  {
    id: 1,
    title: '番茄叶子出现白斑是什么原因？',
    author: '农户老王',
    date: '2024-03-14',
    answers: 5,
    views: 234,
    solved: true
  },
  {
    id: 2,
    title: '多菌灵和百菌清可以一起用吗？',
    author: '新手农夫',
    date: '2024-03-13',
    answers: 3,
    views: 189,
    solved: false
  },
  {
    id: 3,
    title: '黄瓜叶片发黄是怎么回事？',
    author: '蔬菜种植户',
    date: '2024-03-12',
    answers: 8,
    views: 456,
    solved: true
  }
])

// 搜索和筛选
const searchQuery = ref('')
const selectedCategory = ref('all')

// 搜索文章
function searchArticles() {
  // 模拟搜索
  console.log('Searching:', searchQuery.value, 'Category:', selectedCategory.value)
}

// 获取分类图标
function getCategoryIcon(icon: string): string {
  const icons: Record<string, string> = {
    disease: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
    technology: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z',
    pesticide: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z',
    farming: 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
  }
  return icons[icon] || icons.disease
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
    
    <!-- 搜索和筛选 -->
    <div class="bg-white rounded-xl p-6 shadow-md">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索文章、问题..."
            class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
          />
        </div>
        <select
          v-model="selectedCategory"
          class="px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
        >
          <option value="all">全部分类</option>
          <option
            v-for="cat in categories"
            :key="cat.id"
            :value="cat.id"
          >
            {{ cat.name }}
          </option>
        </select>
        <button
          @click="searchArticles"
          class="px-6 py-3 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600 transition-colors"
        >
          搜索
        </button>
      </div>
    </div>

    <!-- 分类导航 -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow cursor-pointer"
      >
        <div class="w-14 h-14 bg-green-100 rounded-xl flex items-center justify-center mb-3">
          <svg class="w-7 h-7 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getCategoryIcon(cat.icon)" />
          </svg>
        </div>
        <h3 class="font-bold text-gray-800 mb-1">{{ cat.name }}</h3>
        <p class="text-sm text-gray-500">{{ cat.count }} 篇文章</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 知识文章 -->
      <div class="lg:col-span-2 space-y-4">
        <div class="bg-white rounded-xl p-6 shadow-md">
          <h3 class="text-lg font-bold text-gray-800 mb-4">热门文章</h3>
          <div class="space-y-4">
            <div
              v-for="article in articles"
              :key="article.id"
              class="border border-gray-200 rounded-xl p-4 hover:border-green-300 transition-colors cursor-pointer"
            >
              <div class="flex items-start justify-between mb-2">
                <div>
                  <span class="px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs font-medium">
                    {{ article.category }}
                  </span>
                  <h4 class="font-bold text-gray-800 mt-2">{{ article.title }}</h4>
                </div>
                <div class="flex items-center gap-4 text-sm text-gray-500">
                  <span class="flex items-center gap-1">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    {{ article.views }}
                  </span>
                </div>
              </div>
              <p class="text-sm text-gray-600 mb-3">{{ article.summary }}</p>
              <div class="flex items-center justify-between">
                <div class="flex gap-2">
                  <span
                    v-for="tag in article.tags"
                    :key="tag"
                    class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs"
                  >
                    {{ tag }}
                  </span>
                </div>
                <div class="text-sm text-gray-500">
                  {{ article.author }} · {{ article.date }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 社区问答 -->
      <div class="bg-white rounded-xl p-6 shadow-md">
        <h3 class="text-lg font-bold text-gray-800 mb-4">社区问答</h3>
        <div class="space-y-4">
          <div
            v-for="question in questions"
            :key="question.id"
            class="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
          >
            <div class="flex items-start gap-3">
              <div
                :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                  question.solved ? 'bg-green-100' : 'bg-yellow-100'
                ]"
              >
                <svg
                  v-if="question.solved"
                  class="w-4 h-4 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <svg
                  v-else
                  class="w-4 h-4 text-yellow-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="flex-1">
                <h4 class="font-medium text-gray-800 mb-1 line-clamp-2">{{ question.title }}</h4>
                <div class="flex items-center gap-3 text-sm text-gray-500">
                  <span>{{ question.author }}</span>
                  <span>{{ question.answers }} 回答</span>
                  <span>{{ question.views }} 浏览</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button class="w-full mt-4 py-3 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors">
          查看更多问题
        </button>

        <!-- 快捷链接 -->
        <div class="mt-6 pt-6 border-t border-gray-200">
          <h4 class="font-medium text-gray-800 mb-3">常用链接</h4>
          <div class="space-y-2">
            <a href="#" class="block text-sm text-green-600 hover:text-green-700">病虫害图谱</a>
            <a href="#" class="block text-sm text-green-600 hover:text-green-700">农药使用指南</a>
            <a href="#" class="block text-sm text-green-600 hover:text-green-700">农事日历</a>
            <a href="#" class="block text-sm text-green-600 hover:text-green-700">专家在线咨询</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
