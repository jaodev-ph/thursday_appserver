<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { NavItem } from './nav'

defineProps<{
  items: NavItem[]
  collapsed?: boolean
}>()
</script>

<template>
  <nav class="nav nav-pills flex-column gap-1 px-2 pb-3" :data-collapsed="collapsed ? 'true' : 'false'">
    <RouterLink
      v-for="item in items"
      :key="item.to"
      class="nav-link"
      :to="item.to"
    >
      <span class="d-inline-flex align-items-center gap-2">
        <i :class="['bi', item.icon, 'nav-icon']" aria-hidden="true"></i>
        <span v-if="!collapsed" class="nav-label">{{ item.label }}</span>
      </span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.nav-link {
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.nav-link.router-link-active {
  background-color: var(--bs-warning-bg-subtle);
  color: var(--bs-emphasis-color);
}

.nav-icon {
  font-size: 1.05rem;
  width: 1.25rem;
  text-align: center;
}

.nav-label {
  white-space: nowrap;
}

/* Center icons when collapsed */
nav[data-collapsed='true'] :deep(.nav-link) {
  justify-content: center;
}
nav[data-collapsed='true'] .nav-icon {
  margin-right: 0;
}
</style>
