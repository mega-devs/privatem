  <template>
    <NavBarComponent stateProp="home" />
    <div class="dummy-form">
        <div class="container-fluid" style="text-align: center;">
            <!-- <button @click.prevent="reset" class="btn btn-primary">Reset</button> -->
            <!-- <p>{{ resetInfo }}</p> -->
            <template v-if="!currentSessionName">
                <h3 class="text-danger" style="color: red;">Please load a session first</h3>
            </template>
            <hr>
        </div>
        <div class="top-bar">
            <div class="input-group">
                <input type="text" class="form-control" placeholder="Session's name..." v-model="sessionName" />
                <button @click="createSession" class="btn btn-primary">Create</button>
            </div>
            <table class="table table-striped mt-3">
                <thead>
                    <tr>
                        <th>Session</th>
                        <th>Open</th>
                        <th>Delete</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="session in sessions" :key="session.id">
                        <td>{{ session.name }}</td>
                        <td><button @click="openSession(session)" class="btn btn-primary">Open</button></td>
                        <td><button @click="deleteSession(session)" class="btn btn-primary">Delete</button></td>
                    </tr>
                </tbody>
            </table>
            <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
            <p v-if="successMessage" class="text-success">{{ successMessage }}</p>
        </div>
    </div>
</template>

<script>
import NavBarComponent from './components/NavBarComponent.vue';
import axios from 'axios';

export default {
    components: {
        NavBarComponent,
    },
    data() {
        return {
            resetInfo: null,
            sessionName: '',
            sessions: [],
            errorMessage: '',
            successMessage: '',
            currentSessionName: this.getCurrentSessionName()
        }
    },
    methods: {
        reset() {
            let token = this.getToken();
            axios.post(`${this.$store.state.back_url}/api/reset`, { token: token })
                .then(res => {
                    this.resetInfo = 'Success';
                })
                .catch(error => {
                    this.resetInfo = 'Error';
                    this.errorMessage = error.response.data.error || 'An error occurred';
                });
        },
        getCurrentSessionName() {
            const name = document.cookie.split('; ').find(row => row.startsWith('currentSessionName='));
            return name ? name.split('=')[1] : null;
        },
        createSession() {
            if (this.sessionName.trim() !== '') {
                let token = this.getToken();
                axios.post(`${this.$store.state.back_url}/api/session/add`, { token: token, name: this.sessionName })
                    .then(res => {
                        if (res.data.data === 'success') {
                            const newSession = { id: Date.now(), name: this.sessionName };
                            this.sessions.push(newSession);
                            this.sessionName = '';
                            this.errorMessage = '';
                            console.log('Create session:', newSession);
                        } else {
                            console.error('Error creating session:', res.data.error);
                            this.errorMessage = res.data.error || 'An error occurred';
                        }
                    })
                    .catch(error => {
                        console.error('Error creating session:', error);
                        this.errorMessage = error.response.data.error || 'An error occurred';
                    });
            } else {
                this.errorMessage = 'Session name cannot be empty';
            }
        },
        openSession(session) {
            document.cookie = `currentSessionName=${session.name}; path=/`;
            this.successMessage = 'Session opened successfully';
            setTimeout(() => {
                window.location.reload();
            }, 1000);
            console.log('Open session:', session);
        },
        deleteSession(session) {
            let token = this.getToken();
            axios.post(`${this.$store.state.back_url}/api/session/del`, { token: token, name: session.name })
                .then(res => {
                    if (res.data.data === 'success') {
                        this.sessions = this.sessions.filter(s => s.id !== session.id);
                        this.errorMessage = '';
                        console.log('Delete session:', session);
                    } else {
                        console.error('Error deleting session:', res.data.error);
                        this.errorMessage = res.data.error || 'An error occurred';
                    }
                })
                .catch(error => {
                    console.error('Error deleting session:', error);
                    this.errorMessage = error.response.data.error || 'An error occurred';
                });
        },
        fetchSessions() {
            let token = this.getToken();
            axios.get(`${this.$store.state.back_url}/api/session/list`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
                .then(res => {
                    this.sessions = res.data.map((item, index) => ({
                        id: index,
                        name: item.data
                    }));
                    this.errorMessage = '';
                })
                .catch(error => {
                    console.error('Error fetching sessions:', error);
                    this.errorMessage = error.response.data.error || 'An error occurred';
                });
        },
        getToken() {
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
    watch: {
        currentSessionName(newValue, oldValue) {
            // Watch for changes in the current session name, if needed
        }
    },
    created() {
        this.fetchSessions();
    }
}
</script>

<style scoped>
.dummy-form {
    overflow: auto;
    margin-top: 2em;
    width: 70%;
    margin: 0 auto;
    height: fit-content;

    background-color: #313131;
    border-radius: 10px;
    padding: 20px;
}

.top-bar {
    //width: 80%;
    display: flex;
    margin-top: 1%;
    margin-bottom: 1%;
    //margin-left: 16%;
    flex-direction: column;
    align-items: flex-start;
    padding: 10px;
    //background-color: #1f2937;
    border-radius: 5px;
    color: white;
}

.form-control {
    margin-right: 10px;
    padding: 10px;
    flex: 1;
}

.btn-success {
    background-color: blue;
    padding: 10px 20px;
}

.table {
    width: 100%;
    margin-top: 20px;
    background-color: white;
    color: rgb(23, 23, 154);
}

.table thead th{
    color: rgb(241, 117, 117);
}
.btn-primary,
.btn-danger {
    padding: 5px 10px;
}

.text-danger {
    color: red;
}

.text-success {
    color: green;
}

/deep/ .btn-primary {
  background-color: var(--primary);
  border: none;
  transition: background-color 0.2s linear;
}

.btn:hover {
  background-color: #cc0000;
}

</style>
