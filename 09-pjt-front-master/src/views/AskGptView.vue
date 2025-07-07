<template>
  <div class="chat-wrapper">
    <h1 class="chat-title">📚 도서 추천</h1>

    <!-- 웃는 얼굴 캐릭터 -->
    <div class="character-container">
      <div class="smiley-face">
        <div class="eyes">
          <div class="eye"></div>
          <div class="eye"></div>
        </div>
        <div
          class="mouth"
          :class="{ talking: isLoading }"
        ></div>
      </div>
    </div>

    <!-- 채팅 메시지 표시 -->
    <div class="chat-container">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.sender]"
      >
        <p>{{ message.text }}</p>
      </div>
      <!-- 로딩 중 메시지 표시 -->
      <div v-if="isLoading" class="message gpt">
        <p>응답 중...</p>
      </div>
    </div>

    <!-- 사용자 입력 -->
    <form @submit.prevent="askGpt" class="input-container">
      <input type="text" id="prompt" v-model="prompt" placeholder="메시지를 입력하세요..." />
      <button>전송</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useGptStore } from '@/stores/gpt'

const gptStore = useGptStore()
const prompt = ref('')
const messages = ref([]) 
const isLoading = ref(false)

const askGpt = async () => {
  if (!prompt.value.trim()) return 

  const userMessage = prompt.value 
  prompt.value = '' 

  
  messages.value.push({ sender: 'user', text: userMessage })

  isLoading.value = true 

  try {
    const response = await gptStore.askGpt(userMessage)

    messages.value.push({ sender: 'gpt', text: response })
  } catch (error) {
    console.error('Error:', error)
    messages.value.push({ sender: 'gpt', text: 'Error: Unable to process your request.' })
  } finally {
    isLoading.value = false 
  }
}
</script>

<style scoped>
.chat-wrapper {
  max-width: 700px;
  margin: 20px auto; /* 공백 줄임 */
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(60, 60, 60, 0.08);
  padding: 1.5rem 1rem; /* 패딩 줄임 */
}

.chat-title {
  font-size: 2rem; /* 제목 크기 줄임 */
  font-weight: 700;
  color: #1cb0f6;
  text-align: center;
  margin-bottom: 1rem; /* 공백 줄임 */
}

.character-container {
  display: flex;
  justify-content: center;
  margin-bottom: 10px; /* 공백 줄임 */
}

.smiley-face {
  position: relative;
  width: 80px; /* 크기 줄임 */
  height: 80px;
  background-color: #f9c74f;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.eyes {
  position: absolute;
  top: 30%;
  display: flex;
  justify-content: space-between;
  width: 50%; /* 크기 줄임 */
}

.eye {
  width: 10px; /* 크기 줄임 */
  height: 10px;
  background-color: #000;
  border-radius: 50%;
}

.mouth {
  position: absolute;
  bottom: 20%;
  width: 40px; /* 크기 줄임 */
  height: 15px;
  background-color: #000;
  border-radius: 0 0 50px 50px;
  transition: transform 0.3s ease;
}

.mouth.talking {
  animation: talking 0.5s infinite;
}

@keyframes talking {
  0%, 100% {
    transform: scaleY(1);
  }
  50% {
    transform: scaleY(0.5);
  }
}

.chat-container {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 10px;
  max-height: 300px; /* 높이 줄임 */
  overflow-y: auto;
  background-color: #f7f9f9;
  margin-bottom: 10px; /* 공백 줄임 */
}

.message {
  margin: 5px 0; /* 공백 줄임 */
  padding: 8px; /* 패딩 줄임 */
  border-radius: 10px;
  max-width: 70%;
  word-wrap: break-word;
}

.message.user {
  background-color: #d1e7dd;
  align-self: flex-end;
  text-align: right;
  margin-left: auto;
}

.message.gpt {
  background-color: #f8d7da;
  align-self: flex-start;
  text-align: left;
  margin-right: auto;
}

.input-container {
  display: flex;
  gap: 5px; /* 간격 줄임 */
}

input[type="text"] {
  flex: 1;
  padding: 8px; /* 패딩 줄임 */
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  padding: 8px 15px; /* 패딩 줄임 */
  background-color: #1cb0f6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background-color: #1592c7;
}
</style>