<template>
  <LayoutComponent :title="currentSessionName || 'Please load a session first'">
    <template #content>
      <div class="dummy-form">
        <div class="top-bar">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="Session's name..." v-model="sessionName"/>
            <button @click="createSession" class="btn btn-primary">Create</button>
          </div>
          <v-data-table-virtual
            class="table"
            style="margin-top: 20px;"
            v-model:items-per-page="itemsPerPage"
            :headers="tableHeader"
            :items="tableDatas"
            :items-length="tableDatas.length"
            :loading="isLoadingSessions"
            item-value="name"
          >
          <template v-slot:item.open="{ item }">
            <v-btn @click="openSession(item)" class="btn btn-primary">Open</v-btn>
          </template>
          <template v-slot:item.delete="{ item }">
            <v-btn @click="deleteSession(item)" class="btn btn-danger">Delete</v-btn>
          </template>
        </v-data-table-virtual>

          <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
          <p v-if="successMessage" class="text-success">{{ successMessage }}</p>
        </div>
      </div>
    </template>
  </LayoutComponent>
</template>

<script>
import axios from 'axios';
import LayoutComponent from '@/components/LayoutComponent.vue';

export default {
  components: {
    LayoutComponent,
  },
  data() {
    return {
      tableHeader: [
        {
          title: 'Session',
          key: 'session',
        },
        {
          title: 'Open',
          key: 'open',
        },
        {
          title: 'Delete',
          key: 'delete',
        },
      ],
      tableDatas: [],
      resetInfo: null,
      sessionName: '',
      errorMessage: '',
      successMessage: '',
      isLoadingSessions: false,
      itemsPerPage: 10,
    }
  },
  computed: {
    currentSessionName() {
      const name = document.cookie.split('; ').find(row => row.startsWith('currentSessionName='));
      return name ? name.split('=')[1] : null;
    },
    token() {
      let token = '';
      let cookies = document.cookie.split(";");
      cookies.forEach(cookie => {
        if (cookie.includes('authToken')) {
          token = cookie.split("=")[1];
        }
      });
      return token;      
    }
  },
  methods: {
    async fetchRequest(url, data, headers, method = 'post') {
      try {
        const res = await axios[method](`${import.meta.env.VITE_BACK_URL}${url}`, data, headers);
        this.resetInfo = 'Success';
        return res;
      } catch (e) {
        this.resetInfo = 'Error';
        this.errorMessage = e.response.data.error || 'An error occurred';
        console.error('Error:', e);
      }
      return null;
    },
    async reset() {
      const res = await this.fetchRequest('/api/reset', {token: this.token})
      if(res != null) {
        this.resetInfo = 'Success';
      }
    },
    async createSession() {
      if (this.sessionName.trim() !== '') {
        const res = await this.fetchRequest('/api/session/add', {token: this.token, name: this.sessionName})
        console.log(res)
        if (res.data.data === 'success') {
          const newSession = {session: this.sessionName};
          this.tableDatas.push(newSession);
          this.sessionName = '';
          this.errorMessage = '';
          console.log('Create session:', newSession);
        } else {
          console.error('Error creating session:', res.data.error);
          this.errorMessage = res.data.error || 'An error occurred';
        }
      } else {
        this.errorMessage = 'Session name cannot be empty';
      }
    },
    openSession(session) {
      document.cookie = `currentSessionName=${session.session}; path=/`;
      this.successMessage = 'Session opened successfully';
      setTimeout(() => {
        window.location.reload();
      }, 1000);
      console.log('Open session:', session);
    },
    async deleteSession(session) {
      const res = await this.fetchRequest('/api/session/del', {token: this.token, name: session.session});
      if (res != null && res.data.data === 'success') {
        this.tableDatas = this.tableDatas.filter(s => s.id !== session.id);
        this.errorMessage = '';
        console.log('Delete session:', session);
      } 
    },
    async fetchSessions() {
      this.isLoadingSessions = true;
      const res = await this.fetchRequest('/api/session/list', null, {
        headers: {'Authorization': `Bearer ${this.token}`}
      }, "get")
      this.tableDatas = res.data.map((item, index) => ({
        id: index,
        session: item.data
      }));
      this.errorMessage = '';
      this.isLoadingSessions = false;
    },
  },
  async created() {
    await this.fetchSessions();
  }
}
</script>

<style lang="scss" scoped>
  .input-group {
    .form-control {
      margin-right: 10px;
      padding: 10px;
      flex: 1;
      background-color: transparent;
      outline: none;
      border: none;
    }
    background-color: var(--bs-body-bg);
    border: var(--bs-border-width) solid var(--bs-border-color);
    border-radius: 5px;
  }

  .top-bar {
    display: flex;
    margin-top: 1%;
    margin-bottom: 1%;
    flex-direction: column;
    align-items: flex-start;
    padding: 10px;
    border-radius: 5px;
    color: white;
  }

</style>
