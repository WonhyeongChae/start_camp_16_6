<template>
  <section class="home-page">
    <travel-test-modal
      v-model:show="showTestModal"
      @submit-result="handleTestResult"
    />

    <div v-if="!showTestModal" class="home-body">
      <header class="home-header">
        <h1>LocalHub Home</h1>
        <p class="subtitle">
          {{ testResultText }}
        </p>
      </header>

      <section class="result-area">
        <div class="section-title">
          <h2>추천 장소</h2>
          <p>당신의 여행 유형에 맞춘 추천 장소입니다.</p>
        </div>
        <div class="horizontal-scroll">
          <article
            v-for="place in recommendedPlaces"
            :key="place.contentId"
            class="place-card"
          >
            <div class="place-image">
              <img :src="place.thumbnailUrl" :alt="place.title" />
            </div>
            <div class="place-meta">
              <strong>{{ place.title }}</strong>
              <span>{{ place.region }}</span>
            </div>
          </article>
        </div>
      </section>

      <section class="category-area">
        <div class="section-title">
          <h2>카테고리</h2>
          <p>원하는 스타일의 여행지를 빠르게 찾아보세요.</p>
        </div>
        <div class="category-grid">
          <button
            v-for="category in categoryButtons"
            :key="category.id"
            type="button"
            class="category-button"
            @click="selectCategory(category.id)"
          >
            <span class="category-icon">{{ category.icon }}</span>
            <span>{{ category.label }}</span>
          </button>
        </div>
      </section>

      <section class="community-area">
        <div class="section-title">
          <h2>커뮤니티 최신 게시글</h2>
          <p>최근에 올라온 질문과 후기입니다.</p>
        </div>
        <ul class="post-list">
          <li v-for="post in recentPosts" :key="post.id" class="post-item">
            <h3>{{ post.title }}</h3>
            <div class="post-meta">
              <span>{{ post.category }}</span>
              <span>{{ post.date }}</span>
            </div>
            <p>{{ post.excerpt }}</p>
          </li>
        </ul>
      </section>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import TravelTestModal from '../components/TravelTestModal.vue'
import { recommendedPlaces, categoryButtons, recentPosts } from '../data/homeMockData'

const STORAGE_KEY = 'localhub-travel-test-result'
const router = useRouter()
const testResult = ref(loadSavedResult())
const showTestModal = ref(!testResult.value)

function loadSavedResult() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function saveTestResult(payload) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
  } catch {
    // localStorage가 없는 환경에서는 무시
  }
}

function handleTestResult(payload) {
  const result = {
    code: payload.code,
    name: payload.name,
    description: payload.description || ''
  }

  testResult.value = result
  saveTestResult(result)
  showTestModal.value = false
}

const testResultText = computed(() => {
  if (!testResult.value) {
    return '여행 유형 테스트 결과를 기다리고 있습니다.'
  }
  return `당신의 여행 유형은 ${testResult.value.name}입니다. 추천 장소를 확인해보세요.`
})

function selectCategory(categoryId) {
  router.push({ path: '/places', query: { category: categoryId } })
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.home-body {
  padding: 20px;
  overflow-y: auto;
}
.home-header {
  margin-bottom: 24px;
}
.subtitle {
  margin-top: 8px;
  color: #555;
}
.section-title h2 {
  margin: 0;
  font-size: 1.2rem;
}
.section-title p {
  margin: 4px 0 16px;
  color: #666;
}
.result-area,
.category-area,
.community-area {
  margin-bottom: 32px;
}
.horizontal-scroll {
  display: flex;
  overflow-x: auto;
  gap: 16px;
  padding-bottom: 8px;
}
.place-card {
  min-width: 240px;
  border: 1px solid #e0e0e0;
  border-radius: 14px;
  background: #fff;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}
.place-image img {
  width: 100%;
  height: 140px;
  object-fit: cover;
}
.place-meta {
  padding: 12px;
}
.place-meta strong {
  display: block;
  margin-bottom: 8px;
}
.place-meta span {
  color: #777;
  font-size: 0.95rem;
}
.category-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}
.category-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 16px;
  background: #fff;
  cursor: pointer;
}
.category-icon {
  font-size: 1.6rem;
}
.post-list {
  display: grid;
  gap: 14px;
}
.post-item {
  padding: 16px;
  border: 1px solid #e6e6e6;
  border-radius: 14px;
  background: #fff;
}
.post-meta {
  margin: 8px 0 0;
  display: flex;
  gap: 12px;
  color: #999;
  font-size: 0.9rem;
}
.post-item p {
  margin: 12px 0 0;
  color: #555;
}
</style>