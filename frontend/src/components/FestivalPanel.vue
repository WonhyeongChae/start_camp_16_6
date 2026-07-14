<script setup>
defineProps({ festivals: { type: Array, required: true } })
</script>

<template>
  <section class="info-panel" aria-labelledby="festival-title">
    <header class="panel-header">
      <h2 id="festival-title"><span aria-hidden="true">▣</span> 다가오는 축제</h2>
      <router-link to="/festivals">전체 일정 보기 <span aria-hidden="true">›</span></router-link>
    </header>
    <div class="festival-list">
      <article v-for="festival in festivals" :key="festival.id" class="festival-card">
        <div class="date-box"><span aria-hidden="true">📅</span><strong>{{ festival.schedule }}</strong></div>
        <div class="festival-copy">
          <span class="festival-chip">축제</span>
          <h3>{{ festival.title }}</h3>
          <p>{{ festival.description }}</p>
          <small>📍 {{ festival.location }}</small>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.info-panel { height: 100%; padding: 20px 18px; background: rgba(255,255,255,.76); border: 1px solid var(--line); border-radius: 14px; }
.panel-header { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 14px; }
.panel-header h2 { margin: 0; font-size: 20px; letter-spacing: -.4px; }
.panel-header h2 span { color: var(--green-900); }
.panel-header a { color: #606865; font-size: 12px; white-space: nowrap; }
.festival-list { display: grid; gap: 11px; }
.festival-card { min-height: 122px; display: grid; grid-template-columns: 70px 1fr; gap: 14px; padding: 11px; border: 1px solid var(--line); border-radius: 11px; background: #fff; }
.date-box { display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 4px; padding: 6px; color: var(--orange); border: 1px solid #ff9f7f; border-radius: 9px; }
.date-box strong { max-width: 58px; font-size: 10px; line-height: 1.35; text-align: center; }
.festival-chip { display: inline-block; padding: 4px 8px; color: var(--orange); background: #fff0e9; border-radius: 999px; font-size: 11px; font-weight: 800; }
.festival-copy h3 { margin: 5px 0 4px; font-size: 17px; }
.festival-copy p { margin: 0 0 5px; color: #707773; font-size: 11px; line-height: 1.45; }
.festival-copy small { color: #717975; font-size: 10px; }
@media (max-width: 560px) { .festival-card { grid-template-columns: 64px 1fr; } }
</style>
