<template>
  <div v-if="show" class="overlay" @click.self="close">
    <div class="modal">
      <button class="close-button" type="button" @click="close">×</button>

      <template v-if="place">
        <h2>{{ place.title }}</h2>
        <p class="meta">{{ place.contentType }} · {{ place.region }}</p>
        <img :src="place.imageUrl" :alt="place.title" class="detail-image" />
        <dl class="detail-grid">
          <div>
            <dt>주소</dt>
            <dd>{{ place.address }} {{ place.detailAddress }}</dd>
          </div>
          <div>
            <dt>전화</dt>
            <dd>{{ place.telephone || '정보 없음' }}</dd>
          </div>
          <div>
            <dt>위치</dt>
            <dd>{{ place.latitude ?? '-' }}, {{ place.longitude ?? '-' }}</dd>
          </div>
          <div>
            <dt>태그</dt>
            <dd>{{ (place.tags || []).join(', ') }}</dd>
          </div>
        </dl>
      </template>

      <template v-else>
        <p>장소 정보를 불러올 수 없습니다.</p>
      </template>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: { type: Boolean, default: false },
  place: { type: Object, default: null }
})

const emit = defineEmits(['update:show'])

function close() {
  emit('update:show', false)
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.45);
  z-index: 1000;
}
.modal {
  position: relative;
  width: min(90%, 740px);
  max-height: 90vh;
  overflow-y: auto;
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
}
.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 999px;
  background: #eee;
  font-size: 1.4rem;
  cursor: pointer;
}
.detail-image {
  width: 100%;
  height: 260px;
  object-fit: cover;
  border-radius: 12px;
  margin: 16px 0;
}
.meta {
  color: #666;
  margin-top: 4px;
}
.detail-grid {
  display: grid;
  gap: 12px;
  margin-top: 16px;
}
.detail-grid dt {
  font-weight: 700;
}
.detail-grid dd {
  margin: 4px 0 12px;
  color: #444;
}
</style>