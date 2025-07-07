<template>
  <div class="create-thread-container">
    <h1 class="title">새로운 쓰레드를 만들어보세요</h1>
    <form @submit.prevent="createThread" class="form">
      <div class="form-group">
        <label for="title" class="form-label">제목</label>
        <input
          type="text"
          id="title"
          v-model="title"
          class="form-input"
          placeholder="쓰레드 제목을 입력하세요"
        />
      </div>
      <div class="form-group">
        <label for="content" class="form-label">내용</label>
        <textarea
          id="content"
          v-model="content"
          class="form-textarea"
          placeholder="쓰레드 내용을 입력하세요"
        ></textarea>
      </div>
      <div class="form-group">
        <label for="hashtags" class="form-label">해시태그</label>
        <input
          type="text"
          id="hashtags"
          v-model="hashtags"
          class="form-input"
          placeholder="#공백으로 구분하여 해시태그를 입력하세요"
        />
      </div>
      <button class="submit-btn">쓰레드 생성</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useThreadStore } from "@/stores/thread"
import { useRoute } from "vue-router"

const threadStore = useThreadStore()
const route = useRoute()
const title = ref("")
const content = ref("")
const hashtags = ref("")
const book = route.params.id

const createThread = () => {
  if (!title.value.trim() || !content.value.trim()) {
    alert("제목과 내용을 모두 입력해주세요.")
    return
  }

  const threadData = {
    title: title.value,
    content: content.value,
    hashtags: hashtags.value.trim() !== "" ? hashtags.value.trim() : "",
  }

  threadStore.createThread(book, threadData)
  alert("쓰레드가 성공적으로 생성되었습니다!")
}
</script>

<style scoped>
.create-thread-container {
  font-family: 'Arial', sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  min-height: 100vh;
  padding: 4rem 2rem;
  background-color: #f9fafb;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333333;
  margin-bottom: 1.5rem;
  text-align: center;
}

.form {
  width: 100%;
  max-width: 800px;
  background-color: #ffffff;
  padding: 2rem;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 1.25rem;
  font-weight: bold;
  color: #555555;
  margin-bottom: 0.5rem;
}

.form-input,
.form-textarea {
  padding: 1rem;
  font-size: 1.125rem;
  border: 1px solid #cccccc;
  border-radius: 4px;
  outline: none;
  transition: border-color 0.3s ease;
  width: 100%;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #1cb0f6;
}

.form-textarea {
  resize: vertical;
  min-height: 150px;
}

.submit-btn {
  padding: 1rem;
  font-size: 1.25rem;
  font-weight: bold;
  color: #ffffff;
  background-color: #1cb0f6;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #0a8cd2;
}

@media (max-width: 768px) {
  .form {
    padding: 2rem;
  }

  .title {
    font-size: 2rem;
  }

  .submit-btn {
    font-size: 1.125rem;
    padding: 0.75rem;
  }
}

@media (max-width: 480px) {
  .form {
    padding: 1.5rem;
  }

  .title {
    font-size: 1.75rem;
  }

  .submit-btn {
    font-size: 1rem;
    padding: 0.5rem;
  }
}
</style>
