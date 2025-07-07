<template>
  <div class="book-detail-container">
    <h1 class="book-detail-title">도서 상세 정보</h1>
    
    <div v-if="loading" class="loading">
      <p>책 정보를 불러오는 중입니다...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>책 정보를 불러오는 중 오류가 발생했습니다.</p>
      <button class="retry-btn" @click="loadBookDetail">다시 시도</button>
    </div>
    
    <div v-else-if="book" class="book-detail-card">
      <img 
        v-if="book.cover" 
        :src="book.cover" 
        :alt="`${book.title} 표지`" 
        class="book-cover-img" 
        @error="handleImageError"
      />
      
      <h2 class="book-title">{{ book.title }}</h2>
      <p v-if="book.subTitle" class="book-subtitle">{{ book.subTitle }}</p>
      <p v-if="book.content" class="book-content">{{ book.content }}</p>
      
      <div class="book-author-section">
        <span class="book-author-label">저자:</span>
        <span class="book-author">{{ book.author }}</span>
        <img 
          v-if="book.author_photo" 
          :src="book.author_photo" 
          :alt="`${book.author} 사진`" 
          class="author-photo" 
          @error="handleAuthorPhotoError"
        />
      </div>
      
      <p v-if="book.author_info" class="book-author-info">
        저자 정보: {{ book.author_info }}
      </p>
      <p v-if="book.description" class="book-description">
        설명: {{ book.description }}
      </p>
      <p v-if="book.published_date" class="book-published-date">
        출판일: {{ formatDate(book.published_date) }}
      </p>
      <p v-if="book.publisher" class="book-publisher">
        출판사: {{ book.publisher }}
      </p>
      <p v-if="book.isbn" class="book-isbn">
        ISBN: {{ book.isbn }}
      </p>
      
      <div v-if="book.voice_file" class="book-voice-file">
        <span>오디오북:</span>
        <audio 
          :src="book.voice_file" 
          controls 
          preload="metadata"
          class="audio-player"
        >
          브라우저가 오디오를 지원하지 않습니다.
        </audio>
      </div>
      
      <div class="book-interest">
        <span>관심 책 여부: </span>
        <span :class="interestClass">
          {{ isInterested ? '관심 있음' : '관심 없음' }}
        </span>
      </div>
      
      <button 
        class="thread-btn" 
        @click="goToThreadCreate"
      >
        쓰레드 생성
      </button>
    </div>
    
    <button class="back-btn" @click="goBack">뒤로가기</button>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useBookStore } from '@/stores/book'
import { useAccountStore } from '@/stores/account'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const bookStore = useBookStore()
const accountStore = useAccountStore()

const book = ref(null)
const userdata = ref(null)
const isInterested = ref(false)
const loading = ref(true)
const error = ref(false)
const updatingInterest = ref(false)

const interestClass = computed(() => ({
  'interested': isInterested.value,
  'not-interested': !isInterested.value
}))

const loadBookDetail = async () => {
  try {
    loading.value = true
    error.value = false
    
    const [userData, bookDetail] = await Promise.all([
      accountStore.getUserInfo(),
      bookStore.getBookDetail(route.params.id)
    ])
    
    userdata.value = userData
    book.value = bookStore.book
    
    if (userdata.value?.data?.interestBooks) {
      isInterested.value = userdata.value.data.interestBooks.some(
        b => b.id == route.params.id
      )
    }
    
    console.log('책 정보:', book.value)
    console.log('관심 책 여부:', isInterested.value)
    
  } catch (err) {
    console.error('Error fetching book details:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}



const goToThreadCreate = () => {
  
  
  router.push({
    name: 'CreateThread',
    params: { id: route.params.id },
  })
}

const goBack = () => {
  router.go(-1)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ko-KR')
  } catch {
    return dateString
  }
}

const handleImageError = (event) => {
  console.warn('Book cover image failed to load:', event.target.src)
  event.target.style.display = 'none'
}

const handleAuthorPhotoError = (event) => {
  console.warn('Author photo failed to load:', event.target.src)
  event.target.style.display = 'none'
}

// Lifecycle
onMounted(() => {
  loadBookDetail()
})
</script>

<style scoped>
.book-detail-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 32px 24px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(60, 60, 60, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.book-detail-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1cb0f6;
  margin-bottom: 24px;
}

.book-detail-card {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.book-cover-img {
  width: 180px;
  height: 260px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(60, 60, 60, 0.08);
  transition: opacity 0.2s;
}

.book-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #22223b;
  text-align: center;
}

.book-subtitle {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 10px;
  text-align: center;
}

.book-content {
  font-size: 1rem;
  color: #333;
  margin-bottom: 12px;
  text-align: center;
  line-height: 1.5;
}

.book-author-section {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  justify-content: center;
}

.book-author-label {
  font-weight: 600;
  color: #1cb0f6;
  margin-right: 6px;
}

.book-author {
  font-size: 1rem;
  color: #333;
  margin-right: 10px;
}

.author-photo {
  width: 36px;
  height: 36px;
  object-fit: cover;
  border-radius: 50%;
  margin-left: 8px;
  border: 1px solid #eee;
}

.book-author-info,
.book-description,
.book-published-date,
.book-publisher,
.book-isbn {
  font-size: 1rem;
  color: #444;
  margin-bottom: 8px;
  text-align: center;
  line-height: 1.4;
}

.book-voice-file {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 8px;
  font-size: 1rem;
  color: #444;
}

.audio-player {
  margin-top: 8px;
  max-width: 300px;
}

.book-interest {
  margin: 16px 0;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
}

.interested {
  color: #1cb0f6;
  font-weight: 700;
}

.not-interested {
  color: #aaa;
}

.interest-toggle-btn {
  padding: 4px 12px;
  background: #f0f8ff;
  color: #1cb0f6;
  border: 1px solid #1cb0f6;
  border-radius: 12px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.interest-toggle-btn:hover:not(:disabled) {
  background: #1cb0f6;
  color: white;
}

.interest-toggle-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.thread-btn {
  margin-top: 18px;
  padding: 12px 28px;
  background: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 18px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.thread-btn:hover:not(:disabled) {
  background: #1592c7;
  transform: translateY(-1px);
}

.thread-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.back-btn {
  margin-top: 32px;
  padding: 10px 24px;
  background: #eee;
  color: #333;
  border: none;
  border-radius: 14px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #d4eafd;
  transform: translateY(-1px);
}

.loading, .error {
  text-align: center;
  padding: 40px 20px;
}

.loading {
  color: #888;
  font-size: 1.1rem;
}

.error {
  color: #e74c3c;
}

.error p {
  margin-bottom: 16px;
  font-size: 1.1rem;
}

.retry-btn {
  padding: 8px 16px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: #c0392b;
}

/* Responsive design */
@media (max-width: 768px) {
  .book-detail-container {
    margin: 20px;
    padding: 24px 16px;
  }
  
  .book-detail-title {
    font-size: 1.5rem;
  }
  
  .book-cover-img {
    width: 150px;
    height: 220px;
  }
  
  .audio-player {
    max-width: 250px;
  }
}
</style>