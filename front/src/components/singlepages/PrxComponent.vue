<template>
    <NavBarComponent stateProp="SinglePRX"/>
    <div class="container-fluid dummy-form">
        <div>
            <div class="row">
                <h2 class="text-center">Proxy Details</h2>
                <div class="col-lg-12">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>IP</th>
                                <th>User</th>
                                <th>Pass</th>
                                <th>Port</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="proxy">
                                <td>{{ proxy.ip }}</td>
                                <td>{{ proxy.user }}</td>
                                <td>{{ proxy.pass }}</td>
                                <td>{{ proxy.port }}</td>
                                <td><button @click="checkProxy(proxy)" class="btn btn-primary">Check</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import NavBarComponent from '../components/NavBarComponent.vue';

export default {
    components: {
        NavBarComponent,
    },
    data() {
        return {
            proxy: {
                ip: '192.168.1.1',
                user: 'username',
                pass: 'password',
                port: 8080
            }
        };
    },
    methods: {
        checkProxy(proxy) {
            console.log('Checking proxy:', proxy);
            // Implement the actual proxy check logic here
        }
    },
    mounted() {
        // Fetch the proxy data when needed
    }
}
</script>

<style scoped>
.dummy-form {
    overflow: auto;
    margin-top: 2em;
    width: auto;
}
.table {
    margin-top: 1em;
}
</style>
