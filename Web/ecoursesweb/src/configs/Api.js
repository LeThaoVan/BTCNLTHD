import axios from 'axios'
import cookies from 'react-cookies'


export const endpoints = {
    "categories": "/categories/",
    "route": "/route/",
    "buses": (routeId) => `/route/${routeId}/buses/`,
    "buses-detail": (busesId) => `/buses/${busesId}/`,
    "login": "/o/token/",
    "current-user": "/users/current-user/",
    "like-buses": (busesId) => `/buses/${busesId}/like/`,
    'rate-buses': (busesId) => `/buses/${busesId}/rating/`,
    "buses-comments": (busesId) => `/buses/${busesId}/comments/`,
    "comments": "/comments/"
}

export const authAxios = () => axios.create({
    baseURL: 'https://nyle657.pythonanywhere.com/',
    headers: {
        'Authorization': `Bearer ${cookies.load('access_token')}`
    }
})

export default axios.create({
    baseURL: 'https://nyle657.pythonanywhere.com/'
}) 