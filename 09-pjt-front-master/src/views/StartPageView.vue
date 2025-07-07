<template>
  <div class="start-container" :class="{ 'fade-out': isZooming }" v-if="showStart">
    <h1 class="start-title">
      <span class="highlight">도서읽을래?</span><br />
      <p>Doseorae</p>
    </h1>
    <p class="start-subtitle">오늘은 어떤 책을 읽을까요??</p>
    <img
      src="@/assets/ChatGPT_Image_2025년_5월_26일_오후_01_50_08-removebg-preview.png"
      alt="책 읽는 판다 이미지"
      class="start-image"
      :class="{ 'zoom-out': isZooming }"
    />
    <button class="start-button" @click="startApp">도서래 시작하기</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isZooming = ref(false)
const showStart = ref(true)

const startApp = () => {
  isZooming.value = true // 애니메이션 시작
  setTimeout(() => {
    showStart.value = false // 페이드아웃 후 숨김
    router.push({ name: 'main' }) // 메인 페이지로 이동
  }, 1000) // 애니메이션 지속 시간 (1초)
}
</script>

<style scoped>
/* 전체 컨테이너를 화면에 꽉 차게 설정 */
.start-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; /* 화면 높이 100% */
  width: 100vw; /* 화면 너비 100% */
  background-color: #f7f9fa;
  text-align: center;
  padding: 32px; /* 여백을 더 추가 */
  overflow: hidden; /* 확대 효과를 위한 설정 */
  box-sizing: border-box;
  opacity: 1;
  transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 제목 스타일 */
.start-title {
  font-size: 4rem; /* 제목 크기 증가 */
  font-weight: bold;
  color: #333;
  margin-bottom: 24px; /* 여백 증가 */
}

.highlight {
  color: #1cb0f6; /* 강조 색상 */
}

/* 부제목 스타일 */
.start-subtitle {
  font-size: 1.5rem; /* 부제목 크기 증가 */
  color: #1cb0f6;
  margin-bottom: 40px; /* 여백 증가 */
}

/* 이미지 스타일 */
.start-image {
  width: 40%; /* 화면 너비의 40% */
  max-width: 500px; /* 최대 너비 증가 */
  height: auto;
  margin-bottom: 40px; /* 여백 증가 */
  transition: transform 1s ease; /* 확대 애니메이션 */
}

.start-image.zoom-out {
  transform: scale(2.5); /* 이미지 확대 비율 증가 */
}

/* 버튼 스타일 */
.start-button {
  background-color: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 12px; /* 버튼 모서리 둥글게 */
  padding: 20px 40px; /* 버튼 크기 증가 */
  font-size: 1.5rem; /* 버튼 텍스트 크기 증가 */
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.start-button:hover {
  background-color: #1390c4;
}

/* 반응형 스타일 */
@media (max-width: 1024px) {
  .start-title {
    font-size: 3.5rem; /* 제목 크기 감소 */
  }

  .start-subtitle {
    font-size: 1.3rem; /* 부제목 크기 감소 */
  }

  .start-image {
    width: 50%; /* 화면 너비의 50% */
  }

  .start-button {
    font-size: 1.3rem; /* 버튼 텍스트 크기 감소 */
    padding: 18px 36px; /* 버튼 크기 감소 */
  }
}

@media (max-width: 768px) {
  .start-title {
    font-size: 3rem; /* 제목 크기 감소 */
  }

  .start-subtitle {
    font-size: 1.2rem; /* 부제목 크기 감소 */
  }

  .start-image {
    width: 60%; /* 화면 너비의 60% */
  }

  .start-button {
    font-size: 1.2rem; /* 버튼 텍스트 크기 감소 */
    padding: 16px 32px; /* 버튼 크기 감소 */
  }
}

@media (max-width: 480px) {
  .start-title {
    font-size: 2.5rem; /* 제목 크기 더 감소 */
  }

  .start-subtitle {
    font-size: 1rem; /* 부제목 크기 더 감소 */
  }

  .start-image {
    width: 80%; /* 화면 너비의 80% */
  }

  .start-button {
    font-size: 1rem; /* 버튼 텍스트 크기 더 감소 */
    padding: 12px 24px; /* 버튼 크기 더 감소 */
  }
}

/* 페이드 아웃 효과 */
.start-container.fade-out {
  opacity: 0;
  pointer-events: none;
}
</style>