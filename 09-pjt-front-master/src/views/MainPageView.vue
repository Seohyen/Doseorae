<template>
  <div class="main-page-container">
    <h1 class="main-title">추천 도서 및 순위</h1>

    <!-- 추천 도서 중앙 포커스 캐러셀 -->
    <div class="centered-carousel-container">
      <button class="carousel-nav-button prev" @click="prevSlide" aria-label="이전 추천">‹</button>
      
      <div class="centered-carousel-wrapper">
        <div 
          class="centered-carousel-track"
          :style="{ transform: `translateX(${translateX}px)` }"
        >
          <div
            v-for="(book, index) in extendedBooks"
            :key="`${book.id}-${index}`"
            :class="['centered-carousel-item', getItemClass(index)]"
            @click="goToSlide(getOriginalIndex(index))"
          >
            <img :src="book.cover" :alt="book.title" class="carousel-book-image" />
            <h3 v-if="isCenterItem(index)" class="carousel-book-title">{{ book.title }}</h3>
          </div>
        </div>
      </div>
      
      <button class="carousel-nav-button next" @click="nextSlide" aria-label="다음 추천">›</button>
      
      <div class="carousel-indicators">
        <span
          v-for="(book, idx) in recommendedBooks"
          :key="book.id"
          :class="{ indicator: true, active: idx === currentSlide }"
          @click="goToSlide(idx)"
        ></span>
      </div>
    </div>

    <div class="book-section">
      <h1 class="section-title">TOP-20</h1>
      <ul class="book-list">
        <li class="book-item" v-for="book in recommendedBooks" :key="book.id">
          <img :src="book.cover" alt="book cover" class="book-image" />
          <div v-if="previewBook && previewBook.id === book.id" class="book-preview">
            <h4>{{ book.title }}</h4>
            <p v-if="book.description">{{ book.description }}</p>
            <p v-if="book.publisher">출판사: {{ book.publisher }}</p>
            <p v-if="book.published_date">출판일: {{ book.published_date }}</p>
          </div>
          <div class="book-info">
            <h3 class="book-title">{{ book.title }}</h3>
            <p class="book-author">저자: {{ book.author }}</p>
          </div>
        </li>
      </ul>
    </div>

    <div class="ranking-section">
      <h2 class="section-title">도서 순위</h2>
      <ol class="ranking-list">
        <li class="ranking-item" v-for="book in rankedBooks" :key="book.id">
          <span class="rank">#{{ book.rank }}</span>
          <span class="rank-title">{{ book.title }}</span>
        </li>
      </ol>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from "vue";
import { useBookStore } from "@/stores/book";

const BookStore = useBookStore();

// 추천 도서 데이터
const recommendedBooks = ref([]);
const rankedBooks = ref([]);
const previewBook = ref(null);

// 캐러셀 상태
const currentSlide = ref(0);
const isTransitioning = ref(false);
let sliderInterval = null;

// 캐러셀 설정
const ITEM_WIDTH = 220; // 중앙 아이템 너비
const ITEM_GAP = 40; // 아이템 간격
const SIDE_SCALE = 0.7; // 사이드 아이템 스케일

// 무한 슬라이딩을 위해 앞뒤로 복제된 책들 포함
const extendedBooks = computed(() => {
  if (recommendedBooks.value.length === 0) return [];
  
  const books = [...recommendedBooks.value];
  // 앞뒤로 2개씩 복제하여 무한 슬라이딩 구현
  const frontClones = books.slice(-2);
  const backClones = books.slice(0, 2);
  
  return [...frontClones, ...books, ...backClones];
});

// translateX 계산
const translateX = computed(() => {
  const centerIndex = 2; // 복제된 앞쪽 아이템 2개 + 현재 인덱스
  const actualIndex = centerIndex + currentSlide.value;
  // 컨테이너 중앙에서 아이템 중앙까지의 거리 계산
  const containerCenter = 600; // 컨테이너 중앙 위치 (1200px / 2)
  const baseOffset = containerCenter - (actualIndex * (ITEM_WIDTH + ITEM_GAP)) - (ITEM_WIDTH / 2);
  return baseOffset;
});

// 아이템 클래스 결정
const getItemClass = (index) => {
  const centerIndex = 2 + currentSlide.value;
  if (index === centerIndex) return 'center';
  return 'side';
};

// 중앙 아이템인지 확인
const isCenterItem = (index) => {
  const centerIndex = 2 + currentSlide.value;
  return index === centerIndex;
};

// 원본 인덱스 계산 (클릭 시 사용)
const getOriginalIndex = (extendedIndex) => {
  const booksLength = recommendedBooks.value.length;
  if (extendedIndex < 2) {
    return booksLength + extendedIndex - 2;
  } else if (extendedIndex >= 2 + booksLength) {
    return extendedIndex - 2 - booksLength;
  } else {
    return extendedIndex - 2;
  }
};

// 다음 슬라이드로 이동
const nextSlide = () => {
  if (isTransitioning.value) return;
  
  isTransitioning.value = true;
  currentSlide.value++;
  
  // 무한 슬라이딩을 위한 위치 리셋
  setTimeout(() => {
    if (currentSlide.value >= recommendedBooks.value.length) {
      currentSlide.value = 0;
    }
    isTransitioning.value = false;
  }, 600);
  
  resetAutoPlay();
};

// 이전 슬라이드로 이동
const prevSlide = () => {
  if (isTransitioning.value) return;
  
  isTransitioning.value = true;
  currentSlide.value--;
  
  // 무한 슬라이딩을 위한 위치 리셋
  setTimeout(() => {
    if (currentSlide.value < 0) {
      currentSlide.value = recommendedBooks.value.length - 1;
    }
    isTransitioning.value = false;
  }, 600);
  
  resetAutoPlay();
};

// 특정 슬라이드로 이동
const goToSlide = (idx) => {
  if (isTransitioning.value || idx === currentSlide.value) return;
  
  isTransitioning.value = true;
  currentSlide.value = idx;
  
  setTimeout(() => {
    isTransitioning.value = false;
  }, 600);
  
  resetAutoPlay();
};

// 자동 재생 시작
const startAutoPlay = () => {
  sliderInterval = setInterval(nextSlide, 3500);
};

// 자동 재생 리셋
const resetAutoPlay = () => {
  if (sliderInterval) {
    clearInterval(sliderInterval);
    startAutoPlay();
  }
};

// 데이터 로드 및 슬라이더 자동 재생
onMounted(async () => {
  await BookStore.top20Books();
  recommendedBooks.value = BookStore.bookList.slice(0, 20).map((book) => ({
    id: book.pk,
    title: book.title,
    cover: book.cover,
    author: book.author,
    description: book.description,
    publisher: book.publisher,
    published_date: book.published_date
  }));
  
  // 순위 데이터도 설정
  rankedBooks.value = recommendedBooks.value.map((book, index) => ({
    ...book,
    rank: index + 1
  }));
  
  // DOM 업데이트 후 자동 재생 시작
  await nextTick();
  setTimeout(() => {
    startAutoPlay();
  }, 1000);
});

// 컴포넌트 언마운트 시 슬라이더 정리
onUnmounted(() => {
  if (sliderInterval) clearInterval(sliderInterval);
});
</script>

<style scoped>
.main-page-container {
  font-family: 'Nunito', 'Arial', sans-serif;
  background: #f7f9fb;
  min-height: 100vh;
  padding: 2.5rem 3rem 2rem 350px; /* padding-left 값을 300px에서 350px으로 증가 */
  box-sizing: border-box;
  width: 100%;
}


.main-title {
  font-size: 2.3rem;
  font-weight: 900;
  color: #1cb0f6;
  text-align: center; 
  margin-bottom: 2.2rem;
  letter-spacing: -1px;
  width: 100%;
}

/* 중앙 포커스 캐러셀 */
.centered-carousel-container {
  position: relative;
  width: 100%;
  max-width: 1200px;
  height: 450px;
  margin: 0 auto 3rem;
  background: linear-gradient(135deg, rgba(28, 176, 246, 0.1), rgba(116, 232, 163, 0.1));
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(28, 176, 246, 0.15);
  backdrop-filter: blur(10px);
}

.centered-carousel-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  align-items: center;
  padding: 40px 0;
}

.centered-carousel-track {
  display: flex;
  align-items: center;
  gap: 40px;
  transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  will-change: transform;
  padding-left: 40px;
}

.centered-carousel-item {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 15px;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  cursor: pointer;
  overflow: hidden;
  position: relative;
  width: 220px;
  height: 320px;
}

.centered-carousel-item.side {
  opacity: 0.6;
  transform: scale(0.7);
}

.centered-carousel-item.center {
  opacity: 1;
  transform: scale(1);
  box-shadow: 0 12px 40px rgba(28, 176, 246, 0.25);
  z-index: 2;
}

.centered-carousel-item:hover {
  transform: scale(0.75);
  box-shadow: 0 15px 50px rgba(28, 176, 246, 0.3);
}

.centered-carousel-item.center:hover {
  transform: scale(1.05);
}

.carousel-book-image {
  width: 100%;
  height: 80%;
  object-fit: cover;
  border-radius: 12px 12px 0 0;
}

.carousel-book-title {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(28, 176, 246, 0.9), transparent);
  color: white;
  padding: 10px 15px 12px;
  font-size: 1.2rem;
  font-weight: 700;
  text-align: center;
  min-height: 60px;
  border-radius: 0 0 12px 12px;
}

.carousel-nav-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.95);
  color: #1cb0f6;
  font-size: 1.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.carousel-nav-button:hover {
  background: white;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 6px 20px rgba(28, 176, 246, 0.2);
}

.carousel-nav-button.prev {
  left: 20px;
}

.carousel-nav-button.next {
  right: 20px;
}

.carousel-indicators {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}

.indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator.active {
  background: #1cb0f6;
  transform: scale(1.2);
  box-shadow: 0 0 10px rgba(28, 176, 246, 0.5);
}

/* 부모 컨테이너 설정 */
.book-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 2rem auto;
  max-width: 1200px;
  width: 100%;
  padding: 0 1rem;
}

/* Top-20 제목 스타일 */
.section-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1cb0f6;
  margin-bottom: 1.5rem;
  text-align: center;
}

/* 이미지 리스트 스타일 */
.book-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  list-style: none;
  padding: 0;
  margin: 0 auto;
  width: 100%;
}

/* 개별 이미지 아이템 스타일 */
.book-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #ffffff;
  padding: 1.2rem 0.7rem;
  border: 1.5px solid #e5e5e5;
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(28, 176, 246, 0.07);
  transition: transform 0.3s, box-shadow 0.3s;
}

.book-item:hover {
  transform: translateY(-7px) scale(1.03);
  box-shadow: 0 8px 24px rgba(28, 176, 246, 0.18);
}

/* 이미지 스타일 */
.book-image {
  width: 140px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(28, 176, 246, 0.10);
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .section-title {
    font-size: 1.3rem; /* 제목 크기 줄이기 */
  }

  .book-list {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); /* 이미지 크기 줄이기 */
    gap: 1.5rem;
  }

  .book-image {
    width: 120px;
    height: 170px; /* 이미지 크기 줄이기 */
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.2rem; /* 제목 크기 더 줄이기 */
  }

  .book-list {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); /* 이미지 크기 더 줄이기 */
    gap: 1rem;
  }

  .book-image {
    width: 100px;
    height: 150px; /* 이미지 크기 더 줄이기 */
  }
}

.ranking-section {
  margin: 2.5rem auto 0;
  max-width: 1200px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 16px rgba(28, 176, 246, 0.08);
  padding: 2rem 1.5rem;
  width: 100%;
}

.ranking-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.ranking-item {
  display: flex;
  align-items: center;
  font-size: 1.15rem;
  margin-bottom: 0.7rem;
  padding: 0.7rem 0.5rem;
  border-bottom: 1px solid #e5e5e5;
  transition: background 0.2s;
}

.ranking-item:hover {
  background: #e3f3fd;
}

.rank {
  font-weight: bold;
  color: #1cb0f6;
  margin-right: 1.2rem;
  font-size: 1.2rem;
}

.rank-title {
  color: #333333;
  font-weight: 600;
}

/* 반응형 */
@media (max-width: 768px) {
  .main-page-container {
    padding: 2rem 1rem 2rem 1rem;
  }
  
  .section-title {
    margin-top: 2rem;
    margin-left: 1rem;
    font-size: 1.3rem;
    scroll-margin-top: 60px;
  }
  
  .centered-carousel-container {
    height: 300px;
    margin-bottom: 2rem;
  }
  
  .centered-carousel-item {
    width: 120px;
    height: 180px;
  }
  
  .centered-carousel-item.side {
    transform: scale(0.6);
  }
  
  .carousel-nav-button {
    width: 40px;
    height: 40px;
    font-size: 1.4rem;
  }
  
  .carousel-book-title {
    font-size: 0.8rem;
    padding: 10px 5px 5px;
  }
  
  .book-list {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    padding: 0 1rem;
  }
  
  .book-image {
    width: 120px;
    height: 170px;
  }
}

@media (max-width: 480px) {
  .main-page-container {
    padding: 1.5rem 0.8rem 2rem 0.8rem;
  }
  
  .main-title {
    font-size: 1.8rem;
  }
  
  .section-title {
    margin-left: 0.5rem;
    font-size: 1.2rem;
  }
  
  .centered-carousel-container {
    height: 250px;
  }
  
  .centered-carousel-item {
    width: 100px;
    height: 150px;
  }
  
  .centered-carousel-item.side {
    transform: scale(0.5);
  }
  
  .book-list {
    padding: 0 0.5rem;
  }
}
</style>