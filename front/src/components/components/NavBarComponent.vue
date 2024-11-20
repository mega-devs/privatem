<template>
  <div class=" d-flex flex-column flex-shrink-0 p-3 start-0 top-0 content" style="overflow: auto">
    <div class="bg_images">
      <img class="bg_image_logo" src="/prviatem.webp" width="50px" height="50px" alt="i"/>
      <img class="bg_image_1" src="/ui-red-dark.png" width="200px" height="10px" alt="i"/>
      <img class="bg_image_2" src="/ui-red-dark.png" width="200px" height="10px" alt="i"/>
      <img class="bg_image_3" src="/ui-red-dark.png" width="200px" height="10px" alt="i"/>
      <img class="bg_image_4" src="/ui-red-dark.png" width="200px" height="10px" alt="i"/>
    </div>

    <ul class="nav nav-pills flex-column">
      <li class="nav-item">
        <i class="bi bi-list-check"></i> <span>TestModes:</span>
      </li>
      <li class="nav-item">
        <RouterLink to="/dashboard/test?mode=normal" style="text-decoration: none;">
          <a :class="['nav-link', stateProp === 'normaltest' ? 'active' : 'text-white']">
            <span>Normal Testmode</span>
          </a>
        </RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink to="/dashboard/test?mode=special" style="text-decoration: none;">
          <a :class="['nav-link', stateProp === 'specialtest' ? 'active' : 'text-white']">
            <span>Special Testmode</span>
          </a>
        </RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink to="/dashboard/sendx" style="text-decoration: none;">
          <a :class="['nav-link', stateProp === 'sendx' ? 'active' : 'text-white']">
            <span>SendX mode</span>
          </a>
        </RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink to="/dashboard/dummy" style="text-decoration: none;">
          <a :class="['nav-link', stateProp === 'dummy' ? 'active' : 'text-white']">
            <span>Dummy</span>
          </a>
        </RouterLink>
      </li>
    </ul>
    <br>
    <ul class="nav nav-pills flex-column">
      <li class="nav-item">
        <i class="bi bi-envelope"></i> <span>Mailing:</span>
      </li>
      <li class="nav-item">
        <RouterLink to="/dashboard/mailing?mode=normal" style="text-decoration: none;">
          <a :class="['nav-link', stateProp === 'normalmailing' ? 'active' : 'text-white']">
            <span>Normal</span>
          </a>
        </RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink to="/dashboard/mailing?mode=special" style="text-decoration: none;">
          <a :class="['nav-link', stateProp === 'specialmailing' ? 'active' : 'text-white']">
            <span>Special</span>
          </a>
        </RouterLink>
      </li>
    </ul>
    <br>
    <ul class="nav nav-pills flex-column">
      <li class="nav-item">
        <RouterLink to="/dashboard/settings" style="text-decoration: none;">
          <a :class="['nav-link', stateProp === 'settings' ? 'active' : 'text-white']">
            <i class="bi bi-gear"></i> <span>Settings</span>
          </a>
        </RouterLink>
        <RouterLink to="/dashboard/resetz" style="text-decoration: none;">
          <a :class="['nav-link', stateProp === 'resetz' ? 'active' : 'text-white']">
            <i class="bi bi-x-circle"></i> <span>Reset</span>
          </a>
        </RouterLink>
      </li>
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
        <p class="table_current_session_item">IMG DOMAINS</p>
        <p class="table_current_session_item">{{ IMGdomainsLoaded }}</p>
      </div>
      <div class="table_current_session_row">
        <p class="table_current_session_item">DOMAINS</p>
        <p class="table_current_session_item">{{ URLdomainsLoaded }}({{ALLdomainsLoaded}} links)</p>
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
      ALLdomainsLoaded: 'X', // Replace 'X' with actual value or bind it dynamically
      IMGdomainsLoaded: 'X', // Replace 'X' with actual value or bind it dynamically
      URLdomainsLoaded: 'X', // Replace 'X' with actual value or bind it dynamically
      socksLoaded: 'X', // Replace 'X' with actual value or bind it dynamically
      mailerStatus: 'STOPPED'
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
            this.ALLdomainsLoaded = res.data.count['allDomains'];
            this.IMGdomainsLoaded = res.data.count['imgDomains'];
            this.URLdomainsLoaded = res.data.count['urlDomains'];
            this.socksLoaded = res.data.count['socks'];
          })
          .catch(error => {
            console.error('Error fetching logs:', error);
          });
    }
  },
  mounted() {
    this.fetchcounts();
    console.log('Current stateProp:', this.stateProp);
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
  background: rgb(32, 32, 32) !important;
  background: radial-gradient(circle, rgba(32, 32, 32, 1) 0%, rgba(0, 0, 0, 1) 100%) !important;
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
  top: 2px;
  left: 2px;
}

.bg_image_2 {
  top: 2px;
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
  transform: translate(-50%, 0);
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

.labelnew {
  /* color:rgb(17, 212, 27); */
  color: #97c2ee;
  font-weight: bold;
  margin-bottom: 3%;
}

.headerzn {
  color: #97c2ee;
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