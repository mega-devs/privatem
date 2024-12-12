<template>
    <div class="panel">
        <HorizontalNavBar/>
        <div class="panel-content">
            <h2 class="panel-content__title" v-if="title">{{ title }}</h2>
            <hr v-if="title" />
            <slot name="content"></slot>
        </div>
    </div>
</template>

<script>
import HorizontalNavBar from './components/HorizontalNavBar.vue';

export default {
    name: "PanelComponent",
    components: {
        HorizontalNavBar,
    },
    props: {
        title: String,
    }
}
</script>

<style lang="scss" scoped>
.panel {
    display: flex;
    flex-direction: column;
    justify-content: start;
    grid-gap: 16px;
    width: 100%;

    height: calc(100vh - 100px); /* Adjusted height to account for horizontal bars */
    
    &-content {
        min-width: 95%;
        max-width: 95%;
        justify-self: center;
        align-self: center;
        border-radius: 16px;
        padding: 15px;
        background-color: #313131;
        overflow-y: auto;
        height: fit-content;
        max-height: calc(80dvh - 100px); /* Adjusted max-height */
        width: fit-content;
        margin-top: 165px; /* Added margin to move below horizontal bars */
        
        &__title {
            margin: 0;
            color: white;
            text-align: center;
        }
    }
}
</style>
