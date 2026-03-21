<script setup lang="ts">
const cases = [
  {
    title: 'E-commerce',
    icon: 'bi-bag',
    desc: 'Answer product questions, handle order status, and recommend items—per tenant storefront.',
  },
  {
    title: 'Customer Support',
    icon: 'bi-headset',
    desc: 'Triage requests, reduce ticket volume, and escalate only when needed.',
  },
  {
    title: 'Lead Generation',
    icon: 'bi-megaphone',
    desc: 'Capture intent, qualify leads, and route them to the right team—without friction.',
  },
]
</script>

<template>
  <section class="py-5">
    <div class="container">
      <div class="text-center mb-4" data-reveal>
        <h2 class="fw-bold">Use cases</h2>
        <p class="text-body-secondary mb-0">Designed for SMB teams who need fast, reliable outcomes.</p>
      </div>

      <div class="row g-3">
        <div v-for="c in cases" :key="c.title" class="col-12 col-md-4" data-reveal>
          <div class="card border-0 shadow-sm rounded-4 h-100 bg-body-tertiary">
            <div class="card-body">
              <div class="d-flex align-items-center gap-2 mb-2">
                <div class="p-2 rounded-3 bg-warning bg-opacity-25 border border-warning border-opacity-25">
                  <i :class="['bi', c.icon, 'fs-4']" aria-hidden="true"></i>
                </div>
                <div class="fw-semibold">{{ c.title }}</div>
              </div>
              <div class="text-body-secondary small">{{ c.desc }}</div>
              <ul class="mt-3 mb-0 ps-3 text-body-secondary small">
                <li>Multi-channel readiness</li>
                <li>Tenant bot customization</li>
                <li>Analytics for improvements</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

