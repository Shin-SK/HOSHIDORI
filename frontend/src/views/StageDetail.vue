<!-- src/views/StageDetail.vue -->
<template>
	<section class="stage-detail mb-footer">
	  <!-- ───────── タイトル & ポスター ───────── -->
	  <h1>{{ stage.title }}</h1>
  
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
			><i class="fas fa-eye"></i><span>観た</span></a>
  
			<a
			  href="#"
			  :class="{ 'status-active': myStatus === 'want' }"
			  @click.prevent="setStatus('want')"
			><i class="fas fa-heart"></i><span>観たい</span></a>
  
			<a
			  href="#"
			  :class="{ 'status-active': myStatus === 'cannot' }"
			  @click.prevent="setStatus('cannot')"
			><i class="fas fa-eye-slash"></i><span>観れない</span></a>
		  </div>
		</div>
	  </div><!-- /.wrap -->
  
	  <!-- ───────── ログ一覧 ───────── -->
<!-- ───────── ログ一覧 ───────── -->
		<div class="log">
		<template v-if="watchedLogs.length">
			<div class="area">
			<div
				v-for="log in watchedLogs"
				:key="log.id"
				class="box"
			>
				<div class="name-box">
				<div class="icon">
					<img v-if="log.user.icon_url" :src="log.user.icon_url" />
					<img v-else src="/img/user-default.png" />
				</div>
				<div class="name">{{ log.user.nickname }} さん</div>
				</div>

				<!-- ステータス / 回数 / レーティング -->
				<div class="wrap">
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
					<span>観劇回数</span>{{ log.times }}
					</div>
					<div class="inner log-rating">
					<span>レビュー</span>
					<div class="star">
						<i
						v-for="i in 5"
						:key="i"
						:class="['fa-star', i <= log.rating ? 'fas' : 'far']"
						/>
					</div>
					</div>
				</div>
				<!-- コメント -->
				<div class="log-comment">{{ log.comment }}</div>
				</div>

				<div class="edit">
				<template v-if="isMine(log)">
					<router-link :to="`/log/${log.id}/edit`">編集</router-link> |
					<a
					href="#"
					class="delete"
					@click.prevent="onClickDelete(log.id)"
					>削除</a>
				</template>
				</div>
			</div>
			</div>
		</template>
		<p v-else>まだログがありません。</p>
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
    const stage          = ref({})
    const logs           = ref([])            // ← 取得した全ログ
    const watchedLogs    = computed(() =>     // ← “観た” だけ抽出
      logs.value.filter(l => l.status === 'watched')
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

    /** 自分のログ判定 */
    const isMine = log =>
      !!currentUserId.value && log.user?.id === currentUserId.value

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
      } catch (e) {
        error.value = e.message
      } finally {
        loading.value = false
      }
    })

    /* ───────── expose ───────── */
    return {
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
      onClickDelete
    }
  }
}
</script>
