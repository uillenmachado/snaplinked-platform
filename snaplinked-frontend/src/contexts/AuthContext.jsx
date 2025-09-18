import { createContext, useContext, useState, useEffect } from 'react'
import { useToast } from '@/hooks/use-toast'

const AuthContext = createContext({})

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const { toast } = useToast()

  // API helper function
  const apiCall = async (endpoint, options = {}) => {
    const token = localStorage.getItem('access_token')
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config)
    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Something went wrong')
    }

    return data
  }

  // Load user from token on app start
  useEffect(() => {
    const loadUser = async () => {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          setLoading(false)
          return
        }

        const response = await apiCall('/auth/me')
        if (response.success) {
          setUser(response.user)
        } else {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        }
      } catch (error) {
        console.error('Failed to load user:', error)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      } finally {
        setLoading(false)
      }
    }

    loadUser()
  }, [])

  const login = async (email, password) => {
    try {
      setLoading(true)
      
      const response = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })

      if (response.success) {
        const { user, tokens } = response
        
        // Store tokens
        localStorage.setItem('access_token', tokens.access_token)
        localStorage.setItem('refresh_token', tokens.refresh_token)
        
        setUser(user)
        
        toast({
          title: 'Login successful',
          description: `Welcome back, ${user.first_name}!`,
        })
        
        return { success: true }
      }
    } catch (error) {
      toast({
        title: 'Login failed',
        description: error.message,
        variant: 'destructive',
      })
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const register = async (userData) => {
    try {
      setLoading(true)
      
      const response = await apiCall('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData),
      })

      if (response.success) {
        const { user, tokens } = response
        
        // Store tokens
        localStorage.setItem('access_token', tokens.access_token)
        localStorage.setItem('refresh_token', tokens.refresh_token)
        
        setUser(user)
        
        toast({
          title: 'Registration successful',
          description: `Welcome to SnapLinked, ${user.first_name}!`,
        })
        
        return { success: true }
      }
    } catch (error) {
      toast({
        title: 'Registration failed',
        description: error.message,
        variant: 'destructive',
      })
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    try {
      await apiCall('/auth/logout', { method: 'POST' })
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local storage and state regardless of API call result
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      setUser(null)
      
      toast({
        title: 'Logged out',
        description: 'You have been successfully logged out.',
      })
    }
  }

  const updateProfile = async (profileData) => {
    try {
      const response = await apiCall('/auth/me', {
        method: 'PUT',
        body: JSON.stringify(profileData),
      })

      if (response.success) {
        setUser(response.user)
        
        toast({
          title: 'Profile updated',
          description: 'Your profile has been updated successfully.',
        })
        
        return { success: true }
      }
    } catch (error) {
      toast({
        title: 'Update failed',
        description: error.message,
        variant: 'destructive',
      })
      return { success: false, error: error.message }
    }
  }

  const changePassword = async (currentPassword, newPassword) => {
    try {
      const response = await apiCall('/auth/change-password', {
        method: 'POST',
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      })

      if (response.success) {
        toast({
          title: 'Password changed',
          description: 'Your password has been changed successfully.',
        })
        
        return { success: true }
      }
    } catch (error) {
      toast({
        title: 'Password change failed',
        description: error.message,
        variant: 'destructive',
      })
      return { success: false, error: error.message }
    }
  }

  // Token refresh function
  const refreshToken = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }

      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${refreshToken}`,
        },
      })

      const data = await response.json()

      if (response.ok && data.success) {
        localStorage.setItem('access_token', data.tokens.access_token)
        localStorage.setItem('refresh_token', data.tokens.refresh_token)
        return data.tokens.access_token
      } else {
        throw new Error('Token refresh failed')
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
      logout()
      return null
    }
  }

  // Enhanced API call with automatic token refresh
  const authenticatedApiCall = async (endpoint, options = {}) => {
    try {
      return await apiCall(endpoint, options)
    } catch (error) {
      // If unauthorized, try to refresh token
      if (error.message.includes('401') || error.message.includes('token')) {
        const newToken = await refreshToken()
        if (newToken) {
          // Retry the request with new token
          return await apiCall(endpoint, options)
        }
      }
      throw error
    }
  }

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    apiCall: authenticatedApiCall,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
