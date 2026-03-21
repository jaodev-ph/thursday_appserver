<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import AppShell from '@/components/layout/AppShell.vue'

const route = useRoute()

const useShell = computed(() => route.meta.layout !== 'landing')
</script>

<template>
  <AppShell v-if="useShell">
    <RouterView />
  </AppShell>
  <RouterView v-else />
</template>
