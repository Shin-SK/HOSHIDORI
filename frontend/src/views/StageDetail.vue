<!-- src/views/StageDetail.vue -->
<template>
	<section class="stage-detail mb-footer">
	  <!-- ───────── タイトル & ポスター ───────── -->
  	  <p v-if="error" class="text-red-600">{{ error }}</p>
	  <p v-else-if="loading">Loading…</p>
  
	  <!-- ========== 本体 ========== -->
	  <div v-else class="wrap">
		<div class="contents">
		  <!-- ポスター -->
		  <div class="poster">
			<img v-if="stage.poster_url" :src="stage.poster_url" :alt="stage.title" />
			<span v-else class="noimage">No&nbsp;Poster</span>
		  </div>
  
		  <div class="contents__wrap">
			<h1>{{ stage.title }}</h1>
			<!-- キャスト -->
			<div class="field">
			  <div class="title">キャスト</div>
			  <ul class="inner">
				<li
				  v-for="c in castCredits"
				  :key="'cast-' + c.person.id"
				>
				  <router-link
					:to="{ name: 'stage-list', query: { search: c.person.name } }"
				  >
					{{ c.person.name }}
				  </router-link>
				</li>
				<li v-if="castCredits.length === 0">出演者情報なし</li>
			  </ul>
			</div>
  
			<!-- スタッフ -->
			<div class="field">
			  <div class="title">スタッフ</div>
			  <ul class="inner">
				<li
				  v-for="s in staffCredits"
				  :key="'staff-' + s.person.id"
				>
				  <router-link
					:to="{ name: 'stage-list', query: { search: s.person.name } }"
				  >
					{{ s.person.name }}
					<template v-if="s.position">（{{ s.position }}）</template>
				  </router-link>
				</li>
				<li v-if="staffCredits.length === 0">スタッフ情報なし</li>
			  </ul>
			</div>

			<div class="field">
				<div class="title">劇場</div>
				<ul class="inner">
					<li v-for="t in theaterList" :key="'theater-' + t.id">
					<router-link :to="{ name: 'stage-list', query: { search: t.name } }">
						{{ t.name }}
					</router-link>
					</li>
					<li v-if="theaterList.length === 0">劇場情報なし</li>
				</ul>
				</div>
  
			<!-- レビュー平均 -->
			<div class="field">
			  <div class="title">レビュー平均</div>
			  <template v-if="avgRating !== null">
				<span class="star">
				  <i
					v-for="i in 5"
					:key="i"
					:class="['fa-star', avgRating >= i ? 'fas' : 'far']"
				  />
				</span>
				(平均 {{ avgRating.toFixed(1) }})
			  </template>
			  <p v-else>まだレビューがありません</p>
			</div>
  
			<!-- 広告などはそのまま -->
			<div class="field ad">
			  <a href="https://amzn.to/3RbO1j1" target="_blank" class="item">
				<img src="/img/ad-amazon.png" alt="Amazon" />
			  </a>
			  <a href="https://t.pia.jp/" target="_blank" class="item">
				<img src="/img/ad-pia.png" alt="Pia" />
			  </a>
			</div>
  
			<!-- 編集リンク -->
			<div class="stage-edit">
			  <router-link :to="`/stage/${stage.id}/edit`">ステージ編集</router-link>
			</div>
		  </div><!-- /.contents__wrap -->
		</div><!-- /.contents -->
  
		<!-- ▽ ステータス変更ボタン ▽ -->
		<div class="status">
		  <div class="box">
			<a
			  href="#"
			  :class="{ 'status-active': myStatus === 'watched' }"
			  @click.prevent="setStatus('watched')"
			><i class="icon-eyes"></i><span>観た</span></a>
  
			<a
			  href="#"
			  :class="{ 'status-active': myStatus === 'want' }"
			  @click.prevent="setStatus('want')"
			><i class="icon-heart"></i><span>観たい</span></a>
  
			<a
			  href="#"
			  :class="{ 'status-active': myStatus === 'cannot' }"
			  @click.prevent="setStatus('cannot')"
			><i class="icon-angel"></i><span>観たかった</span></a>
		  </div>
		</div>
	  </div><!-- /.wrap -->
  
	  <!-- ───────── 自分ログ一覧 ───────── -->
		<div class="log myLog">
			<h2>あなたのログ</h2>
			<template v-if="myLogs.length">
				<div class="area">
					<div
						v-for="log in myLogs"
						:key="log.id"
						class="box"
					>
					<div class="box-header">
						<div class="left">
							<div class="icon">
							<img v-if="log.user.icon_url" :src="log.user.icon_url" />
							<img v-else src="/img/user-default.png" />
							</div>
						</div>
						<div class="right">
							<div class="name">{{ log.user.nickname }} さん</div>
							<div class="outer">
								<div class="inner log-status">
									<div class="inner__wrap">
										<i
										:class="[
											'fas',
											log.status === 'watched'
											? 'fa-eye'
											: log.status === 'want'
											? 'fa-heart'
											: 'fa-eye-slash'
										]"
										/>
										{{ log.status_display }}
									</div>
								</div>
								<div class="inner log-times">
									{{ log.times }}
								</div>
								<div class="inner log-rating">
									<div class="star">
										<i
										v-for="i in 5"
										:key="i"
										:class="['fa-star', i <= log.rating ? 'fas' : 'far']"
										/>
									</div>
								</div>
							</div><!-- outer -->
						</div>




					</div>

					<!-- ステータス / 回数 / レーティング -->
					<div class="wrap">

						<!-- コメント -->
						<div class="log-comment">{{ log.comment }}</div>
					</div>

					<div class="edit">
					<template>
						<router-link :to="`/log/${log.id}/edit`">編集</router-link> |
						<a
						href="#"
						class="delete"
						@click.prevent="onClickDelete(log.id)"
						>削除</a>
					</template>
					</div>

					<div class="like">
						<button
							class="like-btn"
							:class="{ liked: log.is_liked }"
							@click="toggleLike(log)"
						>
							<i class="fas fa-heart" />
							{{ log.like_count }}
						</button>
					</div>
				</div>
				</div>
			</template>
			<p class="text-center" v-else>まだログがありません。</p>
		</div>

		<div class="tab">
			<ul class="tab-nav">
				<li>
					<button
					:class="{ active: activeTab === 'shop' }"
					@click="activeTab = 'shop'"
					>
						観劇の後は
					</button>
				</li>
				<li>
					<button
					:class="{ active: activeTab === 'log' }"
					@click="activeTab = 'log'"
					>
						みんなのログ
					</button>
				</li>
			</ul>
			<transition name="fade">
			<div class="shop" v-show="activeTab === 'shop'">
				<h2>劇場近くのお店</h2>
				<p class="disc">観劇の後は演劇について語らってほしいのです</p>

				<div class="area sponser" v-if="sponsorShops.length">
					<h3>オススメ店</h3>
					<ul>
						<li v-for="s in sponsorShops" :key="s.map_url">
							<a :href="s.map_url" target="_blank" rel="noopener">
								<img :src="s.photo_url || '/img/noimage.png'" alt="" loading="lazy">
								<div class="info">
									<div class="title">
										{{ s.name }}
									</div>
									<div class="meta">
										<span v-if="s.rating">★ {{ s.rating.toFixed(1) }}</span>
										<span v-if="s.distance_m">／{{ s.distance_m }} m</span>
									</div>
									<div class="addr">{{ s.address }}</div>
								</div>
							</a>
						</li>
					</ul>
					
				</div>

				<div class="area partner" v-if="partnerShops.length">
					<h3>協力店</h3><!-- 最初協力してくれた店を出してあげたい。これは消えるかもしれないけど、人情というか -->
					<ul>
						<li v-for="s in partnerShops" :key="s.map_url">
							<a :href="s.map_url" target="_blank" rel="noopener">
								<img :src="s.photo_url || '/img/noimage.png'" alt="" loading="lazy">
								<div class="info">
									<div class="title">
										{{ s.name }}
									</div>
									<div class="meta">
										<span v-if="s.rating">★ {{ s.rating.toFixed(1) }}</span>
										<span v-if="s.distance_m">／{{ s.distance_m }} m</span>
									</div>
									<div class="addr">{{ s.address }}</div>
								</div>
							</a>
						</li>
					</ul>

				</div>
				<div class="area shop-list">
					<ul>
						<li v-for="s in freeShops" :key="s.map_url">
							<a :href="s.map_url" target="_blank" rel="noopener">
								<img :src="s.photo_url || '/img/noimage.png'" alt="" loading="lazy">
								<div class="info">
									<div class="title">
										{{ s.name }}
									</div>
									<div class="meta">
										<span v-if="s.rating">★ {{ s.rating.toFixed(1) }}</span>
										<span v-if="s.distance_m">／{{ s.distance_m }} m</span>
									</div>
									<div class="addr">{{ s.address }}</div>
								</div>
							</a>
						</li>
					</ul>
				</div>
				<p class="powered-by">Powered by Google</p>

			</div>
			</transition>
			<transition name="fade">
			<div class="log watchedLog" v-show="activeTab === 'log'">
				<h2>みんなのログ</h2>
				<template v-if="watchedLogs.length">
				<div class="area">
				<div
					v-for="log in watchedLogs"
					:key="log.id"
					class="box"
				>
					<div class="box-header">
						<div class="left">
							<div class="icon">
							<img v-if="log.user.icon_url" :src="log.user.icon_url" />
							<img v-else src="/img/user-default.png" />
							</div>
						</div>
						<div class="right">
							<div class="name">{{ log.user.nickname }} さん</div>
							<div class="outer">
								<div class="inner log-status">
									<div class="inner__wrap">
										<i
										:class="[
											'fas',
											log.status === 'watched'
											? 'fa-eye'
											: log.status === 'want'
											? 'fa-heart'
											: 'fa-eye-slash'
										]"
										/>
										{{ log.status_display }}
									</div>
								</div>
								<div class="inner log-times">
									{{ log.times }}
								</div>
								<div class="inner log-rating">
									<div class="star">
										<i
										v-for="i in 5"
										:key="i"
										:class="['fa-star', i <= log.rating ? 'fas' : 'far']"
										/>
									</div>
								</div>
							</div><!-- outer -->
						</div>




					</div>

					<!-- ステータス / 回数 / レーティング -->
					<div class="wrap">

						<!-- コメント -->
						<div class="log-comment">{{ log.comment }}</div>
					</div>

					<div class="edit">
					<template >
						<router-link :to="`/log/${log.id}/edit`">編集</router-link> |
						<a
						href="#"
						class="delete"
						@click.prevent="onClickDelete(log.id)"
						>削除</a>
					</template>
					</div>

					<div class="like">
						<button
							class="like-btn"
							:class="{ liked: log.is_liked }"
							@click="toggleLike(log)"
						>
							<i class="fas fa-heart" />
							{{ log.like_count }}
						</button>
					</div>
				</div>
				</div>
				</template>
				<p v-else>まだログがありません。</p>
			</div>
			</transition>


		</div>


	</section>
  </template>


<script>

import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/services/api.js'

export default {
  name: 'StageDetail',

  setup () {
    const route  = useRoute()
    const router = useRouter()

    /* ───────── state ───────── */
	const activeTab = ref('shop')
    const stage          = ref({})
    const logs           = ref([]) // ← 取得した全ログ
    /** 自分のログ判定 */
    const isMine = log =>
      !!currentUserId.value && log.user?.id === currentUserId.value

	const watchedLogs = computed(() =>
	logs.value.filter(l => l.status === 'watched')
	)
	// ――― 自分のログを “すべて” 取る（ステータス不問）―――
	const myLogs = computed(() =>
	logs.value.filter(l => isMine(l) && l.status === 'watched')
	)


    const loading        = ref(true)
    const error          = ref(null)
    const currentUserId  = ref(null)
    const myStatus       = ref(null)          // watched / want / cannot

    /* ───────── computed ───────── */
    const castCredits  = computed(() =>
      (stage.value.credits || []).filter(c => c.role === 'cast')
    )
    const staffCredits = computed(() =>
      (stage.value.credits || []).filter(c => c.role === 'staff')
    )
    const theaterList  = computed(() =>
      stage.value.theaters || []
    )

    /** “観た” だけで平均を計算 */
    const avgRating = computed(() => {
      const rated = watchedLogs.value.filter(l => l.rating)
      return rated.length
        ? rated.reduce((s, l) => s + l.rating, 0) / rated.length
        : null
    })

/* ───────── ステータス変更 ───────── */
const setStatus = async (status) => {
  if (!currentUserId.value) return alert('ログインしてください')

  // ===== 観た！はフォームへ =====
  if (status === 'watched') {
    const mine = logs.value.find(isMine)

    // ★ クエリに toStatus=watched を付けて渡す ★
    router.push(
      mine
        ? { name: 'log-edit',   params: { id: mine.id },      query: { toStatus: 'watched' } }
        : { name: 'log-create', params: { stageId: stage.value.id }, query: { toStatus: 'watched' } }
    )
    return
  }

  // ===== want / cannot はその場更新 =====
  try {
    await apiClient.post('/api/log/', { stage_id: stage.value.id, status })
    await reloadLogs()
  } catch (e) {
    alert('変更に失敗しました: ' + (e.response?.data?.detail || e.message))
    console.error(e)
  }
}

    /* ───────── ログ削除 ───────── */
    const onClickDelete = async (id) => {
      if (!confirm('このログを削除しますか？')) return
      try {
        await apiClient.delete(`/api/log/${id}/`)
        logs.value = logs.value.filter(l => l.id !== id)

        // “観た” を消した時はハイライトも落とす
        if (myStatus.value === 'watched' && !logs.value.find(isMine)) {
          myStatus.value = null
        }
        alert('削除しました')
      } catch (e) {
        alert('削除できませんでした: ' + e.message)
      }
    }

	// ――― いいねトグル ―――
	const toggleLike = async (log) => {
	if (!currentUserId.value) return alert('ログインしてください')
	try {
		const { data } = await apiClient.post(`/api/log/${log.id}/like/`)
		log.is_liked   = data.liked
		log.like_count = data.like_count
	} catch (e) {
		alert('失敗しました: ' + (e.response?.data?.detail || e.message))
	}
	}

	/* ---------- ショップまわり ----------*/
	const sponsorShops = computed(() =>
    (stage.value.shops || []).filter(s => s.sponsor_tier === 'sponsor')
                             .sort((a,b)=> a.priority - b.priority))

	const partnerShops = computed(() =>
		(stage.value.shops || []).filter(s => s.sponsor_tier === 'partner')
								.sort((a,b)=> a.priority - b.priority))

	const freeShops = computed(() =>
		(stage.value.shops || []).filter(s => s.sponsor_tier === 'free'))

    /* ───────── API fetch ───────── */
    const reloadLogs = async () => {
      const res = await apiClient.get('/api/log/', { params: { stage: stage.value.id } })
      logs.value = res.data
      const mine = res.data.find(isMine)
      myStatus.value = mine ? mine.status : null
    }

    onMounted(async () => {     
      try {
        stage.value = (await apiClient.get(`/api/stage/${route.params.id}/`)).data
        try {
          currentUserId.value = (await apiClient.get('/dj-rest-auth/user/')).data.id
        } catch { /* 未ログイン */ }
        await reloadLogs()

    // ここで本当の値を確認
    console.log('currentUserId', currentUserId.value)
    console.table(logs.value.map(l => ({
      id   : l.id,
      uid  : l.user?.id,
      mine : isMine(l),
      st   : l.status
    })))
      } catch (e) {
        error.value = e.message
      } finally {
        loading.value = false
      }
    })



    /* ───────── expose ───────── */
    return {
	  activeTab,
      stage,
      watchedLogs,        // ← テンプレート側はこれを使う
      loading,
      error,
      castCredits,
      staffCredits,
      theaterList,
      avgRating,
      myStatus,
      setStatus,
      isMine,
	  toggleLike,
      onClickDelete,
	  sponsorShops,
	  partnerShops,
	  freeShops,
	  myLogs
    }
  }
}
</script>

