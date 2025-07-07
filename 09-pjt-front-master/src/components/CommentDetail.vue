<template>
  <div v-if="comment">
    <h3>댓글 상세</h3>
    <p><strong>작성자:</strong> {{ comment.user }}</p>
    <p><strong>내용:</strong> {{ comment.content }}</p>
    <p><strong>작성일:</strong> {{ comment.created_at }}</p>
  </div>
  <div v-else>
    <p>댓글 정보를 불러오는 중...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const comment = ref(null)

onMounted(async () => {
  try {
    const threadId = route.params.id
    const commentId = route.params.commentId
    const res = await axios.get(
      `http://127.0.0.1:8000/community/detail/${threadId}/detail_commnet/${commentId}`
    )
    comment.value = res.data
  } catch (err) {
    comment.value = null
    alert('댓글 정보를 불러오지 못했습니다.')
    console.error(err)
  }
})
</script>

<style scoped>
</style>