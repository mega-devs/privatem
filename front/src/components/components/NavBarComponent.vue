<template>
    <div class=" d-flex flex-column flex-shrink-0 p-3 start-0 top-0 content" style="overflow: auto">
      <div class="bg_images">
        <img class="bg_image_logo" src="/prviatem.webp" width="50px" height="50px" alt="i" />
        <img class="bg_image_1" src="/ui-red-dark.png" width="200px" height="10px" alt="i" />
        <img class="bg_image_2" src="/ui-red-dark.png" width="200px" height="10px" alt="i" />
        <img class="bg_image_3" src="/ui-red-dark.png" width="200px" height="10px" alt="i" />
        <img class="bg_image_4" src="/ui-red-dark.png" width="200px" height="10px" alt="i" />
      </div>
     
        <ul class="nav nav-pills flex-column">

          <!-- Dropdown group -->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle text-white" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              {{ currentSessionName || 'Current Session' }}
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown" style="width: 100%;">
              <li class="nav-item">
                  <RouterLink to="/dashboard" style="text-decoration: none;">
                      <a :class="['nav-link', stateProp === 'home' ? 'active' : 'text-white']">
                          <i class="bi bi-house"></i> <span>Home</span>
                      </a>
                  </RouterLink>
              </li>
              <li class="nav-item">
                  <RouterLink to="/dashboard/templates" style="text-decoration: none;">
                      <a :class="['nav-link', stateProp === 'templates' ? 'active' : 'text-white']">
                          <i class="bi bi-house"></i> <span>Templates</span>
                      </a>
                  </RouterLink>
              </li>
              <li class="nav-item">
                  <RouterLink to="/dashboard/proxies" style="text-decoration: none;">
                      <a :class="['nav-link', stateProp === 'proxies' ? 'active' : 'text-white']">
                          <i class="bi bi-house"></i> <span>Proxies</span>
                      </a>
                  </RouterLink>
              </li>

              <li class="nav-item">
                  <RouterLink to="/dashboard/SMTPs" style="text-decoration: none;">
                      <a :class="['nav-link', stateProp === 'SMTPs' ? 'active' : 'text-white']">
                          <i class="bi bi-house"></i> <span>SMTPs</span>
                      </a>
                  </RouterLink>
              </li>

              <li class="nav-item">
                  <RouterLink to="/dashboard/IMAPs" style="text-decoration: none;">
                      <a :class="['nav-link', stateProp === 'IMAPs' ? 'active' : 'text-white']">
                          <i class="bi bi-house"></i> <span>IMAPs</span>
                      </a>
                  </RouterLink>
              </li>

              <li class="nav-item">
                  <RouterLink to="/dashboard/domains" style="text-decoration: none;">
                      <a :class="['nav-link', stateProp === 'domains' ? 'active' : 'text-white']">
                          <i class="bi bi-house"></i> <span>Domains</span>
                      </a>
                  </RouterLink>
              </li>

              <li class="nav-item">
                  <RouterLink to="/dashboard/bases" style="text-decoration: none;">
                      <a :class="['nav-link', stateProp === 'bases' ? 'active' : 'text-white']">
                          <i class="bi bi-house"></i> <span>Bases</span>
                      </a>
                  </RouterLink>
              </li>
            </ul>
          </li>

          <!-- Dropdown group -->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle text-white" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Testmodes
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown" style="width: 100%;">
              <li class="nav-item">
                  <RouterLink to="/dashboard/test" style="text-decoration: none;">
                      <a :class="['nav-link', stateProp === 'test' ? 'active' : 'text-white']">
                          <i class="bi bi-house"></i> <span>Test mode</span>
                      </a>
                  </RouterLink>
              </li>
              <li class="nav-item">
                  <RouterLink to="/dashboard/sendx" style="text-decoration: none;">
                      <a :class="['nav-link', stateProp === 'sendx' ? 'active' : 'text-white']">
                          <i class="bi bi-house"></i> <span>SendX mode</span>
                      </a>
                  </RouterLink>
              </li>
            </ul>
          </li>


          <li class="nav-item">
              <RouterLink to="/dashboard/mailing" style="text-decoration: none;">
                  <a :class="['nav-link', stateProp === 'mailing' ? 'active' : 'text-white']">
                      <i class="bi bi-house"></i> <span>Mailing</span>
                  </a>
              </RouterLink>
          </li>
          <li class="nav-item">
              <RouterLink to="/dashboard/resetz" style="text-decoration: none;">
                  <a :class="['nav-link', stateProp === 'resetz' ? 'active' : 'text-white']">
                      <i class="bi bi-house"></i> <span>Reset</span>
                  </a>
              </RouterLink>
          </li>


<!--            <template v-if="stateProp == 'home'">-->
<!--                <li class="nav-item">-->
<!--                    <RouterLink to="/dashboard" style="text-decoration: none;">-->
<!--                        <a class="nav-link active">-->
<!--                            <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                            <i class="bi bi-house"></i> <span>Home</span>-->
<!--                        </a>-->
<!--                    </RouterLink>-->
<!--                </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--                <li class="nav-item">-->
<!--                    <RouterLink to="/dashboard" style="text-decoration: none;">-->
<!--                        <a class="nav-link text-white">-->
<!--                            <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                            <i class="bi bi-house"></i> <span>Home</span>-->
<!--                        </a>-->
<!--                    </RouterLink>-->
<!--                </li>-->
<!--            </template>-->
<!--            <template v-if="stateProp == 'templates'">-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/templates" style="text-decoration: none;">-->
<!--                    <a class="nav-link active">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-file-earmark"></i> <span>Templates</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/templates" style="text-decoration: none;">-->
<!--                    <a class="nav-link text-white">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-file-earmark"></i> <span>Templates</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-if="stateProp == 'proxies'">-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/proxies" style="text-decoration: none;">-->
<!--                    <a class="nav-link active">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-hdd-stack"></i> <span>Proxies</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/proxies" style="text-decoration: none;">-->
<!--                    <a class="nav-link text-white">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-hdd-stack"></i> <span>Proxies</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-if="stateProp == 'SMTPs'">-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/SMTPs" style="text-decoration: none;">-->
<!--                    <a class="nav-link active">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-mailbox"></i> <span>SMTPs</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/SMTPs" style="text-decoration: none;">-->
<!--                    <a class="nav-link text-white">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-mailbox"></i> <span>SMTPs</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-if="stateProp == 'IMAPs'">-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/IMAPs" style="text-decoration: none;">-->
<!--                    <a class="nav-link active">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-inbox"></i> <span>IMAPs</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/IMAPs" style="text-decoration: none;">-->
<!--                    <a class="nav-link text-white">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-inbox"></i> <span>IMAPs</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-if="stateProp == 'domains'">-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/domains" style="text-decoration: none;">-->
<!--                    <a class="nav-link active">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-router"></i> <span>Domains</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/domains" style="text-decoration: none;">-->
<!--                    <a class="nav-link text-white">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-router"></i> <span>Domains</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-if="stateProp == 'bases'">-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/bases" style="text-decoration: none;">-->
<!--                    <a class="nav-link active">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-person-lines-fill"></i> <span>Bases</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/bases" style="text-decoration: none;">-->
<!--                    <a class="nav-link text-white">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-person-lines-fill"></i> <span>Bases</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-if="stateProp == 'test'">-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/test" style="text-decoration: none;">-->
<!--                    <a class="nav-link active">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-patch-check"></i> <span>Test mode</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/test" style="text-decoration: none;">-->
<!--                    <a class="nav-link text-white">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-patch-check"></i> <span>Test mode</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--             <template v-if="stateProp == 'sendx'">-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/sendx" style="text-decoration: none;">-->
<!--                    <a class="nav-link active">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-patch-check"></i> <span>SendX mode</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/sendx" style="text-decoration: none;">-->
<!--                    <a class="nav-link text-white">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-patch-check"></i> <span>SendX mode</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-if="stateProp == 'mailing'">-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/mailing" style="text-decoration: none;">-->
<!--                    <a class="nav-link active">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-envelope"></i> <span>Mailing</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/mailing" style="text-decoration: none;">-->
<!--                    <a class="nav-link text-white">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-envelope"></i> <span>Mailing</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->
<!--            <template v-if="stateProp == 'resetz'">-->
<!--                <li class="nav-item">-->
<!--                    <RouterLink to="/dashboard/resetz" style="text-decoration: none;">-->
<!--                        <a class="nav-link active">-->
<!--                            <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                            <i class="bi bi-trash"></i> <span>Reset</span>-->
<!--                        </a>-->
<!--                    </RouterLink>-->
<!--                </li>-->
<!--            </template>-->
<!--            <template v-else>-->
<!--            <li class="nav-item">-->
<!--                <RouterLink to="/dashboard/resetz" style="text-decoration: none;">-->
<!--                    <a class="nav-link text-white">-->
<!--                        <svg class="bi pe-none me-2" width="16" height="16"></svg>-->
<!--                        <i class="bi bi-trash"></i> <span>Reset</span>-->
<!--                    </a>-->
<!--                </RouterLink>-->
<!--            </li>-->
<!--            </template>-->

            <hr>
        </ul>
    <div class="table_current_session">
      <div class="table_current_session_row" style="border-radius: 10px 10px 0 0;">
        <p class="table_current_session_item">Total SMTPs</p>
        <p class="table_current_session_item">{{ totalSmtps }}</p>
      </div>
      <div class="table_current_session_row">
        <p class="table_current_session_item">Valid SMTPs</p>
        <p class="table_current_session_item">{{ validSmtps }}</p>
      </div>
      <div class="table_current_session_row">
        <p class="table_current_session_item">Dead SMTPs</p>
        <p class="table_current_session_item">{{ deadSmtps }}</p>
      </div>
      <div class="table_current_session_row">
        <p class="table_current_session_item">Inbox SMTPs</p>
        <p class="table_current_session_item">{{ inboxSmtps }}</p>
      </div>
      <div class="table_current_session_row">
        <p class="table_current_session_item">Junk SMTPs</p>
        <p class="table_current_session_item">{{ junkSmtps }}</p>
      </div>
      <div class="table_current_session_row">
        <p class="table_current_session_item">TEMPLATES</p>
        <p class="table_current_session_item">{{ templatesLoaded }}</p>
      </div>
      <div class="table_current_session_row">
        <p class="table_current_session_item">DOMAINS</p>
        <p class="table_current_session_item">{{ domainsLoaded }}</p>
      </div>
      <div class="table_current_session_row">
        <p class="table_current_session_item">SOCKS</p>
        <p class="table_current_session_item">{{ socksLoaded }}</p>
      </div>
      <div class="table_current_session_row" style="border-radius: 0 0 10px 10px;">
        <p class="table_current_session_item">MAILER STATUS</p>
        <p class="table_current_session_item mailerStatusClass">{{ mailerStatus }}</p>
      </div>
    </div>
      <button @click="reset" class="btn-reset mt-3">Reset</button>
<!--    <ul class="nav nav-pills flex-column mb-auto fixcss">-->
<!--        <li>Loaded Session: <span class="session-name" style="width: 80px !important; display: inline-block; overflow: hidden; text-overflow: ellipsis;">{{ currentSessionName }}</span></li>-->
<!--        <li>Total SMTPs: {{ totalSmtps }}</li>-->
<!--        <li>Valid SMTPs: {{ validSmtps }}</li>-->
<!--        <li>Dead SMTPs:  {{ deadSmtps }}</li>-->
<!--        <li>Inbox SMTPs: {{ inboxSmtps }}</li>-->
<!--        <li>Junk SMTPs:  {{ junkSmtps }}</li>-->
<!--        <li>TEMPLATES:   {{ templatesLoaded }}</li>-->
<!--        <li>DOMAINS: {{ domainsLoaded }}</li>-->
<!--        <li>SOCKS: {{ socksLoaded }}</li>-->
<!--        <li>MAILER STATUS: <span :class="mailerStatusClass">{{ mailerStatus }}</span></li>-->
<!--        <li><br><button @click="reset" class="btn-reset">Reset</button></li>-->
<!--    </ul>-->
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
    --primary: #ef4444;
    --secondary: #191C24;
    --grey-1: #111827;
    --light: #6C7293;
    --dark: #000000;
}
body, html {
    //background-color: #121212 !important;
    background: rgb(32,32,32) !important;
    background: radial-gradient(circle, rgba(32,32,32,1) 0%, rgba(0,0,0,1) 100%) !important;
    color: white;
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
}

.app_full {
    display: flex;
    height: 90vh;
    //overflow: auto;
    /* margin: 11vh; */
    margin-bottom: 0;
    padding-top: 10vh;
    border: 2px solid red;
}
.bg_images {

}
.bg_images > img {
    position: fixed;
    width: 300px;
    height: 9.8vh;
}

.bg_image_1 {
  top:  2px;
  left: 2px;
}
.bg_image_2 {
  top:   2px;
  right: 2px;
  transform: scaleX(-1);
}
.bg_image_3 {
  bottom: 2px;
  //left: 50%;
  left: calc(50% + 50px);
}
.bg_image_4 {
  bottom: 2px;
  transform: scaleX(-1);
  //right: 50%;
  right: calc(50% + 50px);
}
.bg_image_logo {
  width: 100px !important;
  height: 10vh !important;
  bottom: 0;
  left: 50%;
  transform: translate(-50%,0);
}


.content {
  border-right: 1px solid grey;

}

hr {
  border: 1px solid grey !important;
}

.nav-item {
  color: white;
  border-radius: 5px;
  font-weight: 600;
}

.nav-link:hover {
  //color: var(--primary) !important;
  background-color: #2c2c2c !important;
}

.nav-item .active {
    //color: var(--primary) !important;
    //background-color: transparent !important;
  background-color: var(--primary) !important;
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
    //margin-left: 13px;
    padding: 5px 10px;
    background-color: var(--primary);
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


.table_current_session {
  display: flex;
  flex-direction: column;
  width: 250px;
  height: auto;
  border-radius: 10px;
  //overflow: hidden;
}
.table_current_session_row {
  width: 100%;
  background-color: #272727;
  border-bottom: 1px solid #2c3544;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.table_current_session_item {
  font-weight: 600;
  padding: 4px 12px;
  margin: 0;
}


</style>