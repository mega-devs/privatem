<template>
    <div>
      <NavBarComponent stateProp="database"/>
      <div class="container-fluid dummy-form">
        <div class="row">
          <div class="col-lg-6" style="border: 2px solid #fff;">
            <p class="text-info">Socks/Proxies</p>
            <DataTable :data="materials1" :columns="columns1" class="table table-striped">
            </DataTable>
          </div>
          <div class="col-lg-6" style="border: 2px solid #fff;">
            <p class="text-info">SMTPs</p>
            <DataTable :data="materials" :columns="columns" class="table table-striped">
            </DataTable>
          </div>
        </div>
        <div class="row" style="margin-top:30px;">
          <div class="col-lg-6" style="border: 2px solid #fff;">
            <p class="text-info">IMAPs</p>
            <DataTable :data="imapsdata" :columns="imapscolumns" class="table table-striped">
            </DataTable>
          </div>
          <div class="col-lg-6" style="border: 2px solid #fff;">
            <p class="text-info">Domains</p>
            <DataTable :data="domainsdata" :columns="domainscolumns" class="table table-striped">
            </DataTable>
          </div>
        </div>
        <div class="row" style="margin-top:30px;">
          <div class="col-lg-6" style="border: 2px solid #fff;">
            <p class="text-info">Templates</p>
            <DataTable :data="templatesdata" :columns="templatescolumns" class="table table-striped">
            </DataTable>
          </div>
          <div class="col-lg-6" style="border: 2px solid #fff;">
            <p class="text-info">Bases</p>
            <DataTable :data="basesdata" :columns="basescolumns" class="table table-striped">
            </DataTable>
          </div>
        </div>
      </div>
      <hr>
      <ModalViewComponent ref="modal"></ModalViewComponent>
    </div>
  </template>
<script>
import axios from 'axios';
import NavBarComponent from './components/NavBarComponent.vue';
import ModalViewComponent from './components/ModalViewComponent.vue';
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
  margin-top: 1em;
  width: auto;
}
</style>
