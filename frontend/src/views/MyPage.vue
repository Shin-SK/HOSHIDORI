<!-- src/views/MyPage.vue -->
<template>
	<section class="mypage">
	  <!-- ユーザー情報 -->
	  <div class="user">
		<div class="name-box">
		  <div class="icon">
			<!-- ユーザーアイコン -->
			<img v-if="userInfo.icon_url" :src="userInfo.icon_url" alt="User Icon" />
			<img v-else src="/img/user-default.png" alt="Default Icon" />
		  </div>
		  <div class="name">
			{{ userInfo.nickname }}さん
		  </div>
		</div>
		<div class="edit">
			<router-link to="/profile/edit">ユーザー情報を編集</router-link>
		</div>
	  </div>
  
	  <!-- ナビゲーション -->
	  <div class="navi">
		<ul class="navi__wrap">
		  <li><a href="#want"><i class="fas fa-heart"></i><span>観たい</span></a></li>
		  <li><a href="#watched"><i class="fas fa-eye"></i><span>観た</span></a></li>
		  <li><a href="#cannot"><i class="fas fa-eye-slash"></i><span>観れない</span></a></li>
		</ul>
	  </div>
  
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
  
	  <!-- エラーメッセージ -->
	  <div v-if="errorMsg" style="color:red">{{ errorMsg }}</div>
	</section>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import apiClient from '@/services/api.js'
  
  export default {
	name: 'MyPage',
	setup() {
	  // ユーザー情報
	  const userInfo = ref({})
	  // ログ一覧 (すべて取得)
	  const allLogs = ref([])
  
	  // ステータス別の配列
	  const wantLogs = ref([])
	  const watchedLogs = ref([])
	  const cannotLogs = ref([])
  
	  // ロード中フラグやエラー
	  const loading = ref(true)
	  const errorMsg = ref(null)
  
	  onMounted(async () => {
		try {
		  // 1) ユーザー情報を取得
		  const resUser = await apiClient.get('/dj-rest-auth/user/')
		  userInfo.value = resUser.data
  
		  // 2) ログ一覧を取得
		  const resLogs = await apiClient.get('/api/log/')
		  console.log('Logs response:', resLogs.data)  // ← ここ！
		  allLogs.value = resLogs.data
  
		  // 3) Vue側でステータスごとに仕分け
		  wantLogs.value = allLogs.value.filter(log => log.status === 'want')
		  watchedLogs.value = allLogs.value.filter(log => log.status === 'watched')
		  cannotLogs.value = allLogs.value.filter(log => log.status === 'cannot')
  
		} catch (err) {
		  errorMsg.value = err.response?.data?.detail || err.message
		} finally {
		  loading.value = false
		}
	  })
  
	  return {
		userInfo,
		allLogs,
		wantLogs,
		watchedLogs,
		cannotLogs,
		loading,
		errorMsg
	  }
	}
  }
  </script>
  
  <style scoped>
  /* テンプレートに書いていたクラス名をそのまま使えます */
  /* .mypage, .user, .icon, .name, .lists.log, .caution, .want, .watched, .cannot など */
  /* あとでCSSを読み込んで整える */
  </style>
  