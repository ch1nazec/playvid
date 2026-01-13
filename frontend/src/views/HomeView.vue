<!-- views/HomeView.vue -->
<template>
  <div class="home-view fullscreen-desktop">
    <!-- Хедер -->
    <header class="header">
      <div class="container">
        <div class="header-content">
          <div class="logo-section">
            <h1 class="logo">🎬 Видео Хостинг</h1>
            <div class="stats">
              <span class="stat">
                <i class="icon">📹</i>
                <span class="count">{{ videoCount }}</span>
                <span class="label">видео</span>
              </span>
            </div>
          </div>
          
          <!-- Навигация в хедере -->
          <div class="header-nav">
            <router-link to="/upload" class="nav-btn upload-btn">
              <span class="nav-icon">📤</span>
              <span class="nav-text">Загрузить видео</span>
            </router-link>
            
            <button 
              v-if="!isAuthenticated"
              @click="goToLogin"
              class="nav-btn login-btn"
            >
              <span class="nav-icon">🔑</span>
              <span class="nav-text">Войти</span>
            </button>
            
            <div v-else class="user-info">
              <span class="user-icon">👤</span>
              <span class="user-name">{{ userName }}</span>
              <button @click="logout" class="logout-btn" title="Выйти">🚪</button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Основной контент с боковой панелью -->
    <div class="main-wrapper">
      <!-- Боковая панель фильтров -->
      <aside class="sidebar">
        <div class="sidebar-content">
          <h3 class="sidebar-title">Фильтры</h3>
          
          <!-- Поиск -->
          <div class="filter-section">
            <label class="filter-label">Поиск</label>
            <div class="search-box">
              <input
                type="text"
                v-model="searchQuery"
                @input="onSearchInput"
                placeholder="Введите название..."
                class="search-input"
              />
              <span class="search-icon">🔍</span>
            </div>
          </div>

          <!-- Теги -->
          <div class="filter-section">
            <label class="filter-label">Теги</label>
            <div class="tags-cloud">
              <button 
                v-for="tag in allTags" 
                :key="tag"
                @click="toggleTag(tag)"
                :class="['tag-btn', { active: selectedTags.includes(tag) }]"
              >
                #{{ tag }}
              </button>
            </div>
            <select 
              v-model="selectedTag" 
              @change="onTagChange"
              class="tag-select"
            >
              <option value="">Все теги</option>
              <option 
                v-for="tag in allTags" 
                :key="tag" 
                :value="tag"
              >
                #{{ tag }}
              </option>
            </select>
          </div>

          <!-- Сортировка -->
          <div class="filter-section">
            <label class="filter-label">Сортировка</label>
            <div class="sort-options">
              <button 
                v-for="option in sortOptions" 
                :key="option.value"
                @click="selectSort(option.value)"
                :class="['sort-btn', { active: selectedSort === option.value }]"
              >
                {{ option.label }}
              </button>
            </div>
          </div>

          <!-- Статистика -->
          <div class="filter-section stats-section">
            <label class="filter-label">Статистика</label>
            <div class="stats-cards">
              <div class="stat-card">
                <div class="stat-card-icon">📹</div>
                <div class="stat-card-content">
                  <div class="stat-card-value">{{ videoCount }}</div>
                  <div class="stat-card-label">Всего видео</div>
                </div>
              </div>
              <div class="stat-card">
                <div class="stat-card-icon">👁️</div>
                <div class="stat-card-content">
                  <div class="stat-card-value">{{ totalViews }}</div>
                  <div class="stat-card-label">Просмотры</div>
                </div>
              </div>
              <div class="stat-card">
                <div class="stat-card-icon">❤️</div>
                <div class="stat-card-content">
                  <div class="stat-card-value">{{ totalLikes }}</div>
                  <div class="stat-card-label">Лайки</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Быстрые действия -->
          <div class="filter-section">
            <div class="quick-actions">
              <button @click="refreshVideos" class="action-btn" :disabled="isLoading">
                <span class="action-btn-icon">{{ isLoading ? '🔄' : '🔄' }}</span>
                <span class="action-btn-text">Обновить</span>
              </button>
              <button @click="clearFilters" class="action-btn secondary">
                <span class="action-btn-icon">🗑️</span>
                <span class="action-btn-text">Сбросить</span>
              </button>
            </div>
          </div>
        </div>
      </aside>

      <!-- Основной контент -->
      <main class="main-content">
        <div class="content-header">
          <h2 class="content-title">Видео</h2>
          <div class="view-controls">
            <button 
              @click="toggleViewMode('grid')"
              :class="['view-btn', { active: viewMode === 'grid' }]"
              title="Сетка"
            >
              ▦
            </button>
            <button 
              @click="toggleViewMode('list')"
              :class="['view-btn', { active: viewMode === 'list' }]"
              title="Список"
            >
              ☰
            </button>
          </div>
        </div>

        <!-- Состояния загрузки -->
        <div v-if="isLoading" class="loading-state">
          <div class="spinner"></div>
          <p>Загружаем видео...</p>
        </div>

        <!-- Ошибка -->
        <div v-else-if="error" class="error-state">
          <div class="error-icon">❌</div>
          <h3>Ошибка загрузки</h3>
          <p>{{ error }}</p>
          <button @click="refreshVideos" class="retry-btn">
            Повторить попытку
          </button>
        </div>

        <!-- Пустой список -->
        <div v-else-if="videoCount === 0" class="empty-state">
          <div class="empty-icon">📭</div>
          <h3>Видео не найдены</h3>
          <p>Попробуйте изменить фильтры поиска</p>
          <button @click="clearFilters" class="clear-btn">
            Сбросить фильтры
          </button>
        </div>

        <!-- Сетка видео -->
        <div v-else :class="['videos-container', viewMode]">
          <div 
            v-for="video in videos" 
            :key="video.id" 
            :class="['video-item', viewMode]"
          >
            <!-- Видео карточка -->
            <div class="video-card" @click="openVideo(video)">
              <!-- Превью -->
              <div class="video-preview">
                <img 
                  v-if="video.preview" 
                  :src="video.preview" 
                  :alt="video.name"
                  class="preview-image"
                />
                <div v-else class="no-preview">
                  <span class="no-preview-icon">🎬</span>
                  <span class="no-preview-text">Нет превью</span>
                </div>
                
                <!-- Длительность -->
                <div v-if="video.duration" class="video-duration">
                  {{ formatDuration(video.duration) }}
                </div>
                
                <!-- Статус -->
                <div class="video-status" :class="{ public: video.public_video, private: !video.public_video }">
                  {{ video.public_video ? '🌐' : '🔒' }}
                </div>
              </div>

              <!-- Информация -->
              <div class="video-info">
                <h3 class="video-title">{{ video.name }}</h3>
                
                <div class="video-meta">
                  <div class="video-channel">
                    <span class="channel-icon">📺</span>
                    <span class="channel-name">
                      {{ video.channel_id?.channel_name || 'Без канала' }}
                    </span>
                  </div>
                  
                  <div class="video-stats">
                    <span class="stat-item">
                      <span class="stat-icon">👁️</span>
                      {{ video.views_count || 0 }}
                    </span>
                    <span class="stat-item">
                      <span class="stat-icon">❤️</span>
                      {{ video.like_count || 0 }}
                    </span>
                    <span class="stat-item">
                      <span class="stat-icon">💬</span>
                      {{ video.comments_count || 0 }}
                    </span>
                  </div>
                </div>

                <!-- Описание -->
                <p v-if="video.description && viewMode === 'list'" class="video-description">
                  {{ truncateText(video.description, 200) }}
                </p>

                <!-- Теги -->
                <div v-if="video.tags && video.tags.length > 0" class="video-tags">
                  <span 
                    v-for="tag in video.tags.slice(0, viewMode === 'grid' ? 2 : 4)" 
                    :key="tag.id || tag"
                    class="tag"
                    @click.stop="filterByTag(tag)"
                  >
                    #{{ typeof tag === 'object' ? tag.name_tag : tag }}
                  </span>
                  <span 
                    v-if="video.tags.length > (viewMode === 'grid' ? 2 : 4)" 
                    class="tag-more"
                    @click.stop="showAllTags(video)"
                  >
                    +{{ video.tags.length - (viewMode === 'grid' ? 2 : 4) }}
                  </span>
                </div>

                <!-- Дата -->
                <div class="video-date">
                  <span class="date-icon">📅</span>
                  {{ formatDate(video.date_upload) }}
                </div>

                <!-- Действия -->
                <div class="video-actions" @click.stop>
                  <button 
                    @click="likeVideo(video.id)"
                    :class="['action-btn', 'like-btn', { liked: video.is_liked }]"
                    :disabled="!isAuthenticated"
                    :title="isAuthenticated ? 'Лайкнуть' : 'Войдите для лайка'"
                  >
                    <span class="action-icon">❤️</span>
                    <span class="action-count">{{ video.like_count || 0 }}</span>
                  </button>

                  <button 
                    @click="repostVideo(video.id)"
                    :class="['action-btn', 'repost-btn', { reposted: video.is_reposted }]"
                    :disabled="!isAuthenticated"
                    :title="isAuthenticated ? 'Репостнуть' : 'Войдите для репоста'"
                  >
                    <span class="action-icon">🔄</span>
                    <span class="action-count">{{ video.repost_count || 0 }}</span>
                  </button>

                  <button 
                    @click="openComments(video)"
                    class="action-btn comment-btn"
                  >
                    <span class="action-icon">💬</span>
                    <span class="action-count">{{ video.comments_count || 0 }}</span>
                  </button>

                  <button 
                    @click="shareVideo(video)"
                    class="action-btn share-btn"
                    title="Поделиться"
                  >
                    <span class="action-icon">📤</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Пагинация -->
        <div v-if="videoCount > 0 && !isLoading" class="pagination">
          <button 
            @click="loadMore" 
            :disabled="isLoading"
            class="load-more-btn"
          >
            {{ isLoading ? 'Загрузка...' : 'Загрузить еще видео' }}
          </button>
        </div>
      </main>
    </div>

    <!-- Футер -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-info">
            <p class="footer-logo">🎬 Видео Хостинг</p>
            <p class="footer-desc">Лучшая платформа для размещения и просмотра видео</p>
          </div>
          <div class="footer-stats">
            <div class="footer-stat">
              <span class="stat-label">Видео онлайн:</span>
              <span class="stat-value">{{ videoCount }}</span>
            </div>
            <div class="footer-stat">
              <span class="stat-label">Пользователей:</span>
              <span class="stat-value">{{ userCount }}</span>
            </div>
            <div class="footer-stat">
              <span class="stat-label">Всего просмотров:</span>
              <span class="stat-value">{{ totalViews }}</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useVideoStore } from '@/stores/videos'
import { storeToRefs } from 'pinia'
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const videoStore = useVideoStore()

// Реактивные данные
const { videos, isLoading, error, filters, allTags } = storeToRefs(videoStore)
const searchQuery = ref(filters.value.search || '')
const selectedTag = ref(filters.value.tag || '')
const selectedTags = ref([])
const selectedSort = ref(filters.value.ordering || '-date_upload')
const viewMode = ref('grid') // 'grid' или 'list'
const userName = ref('Пользователь')

// Опции сортировки
const sortOptions = [
  { value: '-date_upload', label: 'Новые' },
  { value: 'date_upload', label: 'Старые' },
  { value: '-like_count', label: 'Популярные' },
  { value: '-views_count', label: 'Просмотры' },
  { value: 'name', label: 'А-Я' },
  { value: '-name', label: 'Я-А' }
]

// Проверка авторизации
const isAuthenticated = computed(() => {
  return !!localStorage.getItem('access_token')
})

// Геттеры
const videoCount = computed(() => videos.value.length)
const totalViews = computed(() => {
  return videos.value.reduce((sum, video) => sum + (video.views_count || 0), 0)
})
const totalLikes = computed(() => {
  return videos.value.reduce((sum, video) => sum + (video.like_count || 0), 0)
})
const userCount = computed(() => {
  // Здесь можно добавить логику получения количества пользователей
  return Math.floor(videoCount.value / 3) + 10
})

// Методы
const refreshVideos = () => {
  videoStore.fetchVideos()
}

const onSearchInput = () => {
  clearTimeout(window.searchTimeout)
  window.searchTimeout = setTimeout(() => {
    videoStore.setFilter('search', searchQuery.value)
  }, 300)
}

const onTagChange = () => {
  videoStore.setFilter('tag', selectedTag.value)
}

const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag)
  if (index === -1) {
    selectedTags.value.push(tag)
  } else {
    selectedTags.value.splice(index, 1)
  }
  // Здесь можно добавить логику фильтрации по нескольким тегам
}

const selectSort = (sortValue) => {
  selectedSort.value = sortValue
  videoStore.setFilter('ordering', sortValue)
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedTag.value = ''
  selectedTags.value = []
  selectedSort.value = '-date_upload'
  videoStore.setFilter('search', '')
  videoStore.setFilter('tag', '')
  videoStore.setFilter('ordering', '-date_upload')
}

const toggleViewMode = (mode) => {
  viewMode.value = mode
}

const openVideo = (video) => {
  router.push(`/video/${video.id}`)
}

const likeVideo = (videoId) => {
  if (isAuthenticated.value) {
    videoStore.likeVideo(videoId)
  } else {
    router.push('/login')
  }
}

const repostVideo = (videoId) => {
  if (isAuthenticated.value) {
    videoStore.repostVideo(videoId)
  } else {
    router.push('/login')
  }
}

const filterByTag = (tag) => {
  const tagName = typeof tag === 'object' ? tag.name_tag : tag
  selectedTag.value = tagName
  videoStore.setFilter('tag', tagName)
}

const openComments = (video) => {
  router.push(`/video/${video.id}#comments`)
}

const shareVideo = (video) => {
  const url = `${window.location.origin}/video/${video.id}`
  if (navigator.share) {
    navigator.share({
      title: video.name,
      text: video.description,
      url: url
    })
  } else {
    navigator.clipboard.writeText(url)
    alert('Ссылка скопирована в буфер обмена!')
  }
}

const goToLogin = () => {
  router.push('/login')
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_name')
  window.location.reload()
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) {
    return 'Сегодня'
  } else if (diffDays === 1) {
    return 'Вчера'
  } else if (diffDays < 7) {
    return `${diffDays} дней назад`
  } else {
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: diffDays > 365 ? 'numeric' : undefined
    })
  }
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const formatDuration = (seconds) => {
  if (!seconds) return '0:00'
  const hours = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const showAllTags = (video) => {
  alert(`Все теги видео "${video.name}":\n${video.tags.map(t => 
    typeof t === 'object' ? t.name_tag : t
  ).join(', ')}`)
}

const loadMore = () => {
  // TODO: Реализовать пагинацию
  console.log('Загрузка дополнительных видео...')
}

// Загружаем видео при монтировании
onMounted(() => {
  if (videoCount.value === 0) {
    refreshVideos()
  }
  
  // Получаем имя пользователя из localStorage
  const storedName = localStorage.getItem('user_name')
  if (storedName) {
    userName.value = storedName
  }
})
</script>

<style scoped>
/* Стили для полноэкранного десктопного режима */
.fullscreen-desktop {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Хедер */
.header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: white;
  padding: 15px 0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo {
  font-size: 1.8rem;
  margin: 0;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.stats .stat {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  padding: 8px 15px;
  border-radius: 25px;
  font-size: 14px;
  backdrop-filter: blur(10px);
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 15px;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: none;
  border-radius: 25px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.upload-btn {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
}

.login-btn {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.1);
  padding: 8px 15px;
  border-radius: 25px;
  backdrop-filter: blur(10px);
}

.user-icon {
  font-size: 16px;
}

.logout-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 5px;
  border-radius: 5px;
  transition: background 0.3s;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Основная структура */
.main-wrapper {
  display: flex;
  flex: 1;
  min-height: calc(100vh - 140px);
}

/* Боковая панель */
.sidebar {
  width: 320px;
  background: #ffffff;
  border-right: 1px solid #eaeaea;
  padding: 25px;
  overflow-y: auto;
  position: sticky;
  top: 60px;
  height: calc(100vh - 140px);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
}

.sidebar-title {
  font-size: 1.3rem;
  color: #333;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
}

.filter-section {
  margin-bottom: 25px;
}

.filter-label {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 10px;
  font-weight: 500;
}

/* Поиск */
.search-box {
  position: relative;
  margin-bottom: 15px;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  font-size: 14px;
  transition: all 0.3s;
  background: #f8f9fa;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #667eea;
}

/* Теги */
.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.tag-btn {
  padding: 6px 12px;
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 15px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
  color: #666;
}

.tag-btn:hover {
  background: #eef2ff;
  color: #667eea;
  transform: translateY(-1px);
}

.tag-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.tag-select {
  width: 100%;
  padding: 10px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  background: white;
  font-size: 14px;
  cursor: pointer;
  transition: border-color 0.3s;
}

.tag-select:focus {
  outline: none;
  border-color: #667eea;
}

/* Сортировка */
.sort-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.sort-btn {
  padding: 10px;
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
  color: #666;
  text-align: center;
}

.sort-btn:hover {
  background: #eef2ff;
  color: #667eea;
  transform: translateY(-1px);
}

.sort-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

/* Статистика */
.stats-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 20px;
  border-radius: 15px;
  border: 1px solid #e0e0e0;
}

.stats-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-card-icon {
  font-size: 24px;
  color: #667eea;
}

.stat-card-content {
  flex: 1;
}

.stat-card-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.stat-card-label {
  font-size: 0.8rem;
  color: #666;
}

/* Быстрые действия */
.quick-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.action-btn.secondary {
  background: #6c757d;
}

/* Основной контент */
.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  background: #f8f9fa;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.content-title {
  font-size: 1.8rem;
  color: #333;
  margin: 0;
}

.view-controls {
  display: flex;
  gap: 10px;
}

.view-btn {
  padding: 10px 15px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  color: #666;
}

.view-btn:hover {
  background: #f8f9fa;
  border-color: #667eea;
}

.view-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

/* Контейнер видео */
.videos-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.videos-container.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.video-item.grid {
  display: flex;
}

.video-item.list {
  display: flex;
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

/* Карточка видео */
.video-card {
  flex: 1;
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.video-item.list .video-card {
  flex-direction: row;
  height: 200px;
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

/* Превью видео */
.video-preview {
  position: relative;
  background: #000;
  overflow: hidden;
}

.video-item.grid .video-preview {
  height: 200px;
}

.video-item.list .video-preview {
  width: 300px;
  height: 100%;
  flex-shrink: 0;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.video-card:hover .preview-image {
  transform: scale(1.05);
}

.no-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.no-preview-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.video-duration {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 12px;
  backdrop-filter: blur(5px);
}

.video-status {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(255, 255, 255, 0.9);
  padding: 5px;
  border-radius: 5px;
  font-size: 14px;
}

/* Информация о видео */
.video-info {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.video-title {
  margin: 0 0 10px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  line-height: 1.3;
}

.video-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  font-size: 13px;
  color: #666;
}

.video-channel {
  display: flex;
  align-items: center;
  gap: 5px;
}

.channel-icon {
  font-size: 12px;
}

.video-stats {
  display: flex;
  gap: 15px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 3px;
}

.video-description {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 15px;
  flex: 1;
}

/* Теги */
.video-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.tag {
  background: #eef2ff;
  color: #667eea;
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 11px;
  cursor: pointer;
  transition: background 0.3s;
}

.tag:hover {
  background: #e0e7ff;
  transform: translateY(-1px);
}

.tag-more {
  color: #999;
  font-size: 11px;
  align-self: center;
  cursor: pointer;
}

/* Дата */
.video-date {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #888;
  margin-bottom: 15px;
}

/* Действия */
.video-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 15px;
  border: none;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
  background: #f8f9fa;
  color: #666;
  min-width: 80px;
  justify-content: center;
}

.action-btn:hover:not(:disabled) {
  background: #e9ecef;
  transform: translateY(-2px);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.like-btn.liked {
  background: #fed7d7;
  color: #e53e3e;
}

.repost-btn.reposted {
  background: #c6f6d5;
  color: #38a169;
}

.action-icon {
  font-size: 14px;
}

/* Пагинация */
.pagination {
  text-align: center;
  margin-top: 40px;
}

.load-more-btn {
  padding: 15px 50px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.load-more-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.load-more-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Футер */
.footer {
  background: #1a1a2e;
  color: white;
  padding: 20px 0;
  margin-top: auto;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
}

.footer-logo {
  font-size: 1.2rem;
  margin-bottom: 5px;
  color: #667eea;
}

.footer-desc {
  color: #aaa;
  font-size: 0.9rem;
}

.footer-stats {
  display: flex;
  gap: 30px;
}

.footer-stat {
  text-align: center;
}

.stat-label {
  display: block;
  color: #aaa;
  font-size: 0.8rem;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
}

/* Состояния загрузки */
.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 100px 20px;
  background: white;
  border-radius: 15px;
  margin: 20px 0;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon, .empty-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.retry-btn, .clear-btn {
  padding: 12px 30px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  margin-top: 20px;
  transition: all 0.3s;
}

.retry-btn:hover, .clear-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

/* Адаптивность для декстопа */
@media (min-width: 1200px) {
  .videos-container.grid {
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  }
  
  .video-item.list .video-preview {
    width: 350px;
  }
}

@media (max-width: 1400px) {
  .sidebar {
    width: 280px;
  }
  
  .main-content {
    padding: 25px;
  }
}
</style>