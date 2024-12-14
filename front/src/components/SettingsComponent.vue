<template>
  <NavBarComponent stateProp="settings"/>
  <div id="main-part">
    <HorizontalNavBar stateProp="settgins"/>
    <div class="container-fluid dummy-form">
      <div>
        <h3 style="text-align: center; margin-top: 1em;">Settings</h3>
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
              <div>
                <v-file-input class="panel-loader__settings-json " clearable label="Input settings.json" accept="File/json" @change="importSettings"></v-file-input>
                <v-textarea class="panel-loader__url " label="Enter the settings fetch URL" v-model="fetchUrlInput" variant="outlined"></v-textarea>
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
      </div>
      <div class="password-change-section">
        <h2>Change Password</h2>
        <form @submit.prevent="changePassword">
          <div class="form-group">
            <label for="current-password">Current Password</label>
            <input
                type="password"
                id="current-password"
                v-model="currentPassword"
                required
            />
          </div>

          <div class="form-group">
            <label for="new-password">New Password</label>
            <input
                type="password"
                id="new-password"
                v-model="newPassword"
                required
                minlength="8"
            />
          </div>

          <div class="form-group">
            <label for="confirm-password">Confirm New Password</label>
            <input
                type="password"
                id="confirm-password"
                v-model="confirmPassword"
                required
                minlength="8"
            />
          </div>

          <button type="submit" class="save-password-btn">Save New Password</button>
        </form>
      </div>
    </div>
  </div>

</template>


<script>
import axios from 'axios';
import NavBarComponent from './components/NavBarComponent.vue';
import HorizontalNavBar from "./components/HorizontalNavBar.vue";
import {io} from "socket.io-client";


export default {
  components: {
    NavBarComponent,
    HorizontalNavBar,
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
      settingsFileContent: null,
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
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
      fetchUrlInput: '',
    };
  },
  computed: {
    isPasswordChangeValid() {
      return this.currentPassword &&
          this.newPassword &&
          this.confirmPassword &&
          this.newPassword === this.confirmPassword &&
          this.newPassword.length >= 8
    }
  },
  methods: {
    resetpasswordForm() {
      this.currentPassword = '';
      this.newPassword = '';
      this.confirmPassword = '';
    },
    changePassword() {
      if (this.isPasswordChangeValid) {
        let token = ''
        let cookies = document.cookie.split(";")
        cookies.forEach(cookie => {
          if (cookie.includes('authToken')) {
            token = cookie.split("=")[1];
          }
        })
        axios.post(`${import.meta.env.VITE_BACK_URL}/change_user_password`, {
          token: token,
          current_password: this.currentPassword,
          new_password: this.newPassword
        }).then(res => {
          if (res.data.error) { // Adjusted check
            this.can_run = true;
            this.errorCheck = res.data.error;
          } else {
            // Handle success
            this.$store.dispatch('changeUserPassword', {
              currentPassword: this.currentPassword,
              newPassword: this.newPassword
            });
            this.resetpasswordForm(); // Example of a reusable reset form method
            alert('Password succesfully changed!')
          }
        }).catch(err => {
          console.error('Request failed', err);
          // Check if the error has a response and extract the error message
          if (err.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            const errorMessage = err.response.data.error || 'Something went wrong!';
            if (errorMessage === 'Incorrect password') {
              alert('Password is not changed. Wrong password!');
            } else {
              alert(errorMessage); // Display any other error messages from the server
            }
          } else if (err.request) {
            // The request was made but no response was received
            alert('No response from server. Please try again later!');
          } else {
            // Something happened in setting up the request that triggered an Error
            alert('Error in sending request: ' + err.message);
          }
        });
      } else {
        alert('Invalid input!')
      }
    },
    importSettings(event) {
      const file = event.target.files[0];
      if (!file) {
        this.errorSub = 'No file selected';
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          this.settingsFileContent = JSON.parse(e.target.result);
        } catch (err) {
          this.errorSub = 'Invalid JSON file';
          console.error('JSON parse error:', err);
        }
      };

      reader.readAsText(file);
    },
    loadSelectionSMTP() {
      this.selectedSmtps = JSON.parse(localStorage.getItem('selectedSmtps') || '[]');
    },
    loadSelectionDomain() {
      this.selectedDomains = JSON.parse(localStorage.getItem('selectedDomains') || '[]');
    },
    loadSelectionProxy() {
      this.selectedProxies = JSON.parse(localStorage.getItem('selectedProxies') || '[]');
    },
    loadSelectionTemplates() {
      this.selectedMaterials = JSON.parse(localStorage.getItem('selectedTemplates') || '[]');
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
      const currentSessionName = this.getCurrentSessionName();

      if (this.settingsFileContent || this.fetchUrlInput) {
        const settingsData = this.settingsFileContent || {};
        if (this.fetchUrlInput) {
          settingsData.fetch_url = this.fetchUrlInput;
        }

        axios.post(`${import.meta.env.VITE_BACK_URL}/api/update/settings_from_json`, {
          token: token,
          session: currentSessionName,
          json_data: settingsData
        }).then(res => {
          if (res.data.status === 'success') {
            location.reload();
          } else {
            this.errorSub = res.data.error;
          }
        }).catch(error => {
          this.errorSub = 'An error occurred during settings import.';
          console.error('Settings import error:', error);
        });
      }

      if (this.selectedProxy && this.selectedSmtp && this.base_form_imap) {
        this.can_run = false
        axios.post(`${import.meta.env.VITE_BACK_URL}/api/settings`, {
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
}
;
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

/deep/ .btn-primary {
  background-color: var(--primary) !important;
  border: none;
  transition: background-color 0.2s linear;
}

.btn:hover {
  background-color: #cc0000;
}

.for-input {
  margin-top: 1em;
}

.text-danger {
  color: red !important;
}

.form-control {
  margin: 5px 0 5px 0;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.save-password-btn {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-password-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.password-change-section {
  margin-bottom: 25px;
}

</style>