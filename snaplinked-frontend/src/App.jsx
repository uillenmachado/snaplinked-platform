import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { Toaster } from '@/components/ui/toaster'
import { AuthProvider, useAuth } from '@/contexts/AuthContext'
import { ThemeProvider } from '@/contexts/ThemeContext'

// Pages
import LandingPage from '@/pages/LandingPage'
import LoginPage from '@/pages/LoginPage'
import RegisterPage from '@/pages/RegisterPage'
import DashboardPage from '@/pages/DashboardPage'
import AutomationsPage from '@/pages/AutomationsPage'
import LinkedInAccountsPage from '@/pages/LinkedInAccountsPage'
import AnalyticsPage from '@/pages/AnalyticsPage'
import SettingsPage from '@/pages/SettingsPage'
import ScriptsPage from '@/pages/ScriptsPage'
import PricingPage from '@/pages/PricingPage'
import LinkedInCallbackPage from '@/pages/LinkedInCallbackPage'

// Layout Components
import DashboardLayout from '@/components/layout/DashboardLayout'
import LoadingSpinner from '@/components/ui/loading-spinner'

import './App.css'

// Protected Route Component
function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }
  
  if (!user) {
    return <Navigate to="/login" replace />
  }
  
  return children
}

// Public Route Component (redirect to dashboard if authenticated)
function PublicRoute({ children }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }
  
  if (user) {
    return <Navigate to="/dashboard" replace />
  }
  
  return children
}

function AppRoutes() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/pricing" element={<PricingPage />} />
      
      {/* Auth Routes */}
      <Route 
        path="/login" 
        element={
          <PublicRoute>
            <LoginPage />
          </PublicRoute>
        } 
      />
      <Route 
        path="/register" 
        element={
          <PublicRoute>
            <RegisterPage />
          </PublicRoute>
        } 
      />
      
      {/* LinkedIn OAuth Callback */}
      <Route 
        path="/auth/linkedin/callback" 
        element={<LinkedInCallbackPage />} 
      />
      
      {/* Protected Dashboard Routes */}
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <DashboardPage />
            </DashboardLayout>
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/automations" 
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <AutomationsPage />
            </DashboardLayout>
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/linkedin-accounts" 
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <LinkedInAccountsPage />
            </DashboardLayout>
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/analytics" 
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <AnalyticsPage />
            </DashboardLayout>
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/settings" 
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <SettingsPage />
            </DashboardLayout>
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/scripts" 
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <ScriptsPage />
            </DashboardLayout>
          </ProtectedRoute>
        } 
      />
      
      {/* Catch all route */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="snaplinked-theme">
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-background">
            <AppRoutes />
            <Toaster />
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App
