import axios from 'axios';

// Base API configuration
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized errors
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email: string, password: string) => api.post('/users/login', { username: email, password }),
  register: (userData: any) => api.post('/users/register', userData),
  getCurrentUser: () => api.get('/users/me'),
  updateProfile: (userData: any) => api.put('/users/me', userData),
};

// RFP API
export const rfpAPI = {
  getRFPs: (params?: any) => api.get('/rfps', { params }),
  getRFP: (id: string) => api.get(`/rfps/${id}`),
  createRFP: (rfpData: any) => api.post('/rfps', rfpData),
  updateRFP: (id: string, rfpData: any) => api.put(`/rfps/${id}`, rfpData),
  getRFPResponses: (rfpId: string) => api.get(`/rfps/${rfpId}/responses`),
  createRFPResponse: (rfpId: string, responseData: any) => api.post(`/rfps/${rfpId}/responses`, responseData),
};

// Document API
export const documentAPI = {
  uploadDocument: (formData: FormData) => api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  getDocuments: (params?: any) => api.get('/documents', { params }),
  getDocument: (id: string) => api.get(`/documents/${id}`),
  downloadDocument: (id: string) => api.get(`/documents/${id}/download`, { responseType: 'blob' }),
};

// Notification API
export const notificationAPI = {
  getNotifications: (params?: any) => api.get('/notifications', { params }),
  getNotification: (id: string) => api.get(`/notifications/${id}`),
  markAsRead: (id: string) => api.put(`/notifications/${id}`, { is_read: true }),
  markAllAsRead: () => api.put('/notifications/read-all'),
};

export default api;
