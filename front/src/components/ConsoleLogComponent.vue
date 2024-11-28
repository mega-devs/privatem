<template>
    <div class="console-log">
        <div class="console-log__panel">
            <h3>{{ title }}</h3>
            <v-btn @click="$emit('btn-clicked')" class="btn btn-primary" v-if="btnLabel">{{ btnLabel }}</v-btn>
        </div>
        <div class="console-output" ref="consoleOutput">
            <slot name="content"></slot>
        </div>
    </div>
</template>


<script>
import { defineComponent } from 'vue';


export default defineComponent({
    name: 'ConsoleLogComponent',
    data() {
        return {
        }
    },
    props: {
        title: {
            type: String,
            default: 'Console Log'
        },
        logs: {
            type: Array,
            default: []
        },
        btnLabel: String,
    },
    watch: {
        logs() {
            this.scrollToBottom();
        },
    },    
    emits: ['btn-clicked'],
    methods: {
        scrollToBottom() {
              setTimeout(() => {
                this.$refs.consoleOutput.scrollTop = this.$refs.consoleOutput.scrollHeight;
              }, 50);
        }
    }
});
</script>
<style lang="scss" scoped>

.console-log {
    display: flex;
    flex-direction: column;
    grid-gap: 8px;
    margin: 16px 0px;
    padding: 8px;
    background-color: #000;
    border-radius: 10px;
    &__panel {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .console-output {
        width: 100%;
        height: 200px;
        background-color: #000;
        color: #fff;
        overflow: auto;
        z-index: 9999;
        &::-webkit-scrollbar {
            width: 12px;
        }
        &::-webkit-scrollbar-thumb {
            background-color: #888;
            border-radius: 0 10px 10px 10px;
        }
        &::-webkit-scrollbar-track {
        background-color: #495057;
        border-radius: 0px 8px 8px 0px;
        }
    }
}

</style>
