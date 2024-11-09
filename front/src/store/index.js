import { createStore } from "vuex";
import axios from "axios";

const store = createStore({
    state: {
        back_url: import.meta.env.VITE_BACK_URL,
        sock_url: import.meta.env.VITE_SOCK_URL,
        auth: null,
      },
    mutations: {
        setAuth_(state, isAuth) {
            state.auth = isAuth
          },
    },
    actions: {
        setAuth({dispatch}, token) {
            axios.post(`${this.state.back_url}/api/check/token`, {token: token}).then(res => {
                dispatch('attemptAuth', true);
            })
            .catch(error => {
                dispatch('attemptAuth', false);
            })
        },
        attemptAuth({commit}, isAuth) {
            commit('setAuth_', isAuth);
        },  
    }  
})

export default store;