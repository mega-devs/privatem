<template>
    <div class="container d-flex align-items-center" style="width: 100vw; height: 100vh; position: fixed; background-color: black; top: 0; left: 0; max-width: none;">
        <div id="innerPage" class="w-100">
            <div class="login_div row align-items-center justify-content-center">
                <div class="col-sm-6 col-xs-12 d-sm-block d-none">
                    <div id="imgBgn">
                    </div>
                </div>
                <form method="post" @submit.prevent="submit" id="login-form" class="col-sm-6 col-xs-12 text-white p-5">
                    <div class="lead" style="color:red;">
                        <h3>Welcome Back</h3>
                    </div>
                    <div class="mt-4">
                        <p>Sign In</p>
                    </div>
                    <div class="form-floating mb-3" style="background-color: black;">
                        <input class="form-control" id="username" autocomplete="username" type="text" name="username" v-model="name" placeholder="Enter Login" style="color: white; " />
                        <label for="login">Login</label>
                    </div>
                    <div class="form-floating mb-4" style="background-color: black;">
                        <input class="form-control" id="password" autocomplete="current-password" style="color: white;" type="password" name="password" v-model="password" placeholder="Enter Password" />
                        <label for="current-password">Password</label>
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
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import router from "../router";
import axios from "axios";
import ButtonComponent from "../ui/ButtonComponent.vue";
import { useAuth } from "@/store";


export default {
    components: {
        ButtonComponent,
    },
    data() {
        return {
            name: null,
            password: null,
            error: null,
            uAuth: useAuth(),
        }
    },
    methods: {
        async submit() {
            try {
                const res = await axios.post(`${import.meta.env.VITE_BACK_URL}/api/login`, { name: this.name, password: this.password })
                this.uAuth.createCookie("authToken", res.data.token, 30);
                this.uAuth.setAuth()
                router.push('/dashboard')
            } catch (error) {
                this.error = 'User not found or password is incorrect!';
            }
        }
    },
	beforeMount() {
        let el = document.querySelector('body');
        el.setAttribute("data-bs-theme", "dark");
        el.style.backgroundColor = "black";
	},
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
