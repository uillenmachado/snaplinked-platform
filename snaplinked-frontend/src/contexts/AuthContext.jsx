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

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, config)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || data.error || 'Algo deu errado')
      }

      return data
    } catch (error) {
      console.error('API Call Error:', error)
      throw error
    }
  }

  // Carregar usuário do token ao iniciar app
  useEffect(() => {
    const loadUser = async () => {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          setLoading(false)
          return
        }

        // Verificar se o token ainda é válido
        try {
          const payload = JSON.parse(atob(token.split('.')[1]))
          const currentTime = Date.now() / 1000
          
          if (payload.exp < currentTime) {
            // Token expirado
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            setLoading(false)
            return
          }
          
          // Token válido, definir usuário
          setUser({
            id: payload.user_id,
            email: payload.email,
            name: 'Demo User',
            plan: 'Premium'
          })
        } catch (tokenError) {
          console.error('Token inválido:', tokenError)
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        }
      } catch (error) {
        console.error('Erro ao carregar usuário:', error)
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
      
      // Fazer chamada direta para a API sem usar apiCall para evitar problemas
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()

      if (response.ok && data.success) {
        const { user, token } = data
        
        // Armazenar token
        localStorage.setItem('access_token', token)
        
        // Definir usuário
        setUser(user)
        
        // Toast removido temporariamente para evitar problemas
        console.log('Login realizado com sucesso:', user.name)
        
        return { success: true }
      } else {
        const errorMessage = data.error || 'Credenciais inválidas'
        // Toast removido temporariamente para evitar problemas
        console.error('Falha no login:', errorMessage)
        return { success: false, error: errorMessage }
      }
    } catch (error) {
      console.error('Erro no login:', error)
      const errorMessage = 'Erro de conexão com o servidor'
      // Toast removido temporariamente para evitar problemas
      console.error('Erro de conexão:', errorMessage)
      return { success: false, error: errorMessage }
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
          title: 'Registro realizado com sucesso',
          description: `Bem-vindo ao SnapLinked, ${user.name}!`,
        })
        
        return { success: true }
      }
    } catch (error) {
      toast({
        title: 'Falha no registro',
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
        title: 'Logout realizado',
        description: 'Você foi desconectado com sucesso.',
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
          title: 'Perfil atualizado',
          description: 'Seu perfil foi atualizado com sucesso.',
        })
        
        return { success: true }
      }
    } catch (error) {
      toast({
        title: 'Falha na atualização',
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
          title: 'Senha alterada',
          description: 'Sua senha foi alterada com sucesso.',
        })
        
        return { success: true }
      }
    } catch (error) {
      toast({
        title: 'Falha na alteração da senha',
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
