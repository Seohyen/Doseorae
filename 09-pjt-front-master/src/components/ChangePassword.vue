<template>
  <form @submit.prevent="onChangePassword" class="change-password-form">
    <div class="form-group">
      <label for="old-password">현재 비밀번호</label>
      <input id="old-password" type="password" v-model="oldPassword" class="form-input" />
    </div>
    <div class="form-group">
      <label for="new-password1">새 비밀번호</label>
      <input id="new-password1" type="password" v-model="newPassword1" class="form-input" />
    </div>
    <div class="form-group">
      <label for="new-password2">새 비밀번호 확인</label>
      <input id="new-password2" type="password" v-model="newPassword2" class="form-input" />
    </div>
    <button type="submit" class="submit-button">비밀번호 변경</button>
    <p v-if="error" class="error-message">{{ error }}</p>
    <p v-if="success" class="success-message">비밀번호가 변경되었습니다.</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'

const oldPassword = ref('')
const newPassword1 = ref('')
const newPassword2 = ref('')
const error = ref('')
const success = ref(false)

const accountStore = useAccountStore()

const onChangePassword = async () => {
  error.value = ''
  success.value = false
  const result = await accountStore.changePass({
    old_password: oldPassword.value,
    new_password1: newPassword1.value,
    new_password2: newPassword2.value,
  })
  if (result.success) {
    success.value = true
    oldPassword.value = ''
    newPassword1.value = ''
    newPassword2.value = ''
  } else {
    error.value = result.error?.non_field_errors?.[0] || result.error?.new_password2?.[0] || result.error?.old_password?.[0] || '비밀번호 변경 실패'
  }
}
</script>

<style scoped>
.change-password-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

.form-group {
  width: 100%;
  margin-bottom: 16px;
}

label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #1cb0f6;
  outline: none;
}

.submit-button {
  background: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 16px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-button:hover {
  background: #1390c4;
}

.error-message {
  color: red;
  font-size: 0.9rem;
  margin-top: 8px;
}

.success-message {
  color: green;
  font-size: 0.9rem;
  margin-top: 8px;
}
</style>