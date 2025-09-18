import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Play, 
  Pause, 
  Settings, 
  Users, 
  MessageSquare, 
  Eye,
  Bot,
  AlertCircle,
  CheckCircle,
  Clock,
  Target
} from 'lucide-react';
import api from '@/services/api';

const AutomationsPage = () => {
  const [automations, setAutomations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [runningAutomation, setRunningAutomation] = useState(null);
  const [automationForm, setAutomationForm] = useState({
    type: 'connection_requests',
    keywords: '',
    max_actions: 25,
    message: ''
  });

  useEffect(() => {
    loadAutomations();
  }, []);

  const loadAutomations = async () => {
    try {
      const response = await api.get('/automations');
      if (response.data.success) {
        setAutomations(response.data.automations);
      }
    } catch (error) {
      console.error('Erro ao carregar automações:', error);
    }
  };

  const handleRunAutomation = async (automationConfig = null) => {
    try {
      setLoading(true);
      setError('');
      setRunningAutomation(automationConfig?.id || 'new');
      
      const config = automationConfig || automationForm;
      
      const response = await api.post('/automations/run', config);
      
      if (response.data.success) {
        setSuccess(`Automação executada com sucesso! ${response.data.message}`);
        
        // Mostrar resultados detalhados
        if (response.data.results) {
          const successCount = response.data.results.filter(r => r.result.success).length;
          const totalCount = response.data.results.length;
          setSuccess(`Automação concluída: ${successCount}/${totalCount} ações executadas com sucesso.`);
        }
        
        // Atualizar estatísticas
        loadAutomations();
      } else {
        setError(response.data.error || 'Erro na automação');
      }
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Erro ao executar automação';
      setError(errorMsg);
    } finally {
      setLoading(false);
      setRunningAutomation(null);
    }
  };

  const handleCreateAutomation = () => {
    // Simular criação de automação
    const newAutomation = {
      id: Date.now(),
      name: `Automação ${automationForm.type === 'connection_requests' ? 'Conexões' : 'Visualizações'}`,
      type: automationForm.type,
      status: 'active',
      keywords: automationForm.keywords,
      daily_limit: automationForm.max_actions,
      used_today: 0,
      success_rate: 0,
      automation_type: 'real_browser',
      created_at: new Date().toISOString().split('T')[0],
      last_run: 'Nunca'
    };
    
    setAutomations(prev => [...prev, newAutomation]);
    setShowCreateForm(false);
    setAutomationForm({
      type: 'connection_requests',
      keywords: '',
      max_actions: 25,
      message: ''
    });
    setSuccess('Automação criada com sucesso!');
  };

  const getAutomationTypeIcon = (type) => {
    switch (type) {
      case 'connection_requests':
        return <Users className="w-4 h-4" />;
      case 'messages':
        return <MessageSquare className="w-4 h-4" />;
      case 'profile_views':
        return <Eye className="w-4 h-4" />;
      default:
        return <Bot className="w-4 h-4" />;
    }
  };

  const getAutomationTypeName = (type) => {
    switch (type) {
      case 'connection_requests':
        return 'Solicitações de Conexão';
      case 'messages':
        return 'Mensagens Automáticas';
      case 'profile_views':
        return 'Visualizações de Perfil';
      default:
        return 'Automação';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Automações</h1>
          <p className="mt-2 text-gray-600">
            Configure e execute automações LinkedIn em tempo real
          </p>
        </div>
        <Button onClick={() => setShowCreateForm(true)}>
          <Bot className="w-4 h-4 mr-2" />
          Nova Automação
        </Button>
      </div>

      {/* Alerts */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {success && (
        <Alert className="border-green-200 bg-green-50">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-800">{success}</AlertDescription>
        </Alert>
      )}

      {/* Quick Actions */}
      <div className="grid md:grid-cols-3 gap-4">
        <Card className="cursor-pointer hover:shadow-md transition-shadow" 
              onClick={() => handleRunAutomation({
                type: 'connection_requests',
                keywords: 'desenvolvedor, programador',
                max_actions: 25,
                message: 'Olá! Gostaria de me conectar para expandir minha rede profissional.'
              })}>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Users className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h3 className="font-medium">Conexões Rápidas</h3>
                <p className="text-sm text-gray-600">Enviar 25 solicitações</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => handleRunAutomation({
                type: 'profile_views',
                keywords: 'CEO, founder, startup',
                max_actions: 50,
                message: ''
              })}>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <Eye className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <h3 className="font-medium">Visualizar Perfis</h3>
                <p className="text-sm text-gray-600">Visualizar 50 perfis</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => setShowCreateForm(true)}>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <Settings className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <h3 className="font-medium">Personalizada</h3>
                <p className="text-sm text-gray-600">Configurar automação</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Create Automation Form */}
      {showCreateForm && (
        <Card>
          <CardHeader>
            <CardTitle>Nova Automação</CardTitle>
            <CardDescription>
              Configure uma nova automação LinkedIn personalizada
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="type">Tipo de Automação</Label>
                <Select value={automationForm.type} onValueChange={(value) => 
                  setAutomationForm(prev => ({ ...prev, type: value }))
                }>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="connection_requests">Solicitações de Conexão</SelectItem>
                    <SelectItem value="profile_views">Visualizações de Perfil</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="max_actions">Máximo de Ações</Label>
                <Input
                  id="max_actions"
                  type="number"
                  min="1"
                  max="100"
                  value={automationForm.max_actions}
                  onChange={(e) => setAutomationForm(prev => ({
                    ...prev,
                    max_actions: parseInt(e.target.value) || 25
                  }))}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="keywords">Palavras-chave para Busca</Label>
              <Input
                id="keywords"
                placeholder="Ex: desenvolvedor, programador, tech, startup"
                value={automationForm.keywords}
                onChange={(e) => setAutomationForm(prev => ({
                  ...prev,
                  keywords: e.target.value
                }))}
              />
            </div>

            {automationForm.type === 'connection_requests' && (
              <div className="space-y-2">
                <Label htmlFor="message">Mensagem Personalizada (Opcional)</Label>
                <Textarea
                  id="message"
                  placeholder="Olá! Gostaria de me conectar para expandir minha rede profissional."
                  value={automationForm.message}
                  onChange={(e) => setAutomationForm(prev => ({
                    ...prev,
                    message: e.target.value
                  }))}
                  rows={3}
                />
              </div>
            )}

            <Alert className="border-yellow-200 bg-yellow-50">
              <AlertCircle className="h-4 w-4 text-yellow-600" />
              <AlertDescription className="text-yellow-800">
                <strong>Importante:</strong> A automação será executada imediatamente após a criação. 
                Certifique-se de que sua conta LinkedIn está conectada via login manual.
              </AlertDescription>
            </Alert>

            <div className="flex space-x-3">
              <Button 
                onClick={() => handleRunAutomation()}
                disabled={loading || !automationForm.keywords}
                className="flex-1"
              >
                {loading && runningAutomation === 'new' ? (
                  <>
                    <Clock className="w-4 h-4 mr-2 animate-spin" />
                    Executando...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 mr-2" />
                    Criar e Executar
                  </>
                )}
              </Button>
              <Button 
                variant="outline" 
                onClick={handleCreateAutomation}
                disabled={!automationForm.keywords}
              >
                Apenas Criar
              </Button>
              <Button 
                variant="outline" 
                onClick={() => setShowCreateForm(false)}
              >
                Cancelar
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Existing Automations */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Automações Configuradas</h2>
        
        {automations.length === 0 ? (
          <Card>
            <CardContent className="pt-6 text-center">
              <Bot className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhuma automação configurada</h3>
              <p className="text-gray-600 mb-4">
                Crie sua primeira automação para começar a expandir sua rede no LinkedIn
              </p>
              <Button onClick={() => setShowCreateForm(true)}>
                <Bot className="w-4 h-4 mr-2" />
                Criar Primeira Automação
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {automations.map((automation) => (
              <Card key={automation.id}>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                        {getAutomationTypeIcon(automation.type)}
                      </div>
                      <div>
                        <h3 className="font-medium text-gray-900">{automation.name}</h3>
                        <p className="text-sm text-gray-600">
                          {getAutomationTypeName(automation.type)} • {automation.keywords}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <div className="flex items-center space-x-2">
                          <Badge variant={automation.status === 'active' ? 'default' : 'secondary'}>
                            {automation.status === 'active' ? 'Ativa' : 'Pausada'}
                          </Badge>
                          <Badge variant="outline">
                            {automation.used_today}/{automation.daily_limit} hoje
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">
                          Taxa de sucesso: {automation.success_rate}%
                        </p>
                      </div>
                      
                      <Button
                        onClick={() => handleRunAutomation({
                          id: automation.id,
                          type: automation.type,
                          keywords: automation.keywords,
                          max_actions: Math.min(25, automation.daily_limit - automation.used_today),
                          message: 'Olá! Gostaria de me conectar para expandir minha rede profissional.'
                        })}
                        disabled={loading || automation.used_today >= automation.daily_limit}
                        size="sm"
                      >
                        {loading && runningAutomation === automation.id ? (
                          <>
                            <Clock className="w-4 h-4 mr-2 animate-spin" />
                            Executando
                          </>
                        ) : (
                          <>
                            <Play className="w-4 h-4 mr-2" />
                            Executar
                          </>
                        )}
                      </Button>
                    </div>
                  </div>
                  
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <span className="font-medium text-gray-500">Criada em:</span>
                        <p className="mt-1">{new Date(automation.created_at).toLocaleDateString('pt-BR')}</p>
                      </div>
                      <div>
                        <span className="font-medium text-gray-500">Última execução:</span>
                        <p className="mt-1">{automation.last_run}</p>
                      </div>
                      <div>
                        <span className="font-medium text-gray-500">Método:</span>
                        <p className="mt-1 flex items-center space-x-1">
                          <Target className="w-3 h-3" />
                          <span>Automação Real</span>
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AutomationsPage;
