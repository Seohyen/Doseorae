<template>
  <div class="mypage-container">
    <h1 class="mypage-title">👤 마이페이지</h1>
    <div class="mypage-card">
      
      <div class="profile-image-container">
        <img :src="user.profile || defaultProfileImage" alt="프로필 이미지" class="profile-image" />
      </div>

      <p class="mypage-label"><span>🙍‍♂️ 이름:</span> {{ user.nickName }}</p>
      <p class="mypage-label"><span>🆔 ID:</span> {{ user.username }}</p>
      <p class="mypage-label"><span>📧 Email:</span> {{ user.email }}</p>
      <p class="mypage-label"><span>🏅 레벨:</span> {{ user.level }}</p>

      
      <div class="exp-bar-container">
        <div class="exp-bar">
          <div
            class="exp-bar-fill"
            :style="{ width: `${(user.exp / user.maxExp) * 100}%`, background: gradientColor }"
          ></div>
        </div>
        <p class="exp-text">✨ {{ user.exp }} / {{ user.maxExp }} 경험치</p>
      </div>

      <p class="mypage-label"><span>📚 관심 카테고리:</span> {{ user.likeCategory }}</p>
      <div class="follow-row">
        <button class="follow-btn" @click="showFollowers = true">
          👤 팔로워 <span class="follow-count">{{ followersList.length }}</span>
        </button>
        <button class="follow-btn" @click="showFollowings = true">
          👥 팔로잉 <span class="follow-count">{{ followingsList.length }}</span>
        </button>
      </div>

      <h2 class="interest-title">💖 관심 도서</h2>
      <div class="interest-books-grid">
        <div
          v-for="index in 100"
          :key="index"
          class="book-cover"
          :class="{ filled: index <= user.interestBooks.length }"
          :title="index <= user.interestBooks.length ? user.interestBooks[index - 1]?.title : ''"
        >
          <img
            v-if="index <= user.interestBooks.length"
            :src="user.interestBooks[index - 1]?.cover"
            :alt="user.interestBooks[index - 1]?.title"
          />
        </div>
      </div>
    </div>
    <router-link :to="{ name: 'ChangePassword'}" class="mypage-btn">🔑 비밀번호 변경</router-link>

    <div v-if="showFollowers" class="modal-overlay" @click.self="showFollowers = false">
      <div class="modal">
        <h3>👤 팔로워 목록</h3>
        <ul>
          <li v-if="followersList.length === 0" class="empty-list">팔로워가 없습니다.</li>
          <li v-for="follow in followersList" :key="follow.id">{{ follow }}</li>
        </ul>
        <button class="close-btn" @click="showFollowers = false">닫기</button>
      </div>
    </div>

    <div v-if="showFollowings" class="modal-overlay" @click.self="showFollowings = false">
      <div class="modal">
        <h3>👥 팔로잉 목록</h3>
        <ul>
          <li v-if="followingsList.length === 0" class="empty-list">팔로잉이 없습니다.</li>
          <li v-for="follow in followingsList" :key="follow.id">{{ follow }}</li>
        </ul>
        <button class="close-btn" @click="showFollowings = false">닫기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useAccountStore } from '@/stores/account';

const accountStore = useAccountStore();
const user = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  level: 0,
  exp: 0,
  maxExp: 100,
  likeCategory: '',
  followings: 0,
  followers: 0,
  interestBooks: [],
  profileImage: '', // 프로필 이미지 URL
});

const defaultProfileImage = '@/assets/default-profile.png'; // 기본 프로필 이미지 경로

const followersList = ref([]);
const followingsList = ref([]);
const showFollowers = ref(false);
const showFollowings = ref(false);

const gradientColor = computed(() => {
  const progress = user.value.exp / user.value.maxExp;
  if (progress <= 0.5) {
    return `linear-gradient(90deg, #e0e0e0 ${progress * 100}%, #a8e063 100%)`;
  } else {
    return `linear-gradient(90deg, #a8e063 ${(progress - 0.5) * 200}%, #1cb0f6 100%)`;
  }
});

const getUserInfo = async () => {
  try {
    await accountStore.getUserInfo();
    user.value = accountStore.user;
    followersList.value = accountStore.user.followers || [];
    followingsList.value = accountStore.user.followings || [];
  } catch (error) {
    console.error('사용자 정보 가져오기 실패:', error);
  }
};

onMounted(() => {
  getUserInfo();
});
</script>

<style scoped>
.mypage-container {
  min-height: 100vh;
  background: #f7f9fb;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 60px;
}

.mypage-title {
  font-size: 2.3rem;
  font-weight: 900;
  color: #1cb0f6;
  margin-bottom: 2.2rem;
  letter-spacing: -1px;
  text-align: center;
  width: 100%;
  max-width: 700px;
  background: none;
}

.mypage-card {
  background: #fff;
  border-radius: 22px;
  box-shadow: 0 4px 24px 0 rgba(28, 176, 246, 0.10);
  padding: 32px 40px;
  min-width: 340px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  border: 1.5px solid #e5e5e5;
}

.profile-image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1.5rem;
}

.profile-image {
  width: 120px;
  height: 120px;
  border-radius: 50%; /* 원형으로 표시 */
  object-fit: cover; /* 이미지 크기에 맞게 조정 */
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border: 3px solid #1cb0f6; /* 테두리 추가 */
}

.exp-bar-container {
  width: 100%;
  margin: 20px 0;
}

.exp-bar {
  width: 100%;
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.exp-bar-fill {
  height: 100%;
  transition: width 0.3s ease, background 0.3s ease;
  border-radius: 10px;
}

.exp-text {
  margin-top: 8px;
  font-size: 1rem;
  color: #1cb0f6;
  text-align: center;
  font-weight: 700;
}

.interest-title {
  font-size: 1.3rem;
  color: #1cb0f6;
  margin: 24px 0 12px 0;
  font-weight: 800;
  letter-spacing: -1px;
}

.interest-books-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 7px;
  width: 100%;
  max-width: 600px;
}

.book-cover {
  width: 48px;
  height: 48px;
  background: #eaf6fd;
  border-radius: 6px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid #d0eafd;
}

.book-cover.filled {
  background: none;
  border: none;
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(28, 176, 246, 0.10);
}

.book-cover:hover {
  transform: scale(1.08);
  box-shadow: 0 4px 16px rgba(28, 176, 246, 0.18);
}

.mypage-label {
  font-size: 1.08rem;
  margin-bottom: 14px;
  color: #22223b;
  display: flex;
  align-items: center;
  gap: 7px;
}
.mypage-label span {
  font-weight: 700;
  color: #1cb0f6;
  margin-right: 8px;
  font-size: 1.13rem;
  display: flex;
  align-items: center;
  gap: 3px;
}

.follow-row {
  display: flex;
  gap: 16px;
  margin-bottom: 14px;
}
.follow-btn {
  background: #f0f8ff;
  border: 1.5px solid #1cb0f6;
  color: #1cb0f6;
  border-radius: 14px;
  font-weight: 700;
  font-size: 1.05rem;
  padding: 6px 18px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 7px;
}
.follow-btn:hover {
  background: #1cb0f6;
  color: #fff;
  box-shadow: 0 2px 8px rgba(28,176,246,0.13);
}
.follow-count {
  font-weight: 900;
  margin-left: 4px;
  color: #1cb0f6;
  background: #eaf6fd;
  border-radius: 8px;
  padding: 2px 8px;
  font-size: 1.01rem;
}

.mypage-btn {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 24px;
  background: linear-gradient(90deg, #1cb0f6 60%, #a8e063 100%);
  color: #fff;
  border-radius: 18px;
  font-weight: 800;
  font-size: 1.07rem;
  text-decoration: none;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px 0 rgba(28, 176, 246, 0.10);
  border: none;
  letter-spacing: 0.5px;
}
.mypage-btn:hover {
  background: linear-gradient(90deg, #1391c7 60%, #a8e063 100%);
  box-shadow: 0 4px 16px rgba(28, 176, 246, 0.18);
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(44, 62, 80, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.modal {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(28,176,246,0.13);
  padding: 2rem 2.2rem 1.5rem 2.2rem;
  min-width: 270px;
  max-width: 90vw;
  max-height: 70vh;
  overflow-y: auto;
  text-align: center;
}
.modal h3 {
  color: #1cb0f6;
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 1.2rem;
}
.modal ul {
  list-style: none;
  padding: 0;
  margin: 0 0 1.2rem 0;
}
.modal li {
  padding: 0.5rem 0;
  font-size: 1.07rem;
  color: #22223b;
  border-bottom: 1px solid #e5e5e5;
}
.modal li:last-child {
  border-bottom: none;
}
.empty-list {
  color: #aaa;
  font-style: italic;
}
.close-btn {
  margin-top: 0.5rem;
  background: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 7px 22px;
  font-size: 1.03rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}
.close-btn:hover {
  background: #1391c7;
}
</style>