// stores/videos.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useVideoStore = defineStore('videos', () => {
  // Состояние
  const videos = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const filters = ref({
    search: '',
    tag: '',
    ordering: '-date_upload'
  })
  
  // Действия
  const fetchVideos = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      // Строим URL с фильтрами
      const params = new URLSearchParams()
      
      if (filters.value.search) {
        params.append('search', filters.value.search)
      }
      
      if (filters.value.tag) {
        params.append('tag__name_tag', filters.value.tag)
      }
      
      if (filters.value.ordering) {
        params.append('ordering', filters.value.ordering)
      }
      
      const url = `/api/video/${params.toString() ? '?' + params.toString() : ''}`
      
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`Ошибка HTTP: ${response.status}`)
      }
      
      const data = await response.json()
      videos.value = data
      
    } catch (err) {
      error.value = err.message
      console.error('Ошибка загрузки видео:', err)
    } finally {
      isLoading.value = false
    }
  }
  
  const setFilter = (key, value) => {
    filters.value[key] = value
    fetchVideos() // Автоматически обновляем при изменении фильтров
  }
  
  const likeVideo = async (videoId) => {
    try {
      const response = await fetch(`/api/video/${videoId}/like/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (response.status === 201) {
        // Обновляем локально
        const video = videos.value.find(v => v.id === videoId)
        if (video) {
          // Обновляем счетчик лайков
          const currentLikes = video.like_count || 0
          video.like_count = currentLikes + 1
          video.is_liked = true
        }
      } else if (response.status === 204) {
        // Убираем лайк
        const video = videos.value.find(v => v.id === videoId)
        if (video) {
          const currentLikes = video.like_count || 1
          video.like_count = Math.max(0, currentLikes - 1)
          video.is_liked = false
        }
      }
      
    } catch (err) {
      console.error('Ошибка лайка:', err)
    }
  }
  
  const repostVideo = async (videoId) => {
    try {
      const response = await fetch(`/api/video/${videoId}/repost/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      
      if (response.ok) {
        const video = videos.value.find(v => v.id === videoId)
        if (video) {
          const currentReposts = video.repost_count || 0
          video.repost_count = currentReposts + 1
          video.is_reposted = true
        }
      }
      
    } catch (err) {
      console.error('Ошибка репоста:', err)
    }
  }
  
  // Геттеры
  const videoCount = () => videos.value.length
  
  const allTags = () => {
    const tags = new Set()
    videos.value.forEach(video => {
      if (video.tags) {
        video.tags.forEach(tag => {
          if (typeof tag === 'object') {
            tags.add(tag.name_tag)
          } else {
            tags.add(tag)
          }
        })
      }
    })
    return Array.from(tags)
  }
  
  return {
    // State
    videos,
    isLoading,
    error,
    filters,
    
    // Actions
    fetchVideos,
    setFilter,
    likeVideo,
    repostVideo,
    
    // Getters
    videoCount,
    allTags
  }
})