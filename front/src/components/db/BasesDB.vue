<template>
    <div>
      <NavBarComponent stateProp="BasesDB"/>
      <div class="container-fluid dummy-form">
        <div class="row" style="margin-top:30px;">
          <div class="col-lg-12" style="border: 2px solid #fff;">
            <p class="text-info">Bases</p>
            <DataTable :data="basesdata" :columns="basescolumns" class="table table-striped">
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
      basesdata: [
        { id: 1, email: 'temp1', firstname: 'Doe', lastname: 'Doe' },
        { id: 2, email: 'temp2', firstname: 'Doe', lastname: 'Doe' },
      ],
      basescolumns: [
        { title: 'ID', data: 'id' },
        { title: 'FIRSTNAME', data: 'firstname' },
        { title: 'LASTNAME', data: 'lastname' },
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
