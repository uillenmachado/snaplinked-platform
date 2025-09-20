/**
 * API Service for SnapLinked
 * Handles all communication with the backend
 */

const API_BASE_URL = window.location.origin

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    // Add auth token if available
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Request failed')
      }

      return data
    } catch (error) {
      console.error('API Request failed:', error)
      throw error
    }
  }

  // Auth methods
  async login(email, password) {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
  }

  async register(userData) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    })
  }

  // User methods
  async getUserProfile() {
    return this.request('/api/users/profile')
  }

  async updateUserProfile(userData) {
    return this.request('/api/users/profile', {
      method: 'PUT',
      body: JSON.stringify(userData),
    })
  }

  async getUserStats() {
    return this.request('/api/users/stats')
  }

  async getUserActivity() {
    return this.request('/api/users/activity')
  }

  // Automation methods
  async getAutomations() {
    return this.request('/api/automations')
  }

  async createAutomation(automationData) {
    return this.request('/api/automations', {
      method: 'POST',
      body: JSON.stringify(automationData),
    })
  }

  async updateAutomation(id, automationData) {
    return this.request(`/api/automations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(automationData),
    })
  }

  async deleteAutomation(id) {
    return this.request(`/api/automations/${id}`, {
      method: 'DELETE',
    })
  }

  async toggleAutomation(id) {
    return this.request(`/api/automations/${id}/toggle`, {
      method: 'POST',
    })
  }

  // LinkedIn accounts methods
  async getLinkedInAccounts() {
    return this.request('/api/linkedin-accounts')
  }

  async addLinkedInAccount(accountData) {
    return this.request('/api/linkedin-accounts', {
      method: 'POST',
      body: JSON.stringify(accountData),
    })
  }

  async deleteLinkedInAccount(id) {
    return this.request(`/api/linkedin-accounts/${id}`, {
      method: 'DELETE',
    })
  }

  async verifyLinkedInAccount(id) {
    return this.request(`/api/linkedin-accounts/${id}/verify`, {
      method: 'POST',
    })
  }

  // Analytics methods
  async getAnalytics(timeRange = '7d') {
    return this.request(`/api/analytics?range=${timeRange}`)
  }

  // Settings methods
  async getSettings() {
    return this.request('/api/settings')
  }

  async updateSettings(settingsData) {
    return this.request('/api/settings', {
      method: 'PUT',
      body: JSON.stringify(settingsData),
    })
  }

  // Subscription methods
  async getSubscription() {
    return this.request('/api/subscription')
  }

  async getSubscriptionPlans() {
    return this.request('/api/payments/plans')
  }

  async createCheckoutSession(plan) {
    return this.request('/api/payments/create-checkout-session', {
      method: 'POST',
      body: JSON.stringify({ plan }),
    })
  }

    // LinkedIn OAuth methods
  async connectLinkedIn() {
    return this.request('/api/auth/linkedin/connect')
  }

  async getLinkedInProfile() {
    return this.request('/api/linkedin/profile')
  }

  async disconnectLinkedIn() {
    return this.request('/api/linkedin/disconnect', {
      method: 'POST',
    })
  }

  async getLinkedInStats() {
    return this.request('/api/linkedin/stats')
  }

  async createLinkedInPost(text, visibility = 'PUBLIC') {
    return this.request('/api/linkedin/post', {
      method: 'POST',
      body: JSON.stringify({ text, visibility }),
    })
  }

  async searchLinkedInPeople(keywords, start = 0, count = 25) {
    return this.request(`/api/linkedin/search?keywords=${encodeURIComponent(keywords)}&start=${start}&count=${count}`)
  }

  async getLinkedInConnections(start = 0, count = 50) {
    return this.request(`/api/linkedin/connections?start=${start}&count=${count}`)
  }

  // Health check
  async healthCheck() {
    return this.request('/api/health')
  }
}

const api = new ApiService()
export { api }
export default api
