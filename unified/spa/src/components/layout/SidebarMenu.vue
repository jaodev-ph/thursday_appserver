<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { NavItem } from './nav'

defineProps<{
  items: NavItem[]
}>()
</script>

<template>
  <nav class="nav nav-pills flex-column gap-1 px-2 pb-3">
    <RouterLink
      v-for="item in items"
      :key="item.to"
      class="nav-link"
      :to="item.to"
    >
      {{ item.label }}
    </RouterLink>
  </nav>
</template>

<style scoped>
.nav-link {
  border-radius: 0.75rem;
}
.nav-link.router-link-active {
  background-color: var(--bs-warning-bg-subtle);
  color: var(--bs-emphasis-color);
}
</style>

