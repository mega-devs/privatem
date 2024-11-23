<script setup>
defineProps({
  modelValue: String,
  placeholder: {
    type: String,
    default: 'Enter text',
  },
  rows: {
    type: Number,
    default: 4,
  },
  classNames: {
    type: String,
    default: 'text-area',
  },
  isFull: {
    type: Boolean,
    default: false,
  },
  isRequired: {
    type: Boolean,
    default: false,
  }
})

defineEmits(['update:modelValue'])
</script>

<template>
  <textarea
      :placeholder="placeholder"
      :rows="rows"
      :class="[classNames, { 'w-100': isFull }]"
      :value="modelValue"
      :required="isRequired"
      @input="$emit('update:modelValue', $event.target.value)"
  ></textarea>
</template>

<style scoped>
</style>
