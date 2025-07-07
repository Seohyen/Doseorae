<template>
  <div class="quiz-container">
    <h1 class="quiz-title">📚 도서 퀴즈</h1>

    <div class="input-container">
      <input
        type="text"
        v-model="bookName"
        placeholder="도서 이름을 입력하세요"
        class="quiz-input"
      />
      <button @click="startQuiz" class="quiz-start-btn">퀴즈 시작!</button>
    </div>

   
    <div v-if="isLoading" class="loading-message">
      <p>AI가 퀴즈를 생성 중이에요! 잠시만 기다려주세요...</p>
    </div>

   
    <div v-if="quizResult && !isLoading" class="quiz-result">
      <h2 class="quiz-question-title">GPT의 퀴즈:</h2>
      <p class="quiz-question"><strong>문제:</strong> {{ quize.question }}</p>
      <ul class="quiz-options">
        <li
          v-for="(option, key) in quize.options"
          :key="key"
          @click="onOptionClick(option, key)"
          class="quiz-option"
        >
          {{ key }}: {{ option }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useGptStore } from '@/stores/gpt'
import { useRouter } from 'vue-router'

const gptStore = useGptStore()
const bookName = ref('')
const quizResult = ref(null)
const quize = ref(null)
const queizeCount = ref(0)
const isLoading = ref(false)

const router = useRouter()

const onOptionClick = (selectedOption, selectedKey) => {
  // 선택된 보기를 콘솔로 확인하거나 API로 전송 가능
  console.log('선택한 보기 키:', selectedKey)
  console.log('선택한 보기 내용:', selectedOption)

  if (selectedKey === quize.value.answer) {
    queizeCount.value += 1

    if (queizeCount.value >= quizResult.value.length) {
      alert('퀴즈가 끝났습니다!')
      gptStore.userExp()
      router.go(-1)
      return
    }

    quize.value = quizResult.value[queizeCount.value]
  } else {
    alert('땡! 정답이 아닙니다.')
  }

  // 여기에 선택한 보기 키를 gptStore나 서버로 전송하는 코드도 추가 가능
  // 예: gptStore.sendSelectedAnswer({ key: selectedKey, value: selectedOption })
}

const startQuiz = async () => {
  if (!bookName.value.trim()) {
    alert('도서 이름을 입력하세요!')
    return
  }

  isLoading.value = true

  try {
    const response = await gptStore.makeQuiz(bookName.value.trim())
    quizResult.value = response
    queizeCount.value = 0
    quize.value = quizResult.value[0]
  } catch (err) {
    console.error('Error:', err)
    alert('퀴즈를 가져오는 중 오류가 발생했습니다.')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 40px auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(60, 60, 60, 0.08);
  padding: 2.5rem 2rem;
}

.quiz-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1cb0f6;
  text-align: center;
  margin-bottom: 2rem;
}

.input-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.quiz-input {
  flex: 1;
  padding: 0.7rem 1.2rem;
  border: 2px solid #e5e5e5;
  border-radius: 18px;
  font-size: 1rem;
  background: #f7f9fb;
  transition: border 0.2s;
}

.quiz-input:focus {
  border: 2px solid #1cb0f6;
  outline: none;
}

.quiz-start-btn {
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

.quiz-start-btn:hover {
  background: #1592c7;
  color: #fff;
  box-shadow: 0 4px 16px 0 rgba(28, 176, 246, 0.13);
}

.loading-message {
  text-align: center;
  font-size: 1.2rem;
  color: #888;
  margin-top: 1.5rem;
}

.quiz-result {
  margin-top: 2rem;
}

.quiz-question-title {
  font-size: 1.5rem;
  color: #1cb0f6;
  margin-bottom: 1rem;
  font-weight: 700;
}

.quiz-question {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.quiz-options {
  list-style: none;
  padding: 0;
  margin: 0;
}

.quiz-option {
  padding: 0.7rem 1rem;
  background: #f7f9fb;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.quiz-option:hover {
  background: #1cb0f6;
  color: #fff;
}
</style>