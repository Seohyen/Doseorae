import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/account'
import router from '@/router'
export const useThreadStore = defineStore('thread', () => {
  const BASE_API = `http://127.0.0.1:8000/community`
  const threadList = ref([])
  const accountStore = useAccountStore()
  const thread = ref([]) 
  const allThreads = async function() {
    try {
      const res = await axios({
        url: `${BASE_API}/`,
        method: 'get',
      })
      console.log(res.data,'코멘트오니!~~~??')
      threadList.value = res.data
    } catch (err) {
      console.log(err)
    }
  }

  const createThread = function(book,threadData) {
    axios({
      url: `${BASE_API}/create_thread/${book}`,
      method: 'POST',
      data: threadData,
      headers: {
        Authorization: `Token ${accountStore.token}` 
      }
    })
      .then(res => {
        console.log(res.data, '쓰레드가 생성됐다람쥐쥐')
        router.push({ name: 'ThreadDetail', params: { id: res.data.id } })
      })
      .catch(err => {
        console.error('Thread 생성 실패:', err.response?.data || err.message || err)
      })
  }
  const updateThread = async function(threadId, updatedData) {
    try {
      const res = await axios({
        url: `${BASE_API}/detail/${threadId}`, 
        method: 'PUT',
        data: updatedData,
        headers: {
          Authorization: `Token ${accountStore.token}`, 
        },
      })
      console.log('쓰레드 업데이트 성공')
      thread.value = res.data 
      return res.data
    } catch (err) {
      console.error('쓰레드 업데이트 실패:', err.response?.data || err.message || err)
      throw err
    }
  }

  const deleteThread = async function(threadId) {
    try {
      const res = await axios({
        url: `${BASE_API}/detail/${threadId}`,
        method: 'DELETE',
        headers: {
          Authorization: `Token ${accountStore.token}`
        }
      })
      console.log(res.data, "제거됐다람쥐쥐")

      await allThreads()
    } catch (err) {
      console.log(err)
    }
  }
  
  

  const detailThread = async function(threadId) {
    try {
      const res = await axios({
        url: `${BASE_API}/detail/${threadId}`,
        method: 'get',
      })
      console.log(res.data, '상세정보???!!')
      thread.value = res.data
    } catch (err) {
      console.log(err)
    }
  }
  return { 
    allThreads,
    threadList,
    createThread,
    deleteThread,
    detailThread,
    updateThread,
    thread
  }
})
