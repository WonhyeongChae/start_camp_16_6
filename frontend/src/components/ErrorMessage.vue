<template>
  <div class="error-message">
    <p>{{ message }}</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  message: {
    type: String,
    default: '알 수 없는 오류가 발생했습니다.'
  }
})
</script>

<style>
.error-message {
  color: #b00020;
  background: #fdecea;
  border: 1px solid #f5c2c7;
  padding: 16px;
  border-radius: 8px;
}
</style>