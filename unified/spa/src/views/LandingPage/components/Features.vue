<script setup lang="ts">
const features = [
  {
    title: 'AI-powered chatbot',
    icon: 'bi-chat-dots',
    desc: 'GPT-based responses that handle FAQs, triage, and personalized conversations.',
  },
  {
    title: 'Multi-channel support',
    icon: 'bi-send',
    desc: 'Deploy on Web, Messenger, and WhatsApp with a unified tenant configuration.',
  },
  {
    title: 'Customizable bots per tenant',
    icon: 'bi-diagram-3',
    desc: 'Give each business its own bot setup, voice, and rules—without rebuilding.',
  },
  {
    title: 'Conversation analytics',
    icon: 'bi-graph-up-arrow',
    desc: 'Understand intent trends, engagement, and performance to improve over time.',
  },
  {
    title: 'Easy integration',
    icon: 'bi-plug',
    desc: 'Use API + widget to start fast and scale confidently.',
  },
  {
    title: 'Knowledge base / training',
    icon: 'bi-book',
    desc: 'Train bots using your documentation so answers stay accurate and on-brand.',
  },
]
</script>

<template>
  <section class="py-5" id="features">
    <div class="container">
      <div class="text-center mb-4" data-reveal>
        <h2 class="fw-bold">Everything you need to go live</h2>
        <p class="text-body-secondary mb-0">Core features designed for multi-tenant SaaS teams.</p>
      </div>

      <div class="row g-3">
        <div
          v-for="f in features"
          :key="f.title"
          class="col-12 col-md-6 col-lg-4"
          data-reveal
        >
          <div class="card border-0 shadow-sm h-100 rounded-4 bg-body-tertiary">
            <div class="card-body">
              <div class="d-flex align-items-center gap-2 mb-2">
                <div class="p-2 rounded-3 bg-warning bg-opacity-25 border border-warning border-opacity-25">
                  <i :class="['bi', f.icon, 'fs-4']" aria-hidden="true"></i>
                </div>
                <div class="fw-semibold">{{ f.title }}</div>
              </div>
              <div class="text-body-secondary small">{{ f.desc }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

