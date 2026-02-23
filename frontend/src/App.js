import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './utils/AuthContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import HealthMetrics from './pages/HealthMetrics';
import Predictions from './pages/Predictions';
import HealthTips from './pages/HealthTips';
import Loading from './components/Loading';
import './App.css';

const PrivateRoute = ({ children }) => {
  const { user, loading } = useContext(AuthContext);
  
  if (loading) return <Loading />;
  
  return user ? children : <Navigate to="/login" />;
};

const PublicRoute = ({ children }) => {
  const { user, loading } = useContext(AuthContext);
  
  if (loading) return <Loading />;
  
  return user ? <Navigate to="/" /> : children;
};

function AppContent() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          {/* Public Routes */}
          <Route 
            path="/login" 
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } 
          />
          <Route 
            path="/register" 
            element={
              <PublicRoute>
                <Register />
              </PublicRoute>
            } 
          />

          {/* Private Routes */}
          <Route 
            path="/" 
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/metrics" 
            element={
              <PrivateRoute>
                <HealthMetrics />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/predictions" 
            element={
              <PrivateRoute>
                <Predictions />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/tips" 
            element={
              <PrivateRoute>
                <HealthTips />
              </PrivateRoute>
            } 
          />

          {/* Catch all */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;