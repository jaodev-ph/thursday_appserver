<script setup lang="ts">
import axios from 'axios'
import { computed, onBeforeUnmount, ref, watch } from 'vue'

export type CrudColumn = {
  key: string
  label: string
  sortable?: boolean
  thStyle?: Record<string, string>
  formatter?: (value: unknown, key: string, item: Record<string, unknown>) => unknown
}

export type DatatableViewParams = {
  start: number
  length: number
  sortBy: string
  sortDesc: boolean
  'search[value]': string
}

export type DatatableViewResult<T = Record<string, unknown>> = {
  items: T[]
  total: number
  filtered?: number
}

export type CrudApiEndpoints = {
  read: string
  delete: string
  deleteSelected: string
}

export type CrudConfig = {
  fields: CrudColumn[]
  sort?: {
    field: string
    order: 'asc' | 'desc'
    dbMapping?: string
  }
  baseApi: string
  apiEndpoints: CrudApiEndpoints
  fieldForConfirmation?: string
  extraFilters?: Record<string, unknown>
  components?: {
    new?: string
    detail?: string
  }
}

const props = withDefaults(
  defineProps<{
    title?: string
    crud: CrudConfig
    pageSizeOptions?: number[]
    initialPageSize?: number
    searchPlaceholder?: string
  }>(),
  {
    title: 'Items',
    pageSizeOptions: () => [10, 25, 50],
    initialPageSize: 10,
    searchPlaceholder: 'Search...',
  },
)

const rows = ref<Record<string, unknown>[]>([])
const totalRows = ref(0)
const filteredRows = ref(0)
const loading = ref(false)
const errorMessage = ref('')

const currentPage = ref(1)
const pageSize = ref(props.initialPageSize)
const searchInput = ref('')
const searchValue = ref('')

const sortBy = ref(props.crud.sort?.field ?? props.crud.fields.find((column) => column.sortable)?.key ?? '')
const sortDesc = ref((props.crud.sort?.order ?? 'asc') === 'desc')
const fields = computed(() => props.crud.fields)
const requestSortBy = computed(() => {
  if (props.crud.sort?.dbMapping && sortBy.value === props.crud.sort.field) {
    return props.crud.sort.dbMapping
  }
  return sortBy.value
})

const startRow = computed(() => (filteredRows.value === 0 ? 0 : (currentPage.value - 1) * pageSize.value + 1))
const endRow = computed(() => Math.min(currentPage.value * pageSize.value, filteredRows.value))

let searchDebounce: ReturnType<typeof setTimeout> | null = null
let requestId = 0

watch(searchInput, (value) => {
  if (searchDebounce) {
    clearTimeout(searchDebounce)
  }
  searchDebounce = setTimeout(() => {
    searchValue.value = value.trim()
    currentPage.value = 1
  }, 300)
})

async function loadRows() {
  const activeRequestId = ++requestId
  loading.value = true
  errorMessage.value = ''

  try {
    const requestBody: DatatableViewParams & Record<string, unknown> = {
      start: (currentPage.value - 1) * pageSize.value,
      length: pageSize.value,
      sortBy: requestSortBy.value,
      sortDesc: sortDesc.value,
      'search[value]': searchValue.value,
      ...(props.crud.extraFilters ?? {}),
    }

    const { data: payload } = await axios.post<DatatableViewResult>(
      `${props.crud.baseApi}${props.crud.apiEndpoints.read}`,
      requestBody,
      { headers: { 'Content-Type': 'application/json' } },
    )

    if (activeRequestId !== requestId) {
      return
    }

    rows.value = payload.items ?? []
    totalRows.value = payload.total ?? 0
    filteredRows.value = payload.filtered ?? payload.total ?? 0
  } catch (error) {
    if (activeRequestId !== requestId) {
      return
    }
    rows.value = []
    totalRows.value = 0
    filteredRows.value = 0
    if (axios.isAxiosError(error)) {
      const status = error.response?.status
      errorMessage.value = status
        ? `Failed to load data (${status})`
        : (error.message || 'Failed to load data')
    } else {
      errorMessage.value = error instanceof Error ? error.message : 'Failed to load data'
    }
  } finally {
    if (activeRequestId === requestId) {
      loading.value = false
    }
  }
}

watch([currentPage, pageSize, searchValue, sortBy, sortDesc], loadRows, { immediate: true })

watch(pageSize, () => {
  currentPage.value = 1
})

function onSortChanged(ctx: { sortBy: string; sortDesc: boolean }) {
  sortBy.value = ctx.sortBy
  sortDesc.value = ctx.sortDesc
}

onBeforeUnmount(() => {
  if (searchDebounce) {
    clearTimeout(searchDebounce)
  }
})
</script>

<template>
  <BCard no-body class="crud-card crud-cursor">
    <BCardHeader class="crud-header border-0 d-flex flex-wrap justify-content-between align-items-center gap-3">
      <h2 class="crud-title mb-0">{{ title }}</h2>

      <div class="crud-search d-flex align-items-center gap-2">
        <label class="small text-body-secondary mb-0" for="crud-search">Search</label>
        <BFormInput
          id="crud-search"
          v-model="searchInput"
          type="search"
          size="sm"
          class="crud-search-input"
          :placeholder="searchPlaceholder"
        />
      </div>
    </BCardHeader>

    <BAlert v-if="errorMessage" variant="light" class="crud-alert border-0 small mx-0 mt-0 mb-0 rounded-0" show>
      <span class="text-danger">{{ errorMessage }}</span>
    </BAlert>

    <div class="crud-table-surface">
      <div class="crud-table-wrap">
        <BTable
          :items="rows"
          :fields="fields"
          :busy="loading"
          :sort-by="sortBy"
          :sort-desc="sortDesc"
          hover
          responsive
          show-empty
          empty-text="No records found."
          class="crud-b-table mb-0"
          @sort-changed="onSortChanged"
        >
          <template #table-busy>
            <div class="crud-busy text-center">
              <BSpinner small class="me-2 opacity-50" />
              <span class="text-body-secondary crud-busy-label">Loading</span>
            </div>
          </template>

          <template #cell(clickable)="row">
            <span class="crud-link">{{ row.value }}</span>
          </template>
        </BTable>
      </div>
    </div>

    <BCardFooter class="crud-footer border-0 d-flex flex-wrap justify-content-between align-items-center gap-3">
      <p class="crud-meta mb-0">
        <template v-if="filteredRows === 0">No results</template>
        <template v-else>{{ startRow }}–{{ endRow }} of {{ filteredRows }}</template>
        <span v-if="totalRows !== filteredRows" class="crud-meta-total"> · {{ totalRows }} total</span>
      </p>

      <div class="crud-controls d-flex align-items-center gap-2">
        <label class="small text-body-secondary mb-0" for="crud-page-size">Rows</label>
        <BFormSelect
          id="crud-page-size"
          v-model="pageSize"
          size="sm"
          class="crud-page-select"
          :options="pageSizeOptions"
        />

        <BPagination
          v-model="currentPage"
          size="sm"
          :per-page="pageSize"
          :total-rows="filteredRows"
          align="end"
          class="crud-pagination mb-0"
        />
      </div>
    </BCardFooter>
  </BCard>
</template>

<style scoped>
/* Cursor IDE–like data table: compact, muted chrome, inset surface */
.crud-cursor {
  font-family:
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    'Helvetica Neue',
    Arial,
    sans-serif;
  -webkit-font-smoothing: antialiased;
}

.crud-card {
  border: 1px solid var(--crud-cursor-border, color-mix(in srgb, var(--bs-border-color) 85%, transparent));
  border-radius: 6px;
  box-shadow: none;
  background: var(--bs-body-bg);
  overflow: hidden;
}

.crud-header {
  padding: 0.5rem 0.75rem;
  background: var(--bs-body-bg);
  border-bottom: 1px solid var(--crud-cursor-border, color-mix(in srgb, var(--bs-border-color) 85%, transparent)) !important;
}

.crud-title {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: -0.015em;
  color: var(--bs-emphasis-color);
}

.crud-search {
  min-width: 180px;
  max-width: 260px;
}

.crud-search-input {
  height: 28px;
  padding: 0 0.5rem;
  font-size: 12px;
  line-height: 1.3;
  border-radius: 4px;
  border: 1px solid var(--crud-cursor-border, color-mix(in srgb, var(--bs-border-color) 85%, transparent));
  background: var(--bs-secondary-bg);
  color: var(--bs-body-color);
}

.crud-search-input:focus {
  border-color: color-mix(in srgb, var(--bs-primary) 55%, var(--bs-border-color));
  background: var(--bs-body-bg);
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--bs-primary) 25%, transparent);
}

.crud-alert {
  padding: 0.35rem 0.75rem !important;
  margin: 0 !important;
  font-size: 12px;
  background: color-mix(in srgb, var(--bs-danger) 8%, var(--bs-body-bg)) !important;
  border-bottom: 1px solid var(--crud-cursor-border, color-mix(in srgb, var(--bs-border-color) 85%, transparent)) !important;
}

.crud-table-surface {
  background: var(--bs-tertiary-bg);
  border-top: 1px solid color-mix(in srgb, var(--bs-border-color) 70%, transparent);
  border-bottom: 1px solid color-mix(in srgb, var(--bs-border-color) 70%, transparent);
}

.crud-table-wrap {
  min-width: 0;
  padding: 0;
}

.crud-b-table :deep(table) {
  --bs-table-bg: transparent;
  --bs-table-hover-bg: color-mix(in srgb, var(--bs-body-color) 5%, var(--bs-tertiary-bg));
  margin-bottom: 0;
  border-collapse: separate;
  border-spacing: 0;
}

.crud-b-table :deep(.b-table.b-table-busy .b-table-busy-slot),
.crud-b-table :deep(.b-table.b-table-busy .b-table-busy-slot td) {
  background: transparent !important;
  --bs-table-bg: transparent;
}

.crud-b-table :deep(thead th) {
  border-bottom: 1px solid var(--crud-cursor-border, color-mix(in srgb, var(--bs-border-color) 85%, transparent));
  border-top: none;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.01em;
  text-transform: none;
  color: var(--bs-secondary-color);
  vertical-align: middle;
  background: var(--bs-tertiary-bg);
  white-space: nowrap;
  line-height: 1.2;
}

.crud-b-table :deep(thead th .table-b-table-default),
.crud-b-table :deep(thead th button) {
  font: inherit;
  color: inherit !important;
  text-decoration: none !important;
  padding: 0;
  vertical-align: baseline;
}

.crud-b-table :deep(thead th button:hover),
.crud-b-table :deep(thead th[aria-sort]:hover) {
  color: var(--bs-emphasis-color) !important;
}

.crud-b-table :deep(tbody tr) {
  height: 36px;
}

.crud-b-table :deep(tbody td) {
  height: 36px;
  max-height: 36px;
  padding: 0 10px;
  font-size: 13px;
  line-height: 1.25;
  color: var(--bs-body-color);
  vertical-align: middle;
  box-sizing: border-box;
  border-bottom: 1px solid color-mix(in srgb, var(--bs-border-color) 65%, transparent);
}

.crud-b-table :deep(tbody tr:last-child td) {
  border-bottom: none;
}

.crud-b-table :deep(tbody tr:has(td[colspan])) {
  height: auto;
}

.crud-b-table :deep(tbody tr:has(td[colspan]) td) {
  height: auto;
  max-height: none;
}

.crud-b-table :deep(.b-table-empty-row td) {
  border-bottom: none;
  color: var(--bs-secondary-color);
  font-size: 12px;
  line-height: 1.45;
  padding: 1.75rem 10px;
  text-align: center;
}

.crud-link {
  color: color-mix(in srgb, var(--bs-primary) 92%, var(--bs-body-color));
  font-weight: 400;
  cursor: pointer;
  text-decoration: none;
  border-bottom: none;
  transition: color 0.12s ease;
  font-size: inherit;
  line-height: inherit;
}

.crud-link:hover {
  color: var(--bs-primary);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.crud-footer {
  padding: 6px 10px 8px;
  background: var(--bs-body-bg);
  border-top: 1px solid var(--crud-cursor-border, color-mix(in srgb, var(--bs-border-color) 85%, transparent)) !important;
}

.crud-meta {
  font-size: 11px;
  font-variant-numeric: tabular-nums;
  color: var(--bs-secondary-color);
}

.crud-meta-total {
  opacity: 0.9;
}

.crud-page-select {
  width: 3.5rem;
  height: 26px;
  padding: 0 0.25rem;
  font-size: 11px;
  line-height: 1.2;
  border: 1px solid var(--crud-cursor-border, color-mix(in srgb, var(--bs-border-color) 85%, transparent));
  border-radius: 4px;
  background: var(--bs-secondary-bg);
  color: var(--bs-body-color);
}

.crud-pagination :deep(.pagination) {
  gap: 1px;
  margin-bottom: 0;
}

.crud-pagination :deep(.page-item .page-link) {
  min-width: auto;
  padding: 2px 8px;
  font-size: 11px;
  line-height: 1.5;
  border: none;
  border-radius: 3px;
  background: transparent;
  color: var(--bs-secondary-color);
}

.crud-pagination :deep(.page-item.active .page-link) {
  background: color-mix(in srgb, var(--bs-body-color) 10%, transparent);
  color: var(--bs-emphasis-color);
  font-weight: 500;
}

.crud-pagination :deep(.page-item.disabled .page-link) {
  opacity: 0.35;
}

.crud-pagination :deep(.page-link:hover:not(.disabled)) {
  color: var(--bs-emphasis-color);
  background: color-mix(in srgb, var(--bs-body-color) 6%, transparent);
}

.crud-busy {
  padding: calc(36px * 5 / 9) 10px;
  color: var(--bs-secondary-color);
}

.crud-busy-label {
  font-size: 12px;
  vertical-align: middle;
}

@media (max-width: 900px) {
  .crud-header,
  .crud-footer {
    align-items: stretch !important;
  }

  .crud-search {
    max-width: none;
    width: 100%;
    min-width: 0;
  }

  .crud-controls {
    width: 100%;
    flex-wrap: wrap;
    justify-content: flex-start;
  }

  .crud-pagination {
    width: 100%;
    overflow-x: auto;
  }
}
</style>
