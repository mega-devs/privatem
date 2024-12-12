<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark" style="border-radius: 15px 15px 0 0;">
    <div class="container-fluid justify-content-center">
      <ul class="nav nav-pills">
        <li class="nav-link">
          {{ getCurrentSessionName() || 'No session' }}
        </li>
        <li class="nav-item" >
          <RouterLink to="/dashboard" class="nav-link" :class="{ active: stateProp === 'home' }">
            <i class="bi bi-house"></i> Home
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink to="/dashboard/templates" class="nav-link" :class="{ active: stateProp === 'templates' }">
            <i class="bi bi-file-earmark-text"></i> Templates
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink to="/dashboard/proxies" class="nav-link" :class="{ active: stateProp === 'proxies' }">
            <i class="bi bi-shield-lock"></i> Proxies
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink to="/dashboard/SMTPs" class="nav-link" :class="{ active: stateProp === 'SMTPs' }">
            <i class="bi bi-envelope"></i> SMTPs
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink to="/dashboard/IMAPs" class="nav-link" :class="{ active: stateProp === 'IMAPs' }">
            <i class="bi bi-inbox"></i> IMAPs
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink to="/dashboard/domains" class="nav-link" :class="{ active: stateProp === 'domains' }">
            <i class="bi bi-globe"></i> Domains
          </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink to="/dashboard/bases" class="nav-link" :class="{ active: stateProp === 'bases' }">
            <i class="bi bi-database"></i> Bases
          </RouterLink>
        </li>
        <li class="nav-link" id="currenttime">
          Time: {{ currentTime }}
        </li>
      </ul>    
    </div>
  </nav>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark" style="border-radius: 15px 15px 0 0;">
    <div class="container-fluid justify-content-center">
      <ul class="nav nav-pills">        
        <li class="nav-link">
          Total SMTPs: {{ totalSmtps }}
        </li>
        <li class="nav-link" id="currenttime">
          Valid SMTPs: {{ validSmtps }}
        </li>
        <li class="nav-link" id="currenttime">
          Dead SMTPs: {{ deadSmtps }}
        </li>
        <li class="nav-link" id="currenttime">
          Inbox SMTPs: {{ inboxSmtps }}
        </li>
        <li class="nav-link" id="currenttime">
          Junk SMTPs: {{ junkSmtps }}
        </li>
        <li class="nav-link" id="currenttime">
          TEMPLATES: {{ templatesLoaded }}
        </li>
        <li class="nav-link" id="currenttime">
          IMG DOMAINS: {{ IMGdomainsLoaded }}
        </li>
        <li class="nav-link" id="currenttime">
          DOMAINS: {{ URLdomainsLoaded }} ({{ ALLdomainsLoaded }})
        </li>
        <li class="nav-link" id="currenttime">
          SOCKS: {{ socksLoaded }}
        </li>
        <li class="nav-link" id="currenttime">
          MAILER STATUS: {{ mailerStatus }}
        </li>
      </ul>    
    </div>
  </nav>
  <!-- <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="table_current_session">
          <div class="table_current_session_row">
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
          <div class="table_current_session_row">
            <p class="table_current_session_item">MAILER STATUS</p>
            <p class="table_current_session_item mailerStatusClass">{{ mailerStatus }}</p>
          </div>
        </div>
    </nav> -->
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      totalSmtps: 'X',
      validSmtps: 'X',
      deadSmtps: 'X',
      inboxSmtps: 'X',
      junkSmtps: 'X',
      templatesLoaded: 'X',
      ALLdomainsLoaded: 'X',
      IMGdomainsLoaded: 'X',
      URLdomainsLoaded: 'X',
      socksLoaded: 'X',
      mailerStatus: 'STOPPED',
      currentTime: '00.00.0000, 00:00:00'
    }
  },
  computed: {
    mailerStatusClass() {
      return this.mailerStatus === 'STOPPED' ? 'text-danger' : 'text-success';
    },
    stateProp() {
      return this.$route.name;
    }
  },
  methods: {
    getCurrentSessionName() {
      const name = document.cookie.split('; ').find(row => row.startsWith('currentSessionName='));
      return name ? name.split('=')[1] : null;
    },
    fetchcounts() {
      const currentSessionName = this.getCurrentSessionName();
      if (!currentSessionName) {
        return;
      }

      axios.get(`${import.meta.env.VITE_BACK_URL}/api/count/${currentSessionName}`)
        .then(res => {
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
  }
}
</script>

<style scoped>
.nav-link {
  color: white;
}

.nav-link.active {
  background-color: #007bff;
}

.table_current_session {
  display: flex;
  flex-direction: row;
  /* width: 100%; */
  height: auto;
}

.table_current_session_row {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 8px 16px;
  background-color: #272727;
}

.table_current_session_item {
  margin: 0;
  font-weight: 600;
}

</style>
