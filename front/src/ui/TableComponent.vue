<script setup>
import { ref } from 'vue'

defineProps({
  headers: {
    type: Array,
    required: true,
    // Example structure: [{ key: 'name', label: 'Name', sortable: true }]
  },
  rows: {
    type: Array,
    required: true,
    // Example structure: [{ id: 1, name: 'John Doe', age: 30 }]
  },
  rowKey: {
    type: String,
    default: 'id',
  },
  isSelectable: {
    type: Boolean,
    default: false,
  },
  isSortable: {
    type: Boolean,
    default: false,
  },
  classNames: {
    type: String,
    default: 'table',
  }
})

const selectedRows = ref(new Set())
const sortKey = ref(null)
const sortOrder = ref(1) // 1 for ascending, -1 for descending

const emit = defineEmits(['rowSelected', 'sortChanged'])

// Handle row selection
function handleRowClick(row) {
  if (isSelectable) {
    if (selectedRows.value.has(row[rowKey])) {
      selectedRows.value.delete(row[rowKey])
    } else {
      selectedRows.value.add(row[rowKey])
    }
    emit('rowSelected', Array.from(selectedRows.value))
  }
}

// Handle sorting
function handleSort(header) {
  if (!header.sortable) return

  if (sortKey.value === header.key) {
    sortOrder.value *= -1 // toggle order
  } else {
    sortKey.value = header.key
    sortOrder.value = 1
  }

  emit('sortChanged', { key: sortKey.value, order: sortOrder.value })
}

const sortedRows = computed(() => {
  if (!isSortable || !sortKey.value) return rows

  return [...rows].sort((a, b) => {
    const aValue = a[sortKey.value]
    const bValue = b[sortKey.value]
    if (aValue < bValue) return -1 * sortOrder.value
    if (aValue > bValue) return 1 * sortOrder.value
    return 0
  })
})
</script>

<template>
  <table :class="classNames">
    <thead>
      <tr>
        <th v-if="isSelectable"></th>
        <th v-for="header in headers" :key="header.key" @click="isSortable && header.sortable ? handleSort(header) : null">
          {{ header.label }}
          <span v-if="isSortable && header.sortable && sortKey === header.key">
            {{ sortOrder === 1 ? '↑' : '↓' }}
          </span>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in sortedRows" :key="row[rowKey]" @click="handleRowClick(row)" :class="{ 'selected': selectedRows.has(row[rowKey]) }">
        <td v-if="isSelectable">
          <input type="checkbox" :checked="selectedRows.has(row[rowKey])" @change.stop />
        </td>
        <td v-for="header in headers" :key="header.key">
          {{ row[header.key] }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
}

.table th, .table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table th {
  cursor: pointer;
  background-color: #f2f2f2;
}

.selected {
  background-color: #e6f7ff;
}
</style>
