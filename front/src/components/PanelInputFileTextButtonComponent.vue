<template>
    <div class="panel-imap">
        <v-file-input class="panel-imap-txt " clearable :label="`Input ${what}.txt`" accept="text file/txt" @change="$emit('upload', $event)"></v-file-input>
        <div class="panel-imap__btns">
            <v-btn @click="$emit('submit')" class="btn btn-primary">Submit</v-btn>
            <v-btn @click="$emit('export')" class="btn btn-primary">Export to TXT</v-btn>
        </div>
        <v-textarea class="panel-imap__input " :label="`Enter multiple ${what} separated by new lines`" v-model="imapTextInput" variant="outlined"></v-textarea>
    </div>
</template>


<script>
import { defineComponent } from 'vue';
import ConsoleLogComponent from './ConsoleLogComponent.vue';

export default defineComponent({
    name: "PanelInputFileTextButtonComponent",
    components: {
        ConsoleLogComponent,
    },
    data() {
        return {
            imapTextInput: "",
        }
    },
    props: {
        what: String,
        modelValue: String,
    },
    watch: {
        modelValue() {
            this.imapTextInput = this.modelValue;
        },
        imapTextInput() {
            this.$emit('update:modelValue', this.imapTextInput)
        }
    },
    emits: ['submit', 'export', 'upload', 'update']
});
</script>
<style lang="scss" scoped>
.panel-imap {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-areas: "txt input"
    "btns input";
  grid-gap: 16px;
  &-txt {
    grid-area: txt;
  }
  &__input {
    grid-area: input;
  }
  &__btns {
    grid-area: btns;
    display: flex;
    grid-gap: 16px;
    justify-content: center;
  }  
}
</style>
