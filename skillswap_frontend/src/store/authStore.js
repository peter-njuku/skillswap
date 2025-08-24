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
                    const token = res.data.access_token;
                    const profile = await axios.get('http://localhost:8000/users/me', 
                        {headers:{"Authorization": `Bearer ${token}`}}
                    );
                    set({
                        user: profile.data,
                        token: token,
                    });
                    return res.data
                }catch(err){
                    console.error("Login Failed: ", err.response?.data || err.message);
                    throw err;
                }
            },
            logout: () => set({user: null, token:null}),
            fetchUserSkills: async () =>{
                const token = get().token;
                if(!token) return;
                try{
                    const response = await axios.get('http://localhost:8000/users/me', {
                        headers:{"Authorization": `Bearer ${token}`}
                    });
                    set({user:response.data})
                }catch(err){
                    console.error("Fetching skills failed: ", err.response?.data || err.message)
                }
            }
        }),
        {name:'auth-storage'}
    )
)
