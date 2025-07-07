import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCategoryStore = defineStore('category', () => {
  const BASE_API = `http://127.0.0.1:8000/`

  const categoryList = ref([])

  const allCategories = function(){
    axios({
    url : `${BASE_API}/`,
    method:'get',  
  })
    .then(res =>{
      console.log(res.data)
      categoryList.value = res.data
    })
    .catch(err => console.log(err))
  }



  return { categoryList,allCategories }
})
