<template>
  <section class="places-page">
    <div class="page-hero">
      <div class="page-copy">
        <span class="hero-kicker">GUMI · GYEONGBUK LOCAL PLACES</span>
        <h1>구미·경북의 숨은 장소를<br />한눈에 둘러보세요</h1>
        <p>자연, 문화, 힐링, 음식까지 취향에 맞는 여행지를 찾아보세요.</p>

        <div class="hero-stats">
          <div class="stat-card">
            <strong>{{ places.length }}</strong>
            <span>추천 장소</span>
          </div>
          <div class="stat-card">
            <strong>{{ uniqueRegions.length }}</strong>
            <span>지역 분포</span>
          </div>
          <div class="stat-card">
            <strong>{{ uniqueTypes.length }}</strong>
            <span>콘텐츠 유형</span>
          </div>
        </div>
      </div>

      <div class="hero-side-card">
        <h2>이런 분위기 어때요?</h2>
        <p>산책, 사진, 맛집, 조용한 쉼까지 지역의 매력을 느껴보세요.</p>
        <ul>
          <li v-for="tag in featuredTags" :key="tag">{{ tag }}</li>
        </ul>
      </div>
    </div>

    <div class="toolbar">
      <label class="search-box" for="place-search">
        <span aria-hidden="true">🔎</span>
        <input
          id="place-search"
          v-model="searchText"
          type="text"
          placeholder="장소명·주소·태그로 찾기"
        />
      </label>

      <div class="filter-group" role="tablist" aria-label="장소 유형 필터">
        <button
          v-for="option in typeOptions"
          :key="option.value"
          type="button"
          class="filter-chip"
          :class="{ active: selectedType === option.value }"
          @click="selectedType = option.value"
        >
          {{ option.label }}
        </button>
      </div>
    </div>

    <div v-if="filteredPlaces.length" class="place-grid">
      <article v-for="place in filteredPlaces" :key="place.contentId" class="place-card">
        <button type="button" class="place-button" @click="openPlace(place)">
          <div class="image-wrap">
            <img :src="place.thumbnailUrl || place.imageUrl" :alt="place.title" />
            <span class="category">{{ place.contentType }}</span>
            <span class="match">{{ place.tags.slice(0, 2).join(' · ') }}</span>
          </div>

          <div class="place-copy">
            <div class="place-meta">
              <span class="region">{{ place.region }}</span>
              <span class="type">{{ place.contentType }}</span>
            </div>
            <h3>{{ place.title }}</h3>
            <p>{{ place.address }}</p>
            <div class="tag-list">
              <span v-for="tag in place.tags" :key="tag">{{ tag }}</span>
            </div>
          </div>
        </button>
      </article>
    </div>

    <div v-else class="empty-state">
      <h3>조건에 맞는 장소가 없어요</h3>
      <p>검색어 또는 필터를 바꿔서 다시 찾아보세요.</p>
    </div>

    <PlaceDetailModal
      :show="showPlaceModal"
      :place="selectedPlace"
      @update:show="showPlaceModal = $event"
    />
  </section>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { fetchPlaces, fetchPlaceDetail } from '../api'
import PlaceDetailModal from '../components/PlaceDetailModal.vue'

const route = useRoute()
const places = ref([])
const selectedPlace = ref(null)
const showPlaceModal = ref(false)
const searchText = ref('')
const selectedType = ref('all')

const typeOptions = [
  { value: 'all', label: '전체' },
  { value: '관광지', label: '관광지' },
  { value: '문화시설', label: '문화시설' },
  { value: '음식점', label: '음식점' },
  { value: '레포츠', label: '레포츠' }
]

function normalizePlace(raw) {
  const item = raw || {}

  return {
    contentId: item.contentId || item.content_id || '',
    contentType: item.contentType || item.content_type || '',
    title: item.title || '',
    address: item.address || '',
    detailAddress: item.detailAddress || item.detail_address || '',
    telephone: item.telephone || '',
    imageUrl: item.imageUrl || item.image_url || '',
    thumbnailUrl: item.thumbnailUrl || item.thumbnail_url || '',
    region: item.region || '',
    tags: Array.isArray(item.tags) ? item.tags : []
  }
}

const uniqueRegions = computed(() => [...new Set(places.value.map((place) => place.region))])
const uniqueTypes = computed(() => [...new Set(places.value.map((place) => place.contentType))])
const featuredTags = computed(() => {
  const tags = places.value.flatMap((place) => place.tags || [])
  return [...new Set(tags)].slice(0, 5)
})

const filteredPlaces = computed(() => {
  const term = searchText.value.trim().toLowerCase()

  return places.value.filter((place) => {
    const matchesType = selectedType.value === 'all' || place.contentType === selectedType.value
    const haystack = [place.title, place.address, place.region, place.contentType, ...(place.tags || [])]
      .join(' ')
      .toLowerCase()

    return matchesType && (!term || haystack.includes(term))
  })
})

async function loadPlaces() {
  try {
    const res = await fetchPlaces({
      size: 24,
      type: selectedType.value === 'all' ? undefined : selectedType.value,
      keyword: searchText.value || undefined
    })

    const payload = res?.items || res || []
    places.value = Array.isArray(payload) ? payload.map(normalizePlace) : []
  } catch (error) {
    places.value = []
  }
}

onMounted(() => {
  loadPlaces()
})

watch([selectedType, searchText], () => {
  loadPlaces()
})

async function openPlace(place) {
  try {
    const detail = await fetchPlaceDetail(place.contentId)
    selectedPlace.value = normalizePlace(detail || place)
  } catch (error) {
    selectedPlace.value = normalizePlace(place)
  }

  showPlaceModal.value = true
}

watch(
  () => route.query.selected,
  (selectedId) => {
    if (!selectedId) return

    const place = places.value.find((item) => item.contentId === selectedId)
    if (place) {
      openPlace(place)
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.places-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-hero {
  display: grid;
  grid-template-columns: 1.25fr 0.75fr;
  gap: 18px;
  align-items: stretch;
}

.page-copy,
.hero-side-card {
  padding: 28px;
  border: 1px solid var(--line);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: var(--shadow);
}

.hero-kicker {
  display: inline-block;
  margin-bottom: 12px;
  color: var(--green-700);
  font-size: 11px;
  font-weight: 850;
  letter-spacing: 1.8px;
}

.page-copy h1 {
  margin: 0;
  color: var(--navy);
  font-size: clamp(28px, 3vw, 40px);
  line-height: 1.2;
  letter-spacing: -1.4px;
}

.page-copy p {
  margin: 12px 0 0;
  color: #5d665e;
  font-size: 15px;
  line-height: 1.7;
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-top: 20px;
}

.stat-card {
  padding: 14px 12px;
  border-radius: 16px;
  background: linear-gradient(135deg, #f7fbf3, #eef5e4);
  border: 1px solid #e2edd7;
}

.stat-card strong {
  display: block;
  color: var(--green-900);
  font-size: 20px;
}

.stat-card span {
  color: #627065;
  font-size: 12px;
}

.hero-side-card h2 {
  margin: 0 0 8px;
  font-size: 19px;
  color: var(--navy);
}

.hero-side-card p {
  margin: 0;
  color: #5d665e;
  font-size: 14px;
  line-height: 1.7;
}

.hero-side-card ul {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
}

.hero-side-card li {
  padding: 8px 12px;
  border-radius: 999px;
  background: var(--green-100);
  color: var(--green-900);
  font-size: 12px;
  font-weight: 700;
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 0;
}

.search-box {
  flex: 1 1 280px;
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 48px;
  padding: 0 14px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: #fff;
  box-shadow: 0 6px 20px rgba(17, 28, 44, 0.04);
}

.search-box input {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  color: var(--navy);
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-chip {
  padding: 8px 12px;
  border-radius: 999px;
  background: #f5f5eb;
  color: #5d665e;
  font-size: 13px;
  font-weight: 700;
}

.filter-chip.active {
  color: #fff;
  background: var(--green-800);
}

.place-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.place-card {
  border: 1px solid var(--line);
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 10px 26px rgba(35, 52, 43, 0.06);
  overflow: hidden;
}

.place-button {
  width: 100%;
  padding: 0;
  text-align: left;
  background: none;
  border: none;
}

.image-wrap {
  position: relative;
  aspect-ratio: 1.35;
  overflow: hidden;
  background: #e9f0e4;
}

.image-wrap img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.place-copy {
  padding: 16px;
}

.place-copy h3 {
  margin: 0 0 8px;
  color: var(--navy);
  font-size: 20px;
}

.place-copy p {
  margin: 0 0 10px;
  color: #5d665e;
  line-height: 1.6;
}

.place-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  color: #6b736f;
  font-size: 12px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag-list span {
  padding: 5px 8px;
  border-radius: 999px;
  background: var(--green-100);
  color: var(--green-900);
  font-size: 11px;
}
</style>