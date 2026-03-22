<script setup lang="ts">
defineProps<{
  darkMode: boolean
}>()

const emit = defineEmits<{
  (e: 'toggle-dark'): void
}>()

function scrollToId(id: string) {
  const el = document.getElementById(id)
  el?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<template>
  <header class="position-sticky top-0 z-3">
    <nav class="navbar navbar-expand-lg bg-body-tertiary border-bottom">
      <div class="container py-2">
        <a class="navbar-brand fw-bold" href="#" @click.prevent>
          <span class="d-inline-flex align-items-center gap-2">
            <img src="/thursday.png" alt="Thursday AI" class="img-fluid" style="width: 24px; height: 24px;">
            Thursday AI
          </span>
        </a>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#landingNav"
          aria-controls="landingNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="landingNav">
          <ul class="navbar-nav ms-auto align-items-lg-center gap-lg-2 mt-3 mt-lg-0">
            <li class="nav-item">
              <a class="nav-link" href="#features" @click.prevent="scrollToId('features')"
                >Features</a
              >
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#how" @click.prevent="scrollToId('how')">How it works</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#pricing" @click.prevent="scrollToId('pricing')">Pricing</a>
            </li>
            <li class="nav-item">
              <button class="btn btn-outline-secondary btn-sm" type="button" @click="emit('toggle-dark')">
                {{ darkMode ? 'Light' : 'Dark' }}
              </button>
            </li>
            <li class="nav-item">
              <button
                class="btn btn-warning btn-sm fw-semibold text-dark"
                type="button"
                @click="scrollToId('cta')"
              >
                Start Free Trial
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

