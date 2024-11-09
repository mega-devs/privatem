<template>
    <div>
      <NavBarComponent stateProp="SMTPsDB"/>
      <div class="container-fluid dummy-form">
        <div class="row">
          <div class="col-lg-12" style="border: 2px solid #fff;">
            <p class="text-info">SMTPs</p>
            <DataTable :data="materials" :columns="columns" class="table table-striped">
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
      materials: [
        { id: 1, server: 'server1', email: 'Doe@email.com', pass: 'Doe', port: '3333', status:'VALID' },
        { id: 2, server: 'server2', email: 'Doe@email.com', pass: 'Doe', port: '3333', status:'VALID'  },
        { id: 3, server: 'server3', email: 'Doe@email.com', pass: 'Doe', port: '3333', status:'VALID'  },
      ],
      columns: [
        { title: 'ID', data: 'id' },
        { title: 'SERVER', data: 'server' },
        { title: 'Port', data: 'port' },
        { title: 'Email', data: 'email' },
        { title: 'Pass', data: 'pass' },
        { title: 'Status', data: 'status', render: (data, type, row) => {
            return `
              <a href="" class="btn btn-info">${data}</a>
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
