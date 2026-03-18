<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '@/components/layout/Sidebar.vue'
import TopBar from '@/components/layout/TopBar.vue'
import { NAV_ITEMS } from '@/components/layout/nav'

const route = useRoute()
const isSidebarOpen = ref(true)
const theme = ref<'dark' | 'light'>('dark')

const pageTitle = computed(() => {
  const match = NAV_ITEMS.find((i) => i.to === route.path)
  return match?.label ?? (typeof route.name === 'string' ? route.name : 'App')
})
</script>

<template>
  <div
    class="shell"
    :data-bs-theme="theme"
    :data-sidebar-open="isSidebarOpen"
  >
    <Sidebar :open="isSidebarOpen" :items="NAV_ITEMS" />

    <div class="main">
      <TopBar
        :title="pageTitle"
        :sidebar-open="isSidebarOpen"
        :theme="theme"
        @toggle-sidebar="isSidebarOpen = !isSidebarOpen"
        @toggle-theme="theme = theme === 'dark' ? 'light' : 'dark'"
      />

      <main class="content">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 280px 1fr;
  background: var(--bs-body-bg);
  color: var(--bs-body-color);
}

.shell[data-sidebar-open='false'] {
  grid-template-columns: 1fr;
}

.main {
  display: grid;
  grid-template-rows: 56px 1fr;
  min-width: 0;
}

.content {
  padding: 1rem;
  min-width: 0;
}

@media (max-width: 900px) {
  .shell {
    grid-template-columns: 1fr;
  }
}
</style>

