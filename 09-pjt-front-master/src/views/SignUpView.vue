<template>
  <div class="signup-container">
    <h1 class="signup-title">회원가입</h1>
    <form class="signup-form" @submit.prevent="signUpMember">
      <div class="form-group">
        <label for="nickName">이름</label>
        <input type="text" id="nickName" v-model="nickName" required />
      </div>
      <div class="form-group">
        <label for="user-id">아이디</label>
        <input type="text" id="user-id" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input type="password" id="password" v-model="password1" required />
      </div>
      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model="password2" required />
      </div>
      <div class="form-group">
        <label for="likeCategory">선호 카테고리</label>
        <select id="likeCategory" v-model="likeCategory" required>
          <option value="" disabled>카테고리를 선택하세요</option>
          <option v-for="category in categories" :key="category.pk" :value="category.fields.name">
            {{ category.fields.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="profile">프로필 이미지</label>
        <input type="file" id="profile" @change="onFileChange" accept="image/*" />
      </div>
      <button class="signup-btn" type="submit">Sign Up</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAccountStore } from "@/stores/account.js";

const store = useAccountStore();

const nickName = ref("");
const username = ref("");
const password1 = ref("");
const password2 = ref("");
const likeCategory = ref(""); // 선호 카테고리
const profile = ref(null); // 프로필 이미지

// 카테고리 데이터
const categories = ref([
  { model: "books.category", pk: 1, fields: { name: "소설/시/희곡" } },
  { model: "books.category", pk: 2, fields: { name: "경제/경영" } },
  { model: "books.category", pk: 3, fields: { name: "자기계발" } },
  { model: "books.category", pk: 4, fields: { name: "인문/교양" } },
  { model: "books.category", pk: 5, fields: { name: "취미/실용" } },
  { model: "books.category", pk: 6, fields: { name: "어린이/청소년" } },
  { model: "books.category", pk: 7, fields: { name: "과학" } },
]);

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    profile.value = file;
  }
};

const signUpMember = function () {
  const userData = new FormData(); 
  userData.append("nickName", nickName.value);
  userData.append("username", username.value);
  userData.append("password1", password1.value);
  userData.append("password2", password2.value);
  userData.append("likeCategory", likeCategory.value);
  if (profile.value) {
    userData.append("profile", profile.value); // 파일 추가
  }

  store.signUpMember(userData); // FormData 전송
};
</script>

<style scoped>
.signup-container {
  max-width: 520px;
  min-width: 320px;
  width: 90vw;
  margin: 60px auto;
  padding: 3rem 2.5rem 2.5rem 2.5rem;
  background: #fff;
  border-radius: 22px;
  box-shadow: 0 4px 24px 0 rgba(60, 60, 60, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.signup-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #1cb0f6;
  margin-bottom: 2.2rem;
  letter-spacing: -1px;
}

.signup-form {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: center;
}

.form-group {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
  color: #1cb0f6;
  margin-bottom: 0.2rem;
  font-size: 1.05rem;
}

input[type="text"],
input[type="password"],
select {
  width: 100%;
  padding: 0.9rem 1.1rem;
  border: 2px solid #e5e5e5;
  border-radius: 16px;
  font-size: 1.08rem;
  background: #f7f9fb;
  transition: border 0.2s;
  box-sizing: border-box;
}

input[type="text"]:focus,
input[type="password"]:focus,
select:focus {
  border: 2px solid #1cb0f6;
  outline: none;
}

input[type="file"] {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 2px solid #e5e5e5;
  border-radius: 16px;
  background: #f7f9fb;
  transition: border 0.2s;
}

input[type="file"]:focus {
  border: 2px solid #1cb0f6;
  outline: none;
}

.signup-btn {
  margin-top: 1.5rem;
  width: 100%;
  padding: 0.9rem 0;
  background: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 20px;
  font-weight: 700;
  font-size: 1.15rem;
  cursor: pointer;
  transition: background 0.2s;
}

.signup-btn:hover {
  background: #1592c7;
}

/* 반응형 */
@media (max-width: 600px) {
  .signup-container {
    max-width: 98vw;
    min-width: unset;
    padding: 2rem 0.7rem 1.5rem 0.7rem;
    border-radius: 12px;
  }
  .signup-title {
    font-size: 1.5rem;
    margin-bottom: 1.2rem;
  }
  .signup-form {
    max-width: 100vw;
    gap: 1rem;
  }
  .form-group label {
    font-size: 1rem;
  }
  .signup-btn {
    font-size: 1rem;
    padding: 0.7rem 0;
  }
}
</style>