<script setup lang="ts">
import { onMounted, ref } from 'vue'

import LandingNavbar from './components/LandingNavbar.vue'
import LandingHero from './components/LandingHero.vue'
import TrustedBy from './components/TrustedBy.vue'
import Features from './components/Features.vue'
import HowItWorks from './components/HowItWorks.vue'
import UseCases from './components/UseCases.vue'
import Pricing from './components/Pricing.vue'
import Testimonials from './components/Testimonials.vue'
import FinalCTA from './components/FinalCTA.vue'
import LandingFooter from './components/LandingFooter.vue'

const darkMode = ref(false)

function ensureMeta(name: string, content: string, property = false) {
  const selector = property ? `meta[property="${name}"]` : `meta[name="${name}"]`
  let el = document.head.querySelector(selector) as HTMLMetaElement | null
  if (!el) {
    el = document.createElement('meta')
    if (property) el.setAttribute('property', name)
    else el.setAttribute('name', name)
    document.head.appendChild(el)
  }
  el.setAttribute('content', content)
}

onMounted(() => {
  // SEO (static SPA; we still set document title + common meta tags)
  document.title = 'Thursday AI — Multi-tenant AI Chatbots for Businesses'
  ensureMeta(
    'description',
    'Thursday AI is a multi-tenant AI chatbot platform for SMBs—GPT-based bots, multi-channel support (Web, Messenger, WhatsApp), analytics, and easy API/widget integration.',
  )
  ensureMeta('og:title', 'Thursday AI — Multi-tenant AI Chatbots for Businesses', true)
  ensureMeta(
    'og:description',
    'GPT-based bots for SMBs with multi-channel support, analytics, and easy API/widget integration.',
    true,
  )

  // Subtle fade-in animations on scroll (opt-out for reduced motion)
  const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
  if (reduceMotion) return

  const els = Array.from(document.querySelectorAll<HTMLElement>('[data-reveal]'))
  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible')
          io.unobserve(e.target)
        }
      }
    },
    { threshold: 0.12 },
  )
  for (const el of els) io.observe(el)
})
</script>

<template>
  <div class="landing" :data-bs-theme="darkMode ? 'dark' : 'light'">
    <LandingNavbar :dark-mode="darkMode" @toggle-dark="darkMode = !darkMode" />

    <main>
      <LandingHero />
      <TrustedBy />
      <Features />
      <HowItWorks />
      <UseCases />
      <Pricing />
      <Testimonials />
      <FinalCTA />
    </main>

    <LandingFooter />
  </div>
</template>

<style scoped>
.landing {
  background: var(--bs-body-bg);
}

/* Scroll reveal */
[data-reveal] {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 420ms ease, transform 420ms ease;
}

[data-reveal].is-visible {
  opacity: 1;
  transform: translateY(0);
}
</style>

