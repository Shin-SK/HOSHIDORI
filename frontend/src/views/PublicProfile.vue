<template>
	<section class="public-profile" v-if="profile">
	  <!-- ユーザー -->
	  <div class="user">
		<div class="icon">
		<UserIcon :icon-url="profile.icon_url" :division="profile.division" :rank="profile.rank" />
		</div>
		<h1 class="nickname">{{ profile.nickname || profile.username }}</h1>
		<p class="bio" v-if="profile.bio">{{ profile.bio }}</p>
  
		<ul class="links">
		  <li v-if="profile.website_url"><a :href="profile.website_url" target="_blank">Web</a></li>
		  <li v-if="profile.twitter_url"><a :href="profile.twitter_url" target="_blank">X / Twitter</a></li>
		</ul>
	  </div>
  
<!-- 上部ユーザーエリアに追記 -->
<div class="stats">
  <span class="count">観た！ {{ profile.watched_count }} 本</span>
  <span class="rank">Rank {{ profile.rank }}</span>
</div>

<!-- 劇場ランキング -->
<div class="theater-ranking" v-if="profile.favorite_theaters.length">
  <h2>よく行く劇場</h2>
  <ol>
    <li v-for="t in profile.favorite_theaters" :key="t.id">
      {{ t.name }} <small>×{{ t.times }}</small>
    </li>
  </ol>
</div>

	  <!-- 最近観たログ -->
	  <div class="watched" v-if="watched.length">
		<h2><i class="fas fa-eye"></i> 最近観た</h2>
  
		<div class="card">
		  <div v-for="log in watched" :key="log.id" class="box">
			<router-link :to="`/stage/${log.stage.id}`" class="poster">
			  <img :src="log.stage.poster_url || '/img/noimage.png'" :alt="log.stage.title" />
			</router-link>
			<div class="title">{{ log.stage.title }}</div>
			<div class="rating star">
			  <i v-for="i in 5" :key="i"
				 :class="['fa-star', i <= log.rating ? 'fas' : 'far']" />
			</div>
		  </div>
		</div>
	  </div>
  
	  <p v-else class="caution">まだ観劇ログがありません。</p>
	</section>
  
	<p v-else-if="errorMsg" class="error">{{ errorMsg }}</p>
	<p v-else class="loading">Loading…</p>
  </template>
  
  <script setup>
import { ref, onMounted, computed } from 'vue'
import api          from '@/services/api.js'     // ← これを使う
import UserIcon     from '@/components/UserIcon.vue'
import { useRoute } from 'vue-router'

const route      = useRoute()
const profile    = ref(null)
const errorMsg   = ref(null)
const loading    = ref(true)

onMounted(async () => {
  try {
    // 他人のプロフィールを 1 本取得するだけ
    const { data: raw } = await api.get(`/api/profile/${route.params.username}/`)
    // フラット化： icon_url / nickname をトップレベルに展開
    profile.value = { ...raw, ...raw.user }
  } catch (err) {
    errorMsg.value = err.response?.status === 404
      ? 'ユーザーが見つかりません'
      : err.message
  } finally {
    loading.value = false
  }
})

// “最近観た”　先頭 10 件
const watched = computed(() => profile.value?.watched_logs?.slice(0, 10) || [])
</script>
