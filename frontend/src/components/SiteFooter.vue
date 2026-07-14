<template>
  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <strong><span aria-hidden="true">📍</span> LocalHub</strong>
        <span>구미·경북 공공데이터 기반 지역 여행 서비스</span>
        <span>관광 데이터 출처 · 한국관광공사 TourAPI</span>
      </div>
      <nav aria-label="하단 메뉴">
        <a href="#service">서비스 소개</a>
        <a href="#terms">이용약관</a>
        <a href="#privacy">개인정보처리방침</a>
        <a href="#contact">문의하기</a>
      </nav>
    </div>
  </footer>
</template>

<style scoped>
.site-footer { padding: 28px 0; border-top: 1px solid var(--line); background: rgba(255,255,255,.46); }
.footer-inner { display: flex; align-items: center; justify-content: space-between; gap: 32px; }
.footer-brand { display: grid; grid-template-columns: auto 1fr; column-gap: 28px; row-gap: 3px; color: #6b716e; font-size: 12px; }
.footer-brand strong { grid-row: 1 / 3; align-self: center; color: var(--green-900); font-size: 24px; }
.site-footer nav { display: flex; gap: 28px; color: #59615d; font-size: 13px; }
@media (max-width: 900px) { .footer-inner, .site-footer nav { flex-wrap: wrap; } .footer-brand { grid-template-columns: 1fr; } .footer-brand strong { grid-row: auto; } }
</style>
