import { createRouter, createWebHistory } from "vue-router";
import NotFoundComponent from "../components/NotFoundComponent.vue";
import LoginComponent from "../components/LoginComponent.vue";
import DashboardComponent from "../views/DashboardComponent.vue";
import TemplatesComponent from "../views/TemplatesComponent.vue";
import ProxiesComponent from "../views/ProxiesComponent.vue";
import SMTPsComponent from "../views/SMTPsComponent.vue";
import BasesComponent from "../components/BasesComponent.vue";
import TestComponent from "../components/TestComponent.vue";
import MailingComponent from "../components/MailingComponent.vue";
import DomainsComponent from "../views/DomainsComponent.vue";
import IMAPsComponent from "../views/IMAPsComponent.vue";
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
import SettingsComponent from "@/components/SettingsComponent.vue";
import { useAuth } from "@/store";

const routes = [
    {
        path: "/",
        component: NotFoundComponent,
        beforeEnter: (to, from, next) => {
            return next({
                name: "home"
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
        name: "home",
        component: DashboardComponent,
    },
    {
        path: "/dashboard/templates",
        name: "templates",
        component: TemplatesComponent,
    },
    {
        path: "/dashboard/proxies",
        name: "proxies",
        component: ProxiesComponent,
    },
    {
        path: "/dashboard/SMTPs",
        name: "SMTPs",
        component: SMTPsComponent,
    },
    {
        path: "/dashboard/IMAPs",
        name: "IMAPs",
        component: IMAPsComponent,
    },
    {
        path: "/dashboard/domains",
        name: "domains",
        component: DomainsComponent,
    },
    {
        path: "/dashboard/bases",
        name: "bases",
        component: BasesComponent,
    },
    {
        path: "/dashboard/test",
        name: "Test",
        component: TestComponent,
    },
    {
        path: "/dashboard/mailing",
        name: "Mailing",
        component: MailingComponent,
    },
    {
        path: "/dashboard/sendx",
        name: "SendX",
        component: SendXComponent,
    },
    {
        path: "/dashboard/database/proxies",
        name: "ProxiesDB",
        component: ProxiesDB,
    },
    {
        path: "/dashboard/database/smtps",
        name: "SMTPsDB",
        component: SMTPsDB,
    },
    {
        path: "/dashboard/database/imaps",
        name: "IMAPsDB",
        component: IMAPsDB,
    },
    {
        path: "/dashboard/database/domains",
        name: "DOMAINsDB",
        component: DOMAINsDB,
    },
    {
        path: "/dashboard/database/templates",
        name: "TemplatesDB",
        component: TemplatesDB,
    },
    {
        path: "/dashboard/database/bases",
        name: "BasesDB",
        component: BasesDB,
    },
    {
        path: "/dashboard/resetz",
        name: "ResetDB",
        component: ResetDB,
    },
    {
        path: "/dashboard/dummy",
        name: "Dummy",
        component: Dummy,
    },
    {
        path: "/dashboard/settings",
        name: "Settings",
        component: SettingsComponent,
    },
    {
        path: "/dashboard/templates/:id",
        name: "SingleTPL",
        component: SingleTPL,
        props: true,
    },
    {
        path: "/dashboard/proxies/1",
        name: "SinglePRX",
        component: SinglePRX,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    const uAuth = useAuth()
    if (to.name !== "Login" && !await uAuth.auth) {
        return next({
            name: "Login"
        })
    }
    next()
})

export default router;