<script setup lang="ts">
import type { NavItem } from './nav'
defineProps<{
  title: string
  sidebarOpen: boolean
  theme: 'dark' | 'light'
  profileItems: NavItem[]
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
        <i :class="sidebarOpen ? ['bi', 'bi-list', 'navbar-icon'] : ['bi', 'bi-menu-button', 'navbar-icon']" aria-hidden="true"></i>
      </button>

      <div class="fw-semibold text-truncate flex-grow-1">{{ title }}</div>

      <div class="d-flex gap-2">
        <div class="form-check form-switch d-flex align-items-center">
          <input
            class="form-check-input"
            type="checkbox"
            :id="'themeSwitch'"
            :checked="theme === 'dark'"
            @change="emit('toggleTheme')"
          >
          <label class="form-check-label ms-2" :for="'themeSwitch'">
            <i :class="theme === 'dark' ? 'bi bi-moon-stars' : 'bi bi-sun'" aria-hidden="true"></i>
          </label>
        </div>
        <div class="dropdown">
          <button
            class="btn btn-outline-secondary btn-sm dropdown-toggle"
            type="button"
            id="profileDropdown"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            Profile
          </button>
          <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="profileDropdown">
            <li v-for="item in profileItems" :key="item.to">
              <RouterLink :to="item.to" class="dropdown-item">
                <i :class="item.icon" aria-hidden="true"></i>
                {{ item.label }}
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
/* keep minimal custom css; bootstrap handles the rest */
</style>

