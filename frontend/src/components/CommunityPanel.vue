<script setup>
import usersIcon from '../assets/users.png'

defineProps({ posts: { type: Array, required: true } })
</script>

<template>
  <section class="info-panel" aria-labelledby="community-title">
    <header class="panel-header">
      <h2 id="community-title">
        <img :src="usersIcon" alt="" aria-hidden="true" />
        지금 커뮤니티에서는
      </h2>
      <router-link to="/community">더보기 <span aria-hidden="true">›</span></router-link>
    </header>

    <div class="post-list">
      <router-link v-for="post in posts" :key="post.id" class="post-row" :to="`/community/${post.id}`">
        <div class="post-copy">
          <span class="post-category">{{ post.category }}</span>
          <strong>{{ post.title }}</strong>
        </div>
        <div class="recommend-summary" aria-label="추천 수">
          <span class="heart-icon" aria-hidden="true">💚</span>
          <small>추천 {{ post.recommendationCount || 0 }}</small>
        </div>
      </router-link>
      <p v-if="!posts.length" class="post-empty">아직 등록된 게시글이 없습니다.</p>
    </div>
  </section>
</template>

<style scoped>
.info-panel { height: 100%; padding: 20px 18px; background: rgba(255,255,255,.76); border: 1px solid var(--line); border-radius: 14px; }
.panel-header { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 14px; }
.panel-header h2 { display: flex; align-items: center; gap: 12px; margin: 0; padding-left: 4px; font-size: 20px; letter-spacing: -.4px; }
.panel-header h2 img { width: 23px; height: 23px; object-fit: contain; filter: invert(31%) sepia(25%) saturate(1153%) hue-rotate(98deg) brightness(88%); }
.panel-header a { color: #606865; font-size: 12px; white-space: nowrap; }
.post-list { display: grid; gap: 9px; }
.post-row { min-height: 96px; display: flex; align-items: center; justify-content: space-between; gap: 18px; padding: 14px 16px; background: #fff; border: 1px solid var(--line); border-radius: 10px; transition: border-color 160ms, transform 160ms; }
.post-row:hover { border-color: #b7cfc0; transform: translateX(2px); }
.post-copy { display: flex; min-width: 0; flex: 1; flex-direction: column; justify-content: center; gap: 10px; }
.post-category { align-self: flex-start; padding: 4px 8px; border-radius: 999px; background: var(--green-100); color: var(--green-900); font-size: 10px; font-weight: 800; }
.post-row strong { max-width: 100%; overflow: hidden; color: var(--navy); font-size: 15px; text-overflow: ellipsis; white-space: nowrap; }
.recommend-summary { display: flex; min-width: 54px; flex-direction: column; align-items: center; justify-content: center; gap: 2px; color: var(--green-800); }
.heart-icon { font-size: 16px; font-weight: 400; line-height: 1; }
.recommend-summary small { font-size: 11px; font-weight: 700; white-space: nowrap; }
.post-empty { margin: 0; padding: 28px 12px; color: #737a76; font-size: 12px; text-align: center; }

@media (max-width: 430px) {
  .post-row { min-height: 88px; gap: 12px; padding: 12px 14px; }
}
</style>
