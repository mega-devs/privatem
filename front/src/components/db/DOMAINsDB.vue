<template>
    <div>
      <NavBarComponent stateProp="DOMAINsDB"/>
      < />
      <div class="container-fluid dummy-form">
        <div class="row" style="margin-top:30px;">
          <div class="col-lg-12" style="border: 2px solid #fff;">
            <p class="text-info">Domains</p>
            <DataTable :data="domainsdata" :columns="domainscolumns" class="table table-striped">
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
      domainsdata: [
        { id: 1, domain: 'sock1', name: 'Doe', status: 'Active', action: 'Check' },
        { id: 2, domain: 'sock2', name: 'Doe', status: 'Inactive', action: 'Check' },
      ],
      domainscolumns: [
        { title: 'ID', data: 'id' },
        { title: 'DOMAIN', data: 'domain' },
        { title: 'NAME', data: 'name' },
        { title: 'STATUS', data: 'status', render: (data, type, row) => {
            return `
              <a href="" class="btn btn-primary">${data}</a>
            `;
          }
        },
        { title: 'ACTION', data: 'action', render: (data, type, row) => {
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
