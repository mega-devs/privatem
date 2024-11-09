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
                                <td><button @click.prevent="del($event, item[0])" type="button" class="btn btn-danger"><i class="bi bi-dash"></i></button></td>
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
</template>
 
<script>
import axios from 'axios';

export default {
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
        del(event, id) {
            let token = ''
            let cookies = document.cookie.split(";")
            cookies.forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split("=")[1];
                }
            })
            axios.post(`${this.$store.state.back_url}/api/del/material/id`, {token: token, id: id}).then(res => {
                let toDel
                for (let i = 0; i < this.data.length; i++) {
                    if (this.data[i][0] == id) {
                        toDel = this.data[i]
                    }
                }
                this.data = this.data.filter(item => item !== toDel);
            })
        }
    }
}
</script>
<style scoped>
</style>

