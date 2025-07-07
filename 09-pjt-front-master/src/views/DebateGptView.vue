<template>
  <div class="chat-wrapper">
    <h1>GPT와 토론</h1>
    <div v-show="!isStart">
      <input
        type="text"
        v-model="bookName"
        placeholder="책 제목을 입력하세요"
      />
      <button @click.prevent="initializeDebate">토론 시작</button>
    </div>
    <!-- 사용자 입력 -->
    <form @submit.prevent="sendMessage" class="input-container" v-show = "isStart">
      <input
        type="text"
        v-model="prompt"
        placeholder="토론 주제를 입력하세요"
      />
      <button>Send</button>
    </form>

    <!-- 채팅 메시지 표시 -->
    <div class="chat-container">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.sender]"
      >
        <p>{{ message.text }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const BASE_API = 'http://127.0.0.1:8000' 
const bookName = ref('') 
const prompt = ref('') 
const messages = ref([]) 
const isLoading = ref(false) 
const isStart = ref(false)

const initializeDebate = async () => {
  if (!bookName.value.trim()) {
    alert('책 정보를 입력하세요!')
    return
  }
  try {
    isLoading.value = true
    const response = await axios.post(`${BASE_API}/activity/debate_gpt`, {
      bookName: bookName.value.trim(),
      prompt: "start",
      user_id: "user123", 
    })
    messages.value.push({ sender: 'gpt', text: response.data });
    isStart.value = true
  } catch (err) {
    console.error('Error:', err)
    alert('초기 대화를 시작하는 중 오류가 발생했습니다.')
  } finally {
    isLoading.value = false
  }
}


const sendMessage = async () => {
  if (!prompt.value.trim()) {
    alert('메시지를 입력하세요!')
    return
  }

  const userMessage = prompt.value
  messages.value.push({ sender: 'user', text: userMessage })
  prompt.value = '' 

  try {
    isLoading.value = true
    const response = await axios.post(`${BASE_API}/activity/debate_gpt`, {
      bookName: bookName.value.trim(),
      prompt: userMessage,
      user_id: "user123", 
    })
    messages.value.push({ sender: 'gpt', text: response.data });
  } catch (err) {
    console.error('Error:', err)
    alert('메시지를 보내는 중 오류가 발생했습니다.')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.chat-wrapper {
  max-width: 800px;
  margin: 40px auto;
  padding: 2.5rem 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(60, 60, 60, 0.08);
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1cb0f6;
  text-align: center;
  margin-bottom: 2rem;
}

input[type="text"] {
  flex: 1;
  padding: 0.7rem 1.2rem;
  border: 2px solid #e5e5e5;
  border-radius: 18px;
  font-size: 1rem;
  background: #f7f9fb;
  transition: border 0.2s;
}

input[type="text"]:focus {
  border: 2px solid #1cb0f6;
  outline: none;
}

button {
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

button:hover {
  background: #1592c7;
  color: #fff;
  box-shadow: 0 4px 16px 0 rgba(28, 176, 246, 0.13);
}

.input-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.chat-container {
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  padding: 1rem;
  max-height: 400px;
  overflow-y: auto;
  background-color: #f7f9fb;
  margin-bottom: 2rem;
}

.message {
  margin: 10px 0;
  padding: 10px 14px;
  border-radius: 18px;
  max-width: 70%;
  word-wrap: break-word;
  font-size: 1rem;
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

</style>