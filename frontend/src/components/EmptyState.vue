<template>
  <div class="empty-state">
    <p>{{ message }}</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  message: {
    type: String,
    default: '데이터가 없습니다.'
  }
})
</script>

<style>
.empty-state {
  color: #777;
  padding: 24px;
}
</style>