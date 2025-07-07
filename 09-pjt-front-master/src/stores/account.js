import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const BASE_API = `http://127.0.0.1:8000/accounts`
  const token = ref(null)
  const router = useRouter()
  const user = ref(null)
  const dedetailUser = ref(null)

  const isLogIned = computed(() => {
    return token.value !== null
  })
  
  const signUpMember = function (userdata) {
    axios({
      method: 'post',
      url: `${BASE_API}/signup/`,
      data: userdata,
      headers: {
        'Content-Type': 'multipart/form-data', // 파일 업로드를 위한 헤더 설정
      },
    })
      .then((res) => {
        console.log('회원가입 되었습니다.');
        token.value = res.data.key;
        router.push({ name: 'main' });
      })
      .catch((err) => {
        console.error('회원가입 실패:', err.response.data); // 에러 메시지 출력
      });
  }

const logInMember = function (userdata) {
  axios({
    method: 'post',
    url: `${BASE_API}/login/`,
    data: userdata,
  })
    .then(async res => {
      console.log('로그인 되었습니다')
      token.value = res.data.key
      console.log('받은 토큰:', token.value)

      const result = await getUserInfo()
      if (!result.success) {
        console.error('유저 정보 가져오기 실패:', result.error)
      } else {
        console.log('유저 정보:', user.value)
      }

      router.push({ name: 'main' })
    })
    .catch(err => {
      console.log('로그인 실패', err)
    })
}


  const logOutMember = function(){
    token.value = null
    router.push({name:'main'})
  }
  
  const changePass = async ({ old_password, new_password1, new_password2 }) => {
    try {
      const res = await axios.post(
        `${BASE_API}/password/change/`,
        {
          old_password,
          new_password1,
          new_password2,
        },
        {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        }
      )
      return { success: true, data: res.data }
    } catch (err) {
      return { success: false, error: err.response?.data || err.message }
    }
  }
  const getUserInfo = async () => {
    try {
      const res = await axios.get(`${BASE_API}/detail_user/`, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
      console.log('getUserInfo:', res.data)
      user.value = res.data
      return { success: true, data: res.data }
    } catch (err) {
      return { success: false, error: err.response?.data || err.message }
    }
  }
  const getOtherUserInfo = async (userID) => {
    try {
      const res = await axios.get(`${BASE_API}/user_profile/${userID}`, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
      console.log('getUserInfo:', res.data)
      dedetailUser.value = res.data
      return { success: true, data: res.data }
    } catch (err) {
      return { success: false, error: err.response?.data || err.message }
    }
  }
  const getFollow = async (userId) => {
    console.log('팔로우 요청:', userId)
    try {
      const res = await axios.post(`${BASE_API}/follow/${userId}`, null,
         {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
      console.log('getFollow:', res.data)
      return
    }
    catch (err) {
      console.error('팔로우 실패:', err)
      return
    }
  }

  return { 
    signUpMember,
    logInMember,
    logOutMember,
    isLogIned,
    token,
    changePass,
    getUserInfo,
    user,
    getOtherUserInfo,
    getFollow,
    dedetailUser
  }
}, { persist: true })
