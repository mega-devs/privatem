<template>
    <NavBarComponent stateProp="IMAPs"/>
    <div id="main-part">
        <HorizontalNavBar state-prop="IMAPs"/>
        <div class="container-fluid dummy-form">
            <div class="row">
                <h2 class="text-center headerzn">IMAPs</h2>
                <hr>
                <div>
                    <h3 class="headerzn">Console</h3>
                    <div id="console-output" ref="consoleOutput">
                        <template v-for="(item, index) in logs" :key="index">
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
                <div class="col-lg-6">
                    <div class="row">
                        <div class="col-lg-6 mb-3">
                            <label for="formFile" class="form-label labelnew">Input IMAPs.txt</label>
                            <input ref="inputEl1" class="form-control" type="file" id="formFile1" @change="fileUpload">
                        </div>
                        <div class="col-lg-6 mb-3">
                            <label for="formText" class="form-label labelnew">Input IMAPs</label>
                            <textarea ref="inputEl3" class="form-control" id="formText" v-model="imapTextInput" placeholder="Enter multiple IMAPs separated by new lines"></textarea>
                        </div>
                    </div>
                    <button type="button" @click.prevent="submit" class="btn btn-primary">Submit</button>&nbsp;
                    <button type="button" @click.prevent="exportToTxt" class="btn btn-primary">Export to TXT</button>
                    <p class="text-danger">{{ errorSub }}</p>
                </div>
                <div class="col-lg-12">
                    <DataTable :data="imapsData" :columns="imapsColumns" :class="tableClasses" @click="handleClick">
                    </DataTable>
                </div>
            </div>
            <div>
                <br>
                <hr>
                <p class="headerzn">Check IMAP</p>
                <hr>
                <div class="row">
                    <div class="col-lg-6">
                        <p class="labelnew">IMAP</p>
                        <div class="custom-select" ref="imapDropdown">
                            <div class="select-selected" @click="toggleImapDropdown">{{ isEmpty(selectedImap) ? 'Select IMAP' : selectedImap }}</div>
                            <div v-if="imapDropdownOpen" class="select-items">
                                <div v-for="item in allowedStatuses" :key="item.id" @click="selectImap(item)">{{ item }}</div>
                            </div>
                        </div>
                        <p class="labelnew">Proxy</p>
                        <div class="custom-select" ref="proxyDropdown">
                            <div class="select-selected" @click="toggleProxyDropdown">{{ isEmpty(selectedProxy) ? 'Select Proxy' : selectedProxy }}</div>
                            <div v-if="proxyDropdownOpen" class="select-items">
                                <div v-for="item in allowedStatuses" :key="item.id" @click="selectProxy(item)">{{ item }}</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <br/>
                        <input v-model="timeout" style="margin-top: 1em;" type="text" class="form-control" aria-label="Small" placeholder="timeout">
                    </div>
                </div>
            </div>
            <div v-if="can_check">
                <button style="margin-top: 1em;" type="button" @click.prevent="checkSubmit" class="btn btn-primary">Submit</button>
            </div>
            <div v-else>
                <p class="headerzn">Please wait!</p>
            </div>
            <p class="text-danger">{{ errorCheck }}</p>
            <h3 class="headerzn">Progress</h3>
            <div class="progress">
                <div class="progress-bar" role="progressbar" :style=" 'background-color: #ef4444;'+'width: '+log_progress+'%'" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
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
    </div>
</template>

<script>
import axios from 'axios';
import NavBarComponent from './components/NavBarComponent.vue';
import HorizontalNavBar from "./components/HorizontalNavBar.vue";
import ModalViewComponent from './components/ModalViewComponent.vue';
import JSZip from 'jszip';
import { io } from 'socket.io-client';
import DataTable from 'datatables.net-vue3';

export default {
    components: {
        NavBarComponent,
        HorizontalNavBar,
        ModalViewComponent,
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
            proxies: null,
            timeout: null,
            errorCheck: null,
            log_progress: null,
            log_error: null,
            log_valid: null,
            logs: [],
            can_check: true,
            imapsData: [],
            imapTextInput : '',
            selectedImaps: [],
            imapsColumns: [
                { 
                    title: 'Select',
                    data: 'id',
                    render: (data, type, row) => {
                        return `<input type="checkbox" class="form-check-input" data-id="${data}" data-server="${row.server}" ${this.selectedImaps.some(item => item.id === data) ? 'checked' : ''}>`;
                    },
                    className: 'data-cell'
                },
                { title: 'ID', data: 'id',className: 'data-cell' },
                { title: 'Server', data: 'server',className: 'data-cell' },
                { title: 'Port', data: 'port',className: 'data-cell' },
                { title: 'User', data: 'user',className: 'data-cell' },
                { title: 'Pw', data: 'pw',className: 'data-cell' },
                { title: 'STATUS', data: 'status', render: (data) => {
                    return `<a href="#" class="btn btn-${data}">${data}</a>`;
                }},
                { title: 'DELETE', data: 'id', render: (data) => {
                    return `<button class="btn btn-danger" data-action="delete" data-id="${data}"><i class="bi bi-dash"></i></button>`;
                }},
                { title: 'Check B/L', data: 'id', render: (data) => {
                    return `<button class="btn btn-info" data-action="checkIMAP" data-id="${data}"><i class="bi bi-check"></i></button>`;
                }}
            ],
            tableClasses: 'table text-start align-middle table-bordered table-hover mb-0',
            selectedImap: {},
            selectedProxy: {},
            imapDropdownOpen: false,
            proxyDropdownOpen: false,
            allowedStatuses: ['all','inbox', 'junk', 'dead', 'none', 'checked']
        };
    },
    methods: {
        isEmpty(obj) {
            return Object.keys(obj).length === 0;
        },
        saveSelection() {
            localStorage.setItem('selectedImaps', JSON.stringify(this.selectedImaps));
        },
        loadSelection() {
            this.selectedImaps = JSON.parse(localStorage.getItem('selectedImaps') || '[]');
        },
        getMaterials() {
            const currentSessionName = this.getCurrentSessionName();
            if (!currentSessionName) {
                this.errorSubTemplates = 'No session loaded';
                return;
            }
            axios.get(`${this.$store.state.back_url}/api/get/list/proxies/${currentSessionName}`).then(res => {this.proxies = res.data});
            axios.get(`${this.$store.state.back_url}/api/get/list/imaps/${currentSessionName}`)
                .then(res => {
                    this.materials = res.data;
                    this.imapsData = res.data.map(item => ({
                        id: item.id,
                        server: item.server,
                        port: item.port,
                        user: item.email,
                        pw: item.password,
                        status: item.status
                    }));
                })
                .catch(error => {
                    console.error('Error fetching templates:', error);
                });
        },
        getCurrentSessionName() {
            const name = document.cookie.split('; ').find(row => row.startsWith('currentSessionName='));
            return name ? name.split('=')[1] : null;
        },
        toggleSelection(id, server) {
            const index = this.selectedImaps.findIndex(item => item.id === id);
            if (index !== -1) {
                this.selectedImaps.splice(index, 1);
            } else {
                this.selectedImaps.push({ id, server });
            }
            console.log(this.selectedImaps);
        },
        deleteLog() {
         this.logs = [];
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

        axios.post(`${this.$store.state.back_url}/api/del/log`, {
            token: token,
            session: session,
            type: 'imaps'
        })
        .then(response => {
            if (response.data.data === 'success') {
            this.logs = this.logs.filter(log => log.id !== logId);
            } else {
            this.error = response.data.error;
            }
            this.fetchLogs()
        })
        .catch(error => {
            this.error = 'Error deleting log: ' + error.message;
        });
        },
        handleClick(event) {
            const action = event.target.getAttribute('data-action');
            const id = event.target.getAttribute('data-id');

            if (action === 'view') {
                this.view(id);
            } else if (action === 'delete') {
                this.del(id);
            }else if (action === 'checkIMAP')
            {
                this.checkIMAP(id);
            }
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
        submit() {
            const currentSessionName = this.getCurrentSessionName();
            if (!currentSessionName) {
                this.errorSubTemplates = 'No session loaded';
                return;
            }
            let token = '';
            document.cookie.split(';').forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split('=')[1];
                }
            });
            this.errorSub = '';
            if (this.file || this.imapTextInput) {
                let imapArray = this.imapTextInput.split('\n').map(imap => imap.trim()).filter(imap => imap);
                let fileContent = this.file ? this.file : imapArray.join('\n');
                axios.post(`${this.$store.state.back_url}/api/input/material`, {
                    token: token,
                    session: currentSessionName,
                    type: 'imaps',
                    file: fileContent,
                    fileName: this.fileName || ''
                }).then(res => {
                    this.getMaterials();
                    this.$refs.inputEl1.value = '';
                    this.imapTextInput = '';
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
            this.file = null;
        },
        del(id) {
            let token = '';
            document.cookie.split(';').forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split('=')[1];
                }
            });
            axios.post(`${this.$store.state.back_url}/api/del/material`, { token: token, id: id, type: 'imaps' })
                .then(res => {
                    if (res.data.data === 'success') {
                        this.getMaterials();
                    } else {
                        console.error('Error deleting material:', res.data.error);
                    }
                })
                .catch(error => {
                    console.error('Error deleting material:', error);
                });
        },
        get_zip_data(zip, files_keys, data, callback) {
            zip.files[files_keys[0]].async('string').then(el_data => {
                files_keys.shift();
                callback(data = data + '\n' + el_data);
                if (files_keys.length > 0) {
                    this.get_zip_data(zip, files_keys, data, () => {});
                } else {
                    this.file = data;
                }
            });
        },
        fileUpload(event) {
            if (event.target.getAttribute('id') == 'formFile1') {
                event.target.files[0].arrayBuffer().then((buffer) => {
                    const bufferByteLength = buffer.byteLength;
                    const bufferUint8Array = new Uint8Array(buffer, 0, bufferByteLength);
                    this.file = new TextDecoder().decode(bufferUint8Array);
                });
            }
        },
        view(id) {
            axios.get(`${this.$store.state.back_url}/api/get/materials/${id}`).then(res => {
                let modalData = [];
                res.data.forEach(el => {
                    delete el[1];
                    modalData.push(el);
                });
                this.$refs.modal.data = res.data;
                this.$refs.modal.show = true;
            });
        },
        checkSubmit() {
            this.logs = [];
            console.log(this.check_file);
            console.log(this.timeout);
            console.log(this.proxy_form);
            let token = '';
            document.cookie.split(';').forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split('=')[1].trim();
                }
            });
            this.errorCheck = null;

            if (this.check_file && this.timeout && this.proxy_form) {
                this.can_check = false;

                const postData = {
                    token: token,
                    session: this.getCurrentSessionName(),
                    imap_id: this.check_file,
                    proxy_id: this.proxy_form,
                    timeout: this.timeout
                };

                axios.post(`${this.$store.state.back_url}/api/check/imap`, postData)
                    .then(res => {
                        if (res.data.data == 'error') {
                            this.can_check = true;
                            this.errorCheck = res.data.error;
                        }
                    })
                    .catch(error => {
                        console.error('Error IMAP:', error);
                        this.can_check = true;
                        this.errorCheck = 'Error IMAP. Try again.';
                    });
            } else {
                this.errorCheck = 'Fill in the fields!';
            }
        },
        checkIMAP(id) {
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

                axios.post(`${this.$store.state.back_url}/api/check/imapp`, {
                    token: token,
                    session: this.getCurrentSessionName(),
                    imap_id: id,
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
        fetchLogs() {
            const currentSessionName = this.getCurrentSessionName();
            const logType = 'imaps';
            if (!currentSessionName) {
                return;
            }

            axios.get(`${this.$store.state.back_url}/api/logs/${logType}/${currentSessionName}`)
                .then(res => {
                    console.log(res.data);
                    this.logs = res.data.data;
                })
                .catch(error => {
                    console.error('Error fetching logs:', error);
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
        selectImap(item) {
            this.selectedImap = item;
            this.check_file = item;
            this.imapDropdownOpen = false;
        },
        selectProxy(item) {
            this.selectedProxy = item;
            this.proxy_form = item;
            this.proxyDropdownOpen = false;
        },
        handleClickOutside(event) {
            if (!this.$refs.imapDropdown.contains(event.target)) {
                this.imapDropdownOpen = false;
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

            axios.post(`${this.$store.state.back_url}/api/input/log/imaps/${currentSessionName}`, {
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
        exportToTxt() {
            const data = this.imapsData.map(item => `${item.server},${item.port},${item.user},${item.pw},${item.status}`).join('\n');
            const blob = new Blob([data], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'imaps.txt';
            a.click();
            URL.revokeObjectURL(url);
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
        console.log(this.selectedImaps);
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
        this.connection = io.connect(this.$store.state.back_url);
        this.connection.on('message', (data) => {
            data = data.split(':');
            if (data[0] == 'progress_check_imaps') {
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
            } else if (data[0] == 'logs_check_imaps') {
                this.saveLog(data[2], data[1]);
                this.fetchLogs();
                this.addLogEntry({ TEXT: data[2], status: data[1] });
            }
        });
    }
};
</script>


<style scoped>
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

.col-lg-6, .col-lg-12 {
    margin-top: 2px;
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
/deep/ .form-check-input {
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

/deep/ .form-check-input:checked {
    background-color: var(--primary);
    border-color: var(--primary);
}

/deep/ .form-check-input:checked::after {

    display: block;
    color: white;
    font-size: 14px;
    text-align: center;
    line-height: 20px;
}
/deep/ .btn-dead{
    background-color: var(--primary) !important;
    color: #000;
    width: 100px;
    
}
/deep/ .btn-junk{
    background-color: var(--primary) !important;
    color: #000;
    width: 100px;
}
/deep/ .btn-inbox{
    background-color: #2bff00!important;
    color: #000;
    width: 100px;
}
/deep/ .btn-none{
    background-color: var(--primary) !important;
    color: #000;
    width: 100px;
}
/deep/ .btn-checked{
    background-color: #2bff00 !important;
    color: #000;
    width: 100px;
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
