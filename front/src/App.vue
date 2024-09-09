<script setup>
</script>

<template>  
  <RouterView/>
</template>
<script>
export default {
  data() {
    return {}
  },
  methods: {
    setAuth() {
        let token = ''
        let cookies = document.cookie.split(";")
        cookies.forEach(cookie => {
            if (cookie.includes('authToken')) {
                token = cookie.split("=")[1];
            }
        })
        this.$store.dispatch('setAuth', token)
    },
  },
  beforeMount() {
    this.setAuth()
    let el = document.querySelector('html')
    el.setAttribute("data-bs-theme", "dark")
  },
}
</script>
<style>
</style>
