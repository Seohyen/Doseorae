import axios from 'axios'
import { useAccountStore } from '@/stores/account.js'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    Accept: 'application/json',
  },
})

apiClient.interceptors.request.use(config => {
  const accountStore = useAccountStore()
  if (accountStore.token) {
    config.headers.Authorization = `Token ${accountStore.token}`
  }
  return config
}, error => Promise.reject(error))

export default apiClient
