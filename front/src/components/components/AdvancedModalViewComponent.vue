<template>
    <div v-if="show">
        <div class="modal fade show" id="myModal" style="display: block !important;">
            <div class="modal-dialog" style="max-width: 60%;">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">View</h5>
                    <button style="margin-left: 80%;" @click="closeModal" class="btn btn-danger">Close</button>
                </div>
                <div class="modal-body">
                    <div class="row table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th v-for="item in data" scope="col"></th>
                                <th scope="col"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in data">
                                <td v-for="info in item">{{info}}</td>
                                <td><button @click.prevent="view(item[0])" type="button" class="btn btn-success"><i class="bi bi-binoculars"></i></button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                </div>
                <div class="modal-footer">
                    <button type="button" @click="closeModal" class="btn btn-primary">Close</button>
                </div>
                </div>
            </div>
        </div>
    </div>
    <ModalViewComponent ref="modal"></ModalViewComponent>
</template>
 
<script>
import axios from 'axios';
import ModalViewComponent from './ModalViewComponent.vue';

export default {
    components: {
        ModalViewComponent
    },
    data: function () {
        return {
            show: false,
            data: null,
        }
    },
    methods: {
        closeModal: function () {
            this.show = false
        },
        view(id) {
            this.closeModal()
            // axios.get(`${this.$store.state.back_url}/api/get/materials/${id}`).then(res => {
            //     let modalData = []
            //     res.data.forEach(el => {
            //         delete el[1]
            //         modalData.push(el)
            //     })
            //     console.log(res.data)
            //     this.$refs.modal.data = res.data
            //     this.$refs.modal.show = true                
            // })
        }
    }
}
</script>
<style scoped>
</style>

