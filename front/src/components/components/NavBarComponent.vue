<template>
    <div class="vh-100 d-flex flex-column flex-shrink-0 p-3 position-fixed start-0 top-0 content">
     
        <ul class="nav nav-pills flex-column mb-auto">
            <template v-if="stateProp == 'home'">
                <li class="nav-item">
                    <RouterLink to="/dashboard" style="text-decoration: none;">
                        <a class="nav-link active">
                            <svg class="bi pe-none me-2" width="16" height="16"></svg>
                            <i class="bi bi-house"></i> <span>Home</span>
                        </a>
                    </RouterLink>
                </li>
            </template>
            <template v-else>
                <li class="nav-item">
                    <RouterLink to="/dashboard" style="text-decoration: none;">
                        <a class="nav-link text-white">
                            <svg class="bi pe-none me-2" width="16" height="16"></svg>
                            <i class="bi bi-house"></i> <span>Home</span>
                        </a>
                    </RouterLink>
                </li>
            </template>
            <template v-if="stateProp == 'templates'">
            <li class="nav-item">
                <RouterLink to="/dashboard/templates" style="text-decoration: none;">
                    <a class="nav-link active">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-file-earmark"></i> <span>Templates</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-else>
            <li class="nav-item">
                <RouterLink to="/dashboard/templates" style="text-decoration: none;">
                    <a class="nav-link text-white">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-file-earmark"></i> <span>Templates</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-if="stateProp == 'proxies'">
            <li class="nav-item">
                <RouterLink to="/dashboard/proxies" style="text-decoration: none;">
                    <a class="nav-link active">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-hdd-stack"></i> <span>Proxies</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-else>
            <li class="nav-item">
                <RouterLink to="/dashboard/proxies" style="text-decoration: none;">
                    <a class="nav-link text-white">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-hdd-stack"></i> <span>Proxies</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-if="stateProp == 'SMTPs'">
            <li class="nav-item">
                <RouterLink to="/dashboard/SMTPs" style="text-decoration: none;">
                    <a class="nav-link active">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-mailbox"></i> <span>SMTPs</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-else>
            <li class="nav-item">
                <RouterLink to="/dashboard/SMTPs" style="text-decoration: none;">
                    <a class="nav-link text-white">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-mailbox"></i> <span>SMTPs</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-if="stateProp == 'IMAPs'">
            <li class="nav-item">
                <RouterLink to="/dashboard/IMAPs" style="text-decoration: none;">
                    <a class="nav-link active">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-inbox"></i> <span>IMAPs</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-else>
            <li class="nav-item">
                <RouterLink to="/dashboard/IMAPs" style="text-decoration: none;">
                    <a class="nav-link text-white">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-inbox"></i> <span>IMAPs</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-if="stateProp == 'domains'">
            <li class="nav-item">
                <RouterLink to="/dashboard/domains" style="text-decoration: none;">
                    <a class="nav-link active">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-router"></i> <span>Domains</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-else>
            <li class="nav-item">
                <RouterLink to="/dashboard/domains" style="text-decoration: none;">
                    <a class="nav-link text-white">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-router"></i> <span>Domains</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-if="stateProp == 'bases'">
            <li class="nav-item">
                <RouterLink to="/dashboard/bases" style="text-decoration: none;">
                    <a class="nav-link active">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-person-lines-fill"></i> <span>Bases</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-else>
            <li class="nav-item">
                <RouterLink to="/dashboard/bases" style="text-decoration: none;">
                    <a class="nav-link text-white">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-person-lines-fill"></i> <span>Bases</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-if="stateProp == 'test'">
            <li class="nav-item">
                <RouterLink to="/dashboard/test" style="text-decoration: none;">
                    <a class="nav-link active">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-patch-check"></i> <span>Test mode</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-else>
            <li class="nav-item">
                <RouterLink to="/dashboard/test" style="text-decoration: none;">
                    <a class="nav-link text-white">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-patch-check"></i> <span>Test mode</span>
                    </a>
                </RouterLink>
            </li>
            </template>
             <template v-if="stateProp == 'sendx'">
            <li class="nav-item">
                <RouterLink to="/dashboard/sendx" style="text-decoration: none;">
                    <a class="nav-link active">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-patch-check"></i> <span>SendX mode</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-else>
            <li class="nav-item">
                <RouterLink to="/dashboard/sendx" style="text-decoration: none;">
                    <a class="nav-link text-white">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-patch-check"></i> <span>SendX mode</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-if="stateProp == 'mailing'">
            <li class="nav-item">
                <RouterLink to="/dashboard/mailing" style="text-decoration: none;">
                    <a class="nav-link active">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-envelope"></i> <span>Mailing</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-else>
            <li class="nav-item">
                <RouterLink to="/dashboard/mailing" style="text-decoration: none;">
                    <a class="nav-link text-white">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-envelope"></i> <span>Mailing</span>
                    </a>
                </RouterLink>
            </li>
            </template>
            <template v-if="stateProp == 'resetz'">
                <li class="nav-item">
                    <RouterLink to="/dashboard/resetz" style="text-decoration: none;">
                        <a class="nav-link active">
                            <svg class="bi pe-none me-2" width="16" height="16"></svg>
                            <i class="bi bi-trash"></i> <span>Reset</span>
                        </a>
                    </RouterLink>
                </li>
            </template>
            <template v-else>
            <li class="nav-item">
                <RouterLink to="/dashboard/resetz" style="text-decoration: none;">
                    <a class="nav-link text-white">
                        <svg class="bi pe-none me-2" width="16" height="16"></svg>
                        <i class="bi bi-trash"></i> <span>Reset</span>
                    </a>
                </RouterLink>
            </li>
            </template>

            <hr>
        </ul>
    <ul class="nav nav-pills flex-column mb-auto fixcss">
        <li>Loaded Session: <span class="session-name" style="width: 80px !important; display: inline-block; overflow: hidden; text-overflow: ellipsis;">{{ currentSessionName }}</span></li>
        <li>Total SMTPs: {{ totalSmtps }}</li>
        <li>Valid SMTPs: {{ validSmtps }}</li>
        <li>Dead SMTPs: {{ deadSmtps }}</li>
        <li>Inbox SMTPs: {{ inboxSmtps }}</li>
        <li>Junk SMTPs: {{ junkSmtps }}</li>
        <li>TEMPLATES: {{ templatesLoaded }}</li>
        <li>DOMAINS: {{ domainsLoaded }}</li>
        <li>SOCKS: {{ socksLoaded }}</li>
        <li>MAILER STATUS: <span :class="mailerStatusClass">{{ mailerStatus }}</span></li>
        <li><br><button @click="reset" class="btn-reset">Reset</button></li>
    </ul>
</div>
</template>

<script>
import axios from 'axios';
export default {
    props: ['stateProp'],
    data() {
        return {
            totalSmtps: 'X',
            validSmtps: 'X',
            deadSmtps: 'X',
            inboxSmtps: 'X',
            junkSmtps: 'X',
            templatesLoaded: 'X', // Replace 'X' with actual value or bind it dynamically
            domainsLoaded: 'X', // Replace 'X' with actual value or bind it dynamically
            socksLoaded: 'X', // Replace 'X' with actual value or bind it dynamically
            mailerStatus: 'STOPPED',
            currentSessionName: this.getCurrentSessionName()
        }
    },
    computed: {
        mailerStatusClass() {
            return this.mailerStatus === 'STOPPED' ? 'text-danger' : 'text-success';
        }
    },
    methods: {
        reset() {
            // Remove the current session name from cookies
            document.cookie = 'currentSessionName=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            // Refresh the page
            window.location.reload();
        },
        getCurrentSessionName() {
            const name = document.cookie.split('; ').find(row => row.startsWith('currentSessionName='));
            return name ? name.split('=')[1] : null;
        },
        fetchcounts() {
            const currentSessionName = this.getCurrentSessionName();
            if (!currentSessionName) {
                return;
            }

            axios.get(`${this.$store.state.back_url}/api/count/${currentSessionName}`)
                .then(res => {
                    console.log(res.data);
                    this.totalSmtps = res.data.count['count'];
                    this.validSmtps = res.data.count['valid'];
                    this.deadSmtps = res.data.count['dead'];
                    this.inboxSmtps = res.data.count['inbox'];
                    this.junkSmtps = res.data.count['junk'];
                    this.templatesLoaded = res.data.count['templates'];
                    this.domainsLoaded = res.data.count['domains'];
                    this.socksLoaded = res.data.count['socks'];
                })
                .catch(error => {
                    console.error('Error fetching logs:', error);
                });
        }
    },
    mounted() {
        this.fetchcounts();
    },
    
    watch: {
        currentSessionName(newValue, oldValue) {
            // Watch for changes in the current session name, if needed
        }
    }
}
</script>

<style>
:root {
    --primary: #EB1616;
    --secondary: #191C24;
    --light: #6C7293;
    --dark: #000000;
}

.content {
  border-right: 1px solid gray;

}

hr {
  border: 1px solid grey !important;
}

.nav-item {
  color: white;
}

.nav-link:hover {
  color: var(--primary) !important;
}

.nav-item .active {
    color: var(--primary) !important;
    background-color: transparent !important;
}

.fixcss2 {
    margin-bottom: 40%;
}
.fixcss {
    margin-top: 5%;
    margin-left: 8%;
}
.btn-reset {
    margin-top: -1em;
    margin-left: 13px;
    padding: 5px 10px;
    background-color: red;
    border: none;
    color: #ffffff;
    border-radius: 4px;
    cursor: pointer;
}

.labelnew{
    /* color:rgb(17, 212, 27); */
    color:#97c2ee;
    font-weight:bold;
    margin-bottom: 3%;
}
.headerzn{
    color:#97c2ee;
}
.session-name {
            color: #ffffff; /* Замените "red" на любой цвет, который вам нужен */
  width: 10px !important;
  text-overflow: ellipsis !important;
}
</style>