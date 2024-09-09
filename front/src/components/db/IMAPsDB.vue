<template>
    <div>
      <NavBarComponent stateProp="IMAPsDB"/>
      <div class="container-fluid dummy-form">
        <div class="row" style="margin-top:30px;">
          <div class="col-lg-12" style="border: 2px solid #fff;">
            <p class="text-info">IMAPs</p>
            <DataTable :data="imapsdata" :columns="imapscolumns" class="table table-striped">
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
      imapsdata: [
        { id: 1, socks: 'sock1', user: 'Doe', pass: 'Doe', port: '3333', status:'VALID'  },
        { id: 2, socks: 'sock2', user: 'Doe', pass: 'Doe', port: '3333', status:'VALID'  },
      ],
      imapscolumns: [
        { title: 'ID', data: 'id' },
        { title: 'SERVER', data: 'socks' },
        { title: 'PORT', data: 'port' },
        { title: 'MAIL', data: 'user' },
        { title: 'PASS', data: 'pass' },
        { title: 'Status', data: 'status', render: (data, type, row) => {
            return `
              <a href="" class="btn btn-danger">${data}</a>
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
