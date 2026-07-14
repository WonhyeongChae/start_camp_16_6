<template>
  <div id="app">
    <Header />
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  color: #222;
  min-height: 100vh;
  margin: 0;
}
.app-main {
  padding: 24px;
}
</style>