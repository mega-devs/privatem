import { defineStore } from 'pinia';
import axios from "axios";
import { ref, computed } from 'vue';

export const useAuth = defineStore("auth", () => {
    const back_url = import.meta.env.VITE_BACK_URL;
    const sock_url = import.meta.env.VITE_SOCK_URL;
    const auth = computed(async ()=>{
        const token = document.cookie.split(";").filter(cookie => cookie.includes('authToken'))[0].split("=")[1];
        console.log(token);
        try {
            const res = await axios.post(`${back_url}/api/check/token`, {token: token});
            return res.data.data == "success";
        } catch {
            return false;
        }
    })

    const setAuth = () => {
        let token = ''
        let cookies = document.cookie.split(";")
        cookies.forEach(cookie => {
            if (cookie.includes('authToken')) {
                token = cookie.split("=")[1];
            }
        })
    }

    const createCookie = (name, value, days) => {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/`
    }

    return {
        back_url, auth, sock_url,
        setAuth, createCookie, createCookie
    }
})