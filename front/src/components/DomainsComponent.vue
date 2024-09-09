<template>
    <NavBarComponent stateProp="domains"/>
    <div class="container-fluid dummy-form">
        <div class="row">
            <h2 class="text-center headerzn text-light">Domains</h2>
            <hr class="bg-light">
            <div class="col-lg-8">
                <div class="row">
                    <div class="col-lg-6 mb-3">
                        <label for="formFile1" class="form-label labelnew text-light">Input domains.txt</label>
                        <input ref="inputEl1" class="form-control bg-dark text-light border-secondary" type="file" id="formFile1" @change="fileUpload">
                    </div>
                    <div class="col-lg-6 mb-3">
                          <label for="formText" class="form-label labelnew text-light">Input domains</label>
                          <textarea ref="inputEl3" class="form-control bg-dark text-light border-secondary" id="formText" v-model="domainTextInput" placeholder="Enter multiple domains separated by new lines"></textarea>
                    </div>
                </div>
                <button type="button" @click.prevent="submit" class="btn btn-primary">Submit</button>&nbsp;
                <button type="button" @click.prevent="exportData" class="btn btn-primary">Export to TXT</button>
                <p class="text-danger">{{ errorSub }}</p>
            </div>
            <hr class="bg-light">
            <div class="col-lg-12">
                <DataTable :data="domainsData" :columns="domainsColumns" :class="tableClasses" @click="handleClick">
                </DataTable>
            </div>
        </div>
        <div>
            <hr class="bg-light">
            <p class="headerzn text-light">Check Domains</p>
            <hr class="bg-light">
            <div class="row">
                <div class="col-lg-6">
                    <select v-model="check_file" class="form-select bg-dark text-light border-secondary">
                        <option v-for="item in allowedStatuses" :key="item" :value="item">{{ item }}</option>
                    </select>
                </div>
            </div>
        </div>
        <div v-if="can_check">
            <button style="margin-top: 1em;" type="button" @click.prevent="checkSubmit2" class="btn btn-primary">Submit</button>
        </div>
        <div v-else>
            <p class="text-light">Please wait!</p>
        </div>
        <p class="text-danger">{{ errorCheck }}</p>
        <h3 class="headerzn text-light">Progress</h3>
        <div class="progress">
            <div class="progress-bar bg-primary" role="progressbar" :style="'width: '+log_progress+'%'" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
        <div class="row">
            <div class="col-lg-6">
                <p class="text-success">Valid: {{ log_valid }}</p>
            </div>
            <div class="col-lg-6">
                <p class="text-danger">Errors: {{ log_error }}</p>
            </div>
        </div>
        <div>
            <h3 class="headerzn text-light">Console</h3>
            <div id="console-output">
                <template v-for="item in logs">
                    <span :class="item['status']">{{ item['TEXT'] }}<br/></span>
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
import ModalViewComponent from './components/ModalViewComponent.vue';
import DataTable from 'datatables.net-vue3';
import JSZip from 'jszip';
import { io } from "socket.io-client";

export default {
    components: {
        NavBarComponent,
        ModalViewComponent,
        DataTable
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
            log_progress: null,
            errorCheck: null,
            domainTextInput: '',
            logs: [],
            domainsData: [],
            allowedStatuses: ['all','inbox', 'junk', 'dead', 'none', 'checked'],
            selectedDomains: [],
            domainsColumns: [
                { 
                    title: 'Select',
                    data: 'id',
                    render: (data, type, row) => {
                        return `<input type="checkbox" class="form-check-input" data-id="${data}" data-url="${row.domain}" ${this.selectedDomains.some(item => item.id === data) ? 'checked' : ''}>`;
                    },
                    className: 'data-cell'
                },
                { title: 'ID', data: 'id', className: 'data-cell' },
                { title: 'Domain', data: 'domain', className: 'data-cell' },
                { 
                    title: 'STATUS', 
                    data: 'status', 
                    render: (data) => {
                        return `<a href="#" class="btn btn-${data}">${data}</a>`;
                    },
                    className: 'data-cell'
                },
                { 
                    title: 'DELETE', 
                    data: 'id', 
                    render: (data) => {
                        return `<button class="btn btn-danger" data-action="delete" data-id="${data}"><i class="bi bi-dash"></i></button>`;
                    },
                    className: 'data-cell'
                },
                { 
                    title: 'Check B/L', 
                    data: 'id', 
                    render: (data) => {
                        return `<button class="btn btn-info" data-action="checkDomain" data-id="${data}"><i class="bi bi-check"></i></button>`;
                    },
                    className: 'data-cell'
                }
            ],
            tableClasses: 'table text-start align-middle table-bordered table-hover mb-0'
        };
    },
    methods: {
        saveSelection() {
            localStorage.setItem('selectedDomains', JSON.stringify(this.selectedDomains));
        },
        loadSelection() {
            this.selectedDomains = JSON.parse(localStorage.getItem('selectedDomains') || '[]');
        },
        getMaterials() {
            const currentSessionName = this.getCurrentSessionName();
            if (!currentSessionName) {
                this.errorSub = 'No session loaded';
                return;
            }
            axios.get(`${this.$store.state.back_url}/api/get/list/domains/${currentSessionName}`)
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
        toggleSelection(id, url) {
            const index = this.selectedDomains.findIndex(item => item.id === id);
            if (index !== -1) {
                this.selectedDomains.splice(index, 1);
            } else {
                this.selectedDomains.push({ id, url });
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
            } else if (action === 'checkDomain') {
                this.checkSubmit(id);
            }
        },
        checkSubmit(id) {
            const currentSessionName = this.getCurrentSessionName();
            if (!currentSessionName) {
                this.errorCheck = 'No session loaded';
                return;
            }

            let token = '';
            let cookies = document.cookie.split(";");
            cookies.forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split("=")[1];
                }
            });

            this.logs = [];
            this.errorCheck = null;
            this.can_check = false;

            axios.post(`${this.$store.state.back_url}/api/check/domain`, {
                token: token,
                session: currentSessionName,
                socket: this.connection.id,
                domain_id: id
            }).then(res => {
                if (res.data.data === 'error') {
                    this.can_check = true;
                    this.errorCheck = res.data.error;
                }
            }).catch(error => {
                this.can_check = true;
                this.errorCheck = 'Error checking domain: ' + error.message;
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
            if (this.file || this.domainTextInput) {
                let domainArray = this.domainTextInput.split('\n').map(domain => domain.trim()).filter(domain => domain);
                let fileContent = this.file ? this.file : domainArray.join('\n');
                axios.post(`${this.$store.state.back_url}/api/input/material`, {
                    token: token,
                    session: currentSessionName,
                    type: 'domains',
                    file: fileContent,
                    fileName: this.fileName || ''
                }).then(res => {
                    this.getMaterials();
                    this.$refs.inputEl1.value = '';
                    this.domainTextInput = '';
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
            let token = ''
            let cookies = document.cookie.split(";")
            cookies.forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split("=")[1];
                }
            })
            axios.post(`${this.$store.state.back_url}/api/del/material`, {token: token, id: id, type:'domains'}).then(res => {this.getMaterials()})
        },
        get_zip_data(zip, files_keys, data, callback) {
            zip.files[files_keys[0]].async("string").then(el_data => {
                files_keys.shift()
                callback(data = data + '\n' + el_data)
                if ( files_keys.length > 0 ) {
                    this.get_zip_data(zip, files_keys, data, () => {})
                } else {
                    this.file = data
                }
            })
        },
        fileUpload(event) {
            const file = event.target.files[0];
            this.fileName = file.name;

            if (event.target.getAttribute('id') === 'formFile1') {
                file.arrayBuffer().then((buffer) => {
                    const bufferByteLength = buffer.byteLength;
                    const bufferUint8Array = new Uint8Array(buffer, 0, bufferByteLength);
                    this.file = new TextDecoder().decode(bufferUint8Array);
                });
            } else if (event.target.getAttribute('id') === 'formFile2') {
                this.$refs.inputEl1.value = '';
                file.arrayBuffer().then((buffer) => {
                    const zip = new JSZip();
                    zip.loadAsync(buffer).then((zip) => {
                        let data = '';
                        let files = zip.files;
                        let files_keys = Object.keys(files);
                        this.get_zip_data(zip, files_keys, data, () => {});
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
            })
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

            axios.post(`${this.$store.state.back_url}/api/input/log/domains/${currentSessionName}`, {
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
            const logType = 'domains';
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
                type: 'domains'
            })
            .then(response => {
                if (response.data.data === 'success') {
                    this.logs = "";
                    fetchLogs();  // Fetch logs to ensure the latest data is shown
                } else {
                    this.error = response.data.error;
                }
            })
            .catch(error => {
                this.error = 'Error deleting log: ' + error.message;
            });
        },
        checkSubmit2() {
            this.logs = [];
            let token = '';
            let cookies = document.cookie.split(";");
            cookies.forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split("=")[1];
                }
            });
            this.errorCheck = null;

            // Ensure check_file is referred correctly
            if (this.check_file) {
                this.can_check = false;
                console.log(this.check_file)
                const currentSessionName = this.getCurrentSessionName();
                if (!currentSessionName) {
                    this.errorCheck = 'No session loaded';
                    return;
                }

                axios.post(`${this.$store.state.back_url}/api/check/domain`, {
                    token: token,
                    session: currentSessionName,
                    socket: this.connection.id,  // assuming you have access to the socket ID
                    domain_id: this.check_file
                }).then(res => {
                    if (res.data.data === 'error') {
                        this.can_check = true;
                        this.errorCheck = res.data.error;
                    }
                }).catch(error => {
                    this.can_check = true;
                    this.errorCheck = 'Error checking domains: ' + error.message;
                });
            } else {
                this.errorCheck = 'Fill in the fields!';
            }
        },
        exportData() {
            const data = this.domainsData.map(domain => `${domain.domain}\t${domain.status}`).join('\n');
            const blob = new Blob([data], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'domains.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    },
    mounted() {
        this.loadSelection(); // Load the selected domains from local storage
        this.getMaterials();
        this.fetchLogs();
        console.log(this.selectedDomains)
        // Add event listener to the table for handling checkbox changes
        document.querySelector('.table').addEventListener('change', (event) => {
            if (event.target.classList.contains('form-check-input')) {
                const id = parseInt(event.target.getAttribute('data-id'));
                const url = event.target.dataset.url; // Ensure the server attribute is available in the dataset
                this.toggleSelection(id, url);
                this.saveSelection();
            }
        });
    },
    created() {
        this.connection = io.connect(this.$store.state.back_url);
        this.connection.on('message', (data) => {
            data = data.split(":");
            if (data[0] == 'progress_check_domain') {
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
            } else if (data[0] == 'logs_check_domain') {
                const logText = `${data[2]}:${data[3]}`;
                this.logs.push({'status': data[1], 'TEXT': logText});
                console.log(logText);
                this.saveLog(logText, data[1]);
                this.fetchLogs();
            }
        });
    }
}
</script>

<style scoped>
:root {
    --primary: #EB1616; /* Красный цвет */
    --secondary: #191C24; /* Темный цвет фона */
    --light: #6C7293;
    --dark: #000000;
}
.dummy-form {
    margin-left: 20em;
    margin-right: 10em;
    margin-top: 2em;
    width: auto;
}
#console-output {
  bottom: 0;
  left: 0;
  width: 100%;
  height: 200px;
  background-color: #000;
  color: #fff;
  overflow: scroll;
  z-index: 9999;
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

.text-light {
    color: #ddd !important;
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
    background-color: var(--dark);
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
    background-color: #ff0000 !important;
    color: #000;
    width: 100px;
    
}
/deep/ .btn-junk{
    background-color: #ff0000 !important;
    color: #000;
    width: 100px;
}
/deep/ .btn-inbox{
    background-color: #2bff00!important;
    color: #000;
    width: 100px;
}
/deep/ .btn-none{
    background-color: #ff0000 !important;
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
  background-color: red;
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

.text-success {
  color: limegreen !important;
}

.text-danger {
  color: red !important;
}
</style>
