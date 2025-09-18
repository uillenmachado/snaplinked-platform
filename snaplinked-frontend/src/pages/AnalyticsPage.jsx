import { useState, useEffect } from 'react'
import { BarChart3, TrendingUp, Users, MessageSquare, Eye, Calendar, Download, Filter } from 'lucide-react'
import LoadingSpinner from '@/components/ui/loading-spinner'

const AnalyticsPage = () => {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState('7d')
  const [selectedMetric, setSelectedMetric] = useState('connections')

  // Mock analytics data
  useEffect(() => {
    const mockAnalytics = {
      overview: {
        total_connections: 1247,
        total_messages: 589,
        total_profile_views: 2341,
        success_rate: 78.5,
        connections_growth: 12.5,
        messages_growth: 8.3,
        views_growth: 15.2,
        success_rate_change: 2.1
      },
      daily_stats: [
        { date: '2024-01-14', connections: 23, messages: 12, views: 67, success_rate: 76.2 },
        { date: '2024-01-15', connections: 31, messages: 18, views: 89, success_rate: 78.1 },
        { date: '2024-01-16', connections: 28, messages: 15, views: 72, success_rate: 79.3 },
        { date: '2024-01-17', connections: 35, messages: 22, views: 94, success_rate: 80.1 },
        { date: '2024-01-18', connections: 29, messages: 16, views: 81, success_rate: 77.8 },
        { date: '2024-01-19', connections: 33, messages: 19, views: 88, success_rate: 79.5 },
        { date: '2024-01-20', connections: 27, messages: 14, views: 76, success_rate: 78.9 }
      ],
      automation_performance: [
        { name: 'Tech Professionals Outreach', connections: 156, success_rate: 78.5, status: 'active' },
        { name: 'Follow-up Messages', messages: 89, success_rate: 82.1, status: 'active' },
        { name: 'Profile Views Campaign', views: 342, success_rate: 65.3, status: 'active' }
      ],
      top_keywords: [
        { keyword: 'software engineer', count: 45, success_rate: 82.2 },
        { keyword: 'developer', count: 38, success_rate: 79.1 },
        { keyword: 'tech lead', count: 32, success_rate: 85.3 },
        { keyword: 'product manager', count: 28, success_rate: 76.8 },
        { keyword: 'startup', count: 24, success_rate: 71.4 }
      ],
      hourly_activity: [
        { hour: '09:00', activity: 12 },
        { hour: '10:00', activity: 18 },
        { hour: '11:00', activity: 25 },
        { hour: '12:00', activity: 15 },
        { hour: '13:00', activity: 8 },
        { hour: '14:00', activity: 22 },
        { hour: '15:00', activity: 28 },
        { hour: '16:00', activity: 31 },
        { hour: '17:00', activity: 19 },
        { hour: '18:00', activity: 14 }
      ]
    }
    
    setTimeout(() => {
      setAnalytics(mockAnalytics)
      setLoading(false)
    }, 1000)
  }, [timeRange])

  const formatNumber = (num) => {
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'k'
    }
    return num.toString()
  }

  const getGrowthColor = (growth) => {
    return growth >= 0 ? 'text-green-600' : 'text-red-600'
  }

  const getGrowthIcon = (growth) => {
    return growth >= 0 ? '↗' : '↘'
  }

  const exportData = () => {
    // Mock export functionality
    const data = JSON.stringify(analytics, null, 2)
    const blob = new Blob([data], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `snaplinked-analytics-${timeRange}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600">Acompanhe o desempenho das suas automações</p>
        </div>
        <div className="flex gap-2">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="border rounded-md px-3 py-2"
          >
            <option value="7d">Últimos 7 dias</option>
            <option value="30d">Últimos 30 dias</option>
            <option value="90d">Últimos 90 dias</option>
          </select>
          <button
            onClick={exportData}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center gap-2"
          >
            <Download className="h-4 w-4" />
            Exportar
          </button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-6 rounded-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total de Conexões</p>
              <p className="text-2xl font-bold">{formatNumber(analytics.overview.total_connections)}</p>
              <p className={`text-sm ${getGrowthColor(analytics.overview.connections_growth)}`}>
                {getGrowthIcon(analytics.overview.connections_growth)} {Math.abs(analytics.overview.connections_growth)}%
              </p>
            </div>
            <Users className="h-8 w-8 text-blue-600" />
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total de Mensagens</p>
              <p className="text-2xl font-bold">{formatNumber(analytics.overview.total_messages)}</p>
              <p className={`text-sm ${getGrowthColor(analytics.overview.messages_growth)}`}>
                {getGrowthIcon(analytics.overview.messages_growth)} {Math.abs(analytics.overview.messages_growth)}%
              </p>
            </div>
            <MessageSquare className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Visualizações de Perfil</p>
              <p className="text-2xl font-bold">{formatNumber(analytics.overview.total_profile_views)}</p>
              <p className={`text-sm ${getGrowthColor(analytics.overview.views_growth)}`}>
                {getGrowthIcon(analytics.overview.views_growth)} {Math.abs(analytics.overview.views_growth)}%
              </p>
            </div>
            <Eye className="h-8 w-8 text-purple-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Taxa de Sucesso</p>
              <p className="text-2xl font-bold">{analytics.overview.success_rate}%</p>
              <p className={`text-sm ${getGrowthColor(analytics.overview.success_rate_change)}`}>
                {getGrowthIcon(analytics.overview.success_rate_change)} {Math.abs(analytics.overview.success_rate_change)}%
              </p>
            </div>
            <TrendingUp className="h-8 w-8 text-orange-600" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Daily Performance Chart */}
        <div className="bg-white p-6 rounded-lg border">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Desempenho Diário</h3>
            <select
              value={selectedMetric}
              onChange={(e) => setSelectedMetric(e.target.value)}
              className="border rounded-md px-2 py-1 text-sm"
            >
              <option value="connections">Conexões</option>
              <option value="messages">Mensagens</option>
              <option value="views">Visualizações</option>
              <option value="success_rate">Taxa de Sucesso</option>
            </select>
          </div>
          
          <div className="h-64 flex items-end justify-between gap-2">
            {analytics.daily_stats.map((day, index) => {
              const value = day[selectedMetric]
              const maxValue = Math.max(...analytics.daily_stats.map(d => d[selectedMetric]))
              const height = (value / maxValue) * 100
              
              return (
                <div key={index} className="flex-1 flex flex-col items-center">
                  <div
                    className="w-full bg-blue-500 rounded-t-md transition-all duration-300 hover:bg-blue-600"
                    style={{ height: `${height}%` }}
                    title={`${day.date}: ${value}`}
                  ></div>
                  <span className="text-xs text-gray-600 mt-2">
                    {new Date(day.date).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })}
                  </span>
                </div>
              )
            })}
          </div>
        </div>

        {/* Hourly Activity */}
        <div className="bg-white p-6 rounded-lg border">
          <h3 className="text-lg font-semibold mb-4">Atividade por Hora</h3>
          <div className="space-y-3">
            {analytics.hourly_activity.map((hour, index) => {
              const maxActivity = Math.max(...analytics.hourly_activity.map(h => h.activity))
              const width = (hour.activity / maxActivity) * 100
              
              return (
                <div key={index} className="flex items-center gap-3">
                  <span className="text-sm font-medium w-12">{hour.hour}</span>
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${width}%` }}
                    ></div>
                  </div>
                  <span className="text-sm text-gray-600 w-8">{hour.activity}</span>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Automation Performance */}
        <div className="bg-white p-6 rounded-lg border">
          <h3 className="text-lg font-semibold mb-4">Desempenho das Automações</h3>
          <div className="space-y-4">
            {analytics.automation_performance.map((automation, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-medium">{automation.name}</h4>
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                    {automation.status}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Execuções: </span>
                    <span className="font-medium">
                      {automation.connections || automation.messages || automation.views}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">Taxa de sucesso: </span>
                    <span className="font-medium text-green-600">{automation.success_rate}%</span>
                  </div>
                </div>
                <div className="mt-2">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-green-500 h-2 rounded-full"
                      style={{ width: `${automation.success_rate}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Keywords */}
        <div className="bg-white p-6 rounded-lg border">
          <h3 className="text-lg font-semibold mb-4">Palavras-chave Mais Eficazes</h3>
          <div className="space-y-3">
            {analytics.top_keywords.map((keyword, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <span className="font-medium">{keyword.keyword}</span>
                  <p className="text-sm text-gray-600">{keyword.count} usos</p>
                </div>
                <div className="text-right">
                  <span className="text-sm font-medium text-green-600">{keyword.success_rate}%</span>
                  <p className="text-xs text-gray-600">sucesso</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Insights Section */}
      <div className="mt-6 bg-blue-50 p-6 rounded-lg border border-blue-200">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">💡 Insights e Recomendações</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-blue-800 mb-2">Melhor Horário</h4>
            <p className="text-gray-700">
              Suas automações têm melhor performance entre 15:00-16:00. 
              Considere concentrar suas atividades neste período.
            </p>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-blue-800 mb-2">Palavras-chave Eficazes</h4>
            <p className="text-gray-700">
              "Tech lead" tem a maior taxa de sucesso (85.3%). 
              Considere usar mais esta palavra-chave em suas automações.
            </p>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-blue-800 mb-2">Crescimento</h4>
            <p className="text-gray-700">
              Suas visualizações de perfil cresceram 15.2% no período. 
              Continue focando nesta estratégia.
            </p>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <h4 className="font-medium text-blue-800 mb-2">Otimização</h4>
            <p className="text-gray-700">
              Sua taxa de sucesso geral está acima da média (78.5%). 
              Mantenha as estratégias atuais.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalyticsPage
