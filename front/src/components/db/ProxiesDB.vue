<template>
    <div>
      <NavBarComponent stateProp="ProxiesDB"/>
      <div class="container-fluid dummy-form">
        <div class="row">
          <div class="col-lg-12" style="border: 2px solid #fff;">
            <p class="text-info">Socks/Proxies</p>
            <DataTable :data="materials1" :columns="columns1" class="table table-striped">
            </DataTable>
          </div>
        </div>
      </div>
      <ModalViewComponent ref="modal"></ModalViewComponent>
    </div>
  </template>
<script>
import axios from 'axios';
import NavBarComponent from '../components/NavBarComponent.vue';
import ModalViewComponent from '../components/ModalViewComponent.vue';
import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net';
DataTable.use(DataTablesCore);
export default {
  components: {
    NavBarComponent,
    ModalViewComponent,
    DataTable
  },
  data() {
    return {
      name: '',
      errorSub: '',
      file: null,
      materials1: [
        { id: 1, socks: 'sock1', user: 'Doe', pass: 'Doe', port: '3333', status:'VALID'  },
        { id: 2, socks: 'sock2', user: 'Doe', pass: 'Doe', port: '3333', status:'VALID'  },
        { id: 3, socks: 'sock3', user: 'Doe', pass: 'Doe', port: '3333', status:'VALID'  },
      ],
      columns1: [
        { title: 'ID', data: 'id' },
        { title: 'Socks', data: 'socks' },
        { title: 'Port', data: 'port' },
        { title: 'User', data: 'user' },
        { title: 'Pass', data: 'pass' },
        { title: 'Status', data: 'status', render: (data, type, row) => {
            return `
              <a href="" class="btn btn-primary">${data}</a>
            `;
          }
        }
      ],
    };
  },
  methods: {
  },
  mounted() {
  }
}
</script>

<style scoped>
.dummy-form {
  margin-left: 20em;
  margin-right: 10em;
  margin-top: 2em;
  width: auto;
}
</style>
