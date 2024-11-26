<template>
    <div class="layout">
        <NavBarComponent stateProp="templates"/>
        <PanelComponent :title="title" class="layout__content">
            <template #content>
                <slot name="content"></slot>
            </template>
        </PanelComponent>        
    </div>
</template>

<script>
import NavBarComponent from './components/NavBarComponent.vue';
import PanelComponent from './PanelComponent.vue';

export default {
    name: "LayoutComponent",
    components: {
        NavBarComponent,
        PanelComponent
    },
    props: {
        title: String,
    }
}
</script>

<style lang="scss" scoped>
.layout {
    width: 100%;
    display: grid;
    grid-template-columns: min-content 1fr;
    &__content {
        height: 80%;
    }
}
</style>
