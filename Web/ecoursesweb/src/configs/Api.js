import axios from 'axios'
import cookies from 'react-cookies'

export const endpoints = {
    "categories": "/categories/",
    "route": "/route/",
    "login": "/o/token/",
    "current-user": "/users/current-user/",
}

export const authApi = () => {
    return axios.create({
        baseURL: "https://nyle657.pythonanywhere.com",
        headers: {
            'Authorization': `Bearer ${cookies.load('token')}`
        }
    })
}

export default axios.create({
    baseURL: "https://nyle657.pythonanywhere.com"
})