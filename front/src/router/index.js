import { createRouter, createWebHistory } from "vue-router";
import NotFoundComponent from "../components/NotFoundComponent.vue";
import LoginComponent from "../components/LoginComponent.vue";
import DashboardComponent from "../components/DashboardComponent.vue";
import TemplatesComponent from "../components/TemplatesComponent.vue";
import ProxiesComponent from "../components/ProxiesComponent.vue";
import SMTPsComponent from "../components/SMTPsComponent.vue";
import BasesComponent from "../components/BasesComponent.vue";
import TestComponent from "../components/TestComponent.vue";
import MailingComponent from "../components/MailingComponent.vue";
import DomainsComponent from "../components/DomainsComponent.vue";
import IMAPsComponent from "../components/IMAPsComponent.vue";
import ProxiesDB from "../components/db/ProxiesDB.vue";
import SendXComponent from "../components/SendXComponent.vue";
import SMTPsDB from "../components/db/SMTPsDB.vue";
import IMAPsDB from "../components/db/IMAPsDB.vue";
import DOMAINsDB from "../components/db/DOMAINsDB.vue";
import TemplatesDB from "../components/db/TemplatesDB.vue";
import BasesDB from "../components/db/BasesDB.vue";
import ResetDB from "../components/db/ResetDB.vue";
import Dummy from "../components/DummyComponent.vue";
import SingleTPL from "../components/singlepages/TplComponent.vue";
import SinglePRX from "../components/singlepages/PrxComponent.vue";
import store from "../store"
import SettingsComponent from "@/components/SettingsComponent.vue";

const routes = [
    {
        path: "/",
        component: NotFoundComponent,
        beforeEnter: (to, from, next) => {
            return next({
                name: "Dashboard"
            })
        }
    },
    {
        path: "/login",
        name: "Login",
        component: LoginComponent,
    },
    {
        path: "/dashboard",
        name: "Dashboard",
        component: DashboardComponent,
    },
    {
        path: "/dashboard/templates",
        name: "Templates",
        component: TemplatesComponent,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/proxies",
        name: "Proxies",
        component: ProxiesComponent,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/SMTPs",
        name: "SMTPs",
        component: SMTPsComponent,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/IMAPs",
        name: "IMAPs",
        component: IMAPsComponent,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/domains",
        name: "Domains",
        component: DomainsComponent,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/bases",
        name: "Bases",
        component: BasesComponent,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/test",
        name: "Test",
        component: TestComponent,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/mailing",
        name: "Mailing",
        component: MailingComponent,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/sendx",
        name: "SendX",
        component: SendXComponent,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/database/proxies",
        name: "ProxiesDB",
        component: ProxiesDB,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/database/smtps",
        name: "SMTPsDB",
        component: SMTPsDB,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/database/imaps",
        name: "IMAPsDB",
        component: IMAPsDB,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/database/domains",
        name: "DOMAINsDB",
        component: DOMAINsDB,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/database/templates",
        name: "TemplatesDB",
        component: TemplatesDB,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/database/bases",
        name: "BasesDB",
        component: BasesDB,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/resetz",
        name: "ResetDB",
        component: ResetDB,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/dummy",
        name: "Dummy",
        component: Dummy,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/settings",
        name: "Settings",
        component: SettingsComponent,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/templates/:id",
        name: "SingleTPL",
        component: SingleTPL,
        props: true,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
    {
        path: "/dashboard/proxies/1",
        name: "SinglePRX",
        component: SinglePRX,
        beforeEnter: (to, from, next) => {
            if (!store.state.auth) {
                return next({
                    name: "Login"
                })
            }
            next()
        }
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;