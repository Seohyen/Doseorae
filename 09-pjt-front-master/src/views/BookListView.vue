<template>
  <div class="container">
    <button
    class="toggle-button"
    @mousedown="startDrag"
    @click="toggleSidebar" 
    ref="toggleButton"
  >
  <!-- {{ isSidebarVisible ? '카테고리 숨기기' : '카테고리 보기' }} -->
    <img
        src="@/assets/ChatGPT_Image_2025년_5월_26일_오후_01_50_08-removebg-preview.png"
        alt="토글 버튼"
        class="toggle-button-image"
      />
  </button>

    <aside class="sidebar" v-show="isSidebarVisible">
      <ul class="category-list">
        <li
          v-for="category in categoryInfo"
          :key="category.pk"
          :class="{ active: selectedCategory === category.fields.name }"
          @click="selectedCategory = category.fields.name"
        >
          {{ category.fields.name }}
        </li>
      </ul>
    </aside>

    <main class="book-list">
      <BookCard
        v-for="book in filteredBooks"
        :key="book.pk"
        :book="book"
      />
    </main>
  </div>
</template>

<script setup>
import BookCard from '@/components/BookCard.vue'
import { ref, computed, onMounted } from 'vue'
import { useBookStore } from '@/stores/book'

const bookStore = useBookStore()
const bookList = ref([])
const categoryInfo = ref([])
const isSidebarVisible = ref(true)
const selectedCategory = ref('전체')
const toggleButton = ref(null) 
let isDragging = false 
let offsetX = 0
let offsetY = 0

onMounted(async () => {
  await bookStore.allBooks()
  bookList.value = bookStore.bookList
  categoryInfo.value = bookStore.categoryInfo
})

const filteredBooks = computed(() => {
  if (selectedCategory.value === '전체') return bookList.value
  return bookList.value.filter(book => book.category === selectedCategory.value)
})

const toggleSidebar = () => {
  isSidebarVisible.value = !isSidebarVisible.value
}


const startDrag = (event) => {
  isDragging = true
  const button = toggleButton.value
  offsetX = event.clientX - button.getBoundingClientRect().left
  offsetY = event.clientY - button.getBoundingClientRect().top
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}


const onDrag = (event) => {
  if (!isDragging) return
  const button = toggleButton.value
  button.style.position = 'fixed' 
  button.style.left = `${event.clientX - offsetX}px`
  button.style.top = `${event.clientY - offsetY}px`
}


const stopDrag = () => {
  isDragging = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  gap: 24px;
  padding: 16px;
  position: relative;
  
}

.toggle-button {
  position: fixed; 
  top: 16px;
  left: 16px;
  z-index: 1000;
  width: 50px; /* 버튼 크기 조정 */
  height: 50px; /* 버튼 크기 조정 */
  padding: 0; /* 내부 여백 제거 */
  background: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 50%; /* 동그랗게 만들기 */
  cursor: grab; /* 드래그 가능 표시 */
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 약간의 그림자 추가 */
  transition: background 0.3s, transform 0.2s;
}

.toggle-button:active {
  cursor: grabbing; /* 드래그 중 표시 */
  transform: scale(0.95); /* 클릭 시 살짝 축소 */
}

.toggle-button:hover {
  background: #1390c4;
}

.toggle-button-image {
  width: 70%; /* 이미지 크기 조정 */
  height: 70%; /* 이미지 크기 조정 */
  object-fit: contain; /* 이미지 비율 유지 */
}

.sidebar {
  width: 220px;
  background: #f7f9fb;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 16px;
  height: fit-content;
}

.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-list li {
  padding: 10px 14px;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.3s, color 0.3s;
}

.category-list li:hover {
  background: #d0ebf7;
}

.category-list li.active {
  background: #1cb0f6;
  color: #fff;
  font-weight: bold;
}

.book-list {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
 
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>