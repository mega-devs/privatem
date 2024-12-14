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
                                <th v-for="item in columns" scope="col">{{ item }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in data">
                                <td v-for="info in item">{{info}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>
 
<script>
import axios from 'axios';

export default {
    data: function () {
        return {
            show: false,
            data: null,
            columns: null,
        }
    },
    methods: {
        closeModal: function () {
            this.show = false
        }
    }
}
</script>
<style scoped>
</style>

