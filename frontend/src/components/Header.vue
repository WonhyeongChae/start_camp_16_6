<template>
  <header class="header">
    <div class="brand">
      <router-link to="/">LocalHub</router-link>
    </div>
    <nav class="nav">
      <router-link to="/">Home</router-link>
      <router-link to="/places">Places</router-link>
      <router-link to="/community">Community</router-link>
      <router-link to="/travel-test">Travel Test</router-link>
      <router-link to="/festivals">Festivals</router-link>
    </nav>
  </header>
</template>

<style>
.header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #ddd;
  background: #fafafa;
}
.brand a {
  font-weight: bold;
  font-size: 1.2rem;
  color: #333;
  text-decoration: none;
}
.nav a {
  margin-left: 16px;
  color: #555;
  text-decoration: none;
}
.nav a.router-link-active {
  font-weight: 700;
  color: #000;
}
</style>