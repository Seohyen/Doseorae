import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/account'
import { ref } from 'vue'
export const useCommentStore = defineStore('comment', () => {
  const accountStore = useAccountStore()

  const createComment = async (commentData) => {
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/community/detail/${commentData.thread}/create_comment/`,
        commentData,
        {
          headers: {
            Authorization: `Token ${accountStore.token}`,
          },
        }
      )
      console.log('댓글 생성 성공:', response.data)
      return response.data 
    } catch (err) {
      console.error('댓글 등록 실패', err)
      throw err 
    }
  }

  return {
    createComment,
  }
})