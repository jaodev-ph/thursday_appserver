<script setup lang="ts">
const testimonials = [
  {
    name: 'Maya Chen',
    role: 'E-commerce Ops Lead',
    quote:
      'We replaced fragmented support flows with one multi-tenant bot. Customers get instant answers, and our team finally has analytics we can act on.',
  },
  {
    name: 'Daniel Ruiz',
    role: 'Customer Support Manager',
    quote:
      'Thursday AI made onboarding new brands painless. The widget + API combo means we ship faster, and conversation analytics helped us improve resolution rates.',
  },
  {
    name: 'Samira Khan',
    role: 'Growth Lead',
    quote:
      'Lead generation became consistent. The bots understand intent, route follow-ups, and keep the experience smooth across web and messenger.',
  },
]
</script>

<template>
  <section class="py-5" id="testimonials">
    <div class="container">
      <div class="text-center mb-4" data-reveal>
        <h2 class="fw-bold">Teams love the results</h2>
        <p class="text-body-secondary mb-0">Sample testimonials you can replace anytime.</p>
      </div>

      <div class="row g-3">
        <div
          v-for="t in testimonials"
          :key="t.name"
          class="col-12 col-md-4"
          data-reveal
        >
          <figure class="card border-0 shadow-sm rounded-4 h-100 bg-body-tertiary px-4 py-4">
            <blockquote class="blockquote mb-3">
              <div class="text-body-secondary">{{ t.quote }}</div>
            </blockquote>
            <figcaption class="blockquote-footer mb-0">
              <span class="fw-semibold">{{ t.name }}</span> <span class="text-body-secondary">· {{ t.role }}</span>
            </figcaption>
          </figure>
        </div>
      </div>
    </div>
  </section>
</template>

