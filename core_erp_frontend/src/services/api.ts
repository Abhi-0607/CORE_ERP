import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000", // your FastAPI backend
  headers: {
    "Content-Type": "application/json",
  },
});

// Middleware: attach JWT token if exists
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default API;
