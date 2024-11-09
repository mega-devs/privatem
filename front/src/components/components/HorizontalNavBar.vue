<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid justify-content-center">
            <ul class="nav nav-pills">
                <li class="nav-item">
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
            </ul>
        </div>
    </nav>
</template>

<script>
export default {
    props: {
        stateProp: {
            type: String,
            required: true
        }
    }
};
</script>

<style scoped>

.nav-link {
  margin: 0 10px;
}

.nav-link {
    color: white; /* Default link color */
}
.nav-link.active {
    background-color: #007bff; /* Active link background color */
}
</style>