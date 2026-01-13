<!-- App.vue -->
<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useVideoStore } from '@/stores/videos'

const videoStore = useVideoStore()

onMounted(() => {
  // Авторизация (если токен сохранен)
  const token = localStorage.getItem('access_token')
  if (token) {
    // Можно добавить проверку токена
    console.log('Пользователь авторизован')
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  min-height: 100vh;
}
</style>