<template>
    <NavBarComponent stateProp="test"/>
    <div class="container-fluid dummy-form">
        <!-- Add Select Form -->
        <div class="form-selector">
            <label for="formType" style="margin-bottom: 1em;">Select Form Type:</label>
            <select v-model="formType" class="form-select" id="formType">
                <option value="main">Status Form</option>
                <option value="placeholder">Select Form</option>
            </select>
        </div>
        <!-- Status form -->
        <div v-if="formType === 'main'">
            <div>
                <h3 style="text-align: center; margin-top: 1em;">Select material</h3>
                <div class="row">
                    <div class="col-lg-6">
                        <div>
                            <p>Templates</p>
                            <select v-model="dummy_form" class="form-select">
                                <option v-for="item in allowedStatuses" :key="item['id']">{{item}}</option>
                            </select>
                        </div>
                        <div>
                            <p>Bases</p>
                            <div class="custom-select" ref="basesDropdown">
                                <div class="select-selected" @click="toggleBasesDropdown">{{ isEmpty(selectedBase) ? 'Select Base': selectedBase }}</div>
                                <div v-if="baseDropdownOpen" class="select-items">
                                    <div v-for="item in allowedStatuses" :key="item.id" @click="selectBase(item)">{{ item }}</div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <p>IMAP</p>
                            <div class="custom-select" ref="imapDropdown">
                                <div class="select-selected" @click="toggleImapDropdown">{{ isEmpty(selectedImap) ? 'Select IMAP': selectedImap }}</div>
                                <div v-if="imapDropdownOpen" class="select-items">
                                    <div v-for="item in allowedStatuses" :key="item.id" @click="selectImap(item)">{{ item }}</div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <p>Proxy</p>
                            <div class="custom-select" ref="proxyDropdown">
                                <div class="select-selected" @click="toggleProxyDropdown">{{ isEmpty(selectedProxy) ? 'Select Proxy' : selectedProxy }}</div>
                                <div v-if="proxyDropdownOpen" class="select-items">
                                    <div v-for="item in allowedStatuses" :key="item.id" @click="selectProxy(item)">{{ item }}</div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <p>Smtps</p>
                            <div class="custom-select" ref="smtpDropdown">
                                <div class="select-selected" @click="toggleSmtpDropdown">{{ isEmpty(selectedSmtp) ? 'Select SMTP': selectedSmtp }}</div>
                                <div v-if="smtpDropdownOpen" class="select-items">
                                    <div v-for="item in allowedStatuses" :key="item.id" @click="selectSmtp(item)">{{ item }}</div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <p>Domains</p>
                            <div class="custom-select" ref="domainDropdown">
                                <div class="select-selected" @click="toggleDomainDropdown">{{ isEmpty(selectedDomain) ? 'Select Domain': selectedDomain }}</div>
                                <div v-if="domainDropdownOpen" class="select-items">
                                    <div v-for="item in allowedStatuses" :key="item.id" @click="selectDomain(item)">{{ item }}</div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <p>base</p>
                            <input v-model="base_form_imap" class="form-control" type="text" placeholder="Input email`s IMAP">
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
                                <input v-model="sending_limit" type="text" class="form-control" aria-label="Small" placeholder="Sending limit">
                            </div>
                            <div class="col-lg-6">
                                <input v-model="emails_per_check" type="text" class="form-control" aria-label="Small" placeholder="Number of emails per check">
                                <input v-model="count_of_material" type="text" class="form-control" aria-label="Small" placeholder="Count of emails to validate">
                                <input v-model="threads_number" type="text" class="form-control" aria-label="Small" placeholder="Count of threads">
                            </div>
                        </div>
                        <div class="col-lg-12">
                            <p>Debug</p>
                            <div id="console-output">
                                <template v-for="item in mailing_logs" :key="item.timestamp">
                                    <span :class="item.level.toLowerCase()">{{ item.message }}<br/></span>
                                </template>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="can_run">
                    <div class="row">
                        <div class="col-lg-6">
                            <button style="margin-top: 1em;" type="button" @click.prevent="submit" class="btn btn-primary">Submit</button>
                            <p class="text-danger">{{errorCheck}}</p>
                        </div>
                        <div class="col-lg-6">
                            <!-- <input v-model="results_form" class="form-control" type="text" placeholder="Input name for file with results"> -->
                        </div>
                    </div>
                </div>
                <div v-else>
                    <p>Please wait!</p>
                </div>
            </div>
        </div>
        <div v-else>
            <h3 style="text-align: center;">Select Form</h3>
            <div class="row">
                <div class="col-lg-6" style="margin-top: 1em;">
                    <h4 class="text-center">Templates</h4>
                     <DataTable :data="selectedMaterials" :columns="templatesColumns" :class="tableClasses" @click="handleClick"></DataTable>
                </div>
                <div class="col-lg-6">
                    <h4 class="text-center">Bases</h4>
                     <DataTable :data="selectedBases" :columns="basesColumns" :class="tableClasses" @click="handleClick"></DataTable>
                </div>
                <div class="col-lg-6">
                    <h4 class="text-center">Selected SMTP</h4>
                            <DataTable :data="selectedSmtps" :columns="smtpsColumns" :class="tableClasses">
                    </DataTable>
                </div>
                <div class="col-lg-6">
                    <h4 class="text-center">Selected Proxy</h4>
                              <DataTable :data="selectedProxies" :columns="proxiesColumns" :class="tableClasses" >
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
                <div class="progress-bar" role="progressbar" :style="'width: '+log_progress+'%'" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <div class="row">
                <div class="col-lg-6">
                    <p class="text-success">Sended emails: {{ log_valid }}</p>
                    <p class="text-danger">Errors: {{ log_error }}</p>
                </div>
                <div class="col-lg-6">
                    <p>{{ status }}</p>
                    <button style="margin-top: 1em;" type="button" class="btn btn-primary">Stop</button>
                </div>
            </div>
        </div>
        <div>
            <h3>Console</h3>
            <div id="console-output">
                <template v-for="item in logs">
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
import ModalViewComponent from './components/ModalViewComponent.vue';
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
            dummy: [],
            proxies: [],
            smtps: [],
            domains: [],
            imaps: [],
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
            baseDropdownOpen:false,
            allowedStatuses: ['inbox', 'junk', 'checked'],
            allowedImapStatuses: ['checked'],
            imapsData: [],
            smtpsData: [],
            mailing_logs:[],
            proxiesData: [],
            domainsData: [],
            selectedImap: {},
            selectedProxies: {},
            selectedSmtp: {},
            selectedBases: {},
            selectedDomain: {},
            selectedSmtps: [],
            selectedDomains: [],
            selectedMaterials:[],
            selectedBase:{},
            smtpsColumns: [
                {
                    title: 'Select',
                    data: 'id',
                    render: (data, type, row) => {
                        return `<input type="checkbox" class="smtp-checkbox" data-id="${data}" data-server="${row.server}" ${this.selectedSmtps.some(item => item.id === data) ? 'checked' : ''}>`;
                    },
                    className: 'data-cell'

                },
                { title: 'ID', data: 'id',className: 'data-cell' },
                { title: 'Server', data: 'server' ,className: 'data-cell'},
                { title: 'STATUS', data: 'status', render: (data) => `<a href="#" class="btn btn-${data}">${data}</a>`,className: 'data-cell' },
                
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
                { title: 'ID', data: 'id',className: 'data-cell'},
                { title: 'IP', data: 'ip',className: 'data-cell'},
                { title: 'STATUS', data: 'status', render: (data) => {
                    return `<a href="#" class="btn btn-${data}">${data}</a>`;
                },className: 'data-cell'},
            ],
            fetchDebugs() {
            axios.get(`${this.$store.state.back_url}/api/debug`)
                .then(response => {
                    this.mailing_logs = response.data.logs;
                })
                .catch(error => {
                    console.error('Error fetching logs:', error);
                });
            },
            domainsColumns: [
                {
                    title: 'Select',
                    data: 'id',
                    render: (data, type, row) => {
                        return `<input type="checkbox" class="domain-checkbox" data-id="${data}" data-url="${row.domain}" ${this.selectedDomains.some(item => item.id === data) ? 'checked' : ''}>`;
                    },
                    className: 'data-cell'

                },
                { title: 'ID', data: 'id',className: 'data-cell' },
                { title: 'Domain', data: 'domain' ,className: 'data-cell'},
                { title: 'STATUS', data: 'status', render: (data) => {
                    return `<a href="#" class="btn btn-${data}">${data}</a>`;
                },className: 'data-cell'},
            ],
            templatesColumns:[
                {
                    title: 'Select',
                    data: 'id',
                    render: (data, type, row) => {
                        return `<input type="checkbox" class="templates-checkbox" data-id="${data}" data-url="${row.name}" ${this.selectedMaterials.some(item => item.id === data) ? 'checked' : ''}>`;
                    },
                    className: 'data-cell'
                },
                { title: 'NAME', data: 'name' },
                { title: 'VIEW', data: 'id', render: (data) => {
                    return `<button class="btn btn-primary" data-action="view" data-id="${data}">Open</button>`;
                },
                className: 'data-cell'},
                { title: 'DELETE', data: 'id', render: (data) => {
                    return `<button class="btn btn-danger" data-action="delete" data-id="${data}">Delete</button>`;
                },
                className: 'data-cell'}
            ],
            basesColumns:[
                {
                    title: 'Select',
                    data: 'id',
                    render: (data, type, row) => {
                        return `<input type="checkbox" class="bases-checkbox" data-id="${data}" data-url="${row.url}" ${this.selectedBases.some(item => item.id === data) ? 'checked' : ''}>`;
                    },
                    className: 'data-cell'
                },
                { title: 'NAME', data: 'url' },
                { title: 'VIEW', data: 'id', render: (data) => {
                    return `<button class="btn btn-primary" data-action="view" data-id="${data}">Open</button>`;
                },
                className: 'data-cell'},
                { title: 'DELETE', data: 'id', render: (data) => {
                    return `<button class="btn btn-danger" data-action="delete" data-id="${data}">Delete</button>`;
                },
                className: 'data-cell'}
            ],
            tableClasses: 'table text-start align-middle table-bordered table-hover mb-0',
            selectedProxy: {},
            imapDropdownOpen: false,
            proxyDropdownOpen: false,
            smtpDropdownOpen: false,
            domainDropdownOpen: false,
            formType: 'main',

        };
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
        saveSelectionBase() {
            localStorage.setItem('selectedBases', JSON.stringify(this.selectedBases));
        },
        loadSelectionBase()
        {
        this.selectedBases = JSON.parse(localStorage.getItem('selectedBases') || '[]');
        },
        isEmpty(obj) {
            return Object.keys(obj).length === 0;
        },
        fetchLogs() {
            const currentSessionName = this.getCurrentSessionName();
            const logType = 'testmode';
            if (!currentSessionName) {
                return;
            }

            axios.get(`${this.$store.state.back_url}/api/logs/${logType}/${currentSessionName}`)
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
            axios.get(`${this.$store.state.back_url}/api/imaps`)
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
            axios.get(`${this.$store.state.back_url}/api/proxies`)
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
            axios.get(`${this.$store.state.back_url}/api/smtps`)
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
            axios.get(`${this.$store.state.back_url}/api/domains`)
                .then(response => {
                    if (response.data && response.data.status === 'success') {
                        this.domains = response.data.domains;
                    }
                })
                .catch(error => {
                    console.error('Failed to fetch domains:', error);
                });
        },
        saveSelectionTemplates() {
            localStorage.setItem('selectedTemplates', JSON.stringify(this.selectedMaterials));
        },
        loadSelectionTemplates() {
        this.selectedMaterials = JSON.parse(localStorage.getItem('selectedTemplates') || '[]');
        },
        getMaterialsSMTP() {
            const currentSessionName = this.getCurrentSessionName();
            if (!currentSessionName) {
                this.errorSubTemplates = 'No session loaded';
                return;
            }
            axios.get(`${this.$store.state.back_url}/api/get/list/proxies/${currentSessionName}`).then(res => {
                this.proxies = res.data;
            });
            axios.get(`${this.$store.state.back_url}/api/get/list/smtps/${currentSessionName}`).then(res => {
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
        getMaterialsDomain() {
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
        toggleSelection(id, server) {
            const index = this.selectedSmtps.findIndex(item => item.id === id);
            if (index !== -1) {
                this.selectedSmtps.splice(index, 1);
            } else {
                this.selectedSmtps.push({ id, server });
            }
            console.log(this.selectedSmtps);
        },
        toggleSelectionProxy(id, ip) {
            const index = this.selectedProxies.findIndex(item => item.id === id);
            if (index !== -1) {
                this.selectedProxies.splice(index, 1);
            } else {
                this.selectedProxies.push({ id, ip });
            }
            console.log(this.selectedProxies);
        },
         toggleSelectionDomain(id, url) {
            const index = this.selectedDomains.findIndex(item => item.id === id);
            if (index !== -1) {
                this.selectedDomains.splice(index, 1);
            } else {
                this.selectedDomains.push({ id, url });
            }
            console.log(this.selectedDomains);
        },
        toggleSelectionBase(id, url) {
            const index = this.selectedBases.findIndex(item => item.id === id);
            if (index !== -1) {
                this.selectedBases.splice(index, 1);
            } else {
                this.selectedBases.push({ id, url });
            }
            console.log(this.selectedBases);
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
            console.log('Check smtps_form:', this.smtps_form);
            console.log('proxies_form:', this.proxies_form);
            console.log('domains_form form:', this.domains_form);
            console.log('imaps_form:', this.imaps_form);
            console.log('emails_per_check:', this.emails_per_check);
            console.log('delay_form:', this.delay_form);
            console.log('count_of_material:', this.count_of_material);
            console.log('timeout_form:', this.timeout_form);
            console.log('to_check:', this.to_check);
            console.log('dummy_form:', this.dummy_form);
            console.log('threads_number:', this.threads_number);
            console.log('sending_limit:', this.sending_limit);
            this.logs = []
            let token = ''
            let cookies = document.cookie.split(";")
            cookies.forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split("=")[1];
                }
            })
            this.errorCheck = null
            if (this.dummy_form && this.proxies_form && this.smtps_form && this.base_form && this.results_form && this.selectedBase && this.to_check) {
                this.can_run = false
                axios.post(`${this.$store.state.back_url}/api/start/test_mode`, {
                    token: token,
                    socket: socket,
                    session: this.getCurrentSessionName(),
                    sending_limit: this.sending_limit,
                    threads_number:this.threads_number,
                    timeout: this.timeout_form,
                    delay: this.delay_form,
                    emails_per_material: this.count_of_material,
                    emails_to_validate: this.emails_per_check,
                    smtp_form: this.smtps_form,
                    proxy: this.proxies_form,
                    imap: this.base_form_imap,
                    domain: this.domains_form,
                    template: this.dummy_form,
                    to_check: this.to_check,
                    results: this.results_form,
                }).then(res => {
                    this.status = res.data
                }).catch(error => {
                    this.errorCheck = error.response.data.detail
                })
                this.can_run = true
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
        selectBase(item) {
            this.selectedBase = item;
            this.baseDropdownOpen = false;
        },
        toggleDomainDropdown() {
            this.domainDropdownOpen = !this.domainDropdownOpen;
        },
        selectDomain(item) {
            this.selectedDomain = item;
            this.domainDropdownOpen = false;
        },
        getCurrentSessionName() {
            // Logic to get current session name
            return 'currentSession';
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

            axios.delete(`${this.$store.state.back_url}/api/logs/${logType}/${currentSessionName}`)
                .then(response => {
                    if (response.data && response.data.status === 'success') {
                        this.logs = [];
                    }
                })
                .catch(error => {
                    console.error('Failed to delete logs:', error);
                });
        }
    },
    mounted() {
       this.fetchLogs();
       this.fetchDebugs();
       this.fetchImaps();
       this.fetchProxies();
       this.fetchSmtps();
       this.fetchDomains();
       this.loadSelectionSMTP();
       this.loadSelectionDomain();
       this.loadSelectionProxy();
       this.getMaterialsSMTP();
       this.getMaterialsDomain();
       this.loadSelectionTemplates();
       this.loadSelectionBase();

       


    },
    beforeDestroy() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    created() {
        this.connection = io.connect(this.$store.state.back_url);
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
.dummy-form {
    margin-left: 20em;
    margin-right: 10em;
    margin-top: 2em;
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

#console-output {
  bottom: 0;
  left: 0;
  width: 100%;
  height: 200px;
  background-color: #000;
  color: #fff;
  overflow: scroll;
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
/deep/ .smtp-checkbox, /deep/ .proxies-checkbox, /deep/ .domain-checkbox,/deep/ .templates-checkbox, /deep/ .bases-checkbox {
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

/deep/ .smtp-checkbox:checked,/deep/ .proxies-checkbox:checked,/deep/ .domain-checkbox:checked,/deep/ .templates-checkbox:checked, /deep/ .bases-checkbox:checked {
    background-color: var(--primary);
    border-color: var(--primary);
}

/deep/ .smtp-checkbox:checked::after,/deep/ .proxies-checkbox:checked::after,/deep/ .domain-checkbox:checked::after,/deep/ .templates-checkbox:checked::after, /deep/ .bases-checkbox:checked::after {
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
/deep/ .btn-undefined{
    background-color: #ff0000 !important;
    color: #000;
    width: 100px;
}

/deep/ .btn-checked{
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
</style>
