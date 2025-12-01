<script setup>
import { IconTheater, IconMasksTheater, IconSitemap } from '@tabler/icons-vue'

const props = defineProps({
  work: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="body mt-2">
    <div class="title fs-4 fw-bold mb-1">{{ work?.title }}</div>
    <div class="text text-muted">
      <div class="wrap">
        <div class="meta">
          <IconTheater />
          <small class="ms-1">
            <router-link 
              :to="`/works?q=${encodeURIComponent(work?.theater?.name)}`" 
              class="text-decoration-none text-muted"
            >
              {{ work?.theater?.name }}
            </router-link>
          </small>
        </div>
        <div v-if="work?.troupe" class="team my-2">
          <IconSitemap />
          <small class="ms-1">
            <router-link 
              :to="`/works?q=${encodeURIComponent(work?.troupe)}`" 
              class="text-decoration-none text-muted"
            >
              {{ work?.troupe }}
            </router-link>
          </small>
        </div>
        <div v-if="work?.actors && work.actors.length > 0" class="actor mt-2">
          <IconMasksTheater />
          <router-link
            v-for="actor in work.actors"
            :key="actor"
            :to="`/works?q=${encodeURIComponent(actor)}`"
            class="ms-1 text-decoration-none"
          >
            <small class="text-secondary">{{ actor }}</small>
          </router-link>
        </div>
        <div v-if="work?.tags && work.tags.length > 0" class="tag mt-2">
          <router-link
            v-for="tag in work.tags" 
            :key="tag"
            :to="`/works?q=${encodeURIComponent(tag)}`"
            class="badge bg-light text-dark me-1 text-decoration-none"
          >
            {{ tag }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
