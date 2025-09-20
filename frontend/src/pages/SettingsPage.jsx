import React, { useState } from 'react'
import { Save, User, Bell, Shield, CreditCard, Trash2, Eye, EyeOff, Download, Upload } from 'lucide-react'
import LoadingSpinner from '@/components/ui/loading-spinner'

const SettingsPage = () => {
  const [activeTab, setActiveTab] = useState('profile')
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [settings, setSettings] = useState({
    profile: {
      first_name: 'Demo',
      last_name: 'User',
      email: 'demo@snaplinked.com',
      company: 'SnapLinked Demo',
      phone: '+55 11 99999-9999',
      timezone: 'America/Sao_Paulo',
      language: 'pt-BR'
    },
    notifications: {
      email_automation_complete: true,
      email_daily_report: true,
      email_weekly_summary: false,
      email_marketing: false,
      push_automation_complete: true,
      push_connection_accepted: true,
      push_daily_limit_reached: true
    },
    security: {
      two_factor_enabled: false,
      login_notifications: true,
      session_timeout: 30
    },
    automation: {
      default_daily_limit: 50,
      auto_pause_on_limit: true,
      randomize_timing: true,
      min_delay_seconds: 30,
      max_delay_seconds: 120,
      working_hours_start: '09:00',
      working_hours_end: '18:00',
      working_days: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    }
  })

  const tabs = [
    { id: 'profile', label: 'Perfil', icon: User },
    { id: 'notifications', label: 'Notificações', icon: Bell },
    { id: 'security', label: 'Segurança', icon: Shield },
    { id: 'automation', label: 'Automação', icon: CreditCard }
  ]

  const handleSave = async () => {
    setLoading(true)
    // Simulate API call
    setTimeout(() => {
      setLoading(false)
      // Show success message (you could use a toast here)
      alert('Configurações salvas com sucesso!')
    }, 1000)
  }

  const handleInputChange = (section, field, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }))
  }

  const exportSettings = () => {
    const data = JSON.stringify(settings, null, 2)
    const blob = new Blob([data], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'snaplinked-settings.json'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const importSettings = (event) => {
    const file = event.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const importedSettings = JSON.parse(e.target.result)
          setSettings(importedSettings)
          alert('Configurações importadas com sucesso!')
        } catch {
          alert('Erro ao importar configurações. Verifique o formato do arquivo.')
        }
      }
      reader.readAsText(file)
    }
  }

  const ProfileTab = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Informações Pessoais</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Nome</label>
            <input
              type="text"
              value={settings.profile.first_name}
              onChange={(e) => handleInputChange('profile', 'first_name', e.target.value)}
              className="w-full border rounded-md px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Sobrenome</label>
            <input
              type="text"
              value={settings.profile.last_name}
              onChange={(e) => handleInputChange('profile', 'last_name', e.target.value)}
              className="w-full border rounded-md px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              value={settings.profile.email}
              onChange={(e) => handleInputChange('profile', 'email', e.target.value)}
              className="w-full border rounded-md px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Empresa</label>
            <input
              type="text"
              value={settings.profile.company}
              onChange={(e) => handleInputChange('profile', 'company', e.target.value)}
              className="w-full border rounded-md px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Telefone</label>
            <input
              type="tel"
              value={settings.profile.phone}
              onChange={(e) => handleInputChange('profile', 'phone', e.target.value)}
              className="w-full border rounded-md px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Fuso Horário</label>
            <select
              value={settings.profile.timezone}
              onChange={(e) => handleInputChange('profile', 'timezone', e.target.value)}
              className="w-full border rounded-md px-3 py-2"
            >
              <option value="America/Sao_Paulo">São Paulo (GMT-3)</option>
              <option value="America/New_York">Nova York (GMT-5)</option>
              <option value="Europe/London">Londres (GMT+0)</option>
              <option value="Asia/Tokyo">Tóquio (GMT+9)</option>
            </select>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">Alterar Senha</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Senha Atual</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                className="w-full border rounded-md px-3 py-2 pr-10"
                placeholder="••••••••"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-2.5 text-gray-400"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Nova Senha</label>
            <input
              type="password"
              className="w-full border rounded-md px-3 py-2"
              placeholder="••••••••"
            />
          </div>
        </div>
      </div>

      <button
        onClick={() => handleSave('profile')}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
      >
        {loading ? <LoadingSpinner size="sm" /> : <Save className="h-4 w-4" />}
        Salvar Alterações
      </button>
    </div>
  )

  const NotificationsTab = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Notificações por Email</h3>
        <div className="space-y-3">
          {[
            { key: 'email_automation_complete', label: 'Automação concluída' },
            { key: 'email_daily_report', label: 'Relatório diário' },
            { key: 'email_weekly_summary', label: 'Resumo semanal' },
            { key: 'email_marketing', label: 'Emails promocionais' }
          ].map(({ key, label }) => (
            <div key={key} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="font-medium">{label}</span>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.notifications[key]}
                  onChange={(e) => handleInputChange('notifications', key, e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">Notificações Push</h3>
        <div className="space-y-3">
          {[
            { key: 'push_automation_complete', label: 'Automação concluída' },
            { key: 'push_connection_accepted', label: 'Conexão aceita' },
            { key: 'push_daily_limit_reached', label: 'Limite diário atingido' }
          ].map(({ key, label }) => (
            <div key={key} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="font-medium">{label}</span>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.notifications[key]}
                  onChange={(e) => handleInputChange('notifications', key, e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          ))}
        </div>
      </div>

      <button
        onClick={() => handleSave('notifications')}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
      >
        {loading ? <LoadingSpinner size="sm" /> : <Save className="h-4 w-4" />}
        Salvar Alterações
      </button>
    </div>
  )

  const SecurityTab = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Autenticação de Dois Fatores</h3>
        <div className="p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <div>
              <p className="font-medium">2FA Status</p>
              <p className="text-sm text-gray-600">
                {settings.security.two_factor_enabled ? 'Ativado' : 'Desativado'}
              </p>
            </div>
            <button
              onClick={() => handleInputChange('security', 'two_factor_enabled', !settings.security.two_factor_enabled)}
              className={`px-4 py-2 rounded-md ${
                settings.security.two_factor_enabled 
                  ? 'bg-red-600 text-white hover:bg-red-700' 
                  : 'bg-green-600 text-white hover:bg-green-700'
              }`}
            >
              {settings.security.two_factor_enabled ? 'Desativar' : 'Ativar'} 2FA
            </button>
          </div>
          <p className="text-sm text-gray-600">
            A autenticação de dois fatores adiciona uma camada extra de segurança à sua conta.
          </p>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">Configurações de Sessão</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Timeout da Sessão (minutos)</label>
            <select
              value={settings.security.session_timeout}
              onChange={(e) => handleInputChange('security', 'session_timeout', parseInt(e.target.value))}
              className="w-full border rounded-md px-3 py-2"
            >
              <option value={15}>15 minutos</option>
              <option value={30}>30 minutos</option>
              <option value={60}>1 hora</option>
              <option value={120}>2 horas</option>
              <option value={480}>8 horas</option>
            </select>
          </div>

          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium">Notificações de Login</p>
              <p className="text-sm text-gray-600">Receber email quando alguém fizer login na sua conta</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.security.login_notifications}
                onChange={(e) => handleInputChange('security', 'login_notifications', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>

      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <h4 className="font-semibold text-red-800 mb-2">Zona de Perigo</h4>
        <p className="text-sm text-red-700 mb-3">
          Estas ações são irreversíveis. Tenha certeza antes de prosseguir.
        </p>
        <button className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 flex items-center gap-2">
          <Trash2 className="h-4 w-4" />
          Excluir Conta
        </button>
      </div>

      <button
        onClick={() => handleSave('security')}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
      >
        {loading ? <LoadingSpinner size="sm" /> : <Save className="h-4 w-4" />}
        Salvar Alterações
      </button>
    </div>
  )

  const AutomationTab = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Configurações Padrão</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Limite Diário Padrão</label>
            <input
              type="number"
              value={settings.automation.default_daily_limit}
              onChange={(e) => handleInputChange('automation', 'default_daily_limit', parseInt(e.target.value))}
              className="w-full border rounded-md px-3 py-2"
              min="1"
              max="200"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Delay Mínimo (segundos)</label>
            <input
              type="number"
              value={settings.automation.min_delay_seconds}
              onChange={(e) => handleInputChange('automation', 'min_delay_seconds', parseInt(e.target.value))}
              className="w-full border rounded-md px-3 py-2"
              min="10"
              max="300"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Delay Máximo (segundos)</label>
            <input
              type="number"
              value={settings.automation.max_delay_seconds}
              onChange={(e) => handleInputChange('automation', 'max_delay_seconds', parseInt(e.target.value))}
              className="w-full border rounded-md px-3 py-2"
              min="30"
              max="600"
            />
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">Horário de Funcionamento</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium mb-1">Início</label>
            <input
              type="time"
              value={settings.automation.working_hours_start}
              onChange={(e) => handleInputChange('automation', 'working_hours_start', e.target.value)}
              className="w-full border rounded-md px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Fim</label>
            <input
              type="time"
              value={settings.automation.working_hours_end}
              onChange={(e) => handleInputChange('automation', 'working_hours_end', e.target.value)}
              className="w-full border rounded-md px-3 py-2"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Dias de Funcionamento</label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {[
              { key: 'monday', label: 'Segunda' },
              { key: 'tuesday', label: 'Terça' },
              { key: 'wednesday', label: 'Quarta' },
              { key: 'thursday', label: 'Quinta' },
              { key: 'friday', label: 'Sexta' },
              { key: 'saturday', label: 'Sábado' },
              { key: 'sunday', label: 'Domingo' }
            ].map(({ key, label }) => (
              <label key={key} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={settings.automation.working_days.includes(key)}
                  onChange={(e) => {
                    const days = settings.automation.working_days
                    if (e.target.checked) {
                      handleInputChange('automation', 'working_days', [...days, key])
                    } else {
                      handleInputChange('automation', 'working_days', days.filter(d => d !== key))
                    }
                  }}
                  className="rounded"
                />
                <span className="text-sm">{label}</span>
              </label>
            ))}
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">Comportamento</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium">Pausar automaticamente no limite</p>
              <p className="text-sm text-gray-600">Pausar automações quando o limite diário for atingido</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.automation.auto_pause_on_limit}
                onChange={(e) => handleInputChange('automation', 'auto_pause_on_limit', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium">Randomizar timing</p>
              <p className="text-sm text-gray-600">Adicionar variação aleatória nos delays para parecer mais humano</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={settings.automation.randomize_timing}
                onChange={(e) => handleInputChange('automation', 'randomize_timing', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
            </label>
          </div>
        </div>
      </div>

      <button
        onClick={() => handleSave('automation')}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
      >
        {loading ? <LoadingSpinner size="sm" /> : <Save className="h-4 w-4" />}
        Salvar Alterações
      </button>
    </div>
  )

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Configurações</h1>
          <p className="text-gray-600">Gerencie suas preferências e configurações da conta</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={exportSettings}
            className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 flex items-center gap-2"
          >
            <Download className="h-4 w-4" />
            Exportar
          </button>
          <label className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center gap-2 cursor-pointer">
            <Upload className="h-4 w-4" />
            Importar
            <input
              type="file"
              accept=".json"
              onChange={importSettings}
              className="hidden"
            />
          </label>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar */}
        <div className="lg:w-64">
          <nav className="space-y-1">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2 text-left rounded-md transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-700'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  {tab.label}
                </button>
              )
            })}
          </nav>
        </div>

        {/* Content */}
        <div className="flex-1 bg-white rounded-lg border p-6">
          {activeTab === 'profile' && <ProfileTab />}
          {activeTab === 'notifications' && <NotificationsTab />}
          {activeTab === 'security' && <SecurityTab />}
          {activeTab === 'automation' && <AutomationTab />}
        </div>
      </div>
    </div>
  )
}

export default SettingsPage
