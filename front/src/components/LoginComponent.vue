<template>
    <div class="container d-flex align-items-center" style="width: 100vw; height: 100vh; position: fixed; background-color: black; top: 0; left: 0; max-width: none;">
        <div id="innerPage" class="w-100">
            <div class="login_div row align-items-center justify-content-center">
                <div class="col-sm-6 col-xs-12 d-sm-block d-none">
                    <div id="imgBgn">
                    </div>
                </div>
                <div class="col-sm-6 col-xs-12 text-white p-5">
                    <div class="lead" style="color:red;">
                        <h3>Welcome Back</h3>
                    </div>
                    <div class="mt-4">
                        <p>Sign In</p>
                    </div>
                    <div class="form-floating mb-3" style="background-color: black;">
                        <input class="form-control" id="floatingInput" type="login" name="" v-model="name" placeholder="Enter Login" style="color: white; " />
                        <label for="floatingInput">Login</label>
                    </div>
                    <div class="form-floating mb-4" style="background-color: black;">
                        <input class="form-control" id="floatingPassword" style="color: white;" type="password" name="" v-model="password" placeholder="Enter Password" />
                        <label for="floatingPassword">Password</label>
                    </div>
                    <p class="mt-4">{{ error }}</p>
                    <ButtonComponent 
                        button-type="submit"
                        @click-handler="submit"
                        button-text="Submit"
                        is-info
                        is-full
                        class-names="mt-4 mb-10"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import router from "../router";
import axios from "axios";
import ButtonComponent from "../ui/ButtonComponent.vue";

function createCookie(name, value, days) {
    let date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + date.toUTCString();
    document.cookie = name + "=" + value + "; " + expires + "; path=/";
}

export default {
    components: {
        ButtonComponent,
    },
    data() {
        return {
            name: null,
            password: null,
            error: null,
        }
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
        submit() {
            console.log('here')
            axios.post(`${this.$store.state.back_url}/api/login`, { name: this.name, password: this.password }).then(res => {
                this.error = ''
                createCookie("authToken", res.data.token, 30)
                this.setAuth()
                router.push('/dashboard')
            }).catch(errors => {
                this.error = 'User not found or password is incorrect!';
            })
        }
    },
	beforeMount() {
    this.setAuth();
    let el = document.querySelector('body');
    el.setAttribute("data-bs-theme", "dark");
    el.style.backgroundColor = "black";

	},

    mounted() {
        setTimeout(() => {
            if (this.$store.state.auth) {
                router.back()
            }
        }, 500)
    }
};
</script>

<style scoped>
body, html {
    background-color: black !important;
    color: white;
    height: 100%;
    margin: 0;
    padding: 0;
}

#innerPage {
    width: 100%;
    max-width: 840px;
    margin: 0 auto;
    border-radius: 12px;
    background: #202630;
    box-shadow: 7px 7px 13px 1px #010b1e, -10px -9px 11px 1px #202630;
}

.form-control {
    background: none;
    border: none;
    border-bottom: 1px solid #202630;
    color: #fff;
}

#imgBgn {
    background: url('../assets/logo.jpg') no-repeat center center;
    background-size: contain;
    min-height: 75vh;
    width: 100%;
    border-radius: 12px 0 0 12px;
}

.container, .row, .col-sm-6, .col-xs-12 {
    padding: 0;
    height: 100%;
}

.login_div {
  padding: 0 0 0 3rem;
  border-radius: 20px;
}

/deep/ .btn-primary {
  background-color: var(--primary) !important;
  color: white !important;
  font-weight: 600 !important;
  border: none;
  transition: background-color 0.2s linear;
}
</style>
