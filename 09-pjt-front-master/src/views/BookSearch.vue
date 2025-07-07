<template>
  <div class="search-container">
    <h1 class="search-title">도서 검색</h1>
    <form class="search-form" @submit.prevent="searchBook">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="책 제목을 입력하세요"
        class="search-input"
      />
      <button class="search-btn">검색</button>
    </form>

    <div v-if="isLoading" class="search-loading">검색 중...</div>
    <div v-if="error" class="search-error">{{ error }}</div>

    <div v-if="books.length" class="search-results">
      <h2 class="results-title">검색 결과:</h2>
      <ul class="book-list">
        <li v-for="book in books" :key="book.id" class="book-card">
          <img v-if="book.cover" :src="book.cover" alt="책 표지" class="book-cover" />
          <div class="book-info">
            <h3 class="book-title">{{ book.title }}</h3>
            <p class="book-author">{{ book.author }}</p>
          </div>
        </li>
      </ul>
    </div>
    <div v-else-if="!isLoading && !error" class="no-results">
      <p>검색 결과가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useBookStore } from '@/stores/book'
import { useRoute } from 'vue-router'

const route = useRoute()
const bookStore = useBookStore()

const searchQuery = ref('')
const books = ref([])
const isLoading = ref(false)
const error = ref(null)

const searchBookByQuery = async (query) => {
  if (!query.trim()) return

  isLoading.value = true
  error.value = null

  try {
    books.value = await bookStore.searchBook(query.trim())
  } catch (err) {
    error.value = '검색 결과가 없습니다.'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

watch(() => route.query.q, (newQuery) => {
  if (newQuery) {
    searchQuery.value = newQuery
    searchBookByQuery(newQuery)
  }
}, { immediate: true })

const searchBook = () => {
  searchBookByQuery(searchQuery.value)
}
</script>

<style scoped>
.search-container {
  max-width: 700px;
  margin: 40px auto 0 auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(60, 60, 60, 0.08);
  padding: 2.5rem 2rem 2rem 2rem;
}

.search-title {
  color: #1cb0f6;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-align: center;
}

.search-form {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: center;
}

.search-input {
  flex: 1;
  padding: 0.7rem 1.2rem;
  border: 2px solid #e5e5e5;
  border-radius: 18px;
  font-size: 1rem;
  background: #f7f9fb;
  transition: border 0.2s;
}

.search-input:focus {
  border: 2px solid #1cb0f6;
  outline: none;
}

.search-btn {
  background: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 18px;
  padding: 0.7rem 1.5rem;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px 0 rgba(60, 60, 60, 0.06);
}

.search-btn:hover,
.search-btn:focus {
  background: #1592c7;
  color: #fff;
  box-shadow: 0 4px 16px 0 rgba(28, 176, 246, 0.13);
}

.search-loading,
.search-error,
.no-results {
  text-align: center;
  margin-top: 1.5rem;
  color: #888;
  font-size: 1.1rem;
}

.search-error {
  color: #e74c3c;
}

.search-results {
  margin-top: 2rem;
}

.results-title {
  font-size: 1.3rem;
  color: #1cb0f6;
  margin-bottom: 1rem;
  font-weight: 700;
}

.book-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 18px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.book-card {
  background: #f7f9fb;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(60, 60, 60, 0.06);
  padding: 1rem;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 1rem;
  transition: box-shadow 0.2s;
}

.book-card:hover {
  box-shadow: 0 4px 16px rgba(28, 176, 246, 0.13);
}

.book-cover {
  width: 70px;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.book-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.book-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1cb0f6;
  margin: 0 0 0.3rem 0;
}

.book-author {
  color: #555;
  font-size: 1rem;
  margin: 0;
}
</style>