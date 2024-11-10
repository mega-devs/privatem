<template>
    <NavBarComponent stateProp="resetz"/>
    <div id="main-part">
        <HorizontalNavBar stateProp="resetz"/>
        <div style="overflow-y: scroll">
          <header>
              <div class="container-fluid dummy-form">
                  <div class="form-group mt-3">
                      <label>Full Reset</label>&nbsp;&nbsp;
                      <button @click.prevent="fullReset" class="btn btn-primary">Delete all sessions and clean all</button>
                  </div>

                  <div class="form-group mt-3">
                      <label for="resetTemplates">Reset templates</label>
                      <select id="resetTemplates" class="form-control" v-model="resetTemplates">
                          <option value="all">Reset all templates</option>
                          <option value="status">Reset templates by status</option>
                      </select>
                      <div v-if="resetTemplates === 'status'" class="mt-2">
                          <label for="templateStatus">Select Status</label>
                          <select id="templateStatus" class="form-control" v-model="templateStatus">
                              <option value="active">Active</option>
                              <option value="inactive">Inactive</option>
                          </select>
                      </div>
                      <button @click.prevent="resetTemplatesAction" class="btn btn-primary mt-2">Execute</button>
                  </div>

                  <div class="form-group mt-3">
                      <label for="resetSmtp">Reset SMTP</label>
                      <select id="resetSmtp" class="form-control" v-model="resetSmtp">
                          <option value="all">Reset all SMTP status</option>
                          <option value="status">Reset SMTP by status</option>
                      </select>
                      <div v-if="resetSmtp === 'status'" class="mt-2">
                          <label for="smtpStatus">Select Status</label>
                          <select id="smtpStatus" class="form-control" v-model="smtpStatus">
                              <option value="active">Active</option>
                              <option value="inactive">Inactive</option>
                          </select>
                      </div>
                      <button @click.prevent="resetSmtpAction" class="btn btn-primary mt-2">Execute</button>
                  </div>

                  <div class="form-group mt-3">
                      <label for="resetDomains">Reset Domains</label>
                      <select id="resetDomains" class="form-control" v-model="resetDomains">
                          <option value="all">Reset all DOMAINs status</option>
                          <option value="status">Reset DOMAINs by status</option>
                      </select>
                      <div v-if="resetDomains === 'status'" class="mt-2">
                          <label for="domainStatus">Select Status</label>
                          <select id="domainStatus" class="form-control" v-model="domainStatus">
                              <option value="active">Active</option>
                              <option value="inactive">Inactive</option>
                          </select>
                      </div>
                      <button @click.prevent="resetDomainsAction" class="btn btn-primary mt-2">Execute</button>
                  </div>

                  <div class="form-group mt-3">
                      <label for="resetProxy">Reset proxy</label>
                      <select id="resetProxy" class="form-control" v-model="resetProxy">
                          <option value="all">Reset all proxy status</option>
                          <option value="status">Reset proxy by status</option>
                      </select>
                      <div v-if="resetProxy === 'status'" class="mt-2">
                          <label for="proxyStatus">Select Status</label>
                          <select id="proxyStatus" class="form-control" v-model="proxyStatus">
                              <option value="active">Active</option>
                              <option value="inactive">Inactive</option>
                          </select>
                      </div>
                      <button @click.prevent="resetProxyAction" class="btn btn-primary mt-2">Execute</button>
                  </div>
              </div>
          </header>
        </div>
    </div>
</template>

<script>
import NavBarComponent from '../components/NavBarComponent.vue';
import HorizontalNavBar from "../components/HorizontalNavBar.vue";
import axios from 'axios';

export default {
    components: {
        NavBarComponent,
        HorizontalNavBar,
    },
    data() {
        return {
            resetTemplates: 'all',
            templateStatus: '',
            resetSmtp: 'all',
            smtpStatus: '',
            resetDomains: 'all',
            domainStatus: '',
            resetProxy: 'all',
            proxyStatus: '',
        };
    },
    methods: {
        getToken() {
            let token = '';
            let cookies = document.cookie.split(";");
            cookies.forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split("=")[1];
                }
            });
            return token;
        },
        fullReset() {
            let token = this.getToken();
            axios.post(`${this.$store.state.back_url}/api/reset`, { token })
                .then(res => { console.log('Full reset success'); })
                .catch(err => { console.log('Full reset error', err); });
        },
        resetTemplatesAction() {
            let token = this.getToken();
            let payload = { token, type: 'templates', status: this.templateStatus };
            axios.post(`${this.$store.state.back_url}/api/reset/status`, payload)
                .then(res => { console.log('Reset templates success'); })
                .catch(err => { console.log('Reset templates error', err); });
        },
        resetSmtpAction() {
            let token = this.getToken();
            let payload = { token, type: 'smtps', status: this.smtpStatus };
            axios.post(`${this.$store.state.back_url}/api/reset/status`, payload)
                .then(res => { console.log('Reset SMTP success'); })
                .catch(err => { console.log('Reset SMTP error', err); });
        },
        resetDomainsAction() {
            let token = this.getToken();
            let payload = { token, type: 'domains', status: this.domainStatus };
            axios.post(`${this.$store.state.back_url}/api/reset/status`, payload)
                .then(res => { console.log('Reset domains success'); })
                .catch(err => { console.log('Reset domains error', err); });
        },
        resetProxyAction() {
            let token = this.getToken();
            let payload = { token, type: 'proxies', status: this.proxyStatus };
            axios.post(`${this.$store.state.back_url}/api/reset/status`, payload)
                .then(res => { console.log('Reset proxy success'); })
                .catch(err => { console.log('Reset proxy error', err); });
        },
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
    margin-top: 1em;
    width: auto;
}
.container-fluid.dummy-form {
    padding: 20px;
    //background-color: #212529;
}
.form-group {
    margin-bottom: 15px;
}

/deep/ .btn-primary {
  background-color: var(--primary) !important;
  border: none;
  transition: background-color 0.2s linear;
}

.btn:hover {
  background-color: #cc0000;
}

</style>
