<script setup lang="ts">
type Tier = {
  name: string
  price: string
  desc: string
  badge?: string
  features: string[]
}

const tiers: Tier[] = [
  {
    name: 'Starter',
    price: '$19',
    desc: 'For new teams getting their first tenant bot live.',
    features: ['1 tenant bot', 'Web chat widget', 'Basic analytics', 'Knowledge base training'],
  },
  {
    name: 'Pro',
    price: '$49',
    desc: 'For support teams scaling conversations across channels.',
    badge: 'Most Popular',
    features: ['Up to 5 tenant bots', 'Messenger + WhatsApp', 'Advanced analytics', 'Team collaboration'],
  },
  {
    name: 'Business',
    price: '$99',
    desc: 'For multi-brand operations and deeper reporting.',
    features: ['Unlimited tenants', 'Custom routing rules', 'Performance dashboards', 'Priority support'],
  },
]
</script>

<template>
  <section class="py-5" id="pricing">
    <div class="container">
      <div class="text-center mb-4" data-reveal>
        <h2 class="fw-bold">Simple, scalable pricing</h2>
        <p class="text-body-secondary mb-0">Pick the tier that matches your deployment and usage.</p>
      </div>

      <div class="row g-3 justify-content-center">
        <div
          v-for="tier in tiers"
          :key="tier.name"
          class="col-12 col-md-4"
          data-reveal
        >
          <div
            class="card border-0 shadow-sm rounded-4 h-100"
            :class="tier.badge ? 'border border-warning border-opacity-50' : ''"
          >
            <div class="card-body p-4">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <div class="fw-semibold fs-5">{{ tier.name }}</div>
                <span v-if="tier.badge" class="badge text-bg-warning">{{ tier.badge }}</span>
              </div>
              <div class="display-6 fw-bold mb-1">{{ tier.price }}</div>
              <div class="text-body-secondary small mb-3">{{ tier.desc }}</div>

              <ul class="list-unstyled mb-4">
                <li v-for="f in tier.features" :key="f" class="d-flex gap-2 mb-2">
                  <i class="bi bi-check2-circle text-warning" aria-hidden="true"></i>
                  <span class="text-body-secondary small">{{ f }}</span>
                </li>
              </ul>

              <button class="btn w-100 btn-warning fw-semibold text-dark" type="button">
                Start Free Trial
              </button>

              <div class="text-body-secondary small mt-2 text-center">
                Cancel anytime
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

