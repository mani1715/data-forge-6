import axios from 'axios';

// Create axios instance with production-grade configuration for large file uploads
const api = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001/api',
  timeout: 0, // No timeout - let the upload complete
  maxContentLength: Infinity, // No limit
  maxBodyLength: Infinity, // No limit
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // For FormData uploads, remove Content-Type to let browser set it with boundary
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - connection issue');
    } else if (error.code === 'ERR_NETWORK') {
      console.error('Network error - check connection');
    } else if (error.response?.status === 413) {
      console.error('File too large - maximum 200MB');
    }
    return Promise.reject(error);
  }
);

export default api;
