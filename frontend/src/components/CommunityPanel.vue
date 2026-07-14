<script setup>
defineProps({ posts: { type: Array, required: true } })
</script>

<template>
  <section class="info-panel" aria-labelledby="community-title">
    <header class="panel-header">
      <h2 id="community-title"><span aria-hidden="true">♧</span> 지금 커뮤니티에서는</h2>
      <router-link to="/community">더보기 <span aria-hidden="true">›</span></router-link>
    </header>
    <div class="post-list">
      <router-link v-for="post in posts" :key="post.id" class="post-row" :to="`/community/${post.id}`">
        <span class="post-chip" :class="`tone-${post.tone}`">{{ post.category }}</span>
        <strong>{{ post.title }}</strong>
        <small>◉ {{ post.views }}　·　{{ post.time }}</small>
      </router-link>
    </div>
  </section>
</template>

<style scoped>
.info-panel { height: 100%; padding: 20px 18px; background: rgba(255,255,255,.76); border: 1px solid var(--line); border-radius: 14px; }
.panel-header { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 14px; }
.panel-header h2 { margin: 0; font-size: 20px; letter-spacing: -.4px; }
.panel-header h2 span { color: var(--green-900); }
.panel-header a { color: #606865; font-size: 12px; white-space: nowrap; }
.post-list { display: grid; gap: 9px; }
.post-row { min-height: 94px; display: flex; flex-direction: column; align-items: flex-start; justify-content: center; gap: 7px; padding: 13px 15px; background: #fff; border: 1px solid var(--line); border-radius: 10px; transition: border-color 160ms, transform 160ms; }
.post-row:hover { border-color: #b7cfc0; transform: translateX(2px); }
.post-row strong { font-size: 15px; }
.post-row small { color: #737a76; font-size: 11px; }
.post-chip { padding: 4px 8px; border-radius: 6px; font-size: 10px; font-weight: 800; }
.tone-green { color: #267249; background: #e3f2df; } .tone-blue { color: #3567a7; background: #e4effd; } .tone-purple { color: #7654a5; background: #eee8fa; }
</style>
