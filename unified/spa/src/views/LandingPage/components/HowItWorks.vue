<script setup lang="ts">
const steps = [
  {
    title: 'Integrate in minutes',
    icon: 'bi-box-arrow-in-right',
    desc: 'Connect your channels using API + widget. Then map tenant bots to your businesses.',
  },
  {
    title: 'Customize each tenant bot',
    icon: 'bi-gear-wide-connected',
    desc: 'Tune tone, rules, and knowledge base training—so every business stays on-brand.',
  },
  {
    title: 'Measure & improve',
    icon: 'bi-bar-chart',
    desc: 'Use conversation analytics to identify gaps, track intent, and continuously improve.',
  },
]
</script>

<template>
  <section class="py-5" id="how">
    <div class="container">
      <div class="text-center mb-4" data-reveal>
        <h2 class="fw-bold">How it works</h2>
        <p class="text-body-secondary mb-0">A simple flow from integration to measurable results.</p>
      </div>

      <div class="row g-3">
        <div v-for="(s, idx) in steps" :key="s.title" class="col-12 col-md-4" data-reveal>
          <div class="card border-0 shadow-sm rounded-4 h-100 bg-body-tertiary">
            <div class="card-body">
              <div class="d-flex align-items-center justify-content-between mb-3">
                <div class="p-2 rounded-3 border bg-warning bg-opacity-25">
                  <i :class="['bi', s.icon]" aria-hidden="true"></i>
                </div>
                <span class="badge rounded-pill text-bg-warning">Step {{ idx + 1 }}</span>
              </div>
              <div class="fw-semibold mb-2">{{ s.title }}</div>
              <div class="text-body-secondary small">{{ s.desc }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

