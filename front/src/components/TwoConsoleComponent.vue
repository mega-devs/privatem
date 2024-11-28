<template>
    <div class="div_two">
        <ConsoleLogComponent title="Console" btn-label="Delete" @btn-clicked="$emit('deleteLog')">
            <template #content>
                <p v-for="(item, index) in logs" :key="index">
                    <span :class="item['status']"><span :style="{ color: 'orange' }">{{
                        formatTime(item['created_at'])
                    }}</span> | {{ item['TEXT'] }}<br/></span>
                </p>
            </template>
        </ConsoleLogComponent>
        <ConsoleLogComponent title="Debug" >
            <template #content>
            <p v-for="item in mailing_logs" :key="item.timestamp">
                <span :class="item.level.toLowerCase()"><span :style="{ color: 'orange' }">{{
                    formatTime(item.timestamp)
                }}</span> | {{ item.message }}<br/></span>
            </p>
            </template>
        </ConsoleLogComponent>
    </div>
</template>


<script>
import ConsoleLogComponent from './ConsoleLogComponent.vue';

export default {
    name: "TwoConsoleComponent",
    components: {
        ConsoleLogComponent,
    },
    props: {
        logs: Array,
        mailing_logs: Array,
    },
    methods: {
        formatTime(timestamp) {
            // Split the timestamp to get the time part
            const timePart = timestamp.split(' ')[1]; // Get the part after the date
            const [time] = timePart.split(','); // Remove milliseconds if present
            return time; // Return only hh:mm:ss
        },
    },
    emits: ['deleteLog']
};
</script>
<style lang="scss" scoped>
    .div_two {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-gap: 16px;
    }
</style>
