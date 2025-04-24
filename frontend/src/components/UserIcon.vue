<template>
  <!-- division と rank を同じ div に付与 -->
  <div :class="['division','rank', division && `division--${division}`, rank != null && `rank--${rank}`]">
    <img :src="iconUrl || '/img/user-default.png'" class="icon" />
  </div>
</template>

<script setup>
defineProps({
  iconUrl : String,
  division: String,   // 'actor' | 'staff' | 'producer' | …
  rank    : Number    // 0 以上の整数。null/undefined ならバッジ非表示
})
</script>
