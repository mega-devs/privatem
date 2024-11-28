<template>
  <NavBarComponent :state-prop="($route.query.mode === 'special' ? 'specialmailing' : 'normalmailing')" />
  <div id="main-part">
      <HorizontalNavBar :state-prop="($route.query.mode === 'special' ? 'specialmailing' : 'normalmailing')" />
      <div class="container-fluid dummy-form">
      <div>
        <h3>Console</h3>
        <div id="console-output" ref="consoleOutput2">
          <template v-for="item in logs">
            <span :class="item['status']"><span :style="{ color: 'orange' }">{{ formatTime(item['created_at']) }}</span> | {{ item['TEXT'] }}<br/></span>
          </template>
        </div>
        <button @click="deleteLog()" class="btn btn-primary btn-delete">Delete</button>
        <div class="col-lg-12">
          <p>Debug</p>
          <div id="console-output" ref="consoleOutput1">
            <template v-for="item in mailing_logs" :key="item.timestamp">
              <span :class="item.level.toLowerCase()"><span :style="{ color: 'orange' }">{{ formatTime(item.timestamp) }}</span> | {{item.message }}<br/></span>
            </template>
          </div>
        </div>
      </div>
      <div v-if="$route.query.mode === 'normal'">
        <div>
          <h3 style="text-align: center; margin-top: 1em;">Select material</h3>
          <div class="row">
            <div class="col-lg-6">
              <div>
                <p style="margin-top: 1em;">Templates</p>
                <select v-model="dummy_form" class="form-select">
                  <option v-for="item in allowedStatuses" :key="item['id']">{{ item }}</option>
                </select>
              </div>
              <div>
                <p class="for-input">Bases</p>
                <div class="custom-select" ref="basesDropdown">
                  <div class="select-selected" @click="toggleBasesDropdown">
                    {{ isEmpty(selectedBase) ? 'Select Base' : selectedBase }}
                  </div>
                  <div v-if="baseDropdownOpen" class="select-items">
                    <div v-for="item in allowedStatuses" :key="item.id" @click="selectBase(item)">{{ item }}</div>
                  </div>
                </div>
              </div>
              <div>
                <p class="for-input">IMAP</p>
                <div class="custom-select" ref="imapDropdown">
                  <div class="select-selected" @click="toggleImapDropdown">
                    {{ isEmpty(selectedImap) ? 'Select IMAP' : selectedImap }}
                  </div>
                  <div v-if="imapDropdownOpen" class="select-items">
                    <div v-for="item in allowedStatuses" :key="item.id" @click="selectImap(item)">{{ item }}</div>
                  </div>
                </div>
              </div>
              <div>
                <p class="for-input">Proxy</p>
                <div class="custom-select" ref="proxyDropdown">
                  <div class="select-selected" @click="toggleProxyDropdown">
                    {{ isEmpty(selectedProxy) ? 'Select Proxy' : selectedProxy }}
                  </div>
                  <div v-if="proxyDropdownOpen" class="select-items">
                    <div v-for="item in allowedStatuses" :key="item.id" @click="selectProxy(item)">{{ item }}</div>
                  </div>
                </div>
              </div>
              <div>
                <p class="for-input">Smtps</p>
                <div class="custom-select" ref="smtpDropdown">
                  <div class="select-selected" @click="toggleSmtpDropdown">
                    {{ isEmpty(selectedSmtp) ? 'Select SMTP' : selectedSmtp }}
                  </div>
                  <div v-if="smtpDropdownOpen" class="select-items">
                    <div v-for="item in allowedStatuses" :key="item.id" @click="selectSmtp(item)">{{ item }}</div>
                  </div>
                </div>
              </div>
              <div>
                <p class="for-input">Domains</p>
                <div class="custom-select" ref="domainDropdown">
                  <div class="select-selected" @click="toggleDomainDropdown">
                    {{ isEmpty(selectedDomain) ? 'Select Domain' : selectedDomain }}
                  </div>
                  <div v-if="domainDropdownOpen" class="select-items">
                    <div v-for="item in allowedStatuses" :key="item.id" @click="selectDomain(item)">{{ item }}</div>
                  </div>
                </div>
                <div>
                  <p>base</p>
                  <input v-model="base_form_imap" class="form-control" type="text" placeholder="Input email`s IMAP">
                </div>
              </div>

            </div>
            <div class="col-lg-6">
              <h4 style="margin-top: 1em;">Options</h4>
              <p>Leave the fields empty if you set the default settings</p>
              <select v-model="to_check" class="form-select">
                <option>proxy</option>
                <option>smtp</option>
                <option>templates</option>
                <option>domains</option>
              </select>
              <div class="row">
                <div class="col-lg-6">
                  <input v-model="delay_form" type="text" class="form-control" aria-label="Small" placeholder="Delay">
                  <input v-model="timeout_form" type="text" class="form-control" aria-label="Small" placeholder="Timeout">
                  <input v-model="sending_limit" type="text" class="form-control" aria-label="Small"
                         placeholder="Sending limit">
                </div>
                <div class="col-lg-6">
                  <input v-model="emails_per_check" type="text" class="form-control" aria-label="Small"
                         placeholder="Number of emails per check">
                  <input v-model="count_of_material" type="text" class="form-control" aria-label="Small"
                         placeholder="Count of emails to validate">
                  <input v-model="threads_number" type="text" class="form-control" aria-label="Small"
                         placeholder="Count of threads">
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
      </div>
      <div v-else>
        <h3 style="text-align: center;">Select Form</h3>
        <div class="row">
          <div class="col-lg-6">
            <h4 class="text-center">Selected Templates List</h4>
            <DataTable :data="selectedMaterials" :columns="templatesColumns" :class="tableClasses"
                       @click="handleClick"></DataTable>
          </div>
          <div class="col-lg-6">
            <h4 class="text-center">Selected Bases List</h4>
            <DataTable :data="selectedBases" :columns="basesColumns" :class="tableClasses"
                       @click="handleClick"></DataTable>
          </div>
          <div class="col-lg-6">
            <h4 class="text-center">Selected SMTP</h4>
            <DataTable :data="selectedSmtps" :columns="smtpsColumns" :class="tableClasses">
            </DataTable>
          </div>
          <div class="col-lg-6">
            <h4 class="text-center">Selected Proxy</h4>
            <DataTable :data="selectedProxies" :columns="proxiesColumns" :class="tableClasses">
            </DataTable>
          </div>
          <div class="col-lg-6">
            <h4 class="text-center">Selected Domains</h4>
            <DataTable :data="selectedDomains" :columns="domainsColumns" :class="tableClasses" @click="handleClick">
            </DataTable>
          </div>

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
            <p>{{ status }}</p>
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
import {io} from "socket.io-client";
import DataTable from 'datatables.net-vue3';


export default {
  components: {
    NavBarComponent,
    ModalViewComponent,
    HorizontalNavBar,
    DataTable
  },
  data() {
    return {
      dummy: [],
      proxies: [],
      smtps: [],
      domains: [],
      imaps: [],
      mailing_logs: [],
      can_run: true,
      to_check: '',
      dummy_form: '',
      proxies_form: '',
      smtps_form: '',
      domains_form: '',
      imaps_form: '',
      results_form: '',
      base_form_imap: '',
      timeout_form: '',
      delay_form: '',
      count_of_material: '',
      emails_per_check: '',
      threads_number: '',
      sending_limit: '',
      errorCheck: '',
      editorConfig: {},
      dummyHtmlMessage: '',
      log_valid: 0,
      log_error: 0,
      log_progress: 0,
      status: '',
      logs: [],
      isPaused: false,
      allowedStatuses: ['inbox', 'junk', 'checked'],
      allowedImapStatuses: ['checked'],
      imapsData: [],
      smtpsData: [],
      proxiesData: [],
      selectedBases: {},
      domainsData: [],
      selectedImap: {},
      selectedBase: {},
      selectedProxies: {},
      selectedSmtp: {},
      selectedDomain: {},
      selectedSmtps: [],
      selectedDomains: [],
      selectedMaterials: [],
      smtpsColumns: [
        {
          title: 'Select',
          data: 'id',
          render: (data, type, row) => {
            return `<input type="checkbox" class="smtp-checkbox" data-id="${data}" data-server="${row.server}" ${this.selectedSmtps.some(item => item.id === data) ? 'checked' : ''}>`;
          },
          className: 'data-cell'

        },
        {title: 'ID', data: 'id', className: 'data-cell'},
        {title: 'Server', data: 'server', className: 'data-cell'},
        {
          title: 'STATUS',
          data: 'status',
          render: (data) => `<a href="#" class="btn btn-${data}">${data}</a>`,
          className: 'data-cell'
        },

      ],
      proxiesColumns: [
        {
          title: 'Select',
          data: 'id',
          render: (data, type, row) => {
            return `<input type="checkbox" class="proxies-checkbox" data-id="${data}" data-ip="${row.ip}" ${this.selectedProxies.some(item => item.id === data) ? 'checked' : ''}>`;
          },
          className: 'data-cell'
        },
        {title: 'ID', data: 'id', className: 'data-cell'},
        {title: 'IP', data: 'ip', className: 'data-cell'},
        {
          title: 'STATUS', data: 'status', render: (data) => {
            return `<a href="#" class="btn btn-${data}">${data}</a>`;
          }, className: 'data-cell'
        },
      ],
      domainsColumns: [
        {
          title: 'Select',
          data: 'id',
          render: (data, type, row) => {
            return `<input type="checkbox" class="domain-checkbox" data-id="${data}" data-url="${row.domain}" ${this.selectedDomains.some(item => item.id === data) ? 'checked' : ''}>`;
          },
          className: 'data-cell'

        },
        {title: 'ID', data: 'id', className: 'data-cell'},
        {title: 'Domain', data: 'domain', className: 'data-cell'},
        {
          title: 'STATUS', data: 'status', render: (data) => {
            return `<a href="#" class="btn btn-${data}">${data}</a>`;
          }, className: 'data-cell'
        },
      ],
      templatesColumns: [
        {
          title: 'Select',
          data: 'id',
          render: (data, type, row) => {
            return `<input type="checkbox" class="templates-checkbox" data-id="${data}" data-url="${row.name}" ${this.selectedMaterials.some(item => item.id === data) ? 'checked' : ''}>`;
          },
          className: 'data-cell'
        },
        {title: 'NAME', data: 'name'},
        {
          title: 'VIEW', data: 'id', render: (data) => {
            return `<button class="btn btn-primary" data-action="view" data-id="${data}">Open</button>`;
          },
          className: 'data-cell'
        },
        {
          title: 'DELETE', data: 'id', render: (data) => {
            return `<button class="btn btn-danger" data-action="delete" data-id="${data}">Delete</button>`;
          },
          className: 'data-cell'
        }
      ],
      basesColumns: [
        {
          title: 'Select',
          data: 'id',
          render: (data, type, row) => {
            return `<input type="checkbox" class="bases-checkbox" data-id="${data}" data-url="${row.url}" ${this.selectedBases.some(item => item.id === data) ? 'checked' : ''}>`;
          },
          className: 'data-cell'
        },
        {title: 'NAME', data: 'url'},
        {
          title: 'VIEW', data: 'id', render: (data) => {
            return `<button class="btn btn-primary" data-action="view" data-id="${data}">Open</button>`;
          },
          className: 'data-cell'
        },
        {
          title: 'DELETE', data: 'id', render: (data) => {
            return `<button class="btn btn-danger" data-action="delete" data-id="${data}">Delete</button>`;
          },
          className: 'data-cell'
        }
      ],
      tableClasses: 'table text-start align-middle table-bordered table-hover mb-0',
      selectedProxy: {},
      imapDropdownOpen: false,
      proxyDropdownOpen: false,
      smtpDropdownOpen: false,
      domainDropdownOpen: false,
      baseDropdownOpen: false,
      formType: 'main',

    };
  },
  watch: {
    logs() {
      this.scrollToBottom();
    },
    mailing_logs() {
      this.scrollToBottom();
    },
    '$route.query.mode'(newValue, oldValue) {
      // Re-run margin application and scrolling down function when form type changes
      this.$nextTick(() => {
        this.applyMargins();
        this.scrollToBottom();
      });
    }
  },
  methods: {
    saveSelectionSMTP() {
      localStorage.setItem('selectedSmtps', JSON.stringify(this.selectedSmtps));
    },
    loadSelectionSMTP() {
      this.selectedSmtps = JSON.parse(localStorage.getItem('selectedSmtps') || '[]');
    },
    saveSelectionDomain() {
      localStorage.setItem('selectedDomains', JSON.stringify(this.selectedDomains));
    },
    loadSelectionDomain() {
      this.selectedDomains = JSON.parse(localStorage.getItem('selectedDomains') || '[]');
    },
    saveSelectionProxy() {
      localStorage.setItem('selectedProxies', JSON.stringify(this.selectedProxies));
    },
    loadSelectionProxy() {
      this.selectedProxies = JSON.parse(localStorage.getItem('selectedProxies') || '[]');
    },
    saveSelectionTemplates() {
      localStorage.setItem('selectedTemplates', JSON.stringify(this.selectedMaterials));
    },
    loadSelectionTemplates() {
      this.selectedMaterials = JSON.parse(localStorage.getItem('selectedTemplates') || '[]');
    },
    saveSelectionBase() {
      localStorage.setItem('selectedBases', JSON.stringify(this.selectedBases));
    },
    loadSelectionBase() {
      this.selectedBases = JSON.parse(localStorage.getItem('selectedBases') || '[]');
    },
    isEmpty(obj) {
      return Object.keys(obj).length === 0;
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
    fetchLogs() {
      const currentSessionName = this.getCurrentSessionName();
      const logType = 'testmode';
      if (!currentSessionName) {
        return;
      }

      axios.get(`${import.meta.env.VITE_BACK_URL}/api/logs/${logType}/${currentSessionName}`)
          .then(response => {
            if (response.data && response.data.status === 'success') {
              this.logs = response.data.logs;
            }
          })
          .catch(error => {
            console.error('Failed to fetch logs:', error);
          });
    },
    fetchImaps() {
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/imaps`)
          .then(response => {
            if (response.data && response.data.status === 'success') {
              this.imaps = response.data.imaps;
            }
          })
          .catch(error => {
            console.error('Failed to fetch imaps:', error);
          });
    },
    fetchProxies() {
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/proxies`)
          .then(response => {
            if (response.data && response.data.status === 'success') {
              this.proxies = response.data.proxies;
            }
          })
          .catch(error => {
            console.error('Failed to fetch proxies:', error);
          });
    },
    fetchSmtps() {
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/smtps`)
          .then(response => {
            if (response.data && response.data.status === 'success') {
              this.smtps = response.data.smtps;
            }
          })
          .catch(error => {
            console.error('Failed to fetch smtps:', error);
          });
    },
    fetchDomains() {
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/domains`)
          .then(response => {
            if (response.data && response.data.status === 'success') {
              this.domains = response.data.domains;
            }
          })
          .catch(error => {
            console.error('Failed to fetch domains:', error);
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
    toggleSelection(id, server) {
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
        this.selectedProxies.splice(index, 1);
      } else {
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
    handleClick(event) {
      const action = event.target.getAttribute('data-action');
      const id = event.target.getAttribute('data-id');

      if (action === 'view') {
        this.view(id);
      } else if (action === 'delete') {
        this.del(id);
      } else if (action === 'checkSMTP') {
        this.checkSMTP(id);
      }
    },
    submit() {
      console.log('BASE', this.base_form);
      console.log('PROXY:', this.selectedProxy);
      console.log('SMTP:', this.selectedSmtp);
      console.log('TEMPLATE:', this.dummy_form);
      console.log('THREAD:', this.threads_number);
      console.log('DOMAINS:', this.selectedDomain);
      console.log('Delay:', this.delay_form);
      console.log('SESSION:', this.getCurrentSessionName());
      console.log('SOKET:', this.connection.id);
      console.log('TIMEOUT:', this.timeout_form);

      this.logs = []
      let token = ''
      let cookies = document.cookie.split(";")
      cookies.forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split("=")[1];
        }
      })
      this.errorCheck = null
      if (this.selectedProxy && this.selectedSmtp && this.base_form_imap) {
        this.can_run = false
        axios.post(`${import.meta.env.VITE_BACK_URL}/api/start/mailing`, {
          token: token,
          socket: this.connection.id,
          session: this.getCurrentSessionName(),
          dummy_form: this.dummy_form,
          proxies_form: this.selectedProxy,
          smtps_form: this.selectedSmtp,
          base_form: this.selectedBase,
          domain_form: this.selectedDomain,
          threads_form: this.threads_number,
          delay_form: this.delay_form,
          sending_limit: this.sending_limit,
          emails_per_check: this.emails_per_check,
          count_of_material: this.count_of_material,
          timeout: this.timeout_form
        }).then(res => {
          if (res.data.data == 'error') {
            this.can_run = true
            this.errorCheck = res.data.error
          }
        })
      } else {
        this.errorCheck = 'Fill in the fields!'
      }
    },
    toggleImapDropdown() {
      this.imapDropdownOpen = !this.imapDropdownOpen;
    },
    toggleBasesDropdown() {
      this.baseDropdownOpen = !this.baseDropdownOpen;
    },

    selectImap(item) {
      this.selectedImap = item;
      this.imapDropdownOpen = false;
    },
    selectBase(item) {
      this.selectedBase = item;
      this.baseDropdownOpen = false;
    },
    toggleProxyDropdown() {
      this.proxyDropdownOpen = !this.proxyDropdownOpen;
    },
    selectProxy(item) {
      this.selectedProxy = item;
      this.proxy_form = item.id;
      this.proxyDropdownOpen = false;
    },
    toggleSmtpDropdown() {
      this.smtpDropdownOpen = !this.smtpDropdownOpen;
    },
    selectSmtp(item) {
      this.selectedSmtp = item;
      this.smtpDropdownOpen = false;
    },
    toggleDomainDropdown() {
      this.domainDropdownOpen = !this.domainDropdownOpen;
    },
    selectDomain(item) {
      this.selectedDomain = item;
      this.domainDropdownOpen = false;
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
      }).catch(error => {
        console.error('Error fetching material details:', error);
      });
    },
    deleteLog() {
      const currentSessionName = this.getCurrentSessionName();
      const logType = 'testmode';
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
    applyMargins() {
      const startCells = document.querySelectorAll('.dt-layout-cell.dt-start');
      const endCells = document.querySelectorAll('.dt-layout-cell.dt-end');
      const tableRows = document.querySelectorAll('.dt-layout-row.dt-layout-table');
      const rows = document.querySelectorAll('.dt-layout-row');

      startCells.forEach(el => el.style.marginBottom = '10px');
      endCells.forEach(el => el.style.marginBottom = '10px');
      tableRows.forEach(el => el.style.marginBottom = '10px');
      rows.forEach(el => el.style.marginBottom = '10px');
    },
    onDataTableRendered() {
      this.applyMargins();
    },
    formatTime(timestamp) {
      // Split the timestamp to get the time part
      const timePart = timestamp.split(' ')[1]; // Get the part after the date
      const [time] = timePart.split(','); // Remove milliseconds if present
      return time; // Return only hh:mm:ss
    }
  },
  mounted() {
    this.fetchDebugs();
    this.fetchLogs();
    this.fetchImaps();
    this.fetchProxies();
    this.fetchSmtps();
    this.fetchDomains();
    this.loadSelectionSMTP();
    this.loadSelectionDomain();
    this.loadSelectionProxy();
    this.loadSelectionTemplates();
    this.getMaterialsSMTP();
    this.getMaterialsDomain();
    this.loadSelectionBase();
    this.scrollToBottom();
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
  },
  created() {
    this.connection = io.connect(import.meta.env.VITE_BACK_URL);
    this.connection.on('message', (data) => {
      data = data.split(':');
      if (data[0] == 'progress_test_mode') {
        this.log_valid = data[1];
        this.log_error = data[2];
        this.log_progress = data[3];
        if (data[3] == '100') {
          this.can_check = true;
          setTimeout(() => {
            this.getMaterialsS();
          }, 1000);
        } else {
          this.can_check = false;
        }
      } else if (data[0] == 'logs_test_mode') {
        this.saveLog(data[2], data[1]);
        this.fetchLogs();
      }
    });
  }
};
</script>
<style scoped>
:root {
  --primary: #ef4444; /* Красный цвет */
  --secondary: #191C24; /* Темный цвет фона */
  --light: #6C7293;
  --dark: #000000;
}

#main-part {
  display: flex;
  flex-direction: column;
  width: 100%;
}


.dummy-form {
  overflow: auto;
  margin-top: 1em;
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

/deep/ .data-cell {
  color: #6C7293 !important;
}

/deep/ .table th {
  color: #fff !important;
}

.table-dark th, .table-dark td {
  border-color: #333;
  color: #ddd;
}

.headerzn {
  color: #ddd;
}

/deep/ .smtp-checkbox, /deep/ .proxies-checkbox, /deep/ .domain-checkbox, /deep/ .templates-checkbox, /deep/ .bases-checkbox {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
  background-color: var(--dark);
  position: relative;
}

/deep/ .smtp-checkbox:checked, /deep/ .proxies-checkbox:checked, /deep/ .domain-checkbox:checked, /deep/ .templates-checkbox:checked, /deep/ .bases-checkbox:checked {
  background-color: var(--primary);
  border-color: var(--primary);
}

/deep/ .smtp-checkbox:checked::after, /deep/ .proxies-checkbox:checked::after, /deep/ .domain-checkbox:checked::after, /deep/ .templates-checkbox:checked::after, /deep/ .bases-checkbox:checked::after {
  content: '✓';
  display: block;
  color: white;
  font-size: 14px;
  text-align: center;
  line-height: 20px;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/deep/ .btn-dead {
  background-color: var(--primary) !important;
  color: #000;
  width: 100px;

}

/deep/ .btn-junk {
  background-color: var(--primary) !important;
  color: #000;
  width: 100px;
}

/deep/ .btn-inbox {
  background-color: #2bff00 !important;
  color: #000;
  width: 100px;
}

/deep/ .btn-none {
  background-color: var(--primary) !important;
  color: #000;
  width: 100px;
}

/deep/ .btn-undefined {
  background-color: var(--primary) !important;
  color: #000;
  width: 100px;
}

/deep/ .btn-checked {
  background-color: #2bff00 !important;
  color: #000;
  width: 100px;
}

/deep/ .btn-primary {
  background-color: var(--primary) !important;
  border: none;
  transition: background-color 0.2s linear;
}

.btn:hover {
  background-color: #cc0000;
}

.btn-delete {
  margin-top: 1em;
  margin-bottom: 1em;
}

.btn-delete:hover {
  background-color: #cc0000;
}

.for-input {
  margin-top: 1em;
}

.text-success {
  color: limegreen !important;
}

.text-danger {
  color: red !important;
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
