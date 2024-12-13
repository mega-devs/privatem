<template>
  <NavBarComponent stateProp="sendx"/>
  <div id="main-part">
    <HorizontalNavBar state-prop="sendx"/>
    <div class="container-fluid dummy-form">
      <div>
        <h3 style="text-align: center;">Select material to sendX</h3>
        <hr>
        <div class="row">
          <div class="col-lg-12">
            <p>Debug</p>
            <div id="console-output" ref="consoleOutput1">
              <template v-for="item in mailing_logs" :key="item.timestamp">
                <span :class="item.level.toLowerCase()"><span :style="{ color: 'orange' }">{{
                    formatTime(item.timestamp)
                  }}</span> | {{ item.message }}<br/></span>
              </template>
            </div>
          </div>
        </div>
        <div>
          <h3>Console</h3>
          <div id="console-output" ref="consoleOutput2">
            <template v-for="item in logs">
              <span :class="item['status']"><span :style="{ color: 'orange' }">{{
                  formatTime(item['created_at'])
                }}</span> | {{ item['TEXT'] }}<br/></span>
            </template>
          </div>
          <button @click="deleteLog()" class="btn btn-primary btn-delete">Delete</button>
        </div>
        <div class="row">
          <div class="col-lg-6">
            <h4 class="text-center">Bases List</h4>
            <DataTable :data="basesData" :columns="basesColumns" class="table table-striped"
                       @click="handleClick"></DataTable>
          </div>
          <div class="col-lg-6">
            <h4 class="text-center">Selected SMTP</h4>
            <DataTable :data="smtpsData" :columns="smtpsColumns" class="table table-striped" @click="handleClick">
            </DataTable>
          </div>
          <div class="col-lg-6" style="margin-top: 2em;">
            <h4 class="text-center">Selected Proxy</h4>
            <DataTable :data="selectedProxies" :columns="proxiesColumns" class="table table-striped">
            </DataTable>
          </div>
          <div class="col-lg-6" style="margin-top: 2em;">
            <h4 class="text-center">Selected Domains</h4>
            <DataTable :data="domainsData" :columns="domainsColumns" class="table table-striped" @click="handleClick">
            </DataTable>
          </div>

        </div>
        <hr>
        <div class="row">
          <div class="col-lg-4">
            <h4 class="text-center">Selected Template</h4>
            <DataTable :data="templatesdata" :columns="templatescolumns" class="table table-striped"
                       @click="handleClick">
            </DataTable>
          </div>
        </div>
        <hr>
        <div class="row">
          <div class="col-lg-12">
            <h4>Options</h4>
            <p>Leave the fields empty if you set the default settings</p>
            <div class="row">
              <div class="col-lg-6">
                <input v-model="threads_form" type="text" class="form-control" aria-label="Small" placeholder="Threads">
                <input v-model="delay_form" type="text" class="form-control" aria-label="Small" placeholder="Delay">
              </div>
              <div class="col-lg-6">
                <input v-model="smtp_timeout_form" type="text" class="form-control" aria-label="Small"
                       placeholder="Smtp timeout">
                <input v-model="proxy_timeout_form" type="text" class="form-control" aria-label="Small"
                       placeholder="Proxy timeout">
              </div>
            </div>
          </div>
        </div>
        <div v-if="can_run">
          <button style="margin-top: 1em;" type="button" @click.prevent="submit" class="btn btn-primary">Submit</button>
          <p class="text-danger">{{ errorCheck }}</p>
        </div>
        <div v-else>
          <p>Please wait!</p>
        </div>

      </div>

      <div>
        <h3>Progress</h3>
        <div class="progress">
          <div class="progress-bar" role="progressbar" :style=" 'background-color: #ef4444;'+'width: '+log_progress+'%'"
               aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
        <div class="row">
          <div class="col-lg-6">
            <p class="text-success bordered">Sended emails: {{ log_valid }}</p>
            <p class="text-danger bordered">Errors: {{ log_error }}</p>
          </div>
          <div class="col-lg-6">
            <button style="margin-top: 1em;" type="button" class="btn btn-primary">Stop</button>
          </div>
        </div>
      </div>
    </div>
    <ModalViewComponent ref="modal"></ModalViewComponent>
  </div>
</template>

<script>
import axios from 'axios';
import NavBarComponent from './components/NavBarComponent.vue';
import ModalViewComponent from './components/ModalViewComponent.vue';
import HorizontalNavBar from "./components/HorizontalNavBar.vue";
import DataTable from 'datatables.net-vue3';
import {io} from "socket.io-client";

export default {
  components: {
    NavBarComponent,
    ModalViewComponent,
    HorizontalNavBar,
    DataTable
  },
  data() {
    return {
      name: null,
      materials: null,
      file: null,
      errorSub: null,
      check_file: null,
      proxy_form: null,
      sendX_count: '',
      sendX_to: '',
      threads_form: '',
      delay_form: '',
      smtp_timeout_form: '',
      proxy_timeout_form: '',
      can_run: true,
      log_progress: 0,
      log_valid: 0,
      log_error: 0,
      logs: [],
      mailing_logs: [],
      smtpsData: [],
      proxiesData: [],
      domainsData: [],
      templatesdata: [],
      errorCheck: null,
      dummyHtmlMessage: '',
      selectedImaps: [],
      selectedSmtps: [],
      selectedSmtp: {},
      selectedProxy: {},
      selectedProxies: [],
      selectedDomains: [],
      basesData: [],
      smtpsColumns: [
        {
          title: 'Select',
          data: 'id',
          render: (data, type, row) => {
            return `<input type="checkbox" class="smtp-checkbox" data-id="${data}" data-server="${row.server}" ${this.selectedSmtps.some(item => item.id === data) ? 'checked' : ''}>`;
          }

        },
        {title: 'ID', data: 'id'},
        {title: 'Server', data: 'server'},
        {title: 'STATUS', data: 'status', render: (data) => `<a href="#" class="btn btn-warning">${data}</a>`},
      ],
      proxiesColumns: [
        {
          title: 'Select',
          data: 'id',
          render: (data, type, row) => {
            return `<input type="checkbox" class="proxies-checkbox" data-id="${data}" data-ip="${row.ip}" ${this.selectedProxies.some(item => item.id === data) ? 'checked' : ''}>`;
          }

        },
        {title: 'ID', data: 'id'},
        {title: 'IP', data: 'ip'},
        {
          title: 'STATUS', data: 'status', render: (data) => {
            return `<a href="#" class="btn btn-warning">${data}</a>`;
          }
        },
      ],
      domainsColumns: [
        {
          title: 'Select',
          data: 'id',
          render: (data, type, row) => {
            return `<input type="checkbox" class="domain-checkbox" data-id="${data}" data-url="${row.domain}" ${this.selectedDomains.some(item => item.id === data) ? 'checked' : ''}>`;
          }

        },
        {title: 'ID', data: 'id'},
        {title: 'Domain', data: 'domain'},
        {
          title: 'STATUS', data: 'status', render: (data) => {
            return `<a href="#" class="btn btn-warning">${data}</a>`;
          }
        },
      ],
      templatescolumns: [
        {title: 'NAME', data: 'name'},
      ],
      basesColumns: [
        {title: 'ID', data: 'id'},
        {title: 'Base Name', data: 'basename'},
        {
          title: 'Status', data: 'status', render: (data) => {
            return `<a href="#" class="btn btn-warning">${data}</a>`;
          }
        },
      ],

      imapDropdownOpen: false,
      proxyDropdownOpen: false,
      allowedStatuses: ['all', 'inbox', 'junk', 'dead', 'none', 'checked']
    }
  },
  watch: {
    logs() {
      this.scrollToBottom();
    }
  },
  methods: {
    isEmpty(obj) {
      return Object.keys(obj).length === 0;
    },
    saveSelectionSMTP() {
      localStorage.setItem('selectedSmtps', JSON.stringify(this.selectedSmtps));
    },
    loadSelectionSMTP() {
      this.selectedSmtps = JSON.parse(localStorage.getItem('selectedSmtps') || '[]');
    },
    saveSelectionProxy() {
      localStorage.setItem('selectedProxies', JSON.stringify(this.selectedProxies));
    },
    loadSelectionProxy() {
      this.selectedProxies = JSON.parse(localStorage.getItem('selectedProxies') || '[]');
    },
    saveSelectionDomain() {
      localStorage.setItem('selectedDomains', JSON.stringify(this.selectedDomains));
    },
    loadSelectionDomain() {
      this.selectedDomains = JSON.parse(localStorage.getItem('selectedDomains') || '[]');
    },
    getTemplates() {
      const currentSessionName = this.getCurrentSessionName();
      if (!currentSessionName) {
        this.errorSubTemplates = 'No session loaded';
        return;
      }

      axios.get(`${import.meta.env.VITE_BACK_URL}/api/get/list/templates/${currentSessionName}`)
          .then(res => {
            this.templatesdata = res.data.map(item => ({
              id: item.id,
              name: item.name
            }));
          })
          .catch(error => {
            console.error('Error fetching templates:', error);
          });
    },
    getMaterialsSMTP() {
      const currentSessionName = this.getCurrentSessionName();
      if (!currentSessionName) {
        this.errorSubTemplates = 'No session loaded';
        return;
      }
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/get/list/proxies/${currentSessionName}`).then(res => {
        this.proxies = res.data;
      });
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/get/list/smtps/${currentSessionName}`).then(res => {
        this.smtpsData = res.data.map(item => ({
          id: item.id,
          server: item.server,
          status: item.status
        }));
      }).catch(error => {
        console.error('Error fetching templates:', error);
      });
    },
    getMaterialsProxy() {
      const currentSessionName = this.getCurrentSessionName();
      if (!currentSessionName) {
        this.errorSubTemplates = 'No session loaded';
        return;
      }
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/get/list/proxies/${currentSessionName}`)
          .then(res => {
            this.proxiesData = res.data.map(item => ({
              id: item.id,
              ip: item.ip,
              port: item.port,
              status: item.status
            }));
          })
          .catch(error => {
            console.error('Error fetching templates:', error);
          });
    },
    getMaterialsDomain() {
      const currentSessionName = this.getCurrentSessionName();
      if (!currentSessionName) {
        this.errorSub = 'No session loaded';
        return;
      }
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/get/list/domains/${currentSessionName}`)
          .then(res => {
            this.domainsData = res.data.map(item => ({
              id: item.id,
              domain: item.url,
              status: item.status
            }));
          })
          .catch(error => {
            console.error('Error fetching domains:', error);
          });
    },
    getBases() {
      const currentSessionName = this.getCurrentSessionName();
      if (!currentSessionName) {
        this.errorSubTemplates = 'No session loaded';
        return;
      }
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/get/list/bases/${currentSessionName}`)
          .then(res => {
            this.basesData = res.data.map(item => ({
              id: item.id,
              basename: item.name,
              status: item.status,
            }));
          })
          .catch(error => {
            console.error('Error fetching materials:', error);
          });
    },
    toggleSelectionSMTP(id, server) {
      const index = this.selectedSmtps.findIndex(item => item.id === id);
      if (index !== -1) {
        this.selectedSmtps.splice(index, 1);
      } else {
        this.selectedSmtps.push({id, server});
      }
      console.log(this.selectedSmtps);
    },
    toggleSelectionProxy(id, ip) {
      const index = this.selectedProxies.findIndex(item => item.id === id);
      if (index !== -1) {
        // Если элемент найден, удаляем его из массива
        this.selectedProxies.splice(index, 1);
      } else {
        // Если элемент не найден, добавляем новый объект
        this.selectedProxies.push({id, ip});
      }
      console.log(this.selectedProxies);
    },
    toggleSelectionDomain(id, url) {
      const index = this.selectedDomains.findIndex(item => item.id === id);
      if (index !== -1) {
        this.selectedDomains.splice(index, 1);
      } else {
        this.selectedDomains.push({id, url});
      }
      console.log(this.selectedDomains);
    },
    getCurrentSessionName() {
      const name = document.cookie.split('; ').find(row => row.startsWith('currentSessionName='));
      return name ? name.split('=')[1] : null;
    },
    fetchLogs() {
      const currentSessionName = this.getCurrentSessionName();
      const logType = 'sendx';
      if (!currentSessionName) {
        return;
      }

      axios.get(`${import.meta.env.VITE_BACK_URL}/api/logs/${logType}/${currentSessionName}`)
          .then(res => {
            console.log(res.data);
            this.logs = res.data.data;
          })
          .catch(error => {
            console.error('Error fetching logs:', error);
          });
    },
    handleClick(event) {
      const action = event.target.getAttribute('data-action');
      const id = event.target.getAttribute('data-id');

      if (action === 'view') {
        this.view(id);
      } else if (action === 'delete') {
        this.del(id);
      } else if (action === 'checkIMAP') {
        this.checkIMAP(id);
      }
    },
    submit() {
      const selectedDomainIds = this.selectedDomains.map(domain => domain.id);
      const selectedProxyIds = this.selectedProxies.map(proxy => proxy.id);
      const selectedSmtpIds = this.selectedSmtps.map(smtp => smtp.id);

      console.log('selectedSmtps file:', selectedSmtpIds);
      console.log('selectedProxies file:', selectedProxyIds);
      console.log('selectedDomains file:', selectedDomainIds);


      this.logs = []
      let token = ''
      let cookies = document.cookie.split(";");
      cookies.forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split("=")[1];
        }
      });

      this.errorCheck = null
      if (this.threads_form && this.smtp_timeout_form && this.proxy_timeout_form && this.delay_form) {
        this.can_run = false
        axios.post(`${import.meta.env.VITE_BACK_URL}/api/start/sendx`, {
          token: token,
          bases: this.basesData,
          smtps: selectedSmtpIds,
          proxies: selectedProxyIds,
          domains: selectedDomainIds,
          templates: this.templatesdata,
          threads_form: this.threads_form,
          smtp_timeout_form: this.smtp_timeout_form,
          proxy_timeout_form: this.proxy_timeout_form,
          delay_form: this.delay_form
        }).then(res => {
          this.getMaterials();
          this.$refs.inputEl1.value = '';
          this.smtpTextInput = '';
          if (res.data.data == 'error') {
            this.can_run = true
            this.errorCheck = res.data.error
          }
        })
      } else {
        this.errorCheck = 'Fill in the fields!'
      }
    },
    del(id) {
      let token = '';
      document.cookie.split(';').forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split('=')[1];
        }
      });
      axios.post(`${import.meta.env.VITE_BACK_URL}/api/del/material`, {token: token, id: id, type: 'smtps'})
          .then(res => {
            if (res.data.data === 'success') {
              this.getMaterialsSMTP();
            } else {
              console.error('Error deleting material:', res.data.error);
            }
          })
          .catch(error => {
            console.error('Error deleting material:', error);
          });
    },
    view(id) {
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/get/materials/${id}`).then(res => {
        let modalData = [];
        res.data.forEach(el => {
          delete el[1];
          modalData.push(el);
        });
        this.$refs.modal.data = res.data;
        this.$refs.modal.show = true;
      });
    },

    toggleImapDropdown() {
      this.imapDropdownOpen = !this.imapDropdownOpen;
      this.proxyDropdownOpen = false;
    },
    toggleProxyDropdown() {
      this.proxyDropdownOpen = !this.proxyDropdownOpen;
      this.imapDropdownOpen = false;
    },
    selectSmtp(item) {
      this.selectedSmtp = item;
      this.check_file = item;
      this.dropdownOpen = false;
    },
    selectProxy(item) {
      this.selectedProxy = item;
      this.proxy_form = item.id;
      this.proxyDropdownOpen = false;
    },
    handleClickOutside(event) {
      if (!this.$refs.smtpDropdown.contains(event.target)) {
        this.dropdownOpen = false;
      }
      if (!this.$refs.proxyDropdown.contains(event.target)) {
        this.proxyDropdownOpen = false;
      }
    },
    saveLog(logText, status) {
      const currentSessionName = this.getCurrentSessionName();
      if (!currentSessionName) {
        return;
      }

      let token = '';
      let cookies = document.cookie.split(";");
      cookies.forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split("=")[1];
        }
      });

      axios.post(`${import.meta.env.VITE_BACK_URL}/api/input/log/sendx/${currentSessionName}`, {
        token: token,
        logtext: logText,
        status: status,
      }).then(res => {
        if (res.data.data !== 'success') {
          console.error('Error saving log:', res.data.error);
        }
      }).catch(error => {
        console.error('Error saving log:', error.message);
      });
    },
    deleteLog() {
      const currentSessionName = this.getCurrentSessionName();
      const logType = 'sendx';
      if (!currentSessionName) {
        return;
      }

      axios.delete(`${import.meta.env.VITE_BACK_URL}/api/logs/${logType}/${currentSessionName}`)
          .then(response => {
            if (response.data && response.data.status === 'success') {
              this.logs = [];
            }
          })
          .catch(error => {
            console.error('Failed to delete logs:', error);
          });
    },
    scrollToBottom() {
      setTimeout(() => {
        const consoleOutput1 = this.$refs.consoleOutput1;
        const consoleOutput2 = this.$refs.consoleOutput2;
        if (consoleOutput1) {
          consoleOutput1.scrollTop = consoleOutput1.scrollHeight;
        }
        if (consoleOutput2) {
          consoleOutput2.scrollTop = consoleOutput2.scrollHeight;
        }
      }, 50); // Adjust delay if needed
    },
    formatTime(timestamp) {
      // Split the timestamp to get the time part
      const timePart = timestamp.split(' ')[1]; // Get the part after the date
      const [time] = timePart.split(','); // Remove milliseconds if present
      return time; // Return only hh:mm:ss
    },
    fetchDebugs() {
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/debug`)
          .then(response => {
            this.mailing_logs = response.data.logs;
          })
          .catch(error => {
            console.error('Error fetching logs:', error);
          });
    },
  },
  mounted() {
    this.loadSelectionSMTP();
    this.loadSelectionProxy();
    this.loadSelectionDomain();
    this.getMaterialsSMTP();
    this.getMaterialsProxy();
    this.getMaterialsDomain();
    this.getTemplates();
    this.fetchLogs();
    this.getBases();
    this.fetchDebugs();
    this.scrollToBottom();
    document.querySelector('.table').addEventListener('change', (event) => {
      if (event.target.classList.contains('smtp-checkbox')) {
        const id = parseInt(event.target.getAttribute('data-id'));
        const server = event.target.dataset.server;
        this.toggleSelectionSMTP(id, server);
        this.saveSelectionSMTP();
      }
    });
    this.scrollToBottom();

  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
  },
  created() {
    this.connection = io.connect(import.meta.env.VITE_BACK_URL);
    this.connection.on('message', (data) => {
      data = data.split(":");
      if (data[0] == 'progress_sendx_send') {
        this.log_valid = data[1];
        this.log_error = data[2];
        this.log_progress = data[3];
        if (data[3] == '100') {
          this.can_run = true;
          setTimeout(() => {
            this.getMaterials();
          }, 1000);
        } else {
          this.can_run = false;
        }
      } else if (data[0] == 'logs_send') {
        this.saveLog(data[2], data[1]);
        this.fetchLogs();
      }
    });
  }
}
</script>

<style scoped>

#main-part {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.dummy-form {
  overflow: auto;
  margin-top: 9em;
  width: auto;
}

.custom-select {
  position: relative;
  font-family: Arial;
}

.select-selected {
  background-color: #2a2e35;
  color: #fff;
  padding: 8px 16px;
  border: 1px solid #444;
  cursor: pointer;
  border-radius: 4px;
}

.select-selected:hover {
  background-color: #3b4048;
}

.select-items {
  position: absolute;
  background-color: #2a2e35;
  border: 1px solid #444;
  z-index: 99;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  border-radius: 4px;
}

.select-items div {
  color: #fff;
  padding: 8px 16px;
  cursor: pointer;
}

.select-items div:hover {
  background-color: #3b4048;
}

.select-selected::after {
  content: "";
  position: absolute;
  top: 14px;
  right: 10px;
  border: 6px solid transparent;
  border-color: #ccc transparent transparent transparent;
}

.select-selected.select-arrow-active::after {
  border-color: transparent transparent #ccc transparent;
  top: 7px;
}


#console-output::-webkit-scrollbar {
  width: 12px;
}

#console-output::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 0 10px 10px 10px;
}

#console-output::-webkit-scrollbar-track {
  background-color: #495057;
  border-radius: 0px 8px 8px 0px;
}

#console-output::-webkit-scrollbar {
  width: 12px;
}

#console-output::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 0 10px 10px 10px;
}

#console-output::-webkit-scrollbar-track {
  background-color: #495057;
  border-radius: 0px 8px 8px 0px;
}

#console-output {
  border-radius: 10px;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 200px;
  background-color: #000;
  color: #fff;
  overflow: auto;
  z-index: 9999;
  padding-left: 1em;
  padding-right: 1em;
  padding-top: 5px;
}

.console-line {
  padding: 5px;
  margin: 0;
  line-height: 1.5rem;
}

.console-error {
  color: #f00;
}

.console-warn {
  color: #ffa500;
}

.console-info {
  color: #00f;
}

.console-debug {
  color: #00ff00;
}

.col-lg-6, .col-lg-12 {
  margin-top: 2px;
}

/deep/ .dt-paging-button {
  border: 1px solid white;
  background-color: transparent;
  margin: 1%;
  border-radius: 7px;
  transition: background-color 0.2s linear;
}

/deep/ .dt-paging-button:hover {
  background-color: red;
  color: white;
}

/deep/ label {
  padding: 1em 1em 1em 0;
}

/deep/ .dt-input {
  margin-right: 1em;
}

/deep/ .dt-info {
  padding: 1em 1em 1em 0;
  margin-bottom: 1%;
}

label {
  color: white;
}

/deep/ .btn-primary {
  background-color: var(--primary) !important;
  border: none;
  transition: background-color 0.2s linear;
}

.btn:hover {
  background-color: #cc0000;
}

.text-success {
  color: limegreen !important;
}

.text-danger {
  color: red !important;
}

.btn-delete {
  margin-top: 1em;
  margin-bottom: 1em;
}

.bordered {
  border: 1px solid grey; /* Change color as needed */
  padding: 10px;
  margin: 10px 0 10px 0;
  background-color: #2c2c2c;
}

.form-control {
  margin: 5px 0 5px 0;
}
</style>