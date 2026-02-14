import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000", // FastAPI backend
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // for cookie-based auth
});

// userd for debuggin, can delte later

// Add this interceptor to debug
API.interceptors.request.use((config) => {
  console.log(`🔵 Request: ${config.method?.toUpperCase()} ${config.url}`);
  console.log(`🔵 WithCredentials: ${config.withCredentials}`);
  console.log(`🔵 Cookies being sent:`, document.cookie);
  return config;
});

API.interceptors.response.use(
  (response) => {
    console.log(`✅ Response: ${response.status} from ${response.config.url}`);
    return response;
  },
  (error) => {
    console.log(`❌ Error: ${error.response?.status} from ${error.config?.url}`);
    return Promise.reject(error);
  }
);

//till here

// Middleware: attach JWT token automatically 

export default API;
