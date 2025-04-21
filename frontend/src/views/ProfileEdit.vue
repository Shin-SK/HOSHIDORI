<!-- src/views/ProfileEdit.vue -->
<template>
	<section class="profile-edit container form-update">
	  <!-- ───────── プロフィール ───────── -->
	  <form @submit.prevent="updateProfile" enctype="multipart/form-data" class="form">
		<h2>プロフィール編集</h2>
  
		<!-- ニックネーム -->
		<div class="field">
		  <label>ニックネーム</label>
		  <input v-model="profile.nickname" type="text" required />
		</div>
  
		<!-- アイコン -->
		<div class="field icon">
			<div class="icon__wrap">
				<!-- 現在のアイコン -->
				<div v-if="profile.icon_url" class="current-icon">
					<img :src="profile.icon_url" alt="current icon" />
					<button type="button" @click="removeIcon">アイコンを削除</button>
				</div>
		
				<!-- 新アイコン FilePond -->
				<input
					id="icon-upload"
					type="file"
					accept="image/*"
					class="filepond"
				/>
				</div>
			</div>

  
		<button type="submit">更新</button>
	  </form>
  
	  <!-- ───────── パスワード変更 ───────── -->
	  <form @submit.prevent="updatePassword" class="form">
		<h2>パスワード更新</h2>
  
		<div class="field">
		  <label>新しいパスワード</label>
		  <input v-model="pw.new1" type="password" required />
		</div>
  
		<div class="field">
		  <label>新しいパスワード(確認)</label>
		  <input v-model="pw.new2" type="password" required />
		</div>
  
		<button type="submit">パスワードを変更</button>
	  </form>
  
	  <!-- エラー / 完了メッセージ -->
	  <p v-if="msg" :style="{color: msgColor}">{{ msg }}</p>
	</section>
  </template>
  
  <script setup>
  import { ref, onMounted, nextTick } from 'vue'
  import apiClient from '@/services/api.js'
  
  /* ---------- FilePond ---------- */
  import * as FilePond from 'filepond'
  import FilePondPluginImagePreview from 'filepond-plugin-image-preview'
  import 'filepond/dist/filepond.min.css'
  import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css'
  FilePond.registerPlugin(FilePondPluginImagePreview)
  
  /* ---------- state ---------- */
  const profile = ref({ nickname: '', icon_url: '' })
  const iconFile = ref(null)
  const pw = ref({ new1: '', new2: '' })
  const msg = ref('')
  const msgColor = ref('red')
  
  /* ---------- helpers ---------- */
  const showMsg = (text, ok = false) => {
	msg.value = text
	msgColor.value = ok ? 'green' : 'red'
  }
  
  /* ---------- FilePond mount ---------- */
  const mountFilePond = () => {
	const el = document.getElementById('icon-upload')
	if (!el || el._pond) return
	FilePond.create(el, {
	  allowMultiple: false,
	  storeAsFile : true,
	  labelIdle   : '<i class="fas fa-plus"></i>',
	  server: {
		process: (_f, file, _m, load) => { iconFile.value = file; load() },
		revert : (_u,   load)          => { iconFile.value = null; load() }
	  }
	})
  }
  
  /* ---------- fetch current user ---------- */
  onMounted(async () => {
	try {
	  const res = await apiClient.get('/dj-rest-auth/user/')
	  profile.value = res.data
	} catch (e) {
	  showMsg(e.message)
	} finally {
	  await nextTick()
	  mountFilePond()
	}
  })
  
  /* ---------- actions ---------- */
  const updateProfile = async () => {
	try {
	  const fd = new FormData()
	  fd.append('nickname', profile.value.nickname)
	  if (iconFile.value) fd.append('icon_file', iconFile.value)
	  await apiClient.put('/dj-rest-auth/user/', fd,
		{ headers:{ 'Content-Type':'multipart/form-data' } })
	  if (iconFile.value) iconFile.value = null
	  showMsg('プロフィールを更新しました', true)
	} catch (e) {
	  showMsg(e.response?.data || e.message)
	}
  }
  
  const removeIcon = async () => {
	try {
	  await apiClient.put('/dj-rest-auth/user/', { icon_url: '' })
	  profile.value.icon_url = ''
	  showMsg('アイコンを削除しました', true)
	} catch (e) {
	  showMsg(e.message)
	}
  }
  
  const updatePassword = async () => {
	if (pw.value.new1 !== pw.value.new2) {
	  return showMsg('パスワード確認が一致しません')
	}
	try {
	  await apiClient.post('/dj-rest-auth/password/change/', {
		new_password1: pw.value.new1,
		new_password2: pw.value.new2
	  })
	  pw.value = { new1: '', new2: '' }
	  showMsg('パスワードを変更しました', true)
	} catch (e) {
	  showMsg(e.response?.data || e.message)
	}
  }
  </script>
  
  <style scoped>
  /* 必要ならスタイルを追加 */
  </style>
  