<template>
  <div class="memory-game-section">
    <h1 class="section-title">같은 카드 맞추기 게임</h1>

    <div v-if="!isGameStarted" class="settings">
      <label for="difficulty">난이도 선택: </label>
      <select v-model="difficulty" id="difficulty">
        <option value="easy">하 (60초)</option>
        <option value="medium">중 (15초)</option>
        <option value="hard">상 (10초)</option>
      </select>
      <button @click="startGame">게임 시작</button>
    </div>

    <div v-else>
      <p class="timer">남은 시간: {{ timer }}초</p>
      <div class="memory-game-grid">
        <div
          v-for="(card, index) in shuffledCards"
          :key="index"
          class="memory-card"
          @click="flipCard(index)"
        >
          <div class="card-inner" :class="{ flipped: card.isFlipped || card.isMatched || showAllCards }">
            <img :src="card.cover" :alt="card.title" class="card-image" />
            <div class="card-back"></div>
          </div>
        </div>
      </div>
      <p v-if="isGameWon" class="game-won-message">축하합니다! 모든 카드를 맞췄습니다! 🎉</p>
      <p v-else-if="timer === 0" class="game-over-message">시간 초과! 다시 시도해보세요. ⏳</p>
      <button @click="resetGame" class="reset-button">다시하기</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useBookStore } from "@/stores/book";
import { useGptStore } from '@/stores/gpt'

const BookStore = useBookStore();
const recommendedBooks = ref([]);
const shuffledCards = ref([]);
const flippedCards = ref([]);
const isGameWon = ref(false);
const timer = ref(0);
const showAllCards = ref(false);
const isGameStarted = ref(false);
const difficulty = ref("easy");
let timerInterval = null;
const gptStore = useGptStore()

const getTimeByDifficulty = () => {
  if (difficulty.value === "easy") return 60;
  if (difficulty.value === "medium") return 15;
  return 10;
};

const shuffleCards = (cards) => {
  const duplicatedCards = [...cards, ...cards];
  for (let i = duplicatedCards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [duplicatedCards[i], duplicatedCards[j]] = [duplicatedCards[j], duplicatedCards[i]];
  }
  return duplicatedCards.map((card) => ({ ...card, isFlipped: false, isMatched: false }));
};

const flipCard = (index) => {
  if (
    timer.value === 0 ||
    isGameWon.value ||
    showAllCards.value ||
    shuffledCards.value[index].isFlipped ||
    shuffledCards.value[index].isMatched ||
    flippedCards.value.length === 2
  ) {
    return;
  }

  shuffledCards.value[index].isFlipped = true;
  flippedCards.value.push(index);

  if (flippedCards.value.length === 2) {
    const [firstIndex, secondIndex] = flippedCards.value;
    if (shuffledCards.value[firstIndex].id === shuffledCards.value[secondIndex].id) {
      shuffledCards.value[firstIndex].isMatched = true;
      shuffledCards.value[secondIndex].isMatched = true;
      flippedCards.value = [];
      checkGameWon();
    } else {
      setTimeout(() => {

        if (timer.value > 0) {
          shuffledCards.value[firstIndex].isFlipped = false;
          shuffledCards.value[secondIndex].isFlipped = false;
          flippedCards.value = [];
        }
      }, 1000);
    }
  }
};

const checkGameWon = () => {
  isGameWon.value = shuffledCards.value.every((card) => card.isMatched);
  
  if (isGameWon.value) {
    gptStore.userExp()
  }
  if (isGameWon.value) clearInterval(timerInterval);
};

const startTimer = () => {
  timer.value = getTimeByDifficulty();
  timerInterval = setInterval(() => {
    if (timer.value > 0) {
      timer.value--;
    } else {
      clearInterval(timerInterval);

      flippedCards.value.forEach(index => {
        if (!shuffledCards.value[index].isMatched) {
          shuffledCards.value[index].isFlipped = false;
        }
      });
      flippedCards.value = [];
    }
  }, 1000);
};

const startGame = async () => {
  isGameStarted.value = true;
  isGameWon.value = false;
  flippedCards.value = [];
  showAllCards.value = true;

  await BookStore.top20Books();
  recommendedBooks.value = BookStore.bookList.slice(0, 10).map((book) => ({
    id: book.pk,
    title: book.title,
    cover: book.cover,
  }));

  shuffledCards.value = shuffleCards(recommendedBooks.value);

  setTimeout(() => {
    showAllCards.value = false;
    startTimer();
  }, 2000);
};

const resetGame = () => {
  clearInterval(timerInterval);
  isGameStarted.value = false;
  timer.value = 0;
};
</script>

<style>
.memory-game-section {
  margin: 3rem auto;
  max-width: 1200px;
  text-align: center;
}

.settings {
  margin: 2rem;
}

.settings select,
.settings button {
  font-size: 1rem;
  padding: 0.5rem;
  margin-left: 1rem;
}

.memory-game-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.memory-card {
  width: 100px;
  height: 140px;
  perspective: 1000px;
  cursor: pointer;
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transform-origin: center center;
  transition: transform 0.6s;
}

.card-inner.flipped {
  transform: rotateY(180deg);
}

.card-image,
.card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  top: 0;
  left: 0;
}

.card-image {
  object-fit: cover;
  transform: rotateY(180deg);
}

.card-back {
  background: 
    url('@/assets/ChatGPT_Image_2025년_5월_26일_오후_01_50_08-removebg-preview.png') no-repeat center center,
    linear-gradient(rgba(128, 130, 131, 0.8), rgba(28, 176, 246, 0.8));
  background-size: cover;
  transform: rotateY(0deg);
}

.timer {
  font-size: 1.2rem;
  font-weight: bold;
  color: #ff5722;
}

.game-won-message {
  margin-top: 2rem;
  font-size: 1.5rem;
  color: #28a745;
  font-weight: bold;
}

.game-over-message {
  margin-top: 2rem;
  font-size: 1.5rem;
  color: #dc3545;
  font-weight: bold;
}

.reset-button {
  margin-top: 1.5rem;
  padding: 0.7rem 1.5rem;
  font-size: 1rem;
  background-color: #1cb0f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>