<script setup lang="ts">
const links: Record<string, string[]> = {
  Product: ['Features', 'API + Widget', 'Analytics'],
  Company: ['About', 'Careers', 'Contact'],
  Legal: ['Privacy', 'Terms'],
}
</script>

<template>
  <footer class="py-5 border-top">
    <div class="container">
      <div class="row g-4">
        <div class="col-12 col-md-4">
          <div class="d-flex align-items-center gap-2 fw-bold mb-2">
            <img src="/thursday.png" alt="Thursday AI" class="img-fluid" style="width: 24px; height: 24px;">
            Thursday AI
          </div>
          <div class="text-body-secondary small">
            Multi-tenant AI chatbot platform for businesses.
          </div>
        </div>

        <div class="col-6 col-md-2" v-for="(items, heading) in links" :key="heading">
          <div class="fw-semibold mb-2">{{ heading }}</div>
          <ul class="list-unstyled mb-0">
            <li v-for="l in items" :key="l" class="mb-2">
              <a class="link-body-emphasis text-decoration-none" href="#" @click.prevent>
                {{ l }}
              </a>
            </li>
          </ul>
        </div>

        <div class="col-12 col-md-4">
          <div class="fw-semibold mb-2">Stay in the loop</div>
          <div class="input-group">
            <input
              class="form-control"
              type="email"
              placeholder="Email address"
              aria-label="Email address"
            />
            <button class="btn btn-warning text-dark fw-semibold" type="button">
              Subscribe
            </button>
          </div>
          <div class="text-body-secondary small mt-2">
            No spam. Just product updates.
          </div>
        </div>
      </div>

      <div class="mt-5 text-body-secondary small">
        © {{ new Date().getFullYear() }} Thursday AI. All rights reserved.
      </div>
    </div>
  </footer>
</template>

