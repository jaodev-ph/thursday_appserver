<script setup lang="ts">
import SidebarMenu from './SidebarMenu.vue'
import type { NavItem } from './nav'

defineProps<{
  open: boolean
  items: NavItem[]
}>()
</script>

<template>
  <aside class="sidebar d-flex flex-column border-end" :data-open="open">
    <div class="px-3 py-3">
      <div class="d-flex align-items-center gap-2">
        <div class="brand__mark">T</div>
        <div>
          <div class="fw-bold">Thursday</div>
          <div class="text-body-secondary small">App Server</div>
        </div>
      </div>
    </div>

    <SidebarMenu :items="items" />

    <div class="mt-auto px-3 pb-3 text-body-secondary small">v0</div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 280px;
}

.sidebar[data-open='false'] {
  display: none;
}

.brand__mark {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  background: var(--bs-warning);
  color: #111;
  font-weight: 800;
}

@media (max-width: 900px) {
  .sidebar {
    position: fixed;
    inset: 0 auto 0 0;
    width: 280px;
    z-index: 20;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
  }
}
</style>

