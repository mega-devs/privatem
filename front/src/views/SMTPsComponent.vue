<template>
  <LayoutComponent title="SMTPs">
    <template #content>
      <TwoConsoleComponent :logs="logs" :mailing_logs="mailing_logs" @delete-log="deleteLog()" />
      <div class="smtp-panel">
        <v-file-input id="SMTPsTxtFileUpload" class="smtp-panel__txt" clearable label="Input SMTPs.txt or csv" accept="text file/txt" @change="fileUpload"></v-file-input>
        <v-file-input id="SMTPsZipFileUpload" class="smtp-panel__zip" clearable label="Input SMTPs.zip" accept="archive file/zip" @change="fileUpload"></v-file-input>
        <v-textarea class="smtp-panel__input " label="Enter multiple SMTPs separated by new lines" v-model="smtpTextInput" variant="outlined"></v-textarea>
        <div class="smtp-panel__btns">
          <v-btn @click="submit()" class="btn btn-primary">Submit</v-btn>
          <v-btn @click="exportToTxt()" class="btn btn-primary">Export to TXT</v-btn>
        </div>
      </div>
      <p class="text-danger">{{ errorSub }}</p>

      <div class="container-fluid dummy-form">

      <div class="row">
        
        <div class="col-lg-12">
          <DataTable :data="smtpsData" :columns="smtpsColumns" :class="tableClasses" class="data-cell"
                     @click="handleClick">
          </DataTable>
        </div>
      </div>
      <div>
        <br>
        <hr>
        <p class="headerzn">Check SMTP</p>
        <hr>
        <div class="panel-two">
          <div>
            <v-select label="Select SMTP" :items="allowedStatuses" v-model="selectedSmtp" />
            <v-select label="Select Proxy" :items="allowedStatuses" v-model="selectedProxy" />
          </div>
          <div>
            <v-select label="Select IMAP" :items="allowedStatuses" v-model="selectedImap" />
            <input v-model="timeout" style="margin-top: 1em;" type="text" class="form-control" aria-label="Small"
                   placeholder="timeout">            
          </div>
        </div>
      </div>
      <div v-if="can_check">
        <button style="margin-top: 1em;" type="button" @click.prevent="checkSubmit" class="btn btn-primary">Submit
        </button>
      </div>
      <div v-else>
        <p class="labelnew">Please wait!</p>
      </div>
      <p class="text-danger">{{ errorCheck }}</p>
      <h3 class="headerzn">Progress</h3>
      <div class="progress">
        <div class="progress-bar" role="progressbar" :style=" 'background-color: #ef4444;'+'width: '+log_progress+'%'"
             aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
      <div class="row">
        <div class="col-lg-6">
          <p class="text-success bordered">Valid: {{ log_valid }}</p>
        </div>
        <div class="col-lg-6">
          <p class="text-danger bordered">Errors: {{ log_error }}</p>
        </div>
      </div>
    </div>
    <ModalViewComponent ref="modal"></ModalViewComponent>
    </template>
  </LayoutComponent>
</template>

<script>
import axios from 'axios';
import ModalViewComponent from '../components/components/ModalViewComponent.vue';
import DataTable from 'datatables.net-vue3';
import JSZip from 'jszip';
import {io} from "socket.io-client";
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
      file: null,
      fileName: null,
      errorSub: null,
      can_check: true,
      log_error: null,
      log_valid: null,
      check_file: null,
      check_file_name: null,
      timeout: null,
      log_progress: null,
      errorCheck: null,
      smtpTextInput: '',
      mailing_logs: [],
      logs: [],
      imaps: [],
      selectedImap: "",
      smtpsData: [],
      allowedStatuses: ['all', 'inbox', 'junk', 'dead', 'none', 'checked'],
      selectedSmtps: [],
      smtpsColumns: [
        {
          title: 'Select',
          data: 'id',
          render: (data, type, row) => {
            return `<input type="checkbox" class="form-check-input" data-id="${data}" data-server="${row.server}" ${this.selectedSmtps.some(item => item.id === data) ? 'checked' : ''}>`;
          },
          className: 'data-cell'

        },
        {title: 'ID', data: 'id', className: 'data-cell'},
        {title: 'Server', data: 'server', className: 'data-cell'},
        {title: 'Port', data: 'port', className: 'data-cell'},
        {title: 'User', data: 'user', className: 'data-cell'},
        {title: 'Pw', data: 'pw', className: 'data-cell'},
        {
          title: 'STATUS',
          data: 'status',
          className: 'data-cell',
          render: (data) => `<span>${data}</span>` // Just plain text
        },
        {
          title: 'DELETE',
          data: 'id',
          render: (data) => `<button class="btn btn-danger" data-action="delete" data-id="${data}"><i class="bi bi-trash"></i></button>`
        },
        {
          title: 'Check B/L', data: 'id', className: 'data-cell', render: (data) => {
            return `<button class="btn btn-info" data-action="checkSMTP" data-id="${data}"><i class="bi bi-check-square-fill"></i></button>`;
          },
        },

      ],
      tableClasses: 'table text-start align-middle table-bordered table-hover mb-0',
      selectedSmtp: "",
      selectedProxy: "",
      imapDropdownOpen: false,
      dropdownOpen: false,
      proxyDropdownOpen: false,
    };
  },
  methods: {
    saveSelection() {
      localStorage.setItem('selectedSmtps', JSON.stringify(this.selectedSmtps));
    },
    loadSelection() {
      this.selectedSmtps = JSON.parse(localStorage.getItem('selectedSmtps') || '[]');
    },
    isEmpty(obj) {
      return Object.keys(obj).length === 0;
    },
    fetchImaps() {
      const currentSessionName = this.getCurrentSessionName()
      axios.get(`${import.meta.env.VITE_BACK_URL}/api/get/list/imaps/${currentSessionName}`)
          .then(response => {
            if (response.data) {
              console.log(`Imaps: ${response.data}`)
              this.imaps = response.data;
            }
          })
          .catch(error => {
            console.error('Failed to fetch imaps:', error);
          });
    },
    getMaterials() {
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
          port: item.port,
          user: item.email,
          pw: item.password,
          status: item.status
        }));
      }).catch(error => {
        console.error('Error fetching templates:', error);
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
    getCurrentSessionName() {
      const name = document.cookie.split('; ').find(row => row.startsWith('currentSessionName='));
      return name ? name.split('=')[1] : null;
    },
    handleClick(event) {
      const action = event.target.getAttribute('data-action') || event.target.parentElement.getAttribute('data-action');
      const id = event.target.getAttribute('data-id') || event.target.parentElement.getAttribute('data-id');

      if (action === 'view') {
        this.view(id);
      } else if (action === 'delete') {
        this.del(id);
      } else if (action === 'checkSMTP') {
        this.checkSMTP(id);
      }
    },
    submit() {
      const currentSessionName = this.getCurrentSessionName();
      if (!currentSessionName) {
        this.errorSubTemplates = 'No session loaded';
        return;
      }
      let token = '';
      document.cookie.split(';').forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split('=')[1].trim();
        }
      });
      this.errorSub = '';
      if (this.file || this.smtpTextInput) {
        let smtpArray = this.smtpTextInput.split('\n').map(smtp => smtp.trim()).filter(smtp => smtp);
        let fileContent = this.file ? this.file : smtpArray.join('\n');
        axios.post(`${import.meta.env.VITE_BACK_URL}/api/input/material`, {
          token: token,
          session: currentSessionName,
          type: 'smtps',
          file: fileContent,
          fileName: this.fileName || ''
        }).then(res => {
          this.getMaterials();
          this.smtpTextInput = '';
          if (res.data.data === 'error') {
            this.errorSub = res.data.error;
          }
        }).catch(error => {
          this.errorSub = 'An error occurred during submission.';
          console.error('Submission error:', error);
        });
      } else {
        this.errorSub = 'Fill in the fields!';
      }
    },
    del(id) {
      let token = '';
      document.cookie.split(';').forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split('=')[1].trim();
        }
      });
      axios.post(`${import.meta.env.VITE_BACK_URL}/api/del/material`, {token: token, id: id, type: 'smtps'}).then(res => {
        this.getMaterials();
      }).catch(error => {
        console.error('Error deleting material:', error);
      });
    },
    get_zip_data(zip, files_keys, data, callback) {
      zip.files[files_keys[0]].async('string').then(el_data => {
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
    fileUpload(event) {
      const file = event.target.files[0];
      this.fileName = file.name;

      if (event.target.getAttribute('id') === 'SMTPsTxtFileUpload') {
        file.arrayBuffer().then((buffer) => {
          const bufferByteLength = buffer.byteLength;
          const bufferUint8Array = new Uint8Array(buffer, 0, bufferByteLength);
          this.file = new TextDecoder().decode(bufferUint8Array);
        });
      } else if (event.target.getAttribute('id') === 'SMTPsZipFileUpload') {
        file.arrayBuffer().then((buffer) => {
          const zip = new JSZip();
          zip.loadAsync(buffer).then((zip) => {
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

      axios.post(`${import.meta.env.VITE_BACK_URL}/api/input/log/smtps/${currentSessionName}`, {
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
    fetchLogs() {
      const currentSessionName = this.getCurrentSessionName();
      const logType = 'smtps';
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
    deleteLog() {
      this.logs = [];
      const session = this.getCurrentSessionName();
      let token = '';
      document.cookie.split(';').forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split('=')[1].trim();
        }
      });
      if (!token || !session) {
        this.error = 'No session or token found';
        return;
      }

      axios.post(`${import.meta.env.VITE_BACK_URL}/api/del/log`, {
        token: token,
        session: session,
        type: 'smtps'
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
      this.logs.push(logEntry);
      this.$nextTick(() => {
        const consoleOutput = this.$refs.consoleOutput;
        if (consoleOutput) {
          consoleOutput.scrollTop = consoleOutput.scrollHeight;
        }
      });
    },
    checkSubmit() {

      console.log('SMTP id:', this.selectedSmtp);
      console.log('Timeout:', this.timeout);
      console.log('Proxy id:', this.selectedProxy);

      this.logs = [];
      let token = '';
      document.cookie.split(';').forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split('=')[1].trim();
        }
      });
      this.errorCheck = null;

      if (this.selectedSmtp && this.timeout && this.selectedProxy) {
        this.can_check = false;

        axios.post(`${import.meta.env.VITE_BACK_URL}/api/check/smtp`, {
          token: token,
          session: this.getCurrentSessionName(),
          smtp_id: this.selectedSmtp,
          proxy_id: this.selectedProxy,
          timeout: this.timeout,
        }).then(res => {
          if (res.data.data == 'success') {
            this.can_check = true;
            this.errorCheck = null;
          } else if (res.data.error) {
            this.can_check = true;
            this.errorCheck = res.data.error;
          }
        }).catch(error => {
          this.can_check = true;
          this.errorCheck = 'Error occurred while submitting';
          console.error('Error submitting:', error);
        });
      } else {
        this.errorCheck = 'Fill in the fields!';
      }
    },
    checkSMTP(id) {
      console.log('Check file:', id);

      this.logs = [];
      let token = '';
      document.cookie.split(';').forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split('=')[1].trim();
        }
      });
      this.errorCheck = null;

      if (id) {
        this.can_check = false;

        axios.post(`${import.meta.env.VITE_BACK_URL}/api/check/smtpp`, {
          token: token,
          session: this.getCurrentSessionName(),
          smtp_id: id,
        }).then(res => {
          if (res.data.data == 'success') {
            this.can_check = true;
            this.errorCheck = null;
          } else if (res.data.error) {
            this.can_check = true;
            this.errorCheck = res.data.error;
          }
        }).catch(error => {
          this.can_check = true;
          this.errorCheck = 'Error occurred while submitting';
          console.error('Error submitting:', error);
        });
      } else {
        this.errorCheck = 'Fill in the fields!';
      }
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
      this.proxyDropdownOpen = false;
    },
    toggleImapDropdown() {
      this.imapDropdownOpen = !this.imapDropdownOpen;
    },
    toggleProxyDropdown() {
      this.proxyDropdownOpen = !this.proxyDropdownOpen;
      this.dropdownOpen = false;
    },
    selectImap(item) {
      this.selectedImap = item;
      this.imapDropdownOpen = false;
    },
    selectSmtp(item) {
      this.selectedSmtp = item;
      this.check_file = item;
      this.dropdownOpen = false;
    },
    selectProxy(item) {
      this.selectedProxy = item;
      this.proxy_form = item;
      this.proxyDropdownOpen = false;
    },
    handleClickOutside(event) {
      if (!this.$refs.smtpDropdown.contains(event.target)) {
        this.dropdownOpen = false;
      }
      if (!this.$refs.proxyDropdown.contains(event.target)) {
        this.proxyDropdownOpen = false;
      }
      if (!this.$refs.imapDropdown.contains(event.target)) {
        this.imapDropdownOpen = false;
      }
    },
    exportToTxt() {
      const data = this.smtpsData.map(item => `${item.server}, ${item.port},  ${item.user},  ${item.pw}, ${item.status}`).join('\n');
      const blob = new Blob([data], {type: 'text/plain'});
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'smtps.txt';
      link.click();
    },
    sendTestEmail() {
      const smtpData = this.smtpTextInput.split('\n').map(line => {
        const [server, port, user, pw] = line.split(',').map(item => item.trim());
        return {server, port, user, pw};
      });

      axios.post('/api/send-test-email', {smtps: smtpData})
          .then(response => {

            console.log('Тестовое письмо успешно отправлено:', response.data);
          })
          .catch(error => {
            console.error('Ошибка при отправке тестового письма:', error);
          });
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
  },
  mounted() {
    this.fetchImaps();
    this.loadSelection();
    this.getMaterials();
    this.fetchLogs();
    this.fetchDebugs();
    this.scrollToBottom();
    console.log(this.selectedSmtps)
    document.querySelector('.table').addEventListener('change', (event) => {
      if (event.target.classList.contains('form-check-input')) {
        const id = parseInt(event.target.getAttribute('data-id'));
        const server = event.target.dataset.server;
        this.toggleSelection(id, server);
        this.saveSelection();
      }
    });
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
  },
  created() {
    this.connection = io.connect(import.meta.env.VITE_BACK_URL);
    this.connection.on('message', (data) => {
      data = data.split(':');
      if (data[0] == 'progress_check_smtps') {
        this.log_valid = data[1];
        this.log_error = data[2];
        this.log_progress = data[3];
        if (data[3] == '100') {
          this.can_check = true;
          setTimeout(() => {
            this.getMaterials();
          }, 1000);
        } else {
          this.can_check = false;
        }
      } else if (data[0] == 'logs_check_smtps') {
        this.saveLog(data[2], data[1]);
        this.fetchLogs();
        this.addLogEntry({TEXT: data[2], status: data[1]});

      }
    });
  }
};
</script>

<style lang="scss" scoped>

.smtp-panel {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-areas: "txt input"
    "zip input"
    "btns btns";
  grid-gap: 16px;
  &__txt {
    grid-area: txt;
  }
  &__zip {
    grid-area: zip;
  }
  &__input {
    grid-area: input;
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

.dt-container label {
  font-size: 14px;
  color: #5c0707;
  margin-right: 100px;
}

.dt-input {
  border: 1px solid #ccc;
  padding: 5px;
  border-radius: 4px;
  background-color: #333;
  color: #ffffff;
}

.dt-input:focus {
  border-color: #66afe9;
  outline: none;
}

.dt-length label {

  margin-left: 10px;
}

.dt-search input {
  margin-left: 10px;
}

.data-cell {
  color: #ff0000 !important;
}

.table th {
  color: white !important;
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

label {
  color: white;
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

p {
  color: white;
  margin: 1em 0 1em 0;
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

</style>
