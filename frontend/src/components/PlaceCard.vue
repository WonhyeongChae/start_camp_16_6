<script setup>
defineProps({ place: { type: Object, required: true } })
</script>

<template>
  <router-link class="place-card" :to="{ path: '/places', query: { selected: place.contentId } }">
    <div class="image-wrap">
      <img :src="place.imageUrl" :alt="place.title" />
      <span class="category">{{ place.category }}</span>
      <span class="match">키워드 {{ place.matchedKeywords.length }}개 일치</span>
    </div>
    <div class="place-copy">
      <h3>{{ place.shortTitle }}</h3>
      <p>{{ place.description }}</p>
      <span class="location">● 구미시</span>
    </div>
  </router-link>
</template>

<style scoped>
.place-card { overflow: hidden; display: flex; flex-direction: column; min-width: 0; background: #fff; border: 1px solid var(--line); border-radius: 13px; transition: transform 160ms, box-shadow 160ms; }
.place-card:hover { transform: translateY(-4px); box-shadow: var(--shadow); }
.image-wrap { position: relative; aspect-ratio: 1.42; overflow: hidden; background: #e8eee8; }
.image-wrap img { width: 100%; height: 100%; object-fit: cover; transition: transform 260ms; }
.place-card:hover img { transform: scale(1.035); }
.category, .match { position: absolute; border-radius: 999px; font-size: 11px; font-weight: 800; }
.category { top: 12px; left: 12px; padding: 6px 12px; color: #fff; background: var(--green-800); }
.match { right: 10px; bottom: 10px; padding: 6px 10px; color: var(--navy); background: rgba(255,255,255,.94); }
.place-copy { flex: 1; display: flex; flex-direction: column; padding: 16px 17px 18px; }
.place-copy h3 { margin: 0 0 8px; font-size: 21px; letter-spacing: -.5px; }
.place-copy p { min-height: 40px; margin: 0 0 12px; color: #6d7470; font-size: 12px; line-height: 1.65; }
.location { margin-top: auto; color: #6b716e; font-size: 12px; }
</style>
