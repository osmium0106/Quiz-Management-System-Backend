# Frontend Integration Guide - CORS Configured

## ✅ CORS Configuration Updated!

Your backend is now configured to accept requests from your frontend running on `http://localhost:3000/`.

## 🔧 Backend Configuration Applied

### CORS Settings Updated:
- ✅ **Allowed Origins**: `http://localhost:3000`, `http://127.0.0.1:3000`
- ✅ **Allow Credentials**: `true` (for JWT cookies if needed)
- ✅ **Allowed Methods**: GET, POST, PUT, PATCH, DELETE, OPTIONS
- ✅ **Allowed Headers**: Authorization, Content-Type, Accept, and more
- ✅ **Development Mode**: All origins allowed in DEBUG mode

## 🚀 Frontend Configuration

### Environment Variables for Your Frontend (.env)
```env
# Backend API Configuration
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_SWAGGER_URL=http://localhost:8000/swagger/
```

### Axios Configuration (recommended)
```javascript
// src/config/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false, // Set to true if using cookies
});

// Add request interceptor for JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken
          });
          
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          
          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

## 🔐 Authentication Example

### Login Function
```javascript
// src/services/authService.js
import api from '../config/api';

export const authService = {
  // Register admin user
  register: async (userData) => {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  },

  // Login user
  login: async (credentials) => {
    const response = await api.post('/auth/login/', credentials);
    const { data } = response.data;
    
    // Store tokens
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  },

  // Logout user
  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        await api.post('/auth/logout/', { refresh_token: refreshToken });
      } catch (error) {
        console.error('Logout error:', error);
      }
    }
    
    // Clear local storage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  // Get current user
  getCurrentUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  }
};
```

## 📊 API Usage Examples

### Quiz Management
```javascript
// src/services/quizService.js
import api from '../config/api';

export const quizService = {
  // Get all quizzes (admin)
  getQuizzes: async (page = 1, search = '') => {
    const response = await api.get(`/admin/quizzes/?page=${page}&search=${search}`);
    return response.data;
  },

  // Create quiz
  createQuiz: async (quizData) => {
    const response = await api.post('/admin/quizzes/', quizData);
    return response.data;
  },

  // Get quiz details
  getQuiz: async (quizId) => {
    const response = await api.get(`/admin/quizzes/${quizId}/`);
    return response.data;
  },

  // Update quiz
  updateQuiz: async (quizId, quizData) => {
    const response = await api.put(`/admin/quizzes/${quizId}/`, quizData);
    return response.data;
  },

  // Delete quiz
  deleteQuiz: async (quizId) => {
    await api.delete(`/admin/quizzes/${quizId}/`);
  },

  // Add question to quiz
  addQuestion: async (quizId, questionData) => {
    const response = await api.post(`/admin/quizzes/${quizId}/questions/`, questionData);
    return response.data;
  }
};
```

### Public Quiz Taking
```javascript
// src/services/publicQuizService.js
import api from '../config/api';

export const publicQuizService = {
  // Get public quizzes
  getPublicQuizzes: async () => {
    const response = await api.get('/public/quizzes/');
    return response.data;
  },

  // Get quiz for taking
  getQuizForTaking: async (quizId) => {
    const response = await api.get(`/public/quizzes/${quizId}/`);
    return response.data;
  },

  // Submit quiz response
  submitQuiz: async (quizId, submissionData) => {
    const response = await api.post(`/public/quizzes/${quizId}/submit/`, submissionData);
    return response.data;
  },

  // Get quiz results
  getResults: async (sessionId) => {
    const response = await api.get(`/public/results/${sessionId}/`);
    return response.data;
  }
};
```

## 🧪 Test Connection

You can test the connection from your frontend with this simple function:

```javascript
// Test connection
const testConnection = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/public/quizzes/');
    const data = await response.json();
    console.log('Backend connection successful:', data);
  } catch (error) {
    console.error('Backend connection failed:', error);
  }
};

// Call this function to test
testConnection();
```

## 🔍 Available Endpoints for Your Frontend

### Public Endpoints (No Auth Required)
- `GET /api/v1/public/quizzes/` - List available quizzes
- `GET /api/v1/public/quizzes/{id}/` - Get quiz for taking
- `POST /api/v1/public/quizzes/{id}/submit/` - Submit quiz
- `GET /api/v1/public/results/{session_id}/` - Get results

### Authentication Endpoints
- `POST /api/v1/auth/register/` - Register admin
- `POST /api/v1/auth/login/` - Login
- `POST /api/v1/auth/logout/` - Logout
- `POST /api/v1/auth/token/refresh/` - Refresh token

### Admin Endpoints (Auth Required)
- `GET /api/v1/admin/quizzes/` - List quizzes
- `POST /api/v1/admin/quizzes/` - Create quiz
- `GET /api/v1/admin/quizzes/{id}/` - Get quiz details
- `PUT /api/v1/admin/quizzes/{id}/` - Update quiz
- `DELETE /api/v1/admin/quizzes/{id}/` - Delete quiz
- `POST /api/v1/admin/quizzes/{id}/questions/` - Add question

## 🎯 Ready to Connect!

Your backend is now properly configured to accept requests from your frontend at `http://localhost:3000/`. 

1. ✅ **CORS is enabled** for your frontend URL
2. ✅ **All necessary headers** are allowed
3. ✅ **Authentication flow** is ready for JWT tokens
4. ✅ **API endpoints** are documented and accessible

Start making API calls from your React frontend and everything should work smoothly!