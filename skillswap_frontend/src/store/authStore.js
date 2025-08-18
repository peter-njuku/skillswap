import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import axios from 'axios';

export const useAuthStore = create(
    persist(
        (set) => ({
            user:null,
            token:null,
            login:async(email, password) => {
                try{
                    const params = new URLSearchParams();
                    params.append("username", email);
                    params.append("password", password);
                    const res = await axios.post(
                        'http://127.0.0.1:8000/auth/login',
                        params,
                        {headers:{"Content-Type":"application/x-www-form-urlencoded"}}
                    );
                    set({
                        user: {email},
                        token: res.data.access_token,
                    });
                    return res.data
                }catch(err){
                    console.error("Login Failed: ", err.response?.data || err.message);
                    throw err;
                }
            },
            logout: () => set({user: null, token:null}),
        }),
        {name:'auth-storage'}
    )
)