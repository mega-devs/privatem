<template>
    <NavBarComponent stateProp="proxies"/>
    <div class="container-fluid dummy-form">
        <div class="row">
            <h2 class="text-center headerzn">Proxies</h2>
            <hr>
            <div class="col-lg-6">
                <div class="row">
                    <div class="col-lg-6 mb-3">
                        <label for="formFile" class="form-label labelnew" style="color: white;">Input proxies.txt</label>
                        <input ref="inputEl1" class="form-control" type="file" id="formFile1" @change="fileUpload">
                    </div>
                    <div class="col-lg-6 mb-3">
                        <label for="formFile" class="form-label labelnew">Input proxies.zip</label>
                        <input ref="inputEl2" class="form-control" type="file" id="formFile2" @change="fileUpload">
                    </div>
                    <div class="col-lg-6 mb-3">
                        <label for="formText" class="form-label labelnew">Input Proxies</label>
                        <textarea ref="inputEl3" class="form-control" id="formText" v-model="proxyTextInput" placeholder="Enter multiple proxies separated by new lines"></textarea>
                    </div>
                    <div class="col-lg-6 mb-3">
                        <label for="formFileSettings" class="form-label labelnew">Import settings.json</label>
                        <input ref="inputElSettings" class="form-control" type="file" id="formFileSettings" @change="importSettings">
                    </div>
                    <div class="col-lg-6 mb-3">
                        <label for="formText" class="form-label labelnew">Input fetchUrl</label>
                        <textarea ref="inputElFetchUrl" class="form-control" id="formTextFetchUrl" v-model="fetchUrlInput" placeholder="Enter the fetch URL"></textarea>
                    </div>
                </div>
                <button type="button" @click.prevent="submit" class="btn btn-primary">Submit</button>&nbsp;
                <button type="button" @click="exportData" class="btn btn-primary">Export to TXT</button>
                <p class="text-danger">{{errorSub}}</p>
            </div>
            <div class="col-lg-6">
                <DataTable :data="proxiesData" :columns="proxiesColumns" :class="tableClasses" @click="handleClick">
                </DataTable>
            </div>
        </div>
        <div>
            <hr>
            <p class="headerzn">Check proxies</p>
            <hr>
            <div class="row">
                <div class="col-lg-6">
                    <select v-model="check_file" class="form-select">
                        <option v-for="item in allowedStatuses" :key="item.id" :value="item">{{ item }}</option>
                    </select>
                </div>
            </div>
        </div>
        <div v-if="can_check">
            <button style="margin-top: 1em;" type="button" @click.prevent="checkSubmit" class="btn btn-primary">Submit</button>
        </div>
        <div v-else>
            <p>Please wait!</p>
        </div>
        <p class="text-danger">{{errorCheck}}</p>
        <h3 class="headerzn">Progress</h3>
        <div class="progress">
            <div class="progress-bar" role="progressbar" :style="'width: '+log_progress+'%'" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
        <div class="row">
            <div class="col-lg-6">
                <p class="text-success">Valid: {{log_valid}}</p>
            </div>
            <div class="col-lg-6">
                <p class="text-danger">Errors: {{log_error}}</p>
            </div>
        </div>
        <div>
            <h3 class="headerzn">Console</h3>
            <div id="console-output" ref="consoleOutput">
                <template v-for="(item, index) in logs" :key="index">
                    <span :class="item['status']">{{item['TEXT']}}<br/></span>
                </template>
            </div>
            <button @click="deleteLog()" class="btn btn-primary btn-delete">Delete</button>
        </div>
    </div>
    <ModalViewComponent ref="modal"></ModalViewComponent>
</template>

<script>
import axios from 'axios';
import NavBarComponent from './components/NavBarComponent.vue';
import ModalViewComponent from './components/ModalViewComponent.vue'
import JSZip from 'jszip';
import { io } from "socket.io-client";
import DataTable from 'datatables.net-vue3';

export default {
    components: {
        NavBarComponent,
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
            check_file_name: null,
            can_check: true,
            log_error: null,
            log_valid: null,
            log_progress: null,
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
                { title: 'ID', data: 'id', className: 'data-cell' },
                { title: 'IP', data: 'ip', className: 'data-cell' },
                { title: 'Port', data: 'port', className: 'data-cell' },
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
                        return `<button class="btn btn-danger" data-action="delete" data-id="${data}"><i class="bi bi-dash"></i></button>`;
                    }
                },
                {
                    title: 'Check', data: 'id', render: (data) => {
                        return `<button class="btn btn-info" data-action="check" data-id="${data}"><i class="bi bi-dash"></i></button>`;
                    }
                }
            ],
            tableClasses: 'table text-start align-middle table-bordered table-hover mb-0',
            fetchUrlInput: '',
            settingsFileContent: null 
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
            axios.get(`${this.$store.state.back_url}/api/get/list/proxies/${currentSessionName}`)
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
                axios.post(`${this.$store.state.back_url}/api/input/material`, {
                    token: token,
                    session: currentSessionName,
                    type: 'proxies',
                    file: fileContent,
                    fileName: this.fileName || ''
                }).then(res => {
                    if (res.data.data === 'error') {
                        this.errorSub = res.data.error;
                    }
                }).catch(error => {
                    this.errorSub = 'An error occurred during submission.';
                    console.error('Submission error:', error);
                });
            }

            if (this.settingsFileContent || this.fetchUrlInput) {
                const settingsData = this.settingsFileContent || {};
                if (this.fetchUrlInput) {
                    settingsData.fetch_url = this.fetchUrlInput;
                }

                axios.post(`${this.$store.state.back_url}/api/update/settings_from_json`, {
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

            this.getMaterials();
            this.$refs.inputEl1.value = '';
            this.proxyTextInput = '';
        },
        toggleSelection(id, ip) {
            const index = this.selectedProxies.findIndex(item => item.id === id);
            if (index !== -1) {
                this.selectedProxies.splice(index, 1);
            } else {
                this.selectedProxies.push({ id, ip });
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
            axios.post(`${this.$store.state.back_url}/api/del/material`, { token: token, id: id, type: 'proxies' })
                .then(res => {
                    this.getMaterials();
                });
        },
        get_zip_data(zip, files_keys, data, callback) {
            zip.files[files_keys[0]].async("string").then(el_data => {
                files_keys.shift();
                callback(data = data + '\n' + el_data);
                if (files_keys.length > 0) {
                    this.get_zip_data(zip, files_keys, data, () => { });
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

            axios.post(`${this.$store.state.back_url}/api/input/log/proxies/${currentSessionName}`, {
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
            if (event.target.getAttribute('id') == 'formFile1') {
                this.$refs.inputEl2.value = ''
                event.target.files[0].arrayBuffer().then((buffer) => {
                    const bufferByteLength = buffer.byteLength;
                    const bufferUint8Array = new Uint8Array(buffer, 0, bufferByteLength);
                    this.file = new TextDecoder().decode(bufferUint8Array);
                });
            } else if (event.target.getAttribute('id') == 'formFile2') {
                this.$refs.inputEl1.value = ''
                event.target.files[0].arrayBuffer().then((buffer) => {
                    const zip = new JSZip();
                    zip.loadAsync(buffer).then(zip => {
                        let data = '';
                        let files = zip.files;
                        let files_keys = Object.keys(files);
                        this.get_zip_data(zip, files_keys, data, () => { });
                    });
                });
            }
        },
        view(id) {
            axios.get(`${this.$store.state.back_url}/api/get/materials/${id}`).then(res => {
                let modalData = []
                res.data.forEach(el => {
                    delete el[1]
                    modalData.push(el)
                })
                this.$refs.modal.data = res.data
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

            axios.post(`${this.$store.state.back_url}/api/del/log`, {
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
                this.logs.push(logEntry);
                this.$nextTick(() => {
                     const consoleOutput = this.$refs.consoleOutput;
                     if (consoleOutput) {
                         consoleOutput.scrollTop = consoleOutput.scrollHeight;
                     }
                });
        },
        handleClick(event) {
            const action = event.target.getAttribute('data-action');
            const id = event.target.getAttribute('data-id');

            if (action === 'view') {
                this.view(id);
            } else if (action === 'delete') {
                this.del(id);
            }
        },
        fetchLogs() {
            const currentSessionName = this.getCurrentSessionName();
            const logType = 'proxies';
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

                axios.post(`${this.$store.state.back_url}/api/check/proxy`, {
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
            const blob = new Blob([rows], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'proxies.txt';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
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
    },
    mounted() {
        this.loadSelection();
        this.getMaterials();
        this.fetchLogs();
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
        this.connection = io.connect(this.$store.state.back_url)
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
                this.addLogEntry({ TEXT: data[2], status: data[1] });
            }
        })
    }
}
</script>

<style scoped>
.dummy-form {
    overflow: auto;
    margin-top: 2em;
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
    background-color: #2bff00!important;
    color: #000;
    width: 100px;
}
/deep/ .btn-none {
    background-color: var(--primary) !important;
    color: #000;
    width: 100px;
}
/deep/ .btn-checked {
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

</style>
