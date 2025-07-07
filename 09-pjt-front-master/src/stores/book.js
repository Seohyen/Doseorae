import { defineStore } from 'pinia'
import { useAccountStore } from '@/stores/account'
import {ref} from 'vue'
import axios from 'axios'
import BookDetail from '@/components/BookDetail.vue'


export const useBookStore = defineStore('books', () => {
  const BASE_API = `http://127.0.0.1:8000/books`
  const bookList = ref([])
  const accountStore = useAccountStore()
  const interestBooks = ref([])
  const readBooks = ref([])
  const book = ref(null) 

  const allBooks = function(){
    axios({
      url:`${BASE_API}/book_list`,
      method:`GET`,
    })
      .then(res => {
        console.log('책리스트 불러오기 성공공')
        bookList.value = res.data
      })
      .catch(err => {
        console.log(err)
      })

  }
    const searchBook = async (title) => {
    try {
      const response = await axios.post(`${BASE_API}/search_book/`, { title })
      return response.data 
    } catch (err) {
      console.error('도서 검색 실패:', err)
      throw err 
    }
  }
  const toggleInterestBook = async (bookPk) => {
    try {
      const res = await axios.post(`${BASE_API}/interest_book/`, { pk: bookPk },{headers: { Authorization: `Token ${accountStore.token}` }})
      const bookIndex = interestBooks.value.findIndex((book) => book.pk === bookPk)
      if (bookIndex === -1) {
        interestBooks.value.push(res.data) // 관심 도서 추가
      } else {
        interestBooks.value.splice(bookIndex, 1)
      }
    } catch (err) {
      console.error('관심 도서 추가/제거 실패:', err)
    }
  }

   const toggleReadBook  = async (bookPk) => {
    try {
      const res = await axios.post(`${BASE_API}/read_book/`, { pk: bookPk },{headers: { Authorization: `Token ${accountStore.token}` }})
      const bookIndex = readBooks.value.findIndex((book) => book.pk === bookPk)
      if (bookIndex === -1) {
        readBooks.value.push(res.data) 
      } else {
        readBooks.value.splice(bookIndex, 1)
      }
    } catch (err) {
      console.error('읽은 도서 추가/제거 실패:', err)
    }
  }

  const top20Books = async () => {
    try {
      const res = await axios.get(`${BASE_API}/get_top_20_books/`)
      return res.data // 상위 20개 도서 반환
    }
    catch (err) {
      console.error('상위 20개 도서 불러오기 실패:', err)
      throw err 
    }
  }

  const getBookDetail = async (bookPk) => {
    try {
      const res = await axios.get(`${BASE_API}/book_detail/${bookPk}/`)
      book.value = res.data 
    }
    catch (err) {
      console.error('도서 상세 정보 불러오기 실패:', err)
      throw err 
    }

  }

  const categoryInfo = ref([
    
    {
        "model": "books.category",
        "pk": 0,
        "fields": {
            "name": "전체"
        }
    },
    {
        "model": "books.category",
        "pk": 1,
        "fields": {
            "name": "소설/시/희곡"
        }
    },
    {
        "model": "books.category",
        "pk": 2,
        "fields": {
            "name": "경제/경영"
        }
    },
    {
        "model": "books.category",
        "pk": 3,
        "fields": {
            "name": "자기계발"
        }
    },
    {
        "model": "books.category",
        "pk": 4,
        "fields": {
            "name": "인문/교양"
        }
    },
    {
        "model": "books.category",
        "pk": 5,
        "fields": {
            "name": "취미/실용"
        }
    },
    {
        "model": "books.category",
        "pk": 6,
        "fields": {
            "name": "어린이/청소년"
        }
    },
    {
        "model": "books.category",
        "pk": 7,
        "fields": {
            "name": "과학"
        }
    }
])


  return {  
    allBooks, book, bookList, searchBook, categoryInfo, toggleInterestBook, top20Books, getBookDetail,toggleReadBook 
    }

  }, { persist: true })
