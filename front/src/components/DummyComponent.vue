<template>
    <NavBarComponent stateProp="dummy"/>
    <div id="main-part">
      <HorizontalNavBar state-prop="dummy"/>
      <div class="container-fluid dummy-form">
          <div>
              <div class="row">
                  <h2 class="text-center headerzn">Dummy</h2>
                  <hr>
                  <div class="col-lg-6">
                      <div>
                          <input class="form-control" type="text" v-model="nameDummy" placeholder="Input dummy name">
                          <div class="mb-3">
                              <label for="formFile" class="form-label labelnew">Input template.html</label>
                              <input class="form-control" type="file" id="formFile" @change="fileUploadDummy($event, 'fileTmp')">
                          </div>
                          <div class="mb-3">
                              <label for="formFileMultiple" class="form-label labelnew">Input from.txt</label>
                              <input class="form-control" type="file" id="formFile" @change="fileUploadDummy($event, 'fileFrom')">
                          </div>
                          <div class="mb-3">
                              <label for="formFileDisabled" class="form-label labelnew">Input links.txt</label>
                              <input class="form-control" type="file" id="formFile" @change="fileUploadDummy($event, 'fileLinks')">
                          </div>
                          <div class="mb-3">
                              <label for="formFileSm" class="form-label labelnew">Input sentences.txt</label>
                              <input class="form-control" id="formFile" type="file" @change="fileUploadDummy($event, 'fileSent')">
                          </div>
                          <div>
                              <label for="formFileLg" class="form-label labelnew">Input subjects.txt</label>
                              <input class="form-control" id="formFile" type="file" @change="fileUploadDummy($event, 'fileSubj')">
                          </div>
                      </div>
                      <button style="margin-top: 1em;" type="button" @click.prevent="submitDummy" class="btn btn-primary">Submit</button>
                      <p class="text-danger">{{errorSubDummy}}</p>
                  </div>
                  <div class="col-lg-6">
                      <DataTable :data="dummyData" :columns="dummyColumns" class="table table-striped" @click="handleClick">
                      </DataTable>
                  </div>
              </div>
          </div>
      </div>
      <AdvancedModalViewComponent ref="modal"></AdvancedModalViewComponent>
    </div>
</template>
<script>
import axios from 'axios';
import NavBarComponent from './components/NavBarComponent.vue';
import AdvancedModalViewComponent from './components/AdvancedModalViewComponent.vue';
import DataTable from 'datatables.net-vue3';
import HorizontalNavBar from "@/components/components/HorizontalNavBar.vue";

export default {
    components: {
      HorizontalNavBar,
        NavBarComponent,
        AdvancedModalViewComponent,
        DataTable
    },
    data() {
        return {
            nameDummy: null,
            materialsDummy: null,
            filesDummy: {
                'fileTmp': null,
                'fileFrom': null,
                'fileLinks': null,
                'fileSent': null,
                'fileSubj': null,
            },
            fileTemplates: null,
            errorSubDummy: null,
            dummyData: [],
            dummyColumns: [
                { title: 'ID', data: 'id' },
                { title: 'Name', data: 'name' },
                { title: 'View', data: 'status', render: (data) => {
                    return `<button class="btn btn-primary" data-action="view" data-id="${data}"><i class="bi bi-binoculars"></i></button>`;
                }},
                { title: 'DELETE', data: 'id', render: (data) => {
                    return `<button class="btn btn-danger" data-action="delete" data-id="${data}"><i class="bi bi-dash"></i></button>`;
                }}
            ]
		}
	},
    methods: {
        getDummy() {
            const currentSessionName = this.getCurrentSessionName();
            if (!currentSessionName) {
                this.errorSubTemplates = 'No session loaded';
                return;
            }
            axios.get(`${this.$store.state.back_url}/api/get/list/dummy/${currentSessionName}`)
            .then(res => {
                    this.dummyData = res.data.map(item => ({
                        id: item.id,
                        name: item.name
                    }));
                })
                .catch(error => {
                    console.error('Error fetching templates:', error);
            });
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
            }
        },
        submitDummy() {
            let token = ''
            let cookies = document.cookie.split(";")
            cookies.forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split("=")[1];
                }
            })
            this.errorSubDummy = ''
            if (this.filesDummy && this.nameDummy) {
                axios.post(`${this.$store.state.back_url}/api/input/material`, {token: token, session:currentSessionName, name: this.nameDummy, type: 'dummy', file: this.filesDummy}).then(res => {
                    this.getDummy()
                    if ( res.data.data == 'error' ) {
                        this.errorSubDummy = res.data.error
                    } 
                })
            } else {
                this.errorSubDummy = 'Fill in the fields!'
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
            axios.post(`${this.$store.state.back_url}/api/del/material`, {token: token, type:'dummy', id: id}).then(res => {this.getDummy();this.getTemplates()})
        },
        view(name) {
            axios.get(`${this.$store.state.back_url}/api/get/manifest/${name}`).then(res => {
                let modalData = []
                res.data.forEach(el => {
                    if (el[2] == 'templatesTmp' || el[2] == 'dummyTmp') {
                        el[2] = 'html'
                    } else if (el[2] == 'templatesFrom' || el[2] == 'dummyFrom') {
                        el[2] = 'from'
                    } else if (el[2] == 'templatesLinks' || el[2] == 'dummyLinks') {
                        el[2] = 'links'
                    } else if (el[2] == 'templatesSubj' || el[2] == 'dummySubj') {
                        el[2] = 'subjects'
                    } else if (el[2] == 'dummySent') {
                        el[2] = 'sentences'
                    }
                    delete el[1]
                    modalData.push(el)
                })
                this.$refs.modal.data = res.data
                this.$refs.modal.show = true
            })
        },
        fileUploadDummy(event, file) {
            event.target.files[0].arrayBuffer().then((buffer)=>{
                const bufferByteLength = buffer.byteLength
                const bufferUint8Array = new Uint8Array(buffer, 0, bufferByteLength)
                this.filesDummy[file] = new TextDecoder().decode(bufferUint8Array)
            })
        },
        get_zip_data(zip, files_keys, data, callback) {
            zip.files[files_keys[0]].async("string").then(el_data => {
                files_keys.shift()
                data.push(el_data)
                callback(data)
                if ( files_keys.length > 0 ) {
                    this.get_zip_data(zip, files_keys, data, () => {})
                } else {
                    this.fileTemplates = data
                }
            })
        },
    },
    mounted() {
        this.getDummy()
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
</style>