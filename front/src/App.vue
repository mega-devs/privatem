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

<template>
  <div>
    <h1>Welcome</h1>
    <button @click="throwError">Trigger Sentry Error</button>
  </div>
</template>

<script>
export default {
  methods: {
    throwError() {
      // Trigger a test error to see if Sentry catches it
      throw new Error("Test error for Sentry!");
    }
  }
};
</script>
