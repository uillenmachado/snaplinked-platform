import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { useAuth } from '@/contexts/AuthContext'

import {
  Users,
  MessageSquare,
  Eye,
  TrendingUp,
  Bot,
  Plus,
  Activity,
  Calendar,
  CheckCircle,
  AlertCircle,
  Clock,
  BarChart3,
  Linkedin,
  Zap,
} from 'lucide-react'
import LoadingSpinner from '@/components/ui/loading-spinner'

export default function DashboardPage() {
  const [stats] = useState({
    connections_sent: 156,
    messages_sent: 89,
    profiles_viewed: 342,
    success_rate: 78.5,
    profiles_viewed_today: 25
  })
  const [recentActivity] = useState([
    {
      id: 1,
      type: 'success',
      action: 'Solicitação de Conexão Enviada',
      description: 'Enviada para John Smith',
      created_at: new Date().toISOString()
    },
    {
      id: 2,
      type: 'success', 
      action: 'Mensagem de Follow-up Enviada',
      description: 'Enviada para Sarah Johnson',
      created_at: new Date().toISOString()
    }
  ])
  const [automations] = useState([
    {
      id: 1,
      name: 'Tech Professionals Outreach',
      automation_type: 'Solicitação de Conexão',
      is_active: true,
      total_executed: 156,
      executions_today: 23,
      daily_limit: 50,
      success_rate: 78.5
    },
    {
      id: 2,
      name: 'Follow-up Messages',
      automation_type: 'Mensagem',
      is_active: false,
      total_executed: 89,
      executions_today: 0,
      daily_limit: 25,
      success_rate: 82.1
    }
  ])
  const { user } = useAuth()

  const getGreeting = () => {
    const hour = new Date().getHours()
    if (hour < 12) return 'Bom dia'
    if (hour < 18) return 'Boa tarde'
    return 'Boa noite'
  }

  const getSubscriptionLimits = (plan) => {
    const limits = {
      free: { automations: 1, connections: 10, messages: 5 },
      basic: { automations: 5, connections: 50, messages: 25 },
      premium: { automations: 20, connections: 200, messages: 100 },
      enterprise: { automations: 100, connections: 1000, messages: 500 },
    }
    return limits[plan] || limits.premium
  }

  const limits = getSubscriptionLimits(user?.subscription_plan)



  return (
    <div className="space-y-4 max-w-7xl">
      {/* Welcome Section - Compacto */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-4 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold mb-1">
              {getGreeting()}, {user?.first_name || 'Demo'}! 👋
            </h1>
            <p className="text-blue-100 text-sm mb-2">
              Aqui está o que está acontecendo com sua automação LinkedIn hoje.
            </p>
            <div className="flex items-center space-x-4 text-sm">
              <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                Premium Plan
              </Badge>
              <span className="text-blue-100">
                {automations.length} de {limits.automations} automações ativas
              </span>
            </div>
          </div>
          <div className="hidden md:block">
            <Link to="/automations">
              <Button variant="secondary" className="bg-white/20 text-white border-white/30 hover:bg-white/30">
                <Plus className="mr-2 h-4 w-4" />
                Nova Automação
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Stats Grid - Compacto */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        <Card className="p-3">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1">
            <CardTitle className="text-sm font-medium">Conexões Enviadas</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="p-0">
            <div className="text-xl font-bold">{stats.connections_sent}</div>
            <div className="flex items-center space-x-2 mt-1">
              <Progress 
                value={(stats.connections_sent / limits.connections) * 100} 
                className="flex-1 h-1" 
              />
              <span className="text-xs text-muted-foreground">
                {limits.connections} limit
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="p-3">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1">
            <CardTitle className="text-sm font-medium">Mensagens Enviadas</CardTitle>
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="p-0">
            <div className="text-xl font-bold">{stats.messages_sent}</div>
            <div className="flex items-center space-x-2 mt-1">
              <Progress 
                value={(stats.messages_sent / limits.messages) * 100} 
                className="flex-1 h-1" 
              />
              <span className="text-xs text-muted-foreground">
                {limits.messages} limit
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="p-3">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1">
            <CardTitle className="text-sm font-medium">Perfis Visualizados</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="p-0">
            <div className="text-xl font-bold">{stats.profiles_viewed}</div>
            <p className="text-xs text-muted-foreground mt-1">
              +{stats.profiles_viewed_today} hoje
            </p>
          </CardContent>
        </Card>

        <Card className="p-3">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1">
            <CardTitle className="text-sm font-medium">Taxa de Sucesso</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="p-0">
            <div className="text-xl font-bold">{stats.success_rate}%</div>
            <p className="text-xs text-muted-foreground mt-1">
              Média de sucesso das automações
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content - Layout otimizado sem scroll */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Active Automations */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Automações Ativas</CardTitle>
              <Link to="/automations">
                <Button variant="outline" size="sm">
                  Ver Todas
                </Button>
              </Link>
            </div>
            <CardDescription className="text-sm">
              Suas automações LinkedIn em execução
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {automations.map((automation) => (
              <div key={automation.id} className="flex items-center justify-between p-2 border rounded-lg">
                <div className="flex items-center space-x-2">
                  <div className={`w-2 h-2 rounded-full ${
                    automation.is_active ? 'bg-green-500' : 'bg-gray-400'
                  }`} />
                  <div>
                    <p className="font-medium text-sm">{automation.name}</p>
                    <p className="text-xs text-gray-500">
                      {automation.executions_today}/{automation.daily_limit} hoje • {automation.success_rate}% sucesso
                    </p>
                  </div>
                </div>
                <Badge variant={automation.is_active ? 'default' : 'secondary'} className="text-xs">
                  {automation.is_active ? 'Ativa' : 'Pausada'}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Atividade Recente</CardTitle>
              <Link to="/analytics">
                <Button variant="outline" size="sm">
                  <BarChart3 className="mr-2 h-4 w-4" />
                  Analytics
                </Button>
              </Link>
            </div>
            <CardDescription className="text-sm">
              Últimas execuções e eventos do sistema
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-start space-x-2 p-2 border rounded-lg">
                <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium">{activity.action}</p>
                  <p className="text-xs text-gray-500">{activity.description}</p>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {new Date(activity.created_at).toLocaleString('pt-BR')}
                  </p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions - Layout compacto */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-base">Ações Rápidas</CardTitle>
          <CardDescription className="text-sm">
            Tarefas comuns para começar com o SnapLinked
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <Link to="/linkedin-accounts" className="block">
              <div className="p-3 border rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Linkedin className="w-4 h-4 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="font-medium text-sm">Conectar LinkedIn</h3>
                    <p className="text-xs text-muted-foreground">Adicione sua conta LinkedIn</p>
                  </div>
                </div>
              </div>
            </Link>

            <Link to="/automations" className="block">
              <div className="p-3 border rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                    <Zap className="w-4 h-4 text-purple-600" />
                  </div>
                  <div>
                    <h3 className="font-medium text-sm">Criar Automação</h3>
                    <p className="text-xs text-muted-foreground">Configure sua primeira automação</p>
                  </div>
                </div>
              </div>
            </Link>

            <Link to="/analytics" className="block">
              <div className="p-3 border rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                    <BarChart3 className="w-4 h-4 text-green-600" />
                  </div>
                  <div>
                    <h3 className="font-medium text-sm">Ver Analytics</h3>
                    <p className="text-xs text-muted-foreground">Acompanhe o desempenho</p>
                  </div>
                </div>
              </div>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
