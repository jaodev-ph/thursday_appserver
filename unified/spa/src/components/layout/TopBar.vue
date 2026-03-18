<script setup lang="ts">
defineProps<{
  title: string
  sidebarOpen: boolean
  theme: 'dark' | 'light'
}>()

const emit = defineEmits<{
  (e: 'toggleSidebar'): void
  (e: 'toggleTheme'): void
}>()
</script>

<template>
  <header class="navbar border-bottom px-3" style="min-height: 56px">
    <div class="d-flex align-items-center gap-2 w-100">
      <button class="btn btn-outline-secondary btn-sm" type="button" @click="emit('toggleSidebar')">
        {{ sidebarOpen ? 'Hide' : 'Menu' }}
      </button>

      <div class="fw-semibold text-truncate flex-grow-1">{{ title }}</div>

      <div class="d-flex gap-2">
        <button class="btn btn-outline-warning btn-sm" type="button" @click="emit('toggleTheme')">
          {{ theme === 'dark' ? 'Light' : 'Dark' }}
        </button>
        <button class="btn btn-outline-secondary btn-sm" type="button">Profile</button>
      </div>
    </div>
  </header>
</template>

<style scoped>
/* keep minimal custom css; bootstrap handles the rest */
</style>

