/**
 * Serviço unificado de API para SnapLinked
 * Centraliza todas as chamadas HTTP com interceptors e tratamento de erros
 */

class ApiService {
  constructor() {
    this.baseURL = window.location.origin
    this.defaultHeaders = {
      'Content-Type': 'application/json'
    }
  }

  /**
   * Método base para requisições HTTP
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    
    const config = {
      headers: {
        ...this.defaultHeaders,
        ...options.headers,
      },
      ...options,
    }

    // Adicionar token de autenticação se disponível
    const token = this.getAuthToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    try {
      const response = await fetch(url, config)
      
      // Verificar se a resposta é JSON
      const contentType = response.headers.get('content-type')
      const isJson = contentType && contentType.includes('application/json')
      
      let data
      if (isJson) {
        data = await response.json()
      } else {
        data = { message: await response.text() }
      }

      if (!response.ok) {
        // Tratar erro de autenticação
        if (response.status === 401) {
          this.handleAuthError()
        }
        
        throw new ApiError(
          data.message || data.error || 'Erro na requisição',
          response.status,
          data
        )
      }

      return data
    } catch (error) {
      if (error instanceof ApiError) {
        throw error
      }
      
      // Erro de rede ou outro erro
      throw new ApiError(
        'Erro de conexão. Verifique sua internet.',
        0,
        { originalError: error.message }
      )
    }
  }

  /**
   * Métodos HTTP convenientes
   */
  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const url = queryString ? `${endpoint}?${queryString}` : endpoint
    
    return this.request(url, { method: 'GET' })
  }

  async post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async put(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' })
  }

  /**
   * Gerenciamento de autenticação
   */
  getAuthToken() {
    return localStorage.getItem('access_token')
  }

  setAuthToken(token) {
    if (token) {
      localStorage.setItem('access_token', token)
    } else {
      localStorage.removeItem('access_token')
    }
  }

  handleAuthError() {
    // Limpar tokens
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    
    // Redirecionar para login se não estiver na página de login
    if (!window.location.pathname.includes('/login')) {
      window.location.href = '/login'
    }
  }

  /**
   * Métodos específicos da aplicação
   */

  // Autenticação
  async login(email, password) {
    const response = await this.post('/api/auth/login', { email, password })
    
    if (response.success && response.tokens) {
      this.setAuthToken(response.tokens.access_token)
      localStorage.setItem('refresh_token', response.tokens.refresh_token)
    }
    
    return response
  }

  async register(userData) {
    const response = await this.post('/api/auth/register', userData)
    
    if (response.success && response.tokens) {
      this.setAuthToken(response.tokens.access_token)
      localStorage.setItem('refresh_token', response.tokens.refresh_token)
    }
    
    return response
  }

  async logout() {
    try {
      await this.post('/api/auth/logout')
    } finally {
      this.setAuthToken(null)
      localStorage.removeItem('refresh_token')
    }
  }

  async getCurrentUser() {
    return this.get('/api/auth/me')
  }

  // LinkedIn
  async connectLinkedIn() {
    return this.get('/api/auth/linkedin/connect')
  }

  async manualLinkedInLogin(email, password) {
    return this.post('/api/linkedin/manual-login', { email, password })
  }

  async getLinkedInProfile() {
    return this.get('/api/linkedin/profile')
  }

  async disconnectLinkedIn() {
    return this.post('/api/linkedin/disconnect')
  }

  async getLinkedInStats() {
    return this.get('/api/linkedin/stats')
  }

  // Automações
  async getAutomations() {
    return this.get('/api/automations')
  }

  async createAutomation(automationData) {
    return this.post('/api/automations', automationData)
  }

  async updateAutomation(id, automationData) {
    return this.put(`/api/automations/${id}`, automationData)
  }

  async deleteAutomation(id) {
    return this.delete(`/api/automations/${id}`)
  }

  async toggleAutomation(id) {
    return this.post(`/api/automations/${id}/toggle`)
  }

  async runAutomation(config) {
    return this.post('/api/automations/run', config)
  }

  async getAutomationStats() {
    return this.get('/api/automations/stats')
  }

  // Analytics
  async getAnalytics(timeRange = '7d') {
    return this.get('/api/analytics', { range: timeRange })
  }

  async getDashboardStats() {
    return this.get('/api/dashboard/stats')
  }

  // Usuário
  async getUserProfile() {
    return this.get('/api/users/profile')
  }

  async updateUserProfile(userData) {
    return this.put('/api/users/profile', userData)
  }

  async getUserStats() {
    return this.get('/api/users/stats')
  }

  // Pagamentos
  async getSubscriptionPlans() {
    return this.get('/api/payments/plans')
  }

  async createCheckoutSession(plan) {
    return this.post('/api/payments/create-checkout-session', { plan })
  }

  // Health check
  async healthCheck() {
    return this.get('/api/health')
  }
}

/**
 * Classe de erro personalizada para API
 */
class ApiError extends Error {
  constructor(message, status, data = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
}

// Instância singleton
const apiService = new ApiService()

export { apiService, ApiError }
export default apiService
