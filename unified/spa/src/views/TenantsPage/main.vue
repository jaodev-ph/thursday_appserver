<script setup lang="ts">
import CrudTable, {
  type CrudConfig,
} from '@/components/CrudTable.vue'

const tenantCrud: CrudConfig = {
  fields: [
    {
      key: 'clickable',
      label: 'Name',
      sortable: true,
      formatter: (_value, _key, item) => item.name,
    },
    { key: 'contact_number', label: 'Contact Number', sortable: true },
    { key: 'address', label: 'Address', sortable: true },
  ],
  sort: {
    field: 'clickable',
    order: 'asc',
    dbMapping: 'name',
  },
  baseApi: 'http://localhost:5188/api/tenants',
  fieldForConfirmation: 'name',
  extraFilters: {},
  components: {
    new: 'TenantsNew',
    detail: 'TenantsDetail',
  },
  apiEndpoints: {
    read: '/inquiry',
    delete: '/ROWID_REPLACE',
    deleteSelected: '/selected',
  },
}
</script>

<template>
  <section class="container-fluid p-0">
    <CrudTable
      title="Tenants"
      :crud="tenantCrud"
      :page-size-options="[5, 10, 20]"
      :initial-page-size="5"
      search-placeholder="Search by name, contact number, or address"
    />
  </section>
</template>