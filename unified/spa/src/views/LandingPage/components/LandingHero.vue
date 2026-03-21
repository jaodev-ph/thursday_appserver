<script setup lang="ts">
import { reactive, ref } from 'vue'

const form = reactive({
  message: '',
})

type ChatMsg = { role: 'user' | 'assistant'; text: string }
const messages = ref<ChatMsg[]>([
  {
    role: 'assistant',
    text: 'Hi! I can help you evaluate Thursday AI. What are you trying to build?',
  },
])

function pickResponse(q: string) {
  const query = q.toLowerCase()
  if (query.includes('whatsapp')) {
    return 'Thursday AI supports WhatsApp out of the box via multi-channel integrations. Tell me which flows you want to automate.'
  }
  if (query.includes('pricing')) {
    return 'Check the Pricing section below—Starter is great for getting started, and Business adds advanced analytics and higher usage limits.'
  }
  if (query.includes('analytics') || query.includes('report')) {
    return 'Conversation analytics help you track intent, resolution rate, and engagement—so you can improve bot performance over time.'
  }
  return 'Great question. Thursday AI lets you create tenant-specific GPT chatbots, integrate via API/widget, and train with a knowledge base.'
}

function sendMessage() {
  const text = form.message.trim()
  if (!text) return
  messages.value.push({ role: 'user', text })
  form.message = ''

  // Simulate response (no backend required for the landing page demo)
  window.setTimeout(() => {
    messages.value.push({ role: 'assistant', text: pickResponse(text) })
  }, 450)
}
</script>

<template>
  <section class="py-5">
    <div class="container">
      <div class="row align-items-center g-4">
        <div class="col-lg-7">
          <div class="d-inline-flex align-items-center gap-2 mb-3" data-reveal>
            <span class="badge text-bg-warning fw-semibold rounded-pill px-3 py-2"
              >New: Knowledge Base Training</span
            >
            <span class="text-body-secondary small">Multi-tenant GPT chatbot platform</span>
          </div>

          <h1 class="display-5 fw-bold lh-sm mb-3" data-reveal>
            Build AI chatbots that feel native to every business you serve.
          </h1>

          <p class="lead text-body-secondary mb-4" data-reveal>
            Thursday AI is a multi-tenant SaaS AI chatbot platform for SMBs—powered by GPT-style
            responses, multi-channel support (Web, Messenger, WhatsApp), customizable bots per
            tenant, and conversation analytics.
          </p>

          <div class="d-flex flex-wrap gap-2" data-reveal>
            <button class="btn btn-warning btn-lg fw-semibold text-dark" type="button">
              Start Free Trial
            </button>
            <button class="btn btn-outline-secondary btn-lg fw-semibold" type="button">
              View API + Widget
            </button>
          </div>

          <div class="row mt-4 g-3" data-reveal>
            <div class="col-md-4">
              <div class="p-3 border rounded-4 h-100 bg-body-tertiary">
                <div class="fw-bold">GPT-based</div>
                <div class="text-body-secondary small">Smart conversations with modern LLM responses</div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="p-3 border rounded-4 h-100 bg-body-tertiary">
                <div class="fw-bold">Multi-channel</div>
                <div class="text-body-secondary small">Web, Messenger, WhatsApp integrations</div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="p-3 border rounded-4 h-100 bg-body-tertiary">
                <div class="fw-bold">Analytics</div>
                <div class="text-body-secondary small">Track intents, engagement & performance</div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-5">
          <div class="card shadow-sm border-0 rounded-4" data-reveal>
            <div class="card-header bg-transparent border-bottom-0 pt-4 pb-2">
              <div class="d-flex align-items-center justify-content-between">
                <div class="fw-semibold">Live chatbot demo</div>
                <span class="badge text-bg-warning rounded-pill">Widget</span>
              </div>
              <div class="text-body-secondary small mt-1">No backend—mock responses for the landing page</div>
            </div>

            <div class="card-body">
              <div class="chat" role="log" aria-live="polite">
                <div
                  v-for="(m, idx) in messages"
                  :key="idx"
                  class="chat__row"
                  :class="{ 'chat__row--user': m.role === 'user' }"
                >
                  <div class="chat__bubble" :class="{ 'chat__bubble--user': m.role === 'user' }">
                    {{ m.text }}
                  </div>
                </div>
              </div>

              <form class="mt-3 d-flex gap-2" @submit.prevent="sendMessage">
                <input
                  v-model="form.message"
                  class="form-control"
                  type="text"
                  placeholder="Ask about WhatsApp, analytics, or pricing..."
                  aria-label="Chat message"
                />
                <button class="btn btn-warning fw-semibold text-dark" type="submit">
                  <i class="bi bi-send"></i>
                </button>
              </form>

              <div class="text-body-secondary small mt-2">
                Tip: try “How does analytics work?” or “Support WhatsApp?”
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.chat {
  height: 260px;
  overflow: auto;
  padding-right: 6px;
}

.chat__row {
  display: flex;
  margin-bottom: 10px;
}

.chat__row--user {
  justify-content: flex-end;
}

.chat__bubble {
  max-width: 92%;
  border-radius: 14px;
  padding: 10px 12px;
  background: rgba(255, 193, 7, 0.12);
  border: 1px solid rgba(255, 193, 7, 0.25);
}

.chat__bubble--user {
  background: rgba(13, 110, 253, 0.12);
  border-color: rgba(13, 110, 253, 0.25);
}
</style>

