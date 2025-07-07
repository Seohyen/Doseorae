<template>
  
  <div class="app-container">
    <nav class="navbar-vertical" v-if="!isMainPage">
      <div class="nav-logo">
        <img src="@/assets/book-icon.png" alt="Logo" class="nav-logo-icon" />
        <RouterLink class="nav-link1" :to="{ name: 'main' }"> Doseorae</RouterLink>
      </div>
      
      <div class="nav-search">
        <input 
          type="text"
          v-model="searchQuery" 
          placeholder="Search..." 
          class="search-bar"/>
        <button class="click-bt" @click="goToSearch" aria-label="검색">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 20 20">
            <circle cx="9" cy="9" r="7" stroke="#fff" stroke-width="2"/>
            <line x1="14.2" y1="14.2" x2="18" y2="18" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
      <div class="nav-menu">
        <RouterLink class="nav-link" :to="{ name: 'BookList' }">📚 Book</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'CommunityView' }">💬 Community</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'AskGptView' }">🤖 Ask GPT</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'QuizGptView' }">📝 Quiz GPT</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'DebateGptView' }">🗣️ Debate GPT</RouterLink>
        <RouterLink class="nav-link" :to="{ name: 'CardGame' }">🎮 Game</RouterLink> <!-- Game 버튼 추가 -->
      </div>
      <div class="nav-buttons">
        <template v-if="!accountStore.isLogIned">
          <div class="dropdown">
            <button class="dropdown-toggle" @click="toggleDropdown" type="button">🐼</button>
            <ul v-show="isDropdownOpen" class="dropdown-menu">
              <li>
                <RouterLink class="nav-link" :to="{ name: 'SignUpView' }" @click="closeDropdown">🆕Sign In</RouterLink>
              </li>
              <li>
                <RouterLink class="logIn-btn" :to="{ name: 'LogInView' }" @click="closeDropdown">🔑Log In</RouterLink>
              </li>
            </ul>
          </div>
        </template>

        <template v-else>
          <div class="dropdown">
            <button class="dropdown-toggle" @click="toggleDropdown" type="button">🐼</button>
            <ul v-show="isDropdownOpen" class="dropdown-menu">
              <li>
                <RouterLink class="nav-link" :to="{ name: 'MyPageView' }" @click="closeDropdown">🙍My Page</RouterLink>
              </li>
              <li>
                <button class="logout-btn" @click="handleLogout" type="button">🚪Log Out</button>
              </li>
            </ul>
          </div>
        </template>
      </div>
    </nav>
    <!-- RouterView는 항상 렌더링 -->
    <main class="content" @click="closeDropdown">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAccountStore } from '@/stores/account'
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const accountStore = useAccountStore()
const searchQuery = ref('')

const router = useRouter()
const goToSearch = () => {
  router.push({ name: 'BookSearch', query: { q: searchQuery.value } })
  searchQuery.value = '' // 검색 후 입력 필드 초기화
}

const logOutMember = () => {
  accountStore.logOutMember()
  closeDropdown()
}

const handleLogout = () => {
  logOutMember()
}

const route = useRoute()
const isMainPage = ref(false)

// 드롭다운 상태 관리
const isDropdownOpen = ref(false)

const toggleDropdown = (event) => {
  event.stopPropagation() // 이벤트 버블링 방지
  console.log('드롭다운 토글:', !isDropdownOpen.value)
  isDropdownOpen.value = !isDropdownOpen.value
}

const closeDropdown = () => {
  isDropdownOpen.value = false
}

// 외부 클릭 시 드롭다운 닫기
const handleClickOutside = (event) => {
  const dropdown = event.target.closest('.dropdown')
  if (!dropdown && isDropdownOpen.value) {
    closeDropdown()
  }
}

// 컴포넌트 마운트/언마운트 시 이벤트 리스너 추가/제거
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// 현재 라우트가 MainPageView인지 확인
watch(
  () => route.name,
  (newRouteName) => {
    isMainPage.value = newRouteName === 'Start'
  },
  { immediate: true }
)
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.app-container {
  font-family: 'Nunito', 'Arial', sans-serif;
  background: #f7f9fb;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 세로 네비게이션 바 스타일 */
.navbar-vertical {
  position: fixed;
  top: 0;
  left: 0;
  width: 300px; /* 기존 210px → 270px로 넓힘 */
  height: 100vh;
  background: #fff;
  border-right: 2px solid #e5e5e5;
  box-shadow: 2px 0 8px 0 rgba(60, 60, 60, 0.06);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  z-index: 100;
  padding: 1.5rem 0 1.5rem 0;
}

.nav-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2.5rem;
  gap: 0.5rem; /* 로고와 텍스트 간격 */
}

.nav-logo-icon {
  width: 40px; /* 로고 크기 */
  height: 40px;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  margin-bottom: auto;
  align-items: stretch;
  padding: 0 1.2rem;
}
.nav-link1 {
  text-decoration: none;
  color: #1cb0f6;
  font-weight: 700;
  font-size: 1.8rem;
  padding: 0.7rem 1.1rem;
  border-radius: 18px;
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}


.nav-link {
  text-decoration: none;
  color: #1cb0f6;
  font-weight: 700;
  font-size: 1.1rem;
  padding: 0.7rem 1.1rem;
  border-radius: 18px;
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.nav-link:hover {
  background: #e3f3fd;
  color: #1cb0f6;
}

/* nav-buttons 스타일 추가 */
.nav-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 1.2rem;
  margin-top: 2rem;
}

/* 드롭다운 스타일 */
.dropdown {
  position: relative;
  width: 100%;
}

.dropdown-toggle {
  background: #1cb0f6;
  color: #fff;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 18px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  box-shadow: 0 2px 8px 0 rgba(60, 60, 60, 0.06);
  transition: background 0.2s;
  width: 100%;
  margin-bottom: 0.5rem;
}

.dropdown-toggle:hover {
  background: #1592c7;
}

.dropdown-menu {
  position: absolute;
  left: 0;           /* 왼쪽 정렬 */
  bottom: 110%;      /* 버튼 위에 표시 */
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(60, 60, 60, 0.13);
  list-style: none;
  padding: 0.5rem 0;
  margin: 0;
  z-index: 2000;     /* 충분히 높게 */
  min-width: 170px;
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  transition: opacity 0.2s ease, visibility 0.2s ease, transform 0.2s ease;
}

/* 드롭다운이 닫혔을 때의 스타일 */
.dropdown-menu:not([style*="display: none"]) {
  display: block;
}

.dropdown-menu li {
  padding: 0.5rem 1.5rem;
  font-size: 1rem;
  color: #333;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dropdown-menu li:hover {
  background: #e3f3fd;
  color: #1cb0f6;
}

.dropdown-menu li .nav-link {
  padding: 0;
  background: none;
  color: inherit;
  font-size: inherit;
  font-weight: 500;
  width: 100%;
  border-radius: 0;
}

.dropdown-menu li .nav-link:hover {
  background: none;
  color: inherit;
}

.logIn-btn,
.logout-btn {
  background: none;
  color: inherit;
  border: none;
  padding: 0;
  font-weight: 500;
  font-size: inherit;
  cursor: pointer;
  transition: color 0.2s;
  width: 100%;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logIn-btn:hover,
.logout-btn:hover {
  color: inherit;
  background: none;
}

/* 검색바 스타일 */
.search-bar {
  width: 200px;
  padding: 0.7rem 1.2rem;
  border: 2px solid #e5e5e5;
  border-radius: 18px;
  font-size: 1rem;
  background: #f7f9fb;
  transition: border 0.2s;
  margin: 0;
}

.search-bar:focus {
  border: 2px solid #1cb0f6;
  outline: none;
}



.search-bar + button:hover {
  background: #1592c7;
  color: #fff;
}

.click-bt {
  background: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 18px;
  padding: 0.7rem 1.1rem;
  font-size: 1rem;
  font-weight: 700;
  margin-left: 0.2rem; /* 더 좁게 조정 */
  cursor: pointer;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px 0 rgba(60, 60, 60, 0.06);
  vertical-align: middle;
  outline: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.click-bt:hover,
.click-bt:focus {
  background: #1592c7;
  color: #fff;
  box-shadow: 0 4px 16px 0 rgba(28, 176, 246, 0.13);
}

@media (max-width: 900px) {
  .navbar-vertical {
    width: 100vw;
    height: auto;
    flex-direction: row;
    position: static;
    border-right: none;
    border-bottom: 2px solid #e5e5e5;
    box-shadow: 0 2px 8px 0 rgba(60, 60, 60, 0.06);
    padding: 0.7rem 0.5rem;
  }
  .nav-logo {
    margin-bottom: 0;
    margin-right: 1.2rem;
  }
  .nav-menu {
    flex-direction: row;
    gap: 1rem;
    margin-bottom: 0;
    padding: 0;
  }
  .nav-buttons {
    margin-top: 0;
    padding: 0;
  }
  .search-bar {
    margin: 0;
    width: 100%;
  }
  .search-bar + button {
    width: 100%;
    margin: 0;
    padding: 0.7rem 0;
    font-size: 1rem;
  }
  .content {
    margin-left: 0;
    padding: 1.2rem 0.2rem 0 0.2rem;
  }
  
  .dropdown-menu {
    bottom: auto;
    top: 110%;
  }
}

.nav-search {
  display: flex;
  flex-direction: row;
  align-items: center; /* 이 줄이 중요! */
  gap: 0.7rem;
  margin: 0 1.2rem 1.5rem 1.2rem;
}
</style>