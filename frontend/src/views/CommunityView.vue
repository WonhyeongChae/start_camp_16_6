<script setup>
import { computed, onMounted, ref } from 'vue'

import { fetchPosts } from '../api'

const posts = ref([])
const recommendedPosts = ref([])
const isLoading = ref(true)
const errorMessage = ref('')
const selectedCategory = ref('all')

const POST_CATEGORIES = ['여행', '맛집', '축제', '생활', '자유']

const todayPosts = computed(() => recommendedPosts.value)
const categoryCount = computed(() => new Set(posts.value.map((post) => post.category).filter(Boolean)).size)
const categoryFilters = computed(() => [
  { value: 'all', label: '전체', count: posts.value.length },
  ...POST_CATEGORIES.map((category) => ({
    value: category,
    label: category,
    count: posts.value.filter((post) => post.category === category).length
  }))
])
const visiblePosts = computed(() => selectedCategory.value === 'all'
  ? posts.value
  : posts.value.filter((post) => post.category === selectedCategory.value))

function formatDate(value) {
  return value ? new Date(value).toLocaleDateString('ko-KR') : ''
}

onMounted(async () => {
  try {
    const [latestData, recommendedData] = await Promise.all([
      fetchPosts({ page: 1, size: 50, sort: 'latest' }),
      fetchPosts({ page: 1, size: 2, sort: 'recommendations' })
    ])
    posts.value = latestData.items || []
    recommendedPosts.value = recommendedData.items || []
  } catch (error) {
    errorMessage.value = error?.error?.detail || error?.message || '게시글을 불러오지 못했습니다.'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <section class="community-page">
    <div class="page-hero">
      <div class="page-copy">
        <span class="hero-kicker">GUMI · GYEONGBUK COMMUNITY</span>
        <h1>여행 이야기를 나누는<br />커뮤니티</h1>
        <p class="hero-description">구미·경북 여행지 추천부터 생생한 후기까지,<br />서로의 여행 경험을 자유롭게 나눠보세요.</p>
        <div class="hero-summary" aria-label="커뮤니티 게시글 요약">
          <div><strong>{{ posts.length }}</strong><span>여행 이야기</span></div>
          <span class="summary-divider" aria-hidden="true"></span>
          <div><strong>{{ categoryCount }}</strong><span>이야기 주제</span></div>
        </div>
      </div>
      <div class="hero-side-card">
        <div class="recommend-heading">
          <div>
            <span class="recommend-kicker">TODAY'S PICK</span>
            <h2>오늘의 이야기</h2>
          </div>
          <span class="recommend-label">추천 이야기</span>
        </div>

        <div v-if="isLoading" class="recommend-empty">오늘의 이야기를 불러오는 중이에요.</div>
        <div v-else-if="todayPosts.length" class="recommend-list">
          <router-link
            v-for="post in todayPosts"
            :key="post.id"
            class="recommend-card"
            :to="`/community/${post.id}`"
          >
            <span class="recommend-category">{{ post.category || '여행 이야기' }}</span>
            <strong>{{ post.title }}</strong>
            <small>{{ post.nickname }} · 추천 {{ post.recommendationCount || 0 }} · {{ formatDate(post.createdAt) }}</small>
          </router-link>
        </div>
        <div v-else class="recommend-empty">첫 번째 여행 이야기를 기다리고 있어요.</div>
      </div>
    </div>

    <div class="community-actions">
      <div class="recent-post-heading">
        <h2>최근 게시글</h2>
        <div class="category-filters" role="group" aria-label="게시글 카테고리 필터">
          <button
            v-for="category in categoryFilters"
            :key="category.value"
            type="button"
            class="category-filter"
            :class="{ 'is-active': selectedCategory === category.value }"
            :aria-pressed="selectedCategory === category.value"
            @click="selectedCategory = category.value"
          >
            {{ category.label }}
            <span>{{ category.count }}</span>
          </button>
        </div>
      </div>
      <router-link class="write-button" to="/community/write">글쓰기</router-link>
    </div>

    <p v-if="isLoading" class="state-message">게시글을 불러오는 중입니다.</p>
    <p v-else-if="errorMessage" class="state-message error" role="alert">{{ errorMessage }}</p>
    <p v-else-if="!posts.length" class="state-message">아직 등록된 게시글이 없습니다. 첫 글을 작성해 보세요.</p>
    <p v-else-if="!visiblePosts.length" class="state-message">
      {{ selectedCategory }} 카테고리에 등록된 게시글이 없습니다.
    </p>
    <div v-else class="community-list">
      <article v-for="post in visiblePosts" :key="post.id" class="post-card">
        <div class="post-top">
          <span class="post-chip">{{ post.category }}</span>
          <span class="post-meta">{{ post.nickname }} · {{ formatDate(post.createdAt) }} · 조회 {{ post.viewCount }} · 추천 {{ post.recommendationCount || 0 }}</span>
        </div>
        <h3>{{ post.title }}</h3>
        <p>{{ post.content.length > 120 ? `${post.content.slice(0, 120)}…` : post.content }}</p>
        <router-link class="read-more" :to="`/community/${post.id}`">자세히 보기 ›</router-link>
      </article>
    </div>
  </section>
</template>

<style scoped>
.community-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-hero {
  display: grid;
  grid-template-columns: 1.05fr .95fr;
  gap: 18px;
  align-items: stretch;
}

.page-copy, .hero-side-card {
  padding: 28px;
  border: 1px solid var(--line);
  border-radius: 24px;
  background: rgba(255,255,255,.92);
  box-shadow: var(--shadow);
}

.page-copy {
  display: flex;
  flex-direction: column;
}

.hero-kicker, .recommend-kicker {
  display: inline-block;
  color: var(--green-700);
  font-size: 11px;
  font-weight: 850;
  letter-spacing: 1.5px;
}

.hero-kicker {
  margin-bottom: 12px;
}

.page-copy h1 {
  margin: 0;
  color: var(--navy);
  font-size: clamp(28px, 3vw, 40px);
  line-height: 1.2;
}

.page-copy p {
  margin: 14px 0 0;
  color: #5d665e;
  font-size: 15px;
  line-height: 1.75;
}

.hero-summary {
  display: flex;
  align-items: center;
  gap: 22px;
  margin-top: auto;
  padding-top: 22px;
}

.hero-summary div {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 3px 8px;
  align-items: baseline;
}

.hero-summary strong {
  grid-row: 1 / 3;
  color: var(--green-800);
  font-size: 28px;
  line-height: 1;
}

.hero-summary span:not(.summary-divider) {
  color: #6c776f;
  font-size: 12px;
  font-weight: 700;
}

.summary-divider {
  width: 1px;
  height: 30px;
  background: #dfe6e1;
}

.recommend-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.recommend-heading h2 {
  margin: 4px 0 0;
  color: var(--navy);
  font-size: 20px;
}

.recommend-label {
  padding: 7px 11px;
  border-radius: 999px;
  background: var(--green-100);
  color: var(--green-900);
  font-size: 12px;
  font-weight: 800;
  white-space: nowrap;
}

.recommend-list {
  display: grid;
  gap: 9px;
  margin-top: 16px;
}

.recommend-card {
  position: relative;
  display: grid;
  grid-template-columns: auto minmax(0,1fr);
  align-items: center;
  gap: 5px 10px;
  min-height: 66px;
  padding: 11px 13px;
  overflow: hidden;
  border: 1px solid #e1e9e3;
  border-radius: 14px;
  background: linear-gradient(135deg,#f8fbf8,#f1f6f2);
  color: inherit;
  transition: transform .18s ease,border-color .18s ease,box-shadow .18s ease;
}

.recommend-card:hover {
  transform: translateY(-1px); border-color: #a8cbb4;
  box-shadow: 0 8px 20px rgba(35,52,43,.08);
}

.recommend-category {
  grid-row: 1 / 3;
  align-self: center;
  padding: 6px 8px;
  border-radius: 999px;
  background: var(--green-100);
  color: var(--green-900);
  font-size: 10px;
  font-weight: 800;
  white-space: nowrap;
}

.recommend-card strong {
  min-width: 0;
  overflow: hidden;
  color: var(--navy);
  font-size: 14px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recommend-card small {
  overflow: hidden;
  color: #7b857e;
  font-size: 10px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recommend-empty {
  display: grid;
  min-height: 148px;
  margin-top: 16px;
  place-items: center;
  border-radius: 16px;
  background: #f4f7f4;
  color: #778079;
  font-size: 13px;
  text-align: center;
}

.community-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
}

.community-actions h2 {
  margin: 0;
  color: var(--navy);
  font-size: 20px;
}

.recent-post-heading {
  display: flex;
  align-items: center;
  min-width: 0;
  gap: 16px;
}

.category-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
}

.category-filter {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 7px 10px;
  border: 1px solid #dce6df;
  border-radius: 999px;
  background: #fff;
  color: #59675f;
  font-size: 12px;
  font-weight: 750;
  transition: border-color .18s ease, background .18s ease, color .18s ease;
}

.category-filter:hover {
  border-color: #98bea7;
  color: var(--green-900);
}

.category-filter.is-active {
  border-color: var(--green-800);
  background: var(--green-800);
  color: #fff;
}

.category-filter span {
  display: inline-grid;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  place-items: center;
  border-radius: 999px;
  background: rgba(18, 104, 68, .1);
  font-size: 10px;
}

.category-filter.is-active span {
  background: rgba(255, 255, 255, .2);
}

.write-button {
  display: inline-flex;
  padding: 10px 16px;
  border-radius: 999px;
  background: var(--green-900);
  color: #fff;
  font-size: 13px;
  font-weight: 700;
}

.community-list {
  display: grid;
  gap: 14px;
}

.post-card {
  padding: 20px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 8px 22px rgba(35,52,43,.06);
}

.post-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.post-chip {
  padding: 6px 10px;
  border-radius: 999px;
  background: var(--green-100);
  color: var(--green-900);
  font-size: 11px;
  font-weight: 800;
}

.post-meta {
  color: #6b736f;
  font-size: 12px;
}

.post-card h3 {
  margin: 0 0 8px;
  color: var(--navy);
}

.post-card p {
  margin: 0 0 10px;
  color: #5d665e;
  line-height: 1.6;
  white-space: pre-line;
}

.read-more {
  color: var(--green-900);
  font-weight: 700;
}

.state-message {
  padding: 28px;
  text-align: center;
  color: #66736c;
  background: #fff;
  border-radius: 18px;
}

.state-message.error {
  color: #9b302c;
  background: #fff0ef;
}

@media (max-width: 700px) {
  .page-hero {
    grid-template-columns: 1fr;
  }
  .page-copy, .hero-side-card {
    padding: 20px;
  }
  .hero-summary {
    margin-top: 24px;
  }
  .post-top {
    align-items: flex-start;
    flex-direction: column;
  }
  .community-actions,
  .recent-post-heading {
    align-items: flex-start;
  }
  .recent-post-heading {
    flex-direction: column;
    gap: 10px;
  }
}
@media (max-width: 430px) {
  .hero-summary {
    align-items: flex-start;
    gap: 14px;
  }
  .hero-summary div {
    display: flex;
    flex-direction: column;
  }
  .hero-summary strong {
    font-size: 24px;
  }
  .recommend-heading {
    align-items: flex-start;
  }
}
</style>
