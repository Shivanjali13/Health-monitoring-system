import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/users/token/refresh/`, {
            refresh: refreshToken,
          });
          localStorage.setItem('access_token', response.data.access);
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          return api(originalRequest);
        } catch (err) {
          localStorage.clear();
          window.location.href = '/login';
        }
      } else {
        localStorage.clear();
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/users/register/', data),
  login: (data) => api.post('/users/login/', data),
  getProfile: () => api.get('/users/profile/'),
  updateProfile: (data) => api.put('/users/profile/', data),
};

// Health Metrics API
export const healthAPI = {
  getMetrics: () => api.get('/health/metrics/'),
  createMetric: (data) => api.post('/health/metrics/', data),
  getMetric: (id) => api.get(`/health/metrics/${id}/`),
  getSummary: () => api.get('/health/summary/'),
  getAnomalies: () => api.get('/health/anomalies/'),
};

// Analytics API
export const analyticsAPI = {
  getWeightPrediction: () => api.get('/analytics/weight-prediction/'),
  getDiabetesRisk: () => api.get('/analytics/diabetes-risk/'),
  getHealthTips: () => api.get('/analytics/health-tips/'),
  getDashboard: () => api.get('/analytics/dashboard/'),
  markTipAsRead: (id) => api.patch(`/analytics/health-tips/${id}/`, { is_read: true }),
};

export default api;