<template>
  <section>
    <h1>Community Detail</h1>
    <p>post id: {{ id }}</p>
  </section>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const id = route.params.id
</script>