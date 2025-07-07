import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/account'
import apiClient from './api/apiClient.js'

export const useGptStore = defineStore('gpt', () => {
  const BASE_API = `http://127.0.0.1:8000/activity`
  const answerGpt = ref([])
  const quizGpt = ref([])
  const debateList = ref([])
  const accountStore = useAccountStore()
  const askGpt = async function (prompt) {
    try {
      const response = await axios({
        url: `${BASE_API}/ask_gpt`,
        method: `POST`,
        data: { prompt }, 
      })
      answerGpt.value = response.data
      return response.data 
    } catch (err) {
      console.error('Error:', err)
      throw err 
    }
  }

  const makeQuiz = async function (bookName) {
    try {
      const response = await axios({
        url: `${BASE_API}/quize_gpt`,
        method: `POST`,
        data: { bookName }, // 서버가 요구하는 필드로 데이터 전달
      })
      quizGpt.value = response.data // 응답 데이터를 상태에 저장
      return response.data // 응답 데이터를 반환
    } catch (err) {
      console.error('Error:', err)
      throw err // 에러를 호출한 쪽에서 처리할 수 있도록 throw
    }
  }

  const userExp = async () => {
    try {
      const response = await apiClient.get('/activity/update_exp')
      return response.data
    } catch (error) {
      console.error(error)
      throw error
    }
}


  const debateGpt = async function (prompt) {
    try {
      const response = await axios({
        url: `${BASE_API}/ask_gpt`,
        method: `POST`,
        data: { prompt }, // 사용자 입력 데이터를 서버로 전달
      })
      debateList.value = response.data // 응답 데이터를 상태에 저장
      return response.data // 응답 데이터를 반환
    } catch (err) {
      console.error('Error:', err)
      throw err // 에러를 호출한 쪽에서 처리할 수 있도록 throw
    }
  }


  return { 
    askGpt, answerGpt, makeQuiz, quizGpt, debateGpt, debateList, userExp
      }

  }, { persist: true })
