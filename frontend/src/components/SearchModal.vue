<script setup>
import { ref, nextTick, defineExpose } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const show   = ref(false)
const word   = ref('')
const input  = ref(null)

function open () {
  show.value = true
  nextTick(() => input.value?.focus())
}
function close () { show.value = false }
function submit () {
  const q = word.value.trim()
  if (q) router.push({ name: 'stage-list', query: { search: q } })
  close()
}

defineExpose({ open })
</script>

<template>
  <transition name="fade">
    <div v-if="show" class="modal">
      <div class="box">
        <input ref="input" v-model="word" @keyup.enter="submit" placeholder="検索" />
        <button @click="submit">検索</button>
        <button class="close" @click="close">×</button>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.modal{position:fixed;inset:0;background:#0008;display:flex;justify-content:center;align-items:center;z-index:9999}
.box{background:#fff;padding:1.5rem;border-radius:.75rem;width:90%;max-width:420px;display:flex;gap:.5rem}
input{flex:1;padding:.6rem;font-size:1rem;border:1px solid #ccc;border-radius:6px}
button{padding:.6rem 1rem;border:none;border-radius:6px;cursor:pointer}
.close{background:#eee}
.fade-enter-active,.fade-leave-active{transition:opacity .15s}
.fade-enter-from,.fade-leave-to{opacity:0}
</style>
