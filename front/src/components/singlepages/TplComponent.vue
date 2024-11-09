<template>
    <NavBarComponent stateProp="SingleTPL"/>
    <div class="container-fluid dummy-form" style=" border: 2px solid red; border-radius: 5px 5px 0 0; box-sizing: border-box; padding: 20px; ">
        <div>
            <div class="row">
                <h2 class="text-center">Template ID# {{ templateId }}</h2>
                <div class="col-lg-12">
                    <p>Total Subjects: {{ totalSubjects }}</p>
                    <p>Total From Addresses: {{ totalFromAddresses }}</p>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-12">
                    <h3>Template Details</h3>
                    <DataTable :data="materials" :columns="columns" class="table table-striped" @click="handleClick">
                    </DataTable>
                </div>
            </div>
        </div>
    </div>
    <AdvancedModalViewComponent ref="modal"></AdvancedModalViewComponent>
</template>

<script>
import axios from 'axios';
import NavBarComponent from '../components/NavBarComponent.vue';
import DataTable from 'datatables.net-vue3';
import AdvancedModalViewComponent from '../components/AdvancedModalViewComponent.vue';

export default {
    components: {
        NavBarComponent,
        AdvancedModalViewComponent,
        DataTable
    },
    data() {
        return {
            templateId: null,
            materials: [],
            totalSubjects: 0,
            totalFromAddresses: 0,
            templatePreview: '',
            columns: [
                { title: 'ID', data: 'id' },
                { title: 'BodyName', data: 'bodyName' },
                { title: 'Subjects', data: 'id', render: (data) => {
                    return `<button class="btn btn-primary" data-action="viewSubjects" data-id="${data}"><i class="bi bi-binoculars"></i></button>`;
                }},
                { title: 'Froms', data: 'id', render: (data) => {
                    return `<button class="btn btn-primary" data-action="viewFroms" data-id="${data}"><i class="bi bi-binoculars"></i></button>`;
                }},
                { title: 'Domains', data: 'id', render: (data) => {
                    return `<button class="btn btn-primary" data-action="viewDomains" data-id="${data}"><i class="bi bi-binoculars"></i></button>`;
                }},
                { title: 'Preview', data: 'id', render: (data) => {
                    return `<button class="btn btn-primary" data-action="previewHTML" data-id="${data}"><i class="bi bi-binoculars"></i></button>`;
                }}
            ]
        }
    },
    methods: {
        fetchTemplateData() {
            const { id } = this.$route.params;
            this.templateId = id;
            const type = 'templates';

            axios.get(`${this.$store.state.back_url}/api/get/materials/${id}/${type}/*`)
                .then(res => {
                    const data = res.data;
                    const uniqueData = Array.from(new Set(data.map(item => JSON.stringify(item)))).map(item => JSON.parse(item));
                    const uniqueMaterials = uniqueData.filter((item, index, self) =>
                        index === self.findIndex((t) => (
                            t[7] === item[7]
                        ))
                    );
                    this.materials = uniqueMaterials.map(item => ({
                        id: item[1],
                        bodyName: item[7],
                        subjects: item[4],
                        froms: item[3],
                    }));
                    this.calculateTotals();
                })
                .catch(error => {
                    console.error('Error fetching template data:', error);
                });
        },
        handleClick(event) {
            const action = event.target.getAttribute('data-action');
            const id = event.target.getAttribute('data-id');

            if (action === 'viewFroms') {
                this.viewFroms(id);
            } else if (action === 'delete') {
                this.del(id);
            }
        },
        viewFroms(name) {
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
        calculateTotals() {
            if (this.materials.length > 0) {
                const subjectData = this.materials[0].subject;
                const fromData = this.materials[0].from;
                this.totalSubjects = subjectData.split('|').length;
                this.totalFromAddresses = fromData.split('\n').length;
            } else {
                this.totalSubjects = 0;
                this.totalFromAddresses = 0;
            }
        }
    },
    mounted() {
        this.fetchTemplateData();
    }
}
</script>

<style scoped>
.dummy-form {
    overflow: auto;
    margin-top: 2em;
    width: auto;
}
.table {
    margin-top: 1em;
}
</style>
