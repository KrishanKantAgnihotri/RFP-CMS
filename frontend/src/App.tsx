import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container } from '@mui/material';
import { useAuth } from './hooks/useAuth';

// Layouts
import MainLayout from './components/layouts/MainLayout';
import AuthLayout from './components/layouts/AuthLayout';

// Pages
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import DashboardPage from './pages/dashboard/DashboardPage';
import RFPListPage from './pages/rfp/RFPListPage';
import RFPDetailPage from './pages/rfp/RFPDetailPage';
import CreateRFPPage from './pages/rfp/CreateRFPPage';
import EditRFPPage from './pages/rfp/EditRFPPage';
import ProfilePage from './pages/profile/ProfilePage';
import NotFoundPage from './pages/NotFoundPage';
import LoadingSpinner from './components/LoadingSpinner';

// Route guards
const PrivateRoute: React.FC<{ element: React.ReactElement }> = ({ element }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner message="Authenticating..." />;
  }

  return isAuthenticated ? element : <Navigate to="/login" />;
};

const PublicRoute: React.FC<{ element: React.ReactElement }> = ({ element }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner message="Authenticating..." />;
  }

  return isAuthenticated ? <Navigate to="/dashboard" /> : element;
};

const App: React.FC = () => {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<AuthLayout />}>
        <Route index element={<Navigate to="/login" />} />
        <Route
          path="login"
          element={<PublicRoute element={<LoginPage />} />}
        />
        <Route
          path="register"
          element={<PublicRoute element={<RegisterPage />} />}
        />
      </Route>

      {/* Private routes */}
      <Route path="/" element={<MainLayout />}>
        <Route
          path="dashboard"
          element={<PrivateRoute element={<DashboardPage />} />}
        />
        <Route
          path="rfps"
          element={<PrivateRoute element={<RFPListPage />} />}
        />
        <Route
          path="rfps/:id"
          element={<PrivateRoute element={<RFPDetailPage />} />}
        />
        <Route
          path="rfps/create"
          element={<PrivateRoute element={<CreateRFPPage />} />}
        />
        <Route
          path="rfps/:id/edit"
          element={<PrivateRoute element={<EditRFPPage />} />}
        />
        <Route
          path="profile"
          element={<PrivateRoute element={<ProfilePage />} />}
        />
      </Route>

      {/* 404 route */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};

export default App;
