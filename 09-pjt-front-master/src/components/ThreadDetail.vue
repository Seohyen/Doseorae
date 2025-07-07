<template>
  <div class="thread-detail-container">
    <div v-if="thread">
      <div class="profile-section">
        <img :src="thread.user_profile" alt="프로필 사진" class="profile-image" @click="goToUserDetail" />
        <h2 @click="goToUserDetail" class="user-link">
          {{ thread.username }}
        </h2>
      </div>
      <p class = "book-title">{{ thread. book_title}}</p>
      <hr>
      <div class="section">
        <label>📝 제목:</label>
        <h3 v-if="!isEditing">{{ thread.title }}</h3>
        <input v-else v-model="updatedTitle" placeholder="새로운 제목을 입력하세요" />
      </div>

      <div class="section">
        <label>📄 내용:</label>
        <p v-if="!isEditing">{{ thread.content }}</p>
        <textarea v-else v-model="updatedContent" placeholder="새로운 내용을 입력하세요"></textarea>
      </div>

      <div class="section">
        <label>🏷️ 해시태그:</label>
        <p v-if="!isEditing">{{ thread.hashtag_list }}</p>
        <textarea v-else v-model="updatedHashtags" placeholder="새로운 해시태그를 입력하세요"></textarea>
      </div>

      <p class="thread-user-id">🆔 {{ thread.user }}</p>
      <hr> 

      <div v-if="userid === thread?.user">
        <button v-if="!isEditing" @click="startEditing">✏️ 수정</button>
        <button v-else @click="updateThread">💾 저장</button>
        <button @click="deleteThread">🗑️ 삭제</button>
      </div>

      <form @submit.prevent="newComment">
        <div>
          <label for="title">💬 댓글 제목:</label>
          <input type="text" id="title" v-model="updatedCommentTitle" />
        </div>
        <div>
          <label for="content">🗨️ 댓글 내용:</label>
          <input type="text" id="content" v-model="updatedCommentContent" />
        </div>
        <button>➕ 생성</button>
      </form>

      <div>
        <label for="sortOrder">🔽 댓글 정렬:</label>
        <select id="sortOrder" v-model="sortOrder">
          <option value="newest">최신순</option>
          <option value="oldest">오래된 순</option>
        </select>
      </div>

      <div v-for="comment in sortedComments" :key="comment.id" class="comment-card">
        <h3 class="comment-username">💬{{ comment.username }}</h3>
        <h5 class="comment-title">{{ comment.title }}</h5>
        <p class="comment-content">{{ comment.content }}</p>
      </div>
    </div>

    <div v-else>
      <p>❌ 쓰레드를 찾을 수 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useThreadStore } from '@/stores/thread'
import { ref, computed, onMounted } from 'vue'
import { useCommentStore } from '@/stores/comment'
import { useAccountStore } from '@/stores/account'

const accountStore = useAccountStore()
const userid = accountStore.user.id

const commentStore = useCommentStore()
const threadStore = useThreadStore()

const route = useRoute()
const router = useRouter()

const thread = ref(null)
const isEditing = ref(false)
const updatedTitle = ref('')
const updatedContent = ref('')
const updatedHashtags = ref('')
const updatedCommentTitle = ref('')
const updatedCommentContent = ref('')
const sortOrder = ref('newest')

onMounted(async () => {
  const threadId = route.params.id
  if (threadId) {
    try {
      await threadStore.detailThread(threadId)
      thread.value = threadStore.thread

      if (thread.value) {
        updatedTitle.value = thread.value.title || ''
        updatedContent.value = thread.value.content || ''
        updatedHashtags.value = thread.value.hashtag_list?.join(', ') || ''
      }
    } catch (err) {
      console.error('쓰레드 상세 정보 가져오기 실패:', err)
    }
  }
})

const sortedComments = computed(() => {
  if (!thread.value || !thread.value.comments) return []
  return [...thread.value.comments].sort((a, b) => {
    return sortOrder.value === 'newest'
      ? new Date(b.created_at) - new Date(a.created_at)
      : new Date(a.created_at) - new Date(b.created_at)
  })
})

const goToUserDetail = () => {
  if (userid == thread.value.user) {
    router.push({ name: 'MyPageView' })
  } else {
    router.push({ name: 'UserDetail', params: { id: thread.value.user } })
  }
}

const sortComments = (order) => {
  sortOrder.value = order
}

const newComment = async () => {
  console.log('새 댓글 생성:', userid.value)
  if (!updatedCommentTitle.value.trim() || !updatedCommentContent.value.trim()) {
    alert('댓글의 제목과 내용을 모두 입력하세요.')
    return
  }

  const commentData = {
    title: updatedCommentTitle.value,
    content: updatedCommentContent.value,
    thread: route.params.id,
    
  }

  try {
    const createdComment = await commentStore.createComment(commentData)
    thread.value.comments.push(createdComment)
    updatedCommentTitle.value = ''
    updatedCommentContent.value = ''
  } catch (err) {
    console.error('댓글 생성 실패:', err)
    alert('댓글 생성에 실패했습니다.')
  }
}

const startEditing = () => {
  isEditing.value = true
}

const updateThread = async () => {
  if (!updatedTitle.value.trim() || !updatedContent.value.trim()) {
    alert('제목과 내용을 모두 입력하세요.')
    return
  }

  const updatedHashtagArray = updatedHashtags.value
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag !== '')

  try {
    await threadStore.updateThread(route.params.id, {
      title: updatedTitle.value,
      content: updatedContent.value,
      hashtags: updatedHashtagArray.join(' '),
    })
    thread.value.title = updatedTitle.value
    thread.value.content = updatedContent.value
    thread.value.hashtag_list = updatedHashtagArray
    isEditing.value = false
    alert('수정이 완료되었습니다.')
  } catch (err) {
    console.error('쓰레드 수정 실패', err)
    alert('수정에 실패했습니다.')
  }
}

const deleteThread = async () => {
  if (route.params.id) {
    await threadStore.deleteThread(route.params.id)
    router.push({ name: 'ThreadList' })
  } else {
    console.error('Thread ID is undefined, cannot delete.')
  }
}
</script>


<style scoped>
:root {
  --navbar-height: 70px; /* nav 높이에 맞게 조정 */
}
.comment-username {
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 6px;
  display: inline-block;
  background-color: #e1f4fd;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid #1cb0f6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
.thread-detail-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
  background: #f7f9fb;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  /* margin-top 대신 padding-top 사용, nav바 높이만큼 */
  padding-top: var(--navbar-height);
  min-height: 80vh;
}

.profile-section {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  margin-top: 50px;
}

.profile-image {
  width: 100px; /* 기존 크기 유지 */
  height: 100px; /* 기존 크기 유지 */
  border-radius: 50%;
  object-fit: cover;
  margin-right: 16px; /* 간격 유지 */
  border: 3px solid #1cb0f6; /* 테두리 추가 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 약간의 그림자 추가 */
}

.book-title{
  display: inline-block;
  vertical-align: middle; /* 세로 정렬 */
  color: #a8a8a8;
  margin-left: 20px; /* 이미지와 텍스트 사이 간격 */
  font-size: 1rem; /* 텍스트 크기 */
}

.user-link {
  cursor: pointer;
  color: #1cb0f6;
  font-weight: 700;
  font-size: 3rem; /* 기존 1.2rem에서 크기를 키움 */
  transition: color 0.3s, text-decoration 0.3s;
}

.user-link:hover {
  color: #1390c4;
  text-decoration: underline;
}

.section {
  margin-bottom: 24px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section label {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 8px;
  display: block;
}

.thread-user-id {
  color: #888;
  font-size: 0.98rem;
  margin-bottom: 10px;
}

/* 제목 스타일 */
.thread-detail-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1cb0f6;
  text-align: center;
  margin-bottom: 24px;
}

/* 입력 필드 */
input,
textarea {
  width: 100%;
  padding: 12px;
  margin-bottom: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #1cb0f6;
  box-shadow: 0 0 4px rgba(28, 176, 246, 0.4);
}

/* 버튼 스타일 */
button {
  background: #1cb0f6;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-right: 8px;
}

button:hover {
  background: #1390c4;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* 댓글 정렬 셀렉트 */
select {
  width: 100%;
  padding: 12px;
  margin-bottom: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
}

/* 댓글 카드 */
.comment-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.comment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

/* 댓글 제목 */
.comment-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1cb0f6;
  margin-bottom: 8px;
}

/* 댓글 내용 */
.comment-content {
  font-size: 1rem;
  color: #555;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  :root {
    --navbar-height: 60px;
  }
  .thread-detail-container {
    padding: 16px;
    padding-top: var(--navbar-height);
  }
}

@media (max-width: 480px) {
  :root {
    --navbar-height: 50px;
  }
  .thread-detail-container {
    padding: 12px;
    padding-top: var(--navbar-height);
  }
}
</style>