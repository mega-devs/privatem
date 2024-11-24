<script setup>
defineProps({
  modelValue: String,
  placeholder: {
    type: String,
    default: 'Enter text',
  },
  inputType: {
    type: String,
    default: 'text',
  },
  classNames: {
    type: String,
    default: 'input-field',
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
  <input
      :type="inputType"
      :placeholder="placeholder"
      :class="[classNames, { 'w-100': isFull }]"
      :value="modelValue"
      :required="isRequired"
      @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<style scoped>
</style>
