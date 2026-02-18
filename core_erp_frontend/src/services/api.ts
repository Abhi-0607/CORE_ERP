import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000", // FastAPI backend
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // for cookie-based auth
});

// Middleware: attach JWT token automatically 

export default API;
