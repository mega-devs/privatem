<template>
    <div>
      <NavBarComponent stateProp="TemplatesDB"/>
      <div class="container-fluid dummy-form">
        <div class="row" style="margin-top:30px;">
          <div class="col-lg-12" style="border: 2px solid #fff;">
            <p class="text-info">Templates</p>
            <DataTable :data="templatesdata" :columns="templatescolumns" class="table table-striped">
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
      templatesdata: [
        { id: 1, template: 'temp1', name: 'Doe', status: 'Doe', action: 'Activate' },
        { id: 2, template: 'temp2', name: 'Doe', status: 'Doe', action: 'Deactivate' },
      ],
      templatescolumns: [
        { title: 'ID', data: 'id' },
        { title: 'TEMPLATE', data: 'template' },
        { title: 'NAME', data: 'name' },
        { title: 'Status', data: 'status', render: (data, type, row) => {
            return `
              <a href="" class="btn btn-warning">${data}</a>
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
