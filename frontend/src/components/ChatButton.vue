<template>
  <button class="chat-button" type="button" aria-label="LocalHub AI 챗봇 미리보기">
    <span class="spark" aria-hidden="true">✦</span>
    <span class="chat-icon" aria-hidden="true">•••</span>
    <span class="chat-label">LocalHub AI</span>
  </button>
</template>

<style scoped>
.chat-button { position: fixed; z-index: 20; right: 30px; bottom: 28px; width: 70px; height: 70px; display: grid; place-items: center; color: #fff; background: var(--green-900); border: 5px solid rgba(255,255,255,.86); border-radius: 50%; box-shadow: 0 12px 26px rgba(7,92,58,.24); }
.chat-icon { width: 33px; height: 27px; display: grid; place-items: center; border: 2px solid #fff; border-radius: 50%; font-weight: 900; letter-spacing: 2px; line-height: 1; }
.spark { position: absolute; top: 6px; right: 7px; color: #bfe7cd; font-size: 13px; }
.chat-label { position: absolute; top: calc(100% + 5px); right: -3px; padding: 5px 10px; color: #28312d; background: #fff; border-radius: 999px; box-shadow: 0 5px 14px rgba(0,0,0,.1); font-size: 11px; white-space: nowrap; }
@media (max-width: 560px) { .chat-button { right: 16px; bottom: 18px; width: 60px; height: 60px; } }
</style>
