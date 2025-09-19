import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  User, 
  CheckCircle, 
  AlertCircle, 
  Settings, 
  Zap,
  Shield,
  Key,
  Bot
} from 'lucide-react';
import api from '@/services/api';

const LinkedInAccountsPage = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [manualLoginForm, setManualLoginForm] = useState({
    email: '',
    password: ''
  });
  const [showManualLogin, setShowManualLogin] = useState(false);

  useEffect(() => {


    loadProfile();
    checkUrlParams();
  }, []);

  const checkUrlParams = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const successParam = urlParams.get('success');
    const errorParam = urlParams.get('error');

    if (successParam === 'oauth_connected') {
      setSuccess('Conta LinkedIn conectada via OAuth com sucesso!');
      loadProfile();
    } else if (successParam === 'connected') {
      setSuccess('Conta LinkedIn conectada com sucesso!');
      loadProfile();
    } else if (errorParam) {
      const errorMessages = {
        'no_code': 'Código de autorização não recebido',
        'invalid_state': 'Estado de segurança inválido',
        'token_error': 'Erro ao obter token de acesso',
        'callback_error': 'Erro no processo de callback'
      };
      setError(errorMessages[errorParam] || 'Erro na conexão com LinkedIn');
    }

    // Limpar parâmetros da URL
    if (successParam || errorParam) {
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  };

  const loadProfile = async () => {
    try {
      const response = await api.get('/linkedin/profile');
      if (response.data.success) {
        setProfile(response.data.profile);
      }
    } catch {
      // Perfil não conectado - normal
    }
  };

  const handleOAuthConnect = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Usar dados reais do LinkedIn OAuth
      const clientId = import.meta.env.VITE_LINKEDIN_CLIENT_ID || '77jmwin70p0gge';
      const redirectUri = import.meta.env.VITE_LINKEDIN_REDIRECT_URI || 'http://localhost:3000/auth/linkedin/callback';
      const scopes = 'openid profile email';
      
      const authUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scopes)}`;
      
      // Redirecionar para LinkedIn OAuth
      window.location.href = authUrl;
    } catch {
      setError('Erro ao conectar com LinkedIn via OAuth');
    } finally {
      setLoading(false);
    }
  };

  const handleManualLogin = async (e) => {
    e.preventDefault();
    
    if (!manualLoginForm.email || !manualLoginForm.password) {
      setError('Email e senha são obrigatórios');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      const response = await api.post('/linkedin/manual-login', manualLoginForm);
      
      if (response.data.success) {
        setSuccess('Login manual realizado com sucesso! Automações habilitadas.');
        setProfile(response.data.profile);
        setShowManualLogin(false);
        setManualLoginForm({ email: '', password: '' });
      }
    } catch (error) {
      const errorMsg = error.response?.data?.error || 'Erro no login manual';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleDisconnect = async () => {
    try {
      setLoading(true);
      
      const response = await api.post('/linkedin/disconnect');
      
      if (response.data.success) {
        setProfile(null);
        setSuccess('Conta LinkedIn desconectada com sucesso');
      }
    } catch {
      setError('Erro ao desconectar conta');
    } finally {
      setLoading(false);
    }
  };

  const handleTestConnection = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await api.get('/automations/stats');
      
      if (response.data.success) {
        setSuccess('Conexão testada com sucesso! Automações funcionando.');
      }
    } catch {
      setError('Erro ao testar conexão');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Contas LinkedIn</h1>
        <p className="mt-2 text-gray-600">
          Gerencie suas contas LinkedIn conectadas para automação
        </p>
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

      {/* Connection Status */}
      {profile ? (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <User className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">
                    {profile.name || `${profile.firstName} ${profile.lastName}` || 'Usuário LinkedIn'}
                  </CardTitle>
                  <CardDescription>
                    {profile.headline || profile.email || 'Conta LinkedIn conectada'}
                  </CardDescription>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <Badge 
                  variant={profile.connectionType === 'manual' ? 'default' : 'secondary'}
                  className="flex items-center space-x-1"
                >
                  {profile.connectionType === 'manual' ? (
                    <>
                      <Bot className="w-3 h-3" />
                      <span>Automação Ativa</span>
                    </>
                  ) : (
                    <>
                      <Shield className="w-3 h-3" />
                      <span>OAuth Conectado</span>
                    </>
                  )}
                </Badge>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-500">Tipo de Conexão:</span>
                  <p className="mt-1">
                    {profile.connectionType === 'manual' ? 'Login Manual (Automações Habilitadas)' : 'OAuth 2.0 (Dados Básicos)'}
                  </p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Status:</span>
                  <p className="mt-1 flex items-center space-x-1">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>Conectado</span>
                  </p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Última Sincronização:</span>
                  <p className="mt-1">
                    {profile.lastSync ? new Date(profile.lastSync).toLocaleString('pt-BR') : 'Agora'}
                  </p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Automações:</span>
                  <p className="mt-1">
                    {profile.automationEnabled ? 'Habilitadas' : 'Limitadas (apenas dados básicos)'}
                  </p>
                </div>
              </div>

              <Separator />

              <div className="flex space-x-3">
                {profile.connectionType === 'manual' && (
                  <Button onClick={handleTestConnection} disabled={loading} variant="outline">
                    <Zap className="w-4 h-4 mr-2" />
                    Testar Automação
                  </Button>
                )}
                
                <Button onClick={handleDisconnect} disabled={loading} variant="destructive">
                  Desconectar
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-6">
          {/* Connection Options */}
          <div className="grid md:grid-cols-2 gap-6">
            {/* OAuth Connection */}
            <Card>
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Shield className="w-5 h-5 text-blue-600" />
                  <CardTitle>Conexão OAuth 2.0</CardTitle>
                </div>
                <CardDescription>
                  Conexão segura oficial do LinkedIn para obter dados básicos do perfil
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <h4 className="font-medium text-sm text-gray-900">O que você obtém:</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Nome e foto do perfil</li>
                    <li>• Email associado à conta</li>
                    <li>• Dados básicos do perfil</li>
                    <li>• Conexão segura e oficial</li>
                  </ul>
                </div>
                
                <div className="space-y-2">
                  <h4 className="font-medium text-sm text-gray-900">Limitações:</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Sem automações avançadas</li>
                    <li>• Apenas dados básicos</li>
                    <li>• Não permite ações automatizadas</li>
                  </ul>
                </div>

                <Button 
                  onClick={handleOAuthConnect} 
                  disabled={loading}
                  className="w-full"
                  variant="outline"
                >
                  <Key className="w-4 h-4 mr-2" />
                  Conectar via OAuth
                </Button>
              </CardContent>
            </Card>

            {/* Manual Login */}
            <Card>
              <CardHeader>
                <div className="flex items-center space-x-2">
                  <Bot className="w-5 h-5 text-green-600" />
                  <CardTitle>Login Manual</CardTitle>
                </div>
                <CardDescription>
                  Login direto com suas credenciais para automações completas
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <h4 className="font-medium text-sm text-gray-900">O que você obtém:</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Automações completas habilitadas</li>
                    <li>• Envio de conexões automático</li>
                    <li>• Mensagens personalizadas</li>
                    <li>• Visualização de perfis</li>
                    <li>• Controle total das ações</li>
                  </ul>
                </div>

                <div className="space-y-2">
                  <h4 className="font-medium text-sm text-gray-900">Segurança:</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Credenciais não são armazenadas</li>
                    <li>• Simulação de comportamento humano</li>
                    <li>• Delays aleatórios entre ações</li>
                    <li>• Limites de segurança configuráveis</li>
                  </ul>
                </div>

                <Button 
                  onClick={() => setShowManualLogin(!showManualLogin)} 
                  className="w-full"
                >
                  <Bot className="w-4 h-4 mr-2" />
                  {showManualLogin ? 'Cancelar' : 'Login Manual'}
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Manual Login Form */}
          {showManualLogin && (
            <Card>
              <CardHeader>
                <CardTitle>Login Manual no LinkedIn</CardTitle>
                <CardDescription>
                  Insira suas credenciais do LinkedIn para habilitar automações completas
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleManualLogin} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="email">Email do LinkedIn</Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="seu@email.com"
                      value={manualLoginForm.email}
                      onChange={(e) => setManualLoginForm(prev => ({
                        ...prev,
                        email: e.target.value
                      }))}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="password">Senha do LinkedIn</Label>
                    <Input
                      id="password"
                      type="password"
                      placeholder="••••••••"
                      value={manualLoginForm.password}
                      onChange={(e) => setManualLoginForm(prev => ({
                        ...prev,
                        password: e.target.value
                      }))}
                      required
                    />
                  </div>

                  <Alert className="border-yellow-200 bg-yellow-50">
                    <AlertCircle className="h-4 w-4 text-yellow-600" />
                    <AlertDescription className="text-yellow-800">
                      <strong>Importante:</strong> Suas credenciais são usadas apenas para login e não são armazenadas. 
                      O sistema simula comportamento humano para evitar detecção.
                    </AlertDescription>
                  </Alert>

                  <div className="flex space-x-3">
                    <Button type="submit" disabled={loading} className="flex-1">
                      {loading ? 'Conectando...' : 'Fazer Login'}
                    </Button>
                    <Button 
                      type="button" 
                      variant="outline" 
                      onClick={() => setShowManualLogin(false)}
                    >
                      Cancelar
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          )}

          {/* Info Card */}
          <Card className="border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-start space-x-3">
                <Settings className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <h3 className="font-medium text-blue-900">Qual opção escolher?</h3>
                  <p className="mt-1 text-sm text-blue-800">
                    <strong>OAuth 2.0:</strong> Para obter apenas dados básicos do perfil de forma segura e oficial.
                  </p>
                  <p className="mt-1 text-sm text-blue-800">
                    <strong>Login Manual:</strong> Para automações completas como envio de conexões, mensagens e visualização de perfis.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default LinkedInAccountsPage;
