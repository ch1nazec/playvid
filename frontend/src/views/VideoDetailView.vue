<template>
  <div class="video-detail">
    <h1>Детали видео</h1>
    <p>ID видео: {{ $route.params.id }}</p>
    <router-link to="/">← Назад к списку</router-link>
  </div>
</template>