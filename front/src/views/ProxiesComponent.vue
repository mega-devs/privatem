<template>
  <LayoutComponent title="Proxies">
    <template #content>
      <div class="container-fluid dummy-form">   
      <div class="row">
        <TwoConsoleComponent :logs="logs" :mailing_logs="mailing_logs" @delete-log="deleteLog()" />
        <div class="col-lg-6">
          <div class="panel-loader">
            <v-file-input id="proxiesTxtFileUpload" class="panel-loader__proxies-txt " clearable label="Input proxies.txt" accept="text file/txt" @change="fileUpload"></v-file-input>
            <v-file-input id="proxiesZipFileUpload" class="panel-loader__proxies-zip " clearable label="Input proxies.zip" accept="Archice/zip" @change="fileUpload"></v-file-input>
            <v-textarea class="panel-loader__proxies " label="Enter multiple proxies separated by new lines" v-model="proxyTextInput" variant="outlined"></v-textarea>
            <div class="panel-loader__btns">
              <v-btn @click="submit()" class="btn btn-primary">Submit</v-btn>
              <v-btn @click="exportData()" class="btn btn-primary">Export to TXT</v-btn>
            </div>
          </div>
          <p class="text-danger">{{ errorSub }}</p>
        </div>
        <div class="col-lg-6">
          <!-- update -->
          <DataTable :data="proxiesData" :columns="proxiesColumns" :class="tableClasses" @click="handleClick">
          </DataTable>
        </div>
      </div>
      <div style="display: grid; grid-template-columns: auto min-content; height: min-content; grid-gap: 16px;">
        <v-select v-model="check_file" label="Check proxies" :items="allowedStatuses" />
        <v-btn v-if="can_check" @click="checkSubmit" class="btn btn-primary">Submit</v-btn>
        <p v-else>Please wait!</p>
      </div>
      <p class="text-danger">{{ errorCheck }}</p>
      <h3 class="headerzn">Progress</h3>
      <v-progress-linear class="progress-bar" color="primary" :model-value="log_progress" :max="100" :height="11"></v-progress-linear>      
      <div style="display: grid; grid-template-columns: repeat(2, auto); grid-gap: 16px;">
        <p class="text-success bordered">Valid: {{ log_valid }}</p>
        <p class="text-danger bordered">Errors: {{ log_error }}</p>
      </div>
    </div>
    <ModalViewComponent ref="modal"></ModalViewComponent>
    </template>
  </LayoutComponent>
</template>

<script>
import axios from 'axios';
import ModalViewComponent from '@/components/components/ModalViewComponent.vue';
import JSZip from 'jszip';
import {io} from "socket.io-client";
import DataTable from 'datatables.net-vue3';
import LayoutComponent from '@/components/LayoutComponent.vue';
import TwoConsoleComponent from '@/components/TwoConsoleComponent.vue';

export default {
  components: {
    ModalViewComponent,
    DataTable,
    LayoutComponent,
    TwoConsoleComponent
  },
  data() {
    return {
      name: null,
      materials: null,
      file: null,
      errorSub: null,
      check_file: null,
      check_file_name: null,
      can_check: true,
      log_error: null,
      log_valid: null,
      log_progress: null,
      mailing_logs: [],
      logs: [],
      errorCheck: null,
      proxiesData: [],
      proxyTextInput: '',
      allowedStatuses: ['all', 'inbox', 'junk', 'dead', 'none', 'checked'],
      selectedProxies: [],
      proxiesColumns: [
        {
          title: 'Select',
          data: 'id',
          render: (data, type, row) => {
            return `<input type="checkbox" class="form-check-input" data-id="${data}" data-ip="${row.ip}" ${this.selectedProxies.some(item => item.id === data) ? 'checked' : ''}>`;
          },
          className: 'data-cell'
        },
        {title: 'ID', data: 'id', className: 'data-cell'},
        {title: 'IP', data: 'ip', className: 'data-cell'},
        {title: 'Port', data: 'port', className: 'data-cell'},
        {
          title: 'STATUS', data: 'status', render: (data) => {
            return `<a href="#" class="btn btn-${data}">${data}</a>`;
          }
        },
        {
          title: 'VIEW', data: 'id', render: (data) => {
            return `<button class="btn btn-primary" data-action="view" data-id="${data}"><i class="bi bi-binoculars"></i></button>`;
          }
        },
        {
          title: 'DELETE', data: 'id', render: (data) => {
            return `<button class="btn btn-danger btn-delete-proxy" data-action="delete" data-id="${data}"><i class="bi bi-dash"></i></button>`;
          }
        },
        {
          title: 'Check', data: 'id', render: (data) => {
            return `<button class="btn btn-info" data-action="check" data-id="${data}"><i class="bi bi-dash"></i></button>`;
          }
        }
      ],
      tableClasses: 'table text-start align-middle table-bordered table-hover mb-0',
    }
  },
  methods: {
    saveSelection() {
      localStorage.setItem('selectedProxies', JSON.stringify(this.selectedProxies));
    },
    loadSelection() {
      this.selectedProxies = JSON.parse(localStorage.getItem('selectedProxies') || '[]');
    },
    getMaterials() {
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
    submit() {
      const currentSessionName = this.getCurrentSessionName();
      if (!currentSessionName) {
        this.errorSubTemplates = 'No session loaded';
        return;
      }

      let token = '';
      let cookies = document.cookie.split(";");
      cookies.forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split("=")[1];
        }
      });
      this.errorSub = '';

      // Отправка данных прокси
      if (this.file || this.proxyTextInput) {
        let proxyArray = this.proxyTextInput.split('\n').map(proxy => proxy.trim()).filter(proxy => proxy);
        let fileContent = this.file ? this.file : proxyArray.join('\n');
        axios.post(`${import.meta.env.VITE_BACK_URL}/api/input/material`, {
          token: token,
          session: currentSessionName,
          type: 'proxies',
          file: fileContent,
          fileName: this.fileName || ''
        }).then(res => {
          if (res.data.data === 'error') {
            this.errorSub = res.data.error;
          }
          this.getMaterials()
        }).catch(error => {
          this.errorSub = 'An error occurred during submission.';
          console.error('Submission error:', error);
        });
      }
      this.getMaterials();
      this.proxyTextInput = '';
    },
    toggleSelection(id, ip) {
      const index = this.selectedProxies.findIndex(item => item.id === id);
      if (index !== -1) {
        this.selectedProxies.splice(index, 1);
      } else {
        this.selectedProxies.push({id, ip});
      }
      console.log(this.selectedProxies);
    },
    del(id) {
      let token = '';
      document.cookie.split(";").forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split("=")[1];
        }
      });
      axios.post(`${import.meta.env.VITE_BACK_URL}/api/del/material`, {token: token, id: id, type: 'proxies'})
          .then(res => {
            this.getMaterials();
          });
    },
    get_zip_data(zip, files_keys, data, callback) {
      zip.files[files_keys[0]].async("string").then(el_data => {
        files_keys.shift();
        callback(data = data + '\n' + el_data);
        if (files_keys.length > 0) {
          this.get_zip_data(zip, files_keys, data, () => {
          });
        } else {
          this.file = data;
        }
      });
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

      axios.post(`${import.meta.env.VITE_BACK_URL}/api/input/log/proxies/${currentSessionName}`, {
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
    fileUpload(event) {
      if (event.target.getAttribute('id') === 'proxiesTxtFileUpload') {
        event.target.files[0].arrayBuffer().then((buffer) => {
          const bufferByteLength = buffer.byteLength;
          const bufferUint8Array = new Uint8Array(buffer, 0, bufferByteLength);
          this.file = new TextDecoder().decode(bufferUint8Array);
        });
      } else if (event.target.getAttribute('id') === 'proxiesZipFileUpload') {
        event.target.files[0].arrayBuffer().then((buffer) => {
          const zip = new JSZip();
          zip.loadAsync(buffer).then(zip => {
            let data = '';
            let files = zip.files;
            let files_keys = Object.keys(files);
            this.get_zip_data(zip, files_keys, data, () => {
            });
          });
        });
      }
    },
    view(id) {
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/get/materials/${id}/proxies/*`).then(res => {
        let modalData = []
        res.data.forEach(el => {
          modalData.push()
        })
        this.$refs.modal.data = res.data
        this.$refs.modal.columns = ['ID', 'PROXY', 'PORT', 'STATUS', 'SESSION']
        this.$refs.modal.show = true
      })
    },
    deleteLog() {
      const session = this.getCurrentSessionName();
      let token = '';
      document.cookie.split(';').forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split('=')[1];
        }
      });
      if (!token || !session) {
        this.error = 'No session or token found';
        return;
      }

      axios.post(`${import.meta.env.VITE_BACK_URL}/api/del/log`, {
        token: token,
        session: session,
        type: 'proxies'
      })
          .then(response => {
            if (response.data.data === 'success') {
              this.logs = "";
              this.fetchLogs();
            } else {
              this.error = response.data.error;
            }
          })
          .catch(error => {
            this.error = 'Error deleting log: ' + error.message;
          });
    },
    addLogEntry(logEntry) {
      // this.logs.push(logEntry);check_file
      // this.$nextTick(() => {
      //   const consoleOutput = this.$refs.consoleOutput;
      //   if (consoleOutput) {
      //     consoleOutput.scrollTop = consoleOutput.scrollHeight;
      //   }
      // });
    },
    handleClick(event) {
      const action = event.target.getAttribute('data-action') || event.target.parentElement.getAttribute('data-action');
      const id = event.target.getAttribute('data-id') || event.target.parentElement.getAttribute('data-id');

      if (action === 'view') {
        this.view(id);
      } else if (action === 'delete') {
        this.del(id);
      } else if (action === 'check') {
        this.check_file = id
        this.checkSubmit()
      }
    },
    fetchLogs() {
      const currentSessionName = this.getCurrentSessionName();
      const logType = 'proxies';
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
    fetchDebugs() {
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/debug`)
          .then(response => {
            this.mailing_logs = response.data.logs;
          })
          .catch(error => {
            console.error('Error fetching logs:', error);
          });
    },
    checkSubmit() {
      this.logs = [];
      let token = '';
      let cookies = document.cookie.split(";");
      cookies.forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split("=")[1];
        }
      });
      this.errorCheck = null;
      if (this.check_file) {
        this.can_check = false;

        const currentSessionName = this.getCurrentSessionName();
        if (!currentSessionName) {
          this.errorCheck = 'No session loaded';
          return;
        }

        axios.post(`${import.meta.env.VITE_BACK_URL}/api/check/proxy`, {
          token: token,
          session: currentSessionName,
          socket: this.connection.id,
          proxy_id: this.check_file
        }).then(res => {
          if (res.data.data === 'error') {
            this.can_check = true;
            this.errorCheck = res.data.error;
          }
        }).catch(error => {
          this.can_check = true;
          this.errorCheck = 'Error checking proxy: ' + error.message;
        });
      } else {
        this.errorCheck = 'Fill in the fields!';
      }
    },
    getCurrentSessionName() {
      const name = document.cookie.split('; ').find(row => row.startsWith('currentSessionName='));
      return name ? name.split('=')[1] : null;
    },
    exportData() {
      const rows = this.proxiesData.map(proxy => `${proxy.ip}, ${proxy.port}, ${proxy.status}`).join('\n');
      const blob = new Blob([rows], {type: 'text/plain'});
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'proxies.txt';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    },

    formatTime(timestamp) {
      // Split the timestamp to get the time part
      const timePart = timestamp.split(' ')[1]; // Get the part after the date
      const [time] = timePart.split(','); // Remove milliseconds if present
      return time; // Return only hh:mm:ss
    },
  },
  mounted() {
    this.loadSelection();
    this.getMaterials();
    this.fetchLogs();
    this.fetchDebugs();
    console.log(this.selectedProxies);
    document.querySelector('.table').addEventListener('change', (event) => {
      if (event.target.classList.contains('form-check-input')) {
        const id = parseInt(event.target.getAttribute('data-id'));
        const ip = event.target.dataset.ip;
        this.toggleSelection(id, ip);
        this.saveSelection();
      }
    });
  },
  created() {
    this.connection = io.connect(import.meta.env.VITE_BACK_URL)
    this.connection.on('message', (data) => {
      data = data.split(":")
      if (data[0] == 'progress_check_proxy') {
        this.log_valid = data[1]
        this.log_error = data[2]
        this.log_progress = data[3]
        if (data[3] == '100') {
          this.can_check = true
          setTimeout(() => {
            this.getMaterials()
          }, 1000)
        } else {
          this.can_check = false
        }
      } else if (data[0] == 'logs_check_proxy') {
        this.saveLog(data[2], data[1]);
        this.fetchLogs();
        this.addLogEntry({TEXT: data[2], status: data[1]});
      }
    })
  }
}
</script>

<style lang="scss"  scoped>
.progress-bar {
  border-radius: 16px;
}

.panel-loader {
  display: grid;
  grid-gap: 16px;
  padding: 16px 0px;
  grid-template-areas: "proxies-txt proxies-txt"
                       "proxies-zip proxies"
                       "settings-json proxies"
                       "url url"
                       "btns btns";
  &__proxies-txt {
    grid-area: proxies-txt;
  }
  &__proxies-zip {
    grid-area: proxies-zip;
  }
  &__proxies {
    grid-area: proxies;
  }
  &__settings-json {
    grid-area: settings-json;
  }
  &__url {
    grid-area: url;
  }
  &__btns {
    grid-area: btns;
    display: flex;
    grid-gap: 16px;
    justify-content: center;
  }
}




#main-part {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin: 0 auto;
}

.dummy-form {
  overflow: auto;
  margin-top: 1em;
  width: auto;
}

.text-success {
  color: limegreen !important;
}

.text-danger {
  color: red !important;
}

label {
  color: white;
}




.data-cell {
  color: #6C7293 !important;
}

.table th {
  color: #fff !important;
}

.table-dark th, .table-dark td {
  border-color: #333;
  color: #ddd;
}

.headerzn {
  color: #ddd;
}

.form-check-input {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
  background-color: var(--da);
}

.form-check-input:checked {
  background-color: var(--primary);
  border-color: var(--primary);
}

.form-check-input:checked::after {

  display: block;
  color: white;
  font-size: 14px;
  text-align: center;
  line-height: 20px;
}

.btn-dead {
  background-color: var(--primary) !important;
  color: #000;
  width: 100px;
}

.btn-junk {
  background-color: var(--primary) !important;
  color: #000;
  width: 100px;
}

.btn-inbox {
  background-color: #2bff00 !important;
  color: #000;
  width: 100px;
}

.btn-none {
  background-color: var(--primary) !important;
  color: #000;
  width: 100px;
}

.btn-checked {
  background-color: #2bff00 !important;
  color: #000;
  width: 100px;
}

.dt-paging-button {
  border: 1px solid white;
  background-color: transparent;
  margin: 1%;
  border-radius: 7px;
  transition: background-color 0.2s linear;
}

.dt-paging-button:hover {
  background-color: red;
  color: white;
}

label {
  padding: 1em 1em 1em 0;
}

.dt-input {
  margin-right: 1em;
}

.dt-info {
  padding: 1em 1em 1em 0;
  margin-bottom: 1%;
}

.btn-primary {
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

.bordered {
  border: 1px solid grey; /* Change color as needed */
  padding: 10px;
  margin: 10px 0 10px 0;
  background-color: #2c2c2c;
}

</style>
