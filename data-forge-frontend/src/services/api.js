import axios from 'axios';

// Get backend URL from environment variable
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

if (!BACKEND_URL) {
  console.error('REACT_APP_BACKEND_URL is not set!');
}

// Create axios instance with production-grade configuration for large file uploads
const api = axios.create({
  baseURL: BACKEND_URL,
  timeout: 0, // No timeout - let the upload complete
  maxContentLength: Infinity,
  maxBodyLength: Infinity,
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
    console.log('API Request:', config.method?.toUpperCase(), config.baseURL + config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for better error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Error:', error.message, error.config?.url);
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - connection issue');
    } else if (error.code === 'ERR_NETWORK') {
      console.error('Network error - check connection');
    } else if (error.response?.status === 413) {
      console.error('File too large');
    }
    return Promise.reject(error);
  }
);

export default api;
