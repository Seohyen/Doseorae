<template>
  <div v-if="book" class="book-card">
    <div class="book-image-container">
      <img :src="book.cover" alt="책 이미지" class="book-cover" @click="goToDetail"/>
        <button class="interest-button" @click="toggleDropdown">
           ⋮
        </button>
        <ul v-if="isDropdownOpen" class="dropdown-menu">
          <li>
            <button class="create-thread-button" @click="toggleInterestBook">{{ !isInterested ? '관심 도서' : '관심 도서 제거' }}</button>
            <button class="create-thread-button" @click = "toggleReadBook">{{!isRead ? '읽은 도서' : '읽은 도서 제거'}}</button>
          </li>
        </ul>
      </div>
    <div class="book-info">
      <h3 class="book-title">{{ book.title }}</h3>
      <p class="book-content">{{ book.content }}</p>
      <button class="create-thread-button" @click="goToThreadCreate">쓰레드 생성</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account'
import { useBookStore } from '@/stores/book'

const props = defineProps({ book: Object })
const router = useRouter()
const isInterested = ref(false)
const isRead =  ref(false)
const accountStore = useAccountStore()
const bookStore = useBookStore()


onMounted(() => {
  const user = accountStore.user
  if (user) {
    isInterested.value = user.interestBooks?.some(book => book.id === props.book.pk) ?? false
    isRead.value = user.read_books?.some(book => book.id === props.book.pk) ?? false
    console.log(user.username, isInterested.value, '관심 책 여부 확인')
    console.log(user.username, isRead.value, '관심 책 여부 확인')
  } else {
    console.warn('유저 정보가 아직 로딩되지 않았습니다.')
  }
})

const isDropdownOpen = ref(false)
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
  console.log('Dropdown 상태:', isDropdownOpen.value) 
}

const toggleInterestBook = async () => {
  try {
    await bookStore.toggleInterestBook(props.book.pk)
    console.log(props.book.pk,121221212121212)
    isInterested.value = !isInterested.value
    // 관심 목록 업데이트
    if (isInterested.value) {
      accountStore.user.interestBooks.push(props.book.pk)
    } else {
      accountStore.user.interestBooks = accountStore.user.interestBooks.filter(id => id !== props.book.pk)
    }
  } catch (error) {
    alert('관심 책 추가/제거 중 오류가 발생했습니다.')
  }
}

const toggleReadBook = async () => {
  try {
    await bookStore.toggleReadBook (props.book.pk)
    isRead.value = !isRead.value
    if (isRead.value) {
      accountStore.user.read_books.push(props.book.pk)
    } else {
      accountStore.user.read_books = accountStore.user.read_books.filter(id => id !== props.book.pk)
    }
  } catch (error) {
    alert('읽은 책 추가/제거 중 오류가 발생했습니다.')
  }
}


const goToThreadCreate = () => {
  router.push({
    name: 'CreateThread',
    params: { id: props.book.pk },
  })
}

const goToDetail = () => {
  router.push({
    name: 'BookDetail',
    params: { id: props.book.pk },
  })
}
</script>

<style scoped>
.book-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: none;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.book-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.book-image-container {
  position: relative;
  width: 100%;
  max-width: 150px;
}

.book-cover {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.interest-button {
  position: absolute;
  top: 0px;
  right: 8px;
  background: rgba(28, 176, 246, 0.9);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 0.8rem;
  font-weight: 800;

  cursor: pointer;
  transition: background 0.2s;
}

.interest-button:hover {
  background: rgba(19, 144, 196, 0.9);
}

.book-info {
  text-align: center;
  margin-top: 16px;
}

.book-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.book-content {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 16px;
}

.create-thread-button {
  background: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.create-thread-button:hover {
  background: #1390c4;
}

.dropdown {
  position: relative;
}
.dropdown-menu {
  position: absolute;
  top: 0%;
  left: 100%;
  background-color: transparent;  /* 배경을 투명으로 설정 */
  border: 1px solid none;
  border-radius: 3px;
  list-style: none;
  padding: 0;
  margin: 0;
  z-index: 10000;
  display: block;
  width: 10px;
  box-shadow: none; 
}

</style>
