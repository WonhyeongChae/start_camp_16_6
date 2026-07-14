<template>
  <header class="site-header">
    <div class="container header-inner">
      <router-link class="brand" to="/" aria-label="LocalHub 홈">
        <span class="brand-mark" aria-hidden="true">
          <span class="pin-head"></span>
          <span class="pin-shadow"></span>
        </span>
        <span>LocalHub</span>
      </router-link>

      <nav class="main-nav" aria-label="주요 메뉴">
        <router-link
          v-for="link in links"
          :key="link.to"
          :to="link.to"
        >
          {{ link.label }}
        </router-link>
      </nav>

      <div class="header-spacer" aria-hidden="true"></div>
    </div>
  </header>
</template>

<script setup>
const links = [
  { label: '홈', to: '/' },
  { label: '지역 둘러보기', to: '/places' },
  { label: '축제 캘린더', to: '/festivals' },
  { label: '커뮤니티', to: '/community' }
]
</script>

<style scoped>
.site-header {
  height: 82px;
  background: rgba(251, 250, 246, 0.92);
  border-bottom: 1px solid rgba(230, 227, 218, 0.55);
  backdrop-filter: blur(12px);
}
.header-inner {
  height: 100%;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
}
.brand {
  width: max-content;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: var(--green-900);
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -1.1px;
}
.brand-mark {
  position: relative;
  width: 34px;
  height: 42px;
  display: inline-block;
}
.pin-head {
  position: absolute;
  top: 0;
  left: 6px;
  width: 22px;
  height: 29px;
  background: var(--green-800);
  border-radius: 50% 50% 52% 52%;
  clip-path: polygon(0 0, 100% 0, 92% 68%, 50% 100%, 8% 68%);
}
.pin-head::after {
  content: '';
  position: absolute;
  top: 7px;
  left: 7px;
  width: 8px;
  height: 8px;
  background: #ffb75e;
  border-radius: 50%;
}
.pin-shadow {
  position: absolute;
  left: 1px;
  bottom: 1px;
  width: 32px;
  height: 9px;
  background: #9dbb8b;
  border-radius: 50%;
  transform: scaleY(.55);
}
.main-nav {
  height: 100%;
  display: flex;
  align-items: stretch;
  gap: 50px;
}
.main-nav a {
  position: relative;
  display: flex;
  align-items: center;
  color: var(--navy);
  font-size: 16px;
  font-weight: 750;
}
.main-nav a::after {
  content: '';
  position: absolute;
  left: 50%;
  right: 50%;
  bottom: 17px;
  height: 2px;
  background: var(--green-900);
  transition: left 160ms ease, right 160ms ease;
}
.main-nav a:hover::after,
.main-nav a.router-link-exact-active::after {
  left: 0;
  right: 0;
}
.main-nav a.router-link-exact-active {
  color: var(--green-900);
}
.header-spacer {
  min-width: 1px;
}

@media (max-width: 900px) {
  .site-header { height: auto; padding: 14px 0 10px; }
  .header-inner { grid-template-columns: 1fr; gap: 8px; }
  .brand { justify-self: center; }
  .main-nav {
    width: 100%;
    height: auto;
    justify-content: space-between;
    gap: 16px;
    overflow-x: auto;
  }
  .main-nav a { min-height: 38px; font-size: 14px; white-space: nowrap; }
  .main-nav a::after { bottom: 0; }
  .header-spacer { display: none; }
}

@media (max-width: 560px) {
  .brand { font-size: 23px; }
  .brand-mark { width: 29px; height: 36px; transform: scale(.86); }
  .main-nav { gap: 18px; justify-content: flex-start; }
}
</style>
