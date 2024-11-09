<template>
    <NavBarComponent stateProp="templates"/>
    <div id="main-part">
        <HorizontalNavBar state-prop="templates"/>
        <div class="container-fluid dummy-form">
            <div>
                <div class="row">
                    <h2 class="text-center headerzn" style="color: white;">Templates</h2>
                    <hr>
                    <p class="text-danger text-center"><b>{{errorSubTemplates}}</b></p>
                    <div class="col-lg-6">
                        <!-- <input class="form-control" type="text" v-model="nameTemplates" placeholder="Input templates name" readonly> -->
                        <div class="mb-3">
                            <label for="formFile" class="form-label labelnew" style="color: white;">Input templates.zip</label>
                            <input class="form-control" type="file" id="formFile" @change="fileUploadTemplates">
                        </div>
                        <div class="mb-3">
                            <label for="formLink" class="form-label labelnew" style="color: white">Input zip link</label>
                            <input ref="inputEl4" class="form-control" type="text" id="formLink" v-model="zipLink">
                        </div>
                        <button type="button" @click.prevent="submitTemplates" class="btn btn-primary">Submit</button>
                    </div>
                    <div class="col-lg-6">
                        <DataTable :data="templatesdata" :columns="templatescolumns" :style="{color: 'red !important'}" class="table table-striped" @click="handleClick">
                        </DataTable>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios';
import NavBarComponent from './components/NavBarComponent.vue';
import HorizontalNavBar from "./components/HorizontalNavBar.vue";
import JSZip from 'jszip';
import DataTable from 'datatables.net-vue3';

export default {
    components: {
        NavBarComponent,
        HorizontalNavBar,
        DataTable
    },
    data() {
        return {
            nameTemplates: null,
            materialsTemplates: null,
            fileTemplates: [],  // Initialize as an empty array
            errorSubTemplates: null,
            templatesdata: [],
            zipLink: '',  // Add this line
            templatescolumns: [
                { title: 'NAME', data: 'name' },
                { title: 'VIEW', data: 'id', render: (data) => {
                    return `<button class="btn btn-primary" data-action="view" data-id="${data}">Open</button>`;
                }},
                { title: 'DELETE', data: 'id', render: (data) => {
                    return `<button class="btn btn-danger" data-action="delete" data-id="${data}">Delete</button>`;
                }}
            ],
        }
    },
    methods: {
        getTemplates() {
            const currentSessionName = this.getCurrentSessionName();
            if (!currentSessionName) {
                this.errorSubTemplates = 'No session loaded';
                return;
            }

            axios.get(`${this.$store.state.back_url}/api/get/list/templates/${currentSessionName}`)
                .then(res => {
                    this.templatesdata = res.data.map(item => ({
                        id: item.id,
                        name: item.name
                    }));
                })
                .catch(error => {
                    console.error('Error fetching templates:', error);
                });
        },
        submitTemplates() {
            const currentSessionName = this.getCurrentSessionName();
            if (!currentSessionName) {
                this.errorSubTemplates = 'No session loaded';
                return;
            }

            let token = '';
            document.cookie.split(";").forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split("=")[1];
                }
            });

            if (this.zipLink) {
                this.fetchAndProcessZipFromLink(this.zipLink, currentSessionName, token);
            } else if (this.fileTemplates.length > 0 && this.nameTemplates) {
                let files = this.fileTemplates.map(fileData => ({
                    name: this.nameTemplates,
                    data: fileData.content,
                    htmlbodies: fileData.name
                }));

                axios.post(`${this.$store.state.back_url}/api/input/material`, {
                    token: token,
                    session: currentSessionName,
                    type: 'templates',
                    file: files
                })
                .then(res => {
                    this.getTemplates();
                    if (res.data.data === 'error') {
                        this.errorSubTemplates = res.data.error;
                    }else {
                        alert('Template added successfully!');
                    }
                });
            } else {
                this.errorSubTemplates = 'Fill in the fields!';
            }
        },
        del(id) {
            let token = '';
            document.cookie.split(";").forEach(cookie => {
                if (cookie.includes('authToken')) {
                    token = cookie.split("=")[1];
                }
            });
            axios.post(`${this.$store.state.back_url}/api/del/material`, {token: token, id: id, type: 'templates'})
                .then(res => {
                    this.getTemplates();
                });
        },
        visitz(id) {
            this.$router.push(`/dashboard/templates/${id}`);
        },
        get_zip_data(zip, files_keys, data, callback) {
            const fileName = files_keys[0];  // Get the current file name
            zip.files[fileName].async("string").then(el_data => {
                files_keys.shift();  // Remove the processed file from the keys array
                data.push({ name: fileName, content: el_data });  // Store both file name and content

                if (files_keys.length > 0) {
                    this.get_zip_data(zip, files_keys, data, callback);
                } else {
                    this.fileTemplates = data;
                    callback(data);
                }
            });
        },
        fileUploadTemplates(event) {
            const file = event.target.files[0];
            if (file) {
                this.nameTemplates = file.name; // Set the template name to the uploaded file name
                const zip = new JSZip();
                zip.loadAsync(file).then(zip => {
                    const files_keys = Object.keys(zip.files);
                    this.get_zip_data(zip, files_keys, [], (data) => {
                        this.fileTemplates = data;
                        // Log or process each file name here
                        files_keys.forEach(fileName => {
                            console.log('File name:', fileName);
                        });
                    });
                });
            }
        },
        fetchAndProcessZipFromLink(link, currentSessionName, token) {
            const proxyUrl = `${this.$store.state.back_url}/api/proxy?url=${encodeURIComponent(link)}`;

            axios.get(proxyUrl, { responseType: 'arraybuffer' }).then(response => {
                const zip = new JSZip();
                return zip.loadAsync(response.data);
            }).then(zip => {
                const files_keys = Object.keys(zip.files);
                this.get_zip_data(zip, files_keys, [], (data) => {
                    let files = data.map(fileData => ({
                        name: this.nameTemplates || link.split('/').pop(),
                        data: fileData.content,
                        htmlbodies: fileData.name
                    }));

                    axios.post(`${this.$store.state.back_url}/api/input/material`, {
                        token: token,
                        session: currentSessionName,
                        type: 'templates',
                        file: files
                    })
                    .then(res => {
                        this.getTemplates();
                        if (res.data.data === 'error') {
                            this.errorSubTemplates = res.data.error;
                        }else {
                            alert('Template added successfully!');
                        }
                    });
                });
            }).catch(error => {
                console.error('Error fetching or processing zip from link:', error);
                this.errorSubTemplates = 'Error fetching or processing zip from link';
            });
        },
        handleClick(event) {
            const action = event.target.getAttribute('data-action');
            const id = event.target.getAttribute('data-id');

            if (action === 'view') {
                this.visitz(id);
            } else if (action === 'delete') {
                this.del(id);
            }
        },
        getCurrentSessionName() {
            const name = document.cookie.split('; ').find(row => row.startsWith('currentSessionName='));
            return name ? name.split('=')[1] : null;
        }
    },
    mounted() {
        this.getTemplates();
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

/deep/ .table tbody {
  background-color: red;
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

/deep/ tbody {
  color: black;
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
