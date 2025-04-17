// src/services/loginApi.js
import axios from 'axios'

const loginApi = axios.create({
  baseURL: 'http://127.0.0.1:8000/dj-rest-auth',
  withCredentials: true
})

export default loginApi
