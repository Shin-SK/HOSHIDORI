<!-- src/views/StageCreate.vue -->
<template>
	<div>
	  <h1>Create Stage</h1>
  
	  <div v-if="error" style="color:red">{{ error }}</div>
  
	  <form @submit.prevent="createStage">
		<div>
		  <label>Title:</label>
		  <input v-model="formData.title" required />
		</div>
  
		<div>
		  <label>Description:</label>
		  <textarea v-model="formData.description" />
		</div>
  
		<div>
		  <label>Poster URL:</label>
		  <input v-model="formData.poster_url" />
		</div>
  
		<div>
		  <label>Cast:</label>
		  <textarea v-model="formData.cast" />
		</div>
  
		<div>
		  <label>Staff:</label>
		  <textarea v-model="formData.staff" />
		</div>
  
		<button type="submit">Create</button>
	  </form>
	</div>
  </template>
  
  <script>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import apiClient from '@/services/api.js'
  
  export default {
	name: 'StageCreate',
	setup() {
	  const router = useRouter()
	  const error = ref(null)
  
	  // フォームデータ用オブジェクト
	  const formData = ref({
		title: '',
		description: '',
		poster_url: '',
		cast: '',
		staff: ''
	  })
  
	  const createStage = async () => {
		try {
		  error.value = null
		  const response = await apiClient.post('/stage/', formData.value)
		  // 作成成功 → 詳細ページへ飛ぶか、一覧ページへ飛ぶなど自由に
		  // ここでは新規作成したStageのidを使って詳細へ飛ぶ
		  const newId = response.data.id
		  router.push(`/stage/${newId}`)
		} catch (err) {
		  error.value = err.message
		}
	  }
  
	  return {
		formData,
		error,
		createStage
	  }
	}
  }
  </script>
  
  <style scoped>
  /* お好みのスタイル */
  </style>
  