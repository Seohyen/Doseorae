<template>
  <div class="login-container">
    <h1 class="login-title">로그인</h1>
    <form @submit.prevent="logInMember" class="login-form">
      <div class="form-group">
        <label for="username" class="form-label">이메일 또는 아이디</label>
        <input
          type="text"
          id="username"
          name="username"
          v-model="username"
          class="form-input"
          placeholder="이메일 또는 아이디"
        />
      </div>
      <div class="form-group">
        <label for="password" class="form-label">비밀번호</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="form-input"
          placeholder="비밀번호를 입력하세요"
        />
      </div>
      <div class="form-group">
        <button class="login-button">로그인하기</button>
      </div>
      <div class="divider">또는</div>
      <div class="social-login">
        <button class="social-button google">GOOGLE</button>
      </div>
    </form>
    <p class="login-footer">
      도서래에 가입하면 도서래의 이용 약관 및 개인정보처리방침에 동의하게 됩니다.
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account.js'

const store = useAccountStore()
const username = ref('')
const password = ref('')

const logInMember = function () {
  const userData = {
    username: username.value,
    password: password.value,
  }
  store.logInMember(userData)
}
</script>

<style scoped>
/* 전체 컨테이너 */
.login-container {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f7f9fb;
  padding: 0;
  box-sizing: border-box;
}

/* 제목 스타일 */
.login-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1cb0f6;
  margin-bottom: 2rem;
  letter-spacing: -1px;
}

/* 폼 스타일 */
.login-form {
  width: 100%;
  max-width: 400px;
  background: #fff;
  padding: 2.2rem 2rem 1.5rem 2rem;
  border-radius: 18px;
  box-shadow: 0 4px 24px 0 rgba(60, 60, 60, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  align-items: center;
}

.form-group {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 600;
  color: #1cb0f6;
  margin-bottom: 0.2rem;
  font-size: 1.05rem;
  text-align: left;
}

.form-input {
  width: 100%;
  padding: 0.9rem 1.1rem;
  border: 2px solid #e5e5e5;
  border-radius: 14px;
  font-size: 1.08rem;
  background: #f7f9fb;
  transition: border 0.2s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #1cb0f6;
  box-shadow: 0 0 4px rgba(28, 176, 246, 0.13);
}

/* 버튼 스타일 */
.login-button {
  width: 100%;
  background-color: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 18px;
  padding: 0.9rem 0;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 0.5rem;
}

.login-button:hover {
  background-color: #1592c7;
}

/* 구분선 */
.divider {
  margin: 1.2rem 0 0.7rem 0;
  font-size: 0.95rem;
  color: #aaa;
  position: relative;
  width: 100%;
  text-align: center;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%;
  height: 1px;
  background: #e5e5e5;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

/* 소셜 로그인 버튼 */
.social-login {
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 8px;
}

.social-button {
  flex: 1;
  padding: 0.8rem 0;
  border: none;
  border-radius: 14px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  background: #fff;
  color: #1cb0f6;
  border: 2px solid #1cb0f6;
  transition: background 0.2s, color 0.2s;
}

.social-button:hover {
  background: #1cb0f6;
  color: #fff;
}

/* 푸터 스타일 */
.login-footer {
  margin-top: 16px;
  font-size: 0.8rem;
  color: #777;
  line-height: 1.4;
}
</style>