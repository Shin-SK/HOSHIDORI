<!-- src/views/MyPage.vue -->
<template>
	<section class="mypage">
	  <!-- ユーザー情報 -->
	  <div class="user">
		<div class="name-box">
		  <div class="icon">
			<!-- ユーザーアイコン -->
			<UserIcon :icon-url="userInfo.icon_url" :division="userInfo.division" />
		</div>
		  <div class="name">
			{{ userInfo.nickname }}さん
		  </div>
		</div>
		<div class="box">
			<div class="like">
			<div class="head">いいね数</div><span>{{ likedCount }}</span>
		  </div>
		</div>
		<div class="edit">
			<router-link to="/profile/edit">ユーザー情報を編集</router-link>
		</div>
	  </div>
  
	  <!-- ナビゲーション -->
	  <div class="navi">
		<ul class="navi__wrap">
			<li
				:class="{ active: activeTab==='watch' }"
				@click="activeTab='watch'"
			>
				観たい/観た
			</li>

			<li
				:class="{ active: activeTab==='likelog' }"
				@click="activeTab='likelog'"
			>
				いいねされたログ <span>{{ likedCount }}</span>
			</li>
		</ul>
	  </div>

	  <div v-show="activeTab==='watch'" class="tab">

	  <!-- 観たい -->
	  <div class="outer want" id="want">
		<h2><i class="fas fa-heart"></i> 観たい</h2>
		<div v-if="wantLogs.length > 0" class="lists log">
		  <div
			v-for="log in wantLogs"
			:key="log.id"
			class="log-item"
		  >
          <!-- loglist_parts.html 相当の部分 ここから -->
          <div class="lists__wrap">
            <div class="poster">
              <!-- Vue Routerで stage_detail = '/stage/:id' としている想定 -->
              <router-link :to="`/stage/${log.stage.id}`">
                <!-- ポスターURLがあれば img を表示、なければ noimage -->
                <template v-if="log.stage.poster_url">
                  <img
                    :src="log.stage.poster_url"
                    :alt="log.stage.title"
                  />
                </template>
                <template v-else>
                  <span class="noimage">No Poster</span>
                </template>
              </router-link>
            </div>
          </div>
          <!-- loglist_parts.html 相当の部分 ここまで -->
		   
		  </div>
		</div>
		<div v-else class="caution">
		  <router-link to="/stage">作品を探しに行こう</router-link>
		</div>
	  </div>
  
	  <!-- 観た -->
	  <div class="outer watched" id="watched">
		<h2><i class="fas fa-eye"></i> 観た</h2>
		<div v-if="watchedLogs.length > 0" class="card">
		  <div
			v-for="log in watchedLogs"
			:key="log.id"
			class="box"
		  >
				<!-- ★ watched 部分の1アイテム内 ここだけ書き換え -->
				<!-- ポスター -->
				<div class="poster">
					<router-link :to="`/stage/${log.stage.id}`">
					<img v-if="log.stage.poster_url"
						:src="log.stage.poster_url"
						:alt="log.stage.title" />
					<span v-else class="noimage">No Poster</span>
					</router-link>
				</div>

				<!-- ★ 自分のログ詳細 -->
				<div class="log">
					<div class="title">{{ log.stage.title }}</div>
					<div class="meta">
						<div class="times"><span>観劇回数</span> {{ log.times }}</div>
						<div class="rating star">
							<i v-for="i in 5" :key="i"
							:class="['fa-star', i <= log.rating ? 'fas' : 'far']" />
						</div>
					</div>

					<p class="comment" v-if="log.comment">{{ log.comment }}</p>

					<!-- 編集／削除 -->
					<div class="edit">
						<router-link :to="`/log/${log.id}/edit`">編集</router-link> |
						<a href="#" class="delete" @click.prevent="onClickDelete(log.id)">削除</a>
					</div>
				</div>
		  </div><!-- box -->
		</div>
		<div v-else class="caution">
		  <router-link to="/stage">作品を探しに行こう</router-link>
		</div>
	  </div>
  
	  <!-- 観れない -->
	  <div class="outer cannot" id="cannot">
		<h2><i class="fas fa-eye-slash"></i> 観れない</h2>
		<div v-if="cannotLogs.length > 0" class="lists log">
		  <div
			v-for="log in cannotLogs"
			:key="log.id"
			class="log-item"
		  >
          <!-- loglist_parts.html 相当の部分 ここから -->
          <div class="lists__wrap">
            <div class="poster">
              <!-- Vue Routerで stage_detail = '/stage/:id' としている想定 -->
              <router-link :to="`/stage/${log.stage.id}`">
                <!-- ポスターURLがあれば img を表示、なければ noimage -->
                <template v-if="log.stage.poster_url">
                  <img
                    :src="log.stage.poster_url"
                    :alt="log.stage.title"
                  />
                </template>
                <template v-else>
                  <span class="noimage">No Poster</span>
                </template>
              </router-link>
            </div>
          </div>
          <!-- loglist_parts.html 相当の部分 ここまで -->

		  </div>
		</div>
		<div v-else class="caution">
		  <router-link to="/stage">作品を探しに行こう</router-link>
		</div>
	  </div>
  		
	</div>

	<div v-show="activeTab==='likelog'" class="tab">

	  <div class="outer liked" id="liked">
  		<h2><i class="fas fa-heart"></i> いいねされたログ</h2>

		<div v-if="likedLogs.length">
			<div
			v-for="log in likedLogs"
			:key="log.id"
			class="liked-log"
			>
			<div class="outer watched" id="watched">
				<div v-if="watchedLogs.length > 0" class="card">
					<div
						v-for="log in watchedLogs"
						:key="log.id"
						class="box"
					>
							<!-- ★ watched 部分の1アイテム内 ここだけ書き換え -->
							<!-- ポスター -->
							<div class="poster">
								<router-link :to="`/stage/${log.stage.id}`">
								<img v-if="log.stage.poster_url"
									:src="log.stage.poster_url"
									:alt="log.stage.title" />
								<span v-else class="noimage">No Poster</span>
								</router-link>
							</div>

							<!-- ★ 自分のログ詳細 -->
							<div class="log">
								<div class="title">{{ log.stage.title }}</div>
								<div class="meta">
									<div class="times"><span>観劇回数</span> {{ log.times }}</div>
									<div class="rating star">
										<i v-for="i in 5" :key="i"
										:class="['fa-star', i <= log.rating ? 'fas' : 'far']" />
									</div>
								</div>

								<p class="comment" v-if="log.comment">{{ log.comment }}</p>

								<!-- 編集／削除 -->
								<div class="edit">
									<router-link :to="`/log/${log.id}/edit`">編集</router-link> |
									<a href="#" class="delete" @click.prevent="onClickDelete(log.id)">削除</a>
								</div>
							</div>
					</div><!-- box -->
					</div>
					<div v-else class="caution">
					<router-link to="/stage">作品を探しに行こう</router-link>
					</div>
				</div>
			</div>
		</div>

		<p v-else>まだ誰からもいいねされていません</p>
		</div>
		
	</div>


	  <!-- エラーメッセージ -->
	  <div v-if="errorMsg" style="color:red">{{ errorMsg }}</div>
	<div class="logout">
		<button @click="logout">ログアウト</button>
	</div>

	</section>
  </template>
  
  <script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api.js'
import UserIcon  from '@/components/UserIcon.vue'

const router = useRouter() 
const userInfo    = ref({})
const wantLogs    = ref([])
const watchedLogs = ref([])
const cannotLogs  = ref([])
const errorMsg    = ref(null)
const loading     = ref(true)
//likeを集計
const likedCount = computed(() => userInfo.value.liked_count ?? 0)
//Likeを表示
const likedLogs = computed(() => userInfo.value.liked_logs ?? [])

const activeTab = ref('watch')     // 初期は "watch"

onMounted(async () => {
  try {
    // プロフィール（division 含む）
	const { data: raw } = await apiClient.get('/api/profile/me/')
	userInfo.value = { ...raw, ...raw.user }
    // 観劇ログ
    const { data: logs } = await apiClient.get('/api/log/')
    watchedLogs.value = logs.filter(l => l.status === 'watched')
    wantLogs.value    = logs.filter(l => l.status === 'want')
    cannotLogs.value  = logs.filter(l => l.status === 'cannot')
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || err.message
  } finally {
    loading.value = false
  }
  
})

async function logout () {
  try {
    // JWT の場合 refresh を渡すとブラックリスト化できる
    const refresh = localStorage.getItem('refreshToken')
    await apiClient.post('/dj-rest-auth/logout/', { refresh })
	
  } catch (_) { /* 500 等でもあとでトークン消すので無視 */ }

  // トークン類を物理削除
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  router.push('/login')
}

onMounted(() => {
  if (location.hash === '#likelog') activeTab.value = 'likelog'
})
watch(activeTab, t => history.replaceState(null, '', `#${t}`))
</script>
