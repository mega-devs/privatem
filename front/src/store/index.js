import { createStore } from "vuex";
import axios from "axios";

const store = createStore({
    state: {
        back_url: "http://127.0.0.1:5001",
        sock_url: "wss://127.0.0.1:5001",
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