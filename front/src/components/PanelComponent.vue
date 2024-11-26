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
    height: 100%;
    &-content {
        min-width: 80%;
        max-width: 95%;
        justify-self: center;
        align-self: center;
        border-radius: 16px;
        background-color: #313131;
        overflow-y: auto;
        height: 80dvh;
        // padding: 20px;
        width: fit-content;
        &__title {
            margin: 0;
            padding-top: 20px;
            color: white;
            text-align: center;
        }
    }
}
</style>
