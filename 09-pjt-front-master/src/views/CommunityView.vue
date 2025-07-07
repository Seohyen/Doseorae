<template>
  <div class="thread-list-container">
    <h1 class="thread-list-title">Thread List</h1>
    <div 
      class="thread-card"
      v-for="thread in threadStore.threadList"
      :key="thread.id"
    >
      <RouterLink class="thread-title" :to="{ name: 'ThreadDetail', params: { id: thread.pk } }">
        <h3>{{ thread.title }}</h3>
      </RouterLink>
      <img  class = "img" :src="thread.user_profile" alt="프로필 사진"/>
      <p class="thread-user">작성자: {{ thread.username }}</p>
      <p class="book-title"> {{ thread.book_title }}</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useThreadStore } from '@/stores/thread'

const threadStore = useThreadStore()

onMounted(async () => {
  await threadStore.allThreads()
})
</script>

<style scoped>
/* 전체 컨테이너 */
.thread-list-container {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
  background: #f7f9fb;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

/* 제목 스타일 */
.thread-list-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1cb0f6;
  text-align: center;
  margin-bottom: 24px;
}

/* 쓰레드 카드 */
.thread-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.thread-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

/* 쓰레드 제목 */
.thread-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1cb0f6;
  text-decoration: none;
}

.thread-title:hover {
  text-decoration: underline;
}

.thread-user {
  display: inline-block;
  vertical-align: middle; /* 세로 정렬 */
  margin-left: 10px; /* 이미지와 텍스트 사이 간격 */
  font-size: 1rem; /* 텍스트 크기 */
}
.book-title{
   display: inline-block;
  vertical-align: middle; /* 세로 정렬 */
  color: #a8a8a8;
  margin-left: 10px; /* 이미지와 텍스트 사이 간격 */
  font-size: 0.7rem; /* 텍스트 크기 */
}
.img{
  width: 50px;
  height: 50px;
}

/* 반응형 스타일 */
@media (max-width: 1024px) {
  .thread-list-container {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .thread-list-container {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .thread-list-container {
    padding: 12px;
  }
}

</style>