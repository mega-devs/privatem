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
            if (timestamp){
              const timePart = timestamp.split(' ')[1]; // Get the part after the date
              const [time] = timePart.split(','); // Remove milliseconds if present
              return time; // Return only hh:mm:ss
            }
        },
    },
    emits: ['deleteLog'],
            clearLogs() {
            const currentSessionName = this.getCurrentSessionName();
            if (!currentSessionName) {
                // Handle the case where no session is loaded
                console.error("No session loaded. Cannot clear logs.");
                return;
            }

            let token = '';
            document.cookie.split(";").forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split("=")[1];
                }
            });

            axios.post(`${import.meta.env.VITE_BACK_URL}/api/clear/logs`, {
                session: currentSessionName,
                token: token
            })
            .then(response => {
                // Handle the successful response from the backend
                if (response.data.status === 'success') {
                    // Clear the logs in the frontend
                    this.$emit('deleteLog'); // Assuming this emits an event to clear the logs array
                    console.log("Logs cleared successfully.");
                } else {
                    console.error("Failed to clear logs:", response.data.message);
                }
            })
            .catch(error => {
                // Handle errors during the API request
                console.error("Error clearing logs:", error);
            });
        },

        getCurrentSessionName() {
            const name = document.cookie.split('; ').find(row => row.startsWith('currentSessionName='));
            return name ? name.split('=')[1] : null;
        }
};
</script>
<style lang="scss" scoped>
    .div_two {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-gap: 16px;
    }
</style>
