<!-- src/views/StageCreate.vue -->
<template>
	<section class="form-update container">
	  <h2>舞台追加</h2>
  
	  <p v-if="error" class="text-red-600">{{ error }}</p>
  
	  <form @submit.prevent="handleSubmit" enctype="multipart/form-data">
		<!-- ポスター FilePond -->
		<div class="field poster">
		  <input
			id="poster-upload"
			type="file"
			accept="image/*"
			class="filepond"
		  />
		</div>
  
		<!-- タイトル -->
		<div class="field stage-title">
		  <input
			v-model="form.title"
			type="text"
			placeholder="タイトル"
			required
		  />
		</div>
  
		<!-- キャスト -->
		<div class="field cast">
		  <textarea
			v-model="form.cast"
			rows="3"
			placeholder="キャスト (カンマ区切り)"
		  />
		</div>
  
		<!-- スタッフ -->
		<div class="field staff">
		  <textarea
			v-model="form.staff"
			rows="3"
			placeholder="スタッフ (カンマ区切り)"
		  />
		</div>
  
		<button type="submit">保存</button>
	  </form>
	</section>
  </template>
  
  <script setup>
  import { ref, nextTick, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import apiClient from '@/services/api.js'
  
  /* ---------- FilePond ---------- */
  import * as FilePond from 'filepond'
  import FilePondPluginImagePreview from 'filepond-plugin-image-preview'
  import 'filepond/dist/filepond.min.css'
  import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css'
  FilePond.registerPlugin(FilePondPluginImagePreview)
  
  /* ---------- state ---------- */
  const router = useRouter()
  const error  = ref(null)
  const posterFile = ref(null)
  const form = ref({
	title : '',
	cast  : '',
	staff : ''
  })
  
  /* ---------- FilePond mount ---------- */
  const mountFilePond = () => {
	const el = document.getElementById('poster-upload')
	if (!el || el._pond) return
	FilePond.create(el, {
	  allowMultiple: false,
	  storeAsFile  : true,
	  labelIdle    : '<i class="fas fa-plus"></i>',
	  server: {
		process: (_field, file, _meta, load) => { posterFile.value = file; load() },
		revert : (_uid,   load)              => { posterFile.value = null; load() }
	  }
	})
  }
  
  onMounted(async () => {
	await nextTick()
	mountFilePond()
  })
  
  /* ---------- helpers ---------- */
  const splitNames = (str) =>
	str ? str.split(/[,、]/).map(s => s.trim()).filter(Boolean) : []
  
  /* ---------- submit ---------- */
  const handleSubmit = async () => {
	error.value = null
	try {
	  const credits = [
		...splitNames(form.value.cast ).map(n => ({ person_name:n, role:'cast'  })),
		...splitNames(form.value.staff).map(n => ({ person_name:n, role:'staff' }))
	  ]
  
	  const fd = new FormData()
	  fd.append('title', form.value.title)
	  fd.append('credits', JSON.stringify(credits))
	  if (posterFile.value) fd.append('poster_file', posterFile.value)
  
	  const res = await apiClient.post('/api/stage/', fd, {
		headers:{ 'Content-Type':'multipart/form-data' }
	  })
  
	  router.push(`/stage/${res.data.id}`)
	} catch (e) {
	  error.value = e.response?.data
		? JSON.stringify(e.response.data)
		: e.message
	  console.error(e)
	}
  }
  </script>
