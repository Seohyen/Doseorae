<template>
  <div class="mypage-container">
    <h1 class="mypage-title">🙍‍♂️ 유저 정보</h1>
    <div class="mypage-card">
      <p class="mypage-label"><span>📝 이름:</span> {{ detailUser.nickName }}</p>
      <p class="mypage-label"><span>🆔 ID:</span> {{ detailUser.username }}</p>
      <p class="mypage-label"><span>📧 Email:</span> {{ detailUser.email }}</p>
      <p class="mypage-label"><span>🏅 레벨:</span> {{ detailUser.level }}</p>

      <!-- 경험치 바 -->
      <div class="exp-bar-container">
        <div class="exp-bar">
          <div
            class="exp-bar-fill"
            :style="{ width: `${(detailUser.exp / detailUser.maxExp) * 100}%`, background: gradientColor }"
          ></div>
        </div>
        <p class="exp-text">✨ {{ detailUser.exp }} / {{ detailUser.maxExp }} 경험치</p>
      </div>

      <p class="mypage-label"><span>📚 관심 카테고리:</span> {{ detailUser.likeCategory }}</p>
      <p class="mypage-label"><span>👀 팔로잉:</span> {{ detailUser.followings.length }}</p>
      <p class="mypage-label"><span>👥 팔로워:</span> {{ detailUser.followers.length }}</p>
      
      <!-- 팔로우/언팔로우 버튼 -->
      <button
        @click="goToFollow"
        :class="isFollowing ? 'mypage-btn unfollow-btn' : 'mypage-btn follow-btn'"
        :disabled="isLoading"
      >
        {{ isFollowing ? '언팔로우 💔' : '팔로우 💙' }}
      </button>
      
      <h2 class="interest-title">💖 관심 도서</h2>
      <div class="interest-books-grid">
        <!-- 100개의 빈칸 생성 -->
        <div
          v-for="index in 100"
          :key="index"
          class="book-cover"
          :class="{ filled: index <= detailUser.interestBooks.length }"
          :title="index <= detailUser.interestBooks.length ? detailUser.interestBooks[index - 1]?.title : ''"
        >
          <!-- 관심 도서가 있는 경우 이미지 표시 -->
          <img
            v-if="index <= detailUser.interestBooks.length"
            :src="detailUser.interestBooks[index - 1]?.cover"
            :alt="detailUser.interestBooks[index - 1]?.title"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAccountStore } from '@/stores/account';
import { useRoute } from 'vue-router';

const route = useRoute();
const accountStore = useAccountStore();

const isLoading = ref(false);

const detailUser = ref({
  username: '',
  email: '',
  nickName: '',
  level: 0,
  exp: 0,
  maxExp: 100,
  likeCategory: '',
  followings: [],
  followers: [],
  interestBooks: [],
});

const isFollowing = computed(() => {
  if (!accountStore.user || !accountStore.user.followings || !detailUser.value.username) {
    return false;
  }
  return accountStore.user.followings.includes(detailUser.value.username);
});

const gradientColor = computed(() => {
  const progress = detailUser.value.exp / detailUser.value.maxExp;
  if (progress <= 0.5) {
    return `linear-gradient(90deg, #e0e0e0 ${progress * 100}%, #a8e063 100%)`;
  } else {
    return `linear-gradient(90deg, #a8e063 ${(progress - 0.5) * 200}%, #1cb0f6 100%)`;
  }
});

const refreshUserData = async () => {
  try {
    const res = await accountStore.getOtherUserInfo(route.params.id);
    if (res.success) {
      detailUser.value = res.data;
    } else {
      console.error('유저 정보 불러오기 실패:', res.error);
    }

    const userRes = await accountStore.getUserInfo();
    if (userRes.success) {
      accountStore.user = userRes.data;
    }
  } catch (error) {
    console.error('유저 정보를 불러오는 중 오류 발생:', error);
  }
};

refreshUserData();

const goToFollow = async () => {
  if (isLoading.value) return;

  try {
    isLoading.value = true;
    await accountStore.getFollow(route.params.id);
    await refreshUserData();
  } catch (error) {
    console.error('팔로우/언팔로우 중 오류 발생:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* 마이페이지 컨테이너 */
.mypage-container {
  min-height: 100vh;
  background: #f7f9fb;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 60px;
}

/* 제목 스타일 */
.mypage-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #1cb0f6;
  margin-bottom: 32px;
  letter-spacing: -1px;
  text-align: center;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* 카드 스타일 */
.mypage-card {
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 4px 24px 0 rgba(60, 60, 60, 0.08);
  padding: 32px 40px;
  min-width: 340px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* 경험치 바 컨테이너 */
.exp-bar-container {
  width: 100%;
  margin: 20px 0;
}

.exp-bar {
  width: 100%;
  height: 20px;
  background: #e0e0e0; /* 바탕색 */
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.exp-bar-fill {
  height: 100%;
  transition: width 0.3s ease, background 0.3s ease;
}

.exp-text {
  margin-top: 8px;
  font-size: 1rem;
  color: #333;
  text-align: center;
}

/* 관심 도서 섹션 */
.interest-title {
  font-size: 1.5rem;
  color: #1cb0f6;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.interest-books-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr); /* 10칸씩 배치 */
  gap: 5px;
  width: 100%;
  max-width: 600px;
}

.book-cover {
  width: 50px;
  height: 50px;
  background: #e0e0e0; /* 기본 빈칸 색상 */
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.book-cover.filled {
  background: none; /* 이미지가 있는 경우 배경 제거 */
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.book-cover:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* 라벨 스타일 */
.mypage-label {
  font-size: 1.1rem;
  margin-bottom: 16px;
  color: #22223b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.mypage-label span {
  font-weight: 600;
  color: #1cb0f6;
  margin-right: 8px;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

/* 버튼 스타일 */
.mypage-btn {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 24px;
  border-radius: 18px;
  font-weight: 700;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.2s;
  box-shadow: 0 2px 8px 0 rgba(60, 60, 60, 0.08);
  border: none;
  cursor: pointer;
}

.mypage-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.follow-btn {
  background: #1cb0f6;
  color: #fff;
}

.follow-btn:hover:not(:disabled) {
  background: #1391c7;
}

.unfollow-btn {
  background: #ff6b6b;
  color: #fff;
}

.unfollow-btn:hover:not(:disabled) {
  background: #ff5252;
}
</style>
