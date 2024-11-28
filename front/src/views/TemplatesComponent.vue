<template>
    <LayoutComponent title="Templates">
        <template #content>
            <p class="text-danger text-center"><b>{{errorSubTemplates}}</b></p>
            <div class="table-two">
                <div>
                    <v-file-input clearable label="Input templates.zip" accept="archive/zip" @change="fileUploadTemplates"></v-file-input>
                    <v-text-field v-model="zipLink" label="Input zip link" variant="outlined"></v-text-field>
                    <button type="button" @click.prevent="submitTemplates" class="btn btn-primary">Submit</button>
                </div>
                <v-data-table
                    class="table"
                    v-model:items-per-page="itemsPerPage"
                    :headers="templatescolumns"
                    :items="templatesdata"
                    :items-length="templatesdata.length"
                    :loading="isLoadingSessions"
                    item-value="name"
                >
                    <template v-slot:item.view="{ item }">
                        <button @click="visitz(item.id)" class="btn btn-primary">Open</button>
                    </template>
                    <template v-slot:item.delete="{ item }">
                        <button @click="del(item.id)" class="btn btn-danger">Delete</button>
                    </template>
                </v-data-table>
            </div>
        </template>
    </LayoutComponent>
</template>


<script>
import axios from 'axios';
import HorizontalNavBar from "@/components/components/HorizontalNavBar.vue";
import JSZip from 'jszip';
import DataTable from 'datatables.net-vue3';
import LayoutComponent from '@/components/LayoutComponent.vue';

export default {
    components: {
        HorizontalNavBar,
        DataTable,
        LayoutComponent
    },
    data() {
        return {
            isLoadingSessions: false,
            nameTemplates: null,
            materialsTemplates: null,
            fileTemplates: [],
            errorSubTemplates: null,
            templatesdata: [],
            zipLink: '',  
            templatescolumns: [
                { title: 'NAME', key: 'name' },
                { title: 'VIEW', key: 'view' },
                { title: 'DELETE', data: 'key' }
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
            this.isLoadingSessions = true;
            axios.get(`${import.meta.env.VITE_BACK_URL}/api/get/list/templates/${currentSessionName}`)
                .then(res => {
                    this.templatesdata = res.data.map(item => ({
                        id: item.id,
                        name: item.name
                    }));
                })
                .catch(error => {
                    console.error('Error fetching templates:', error);
                });
            this.isLoadingSessions = false;
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

                axios.post(`${import.meta.env.VITE_BACK_URL}/api/input/material`, {
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
            axios.post(`${import.meta.env.VITE_BACK_URL}/api/del/material`, {token: token, id: id, type: 'templates'})
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
            const proxyUrl = `${import.meta.env.VITE_BACK_URL}/api/proxy?url=${encodeURIComponent(link)}`;

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

                    axios.post(`${import.meta.env.VITE_BACK_URL}/api/input/material`, {
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


<style lang="scss" scoped>
.tables {
  width: 100%;
  background-color: #313131 !important;
}

.table-two {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 16px;
    @media(max-width: 1000px) {
        grid-template-columns: repeat(1, 1fr);
    }
}

.table tbody {
  background-color: red;
}

label {
  padding: 1em 1em 1em 0;
}


tbody {
  color: black;
}

.btn-primary {
  background-color: var(--primary) !important;
  border: none;
  transition: background-color 0.2s linear;
}

.btn:hover {
  background-color: #cc0000;
}

</style>
