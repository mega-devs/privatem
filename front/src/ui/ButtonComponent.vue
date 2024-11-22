<script setup>
defineProps({ 
    buttonText: String,
    buttonType: {
        type: String,
        default: 'button',
    },
    classNames: {
        type: String,
        default: 'button',
    },
    isPrimary: {
        type: Boolean,
        default: true,
    },
    isInfo: {
        type: Boolean,
        default: false,
    },
    isFull: {
        type: Boolean,
        default: false,
    },
})
defineEmits({
    clickHandler: null
})
</script>
<template>
    <button
        :type="buttonType"
        @click.prevent="$emit('clickHandler')"
        class="btn"
        :class="[
            classNames,
            {
                'btn-primary': isPrimary,
                'btn-info': isInfo,
                'w-100': isFull,
            },
        ]"
    >
        {{ buttonText }}
    </button>
</template>
<style scoped>
</style>
