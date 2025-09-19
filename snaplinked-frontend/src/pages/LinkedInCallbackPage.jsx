import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import api from '@/services/api';

const LinkedInCallbackPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('processing'); // processing, success, error
  const [message, setMessage] = useState('Processando conexão com LinkedIn...');

  useEffect(() => {
    handleCallback();
  }, []);

  const handleCallback = async () => {
    try {
      const code = searchParams.get('code');
      const error = searchParams.get('error');

      if (error) {
        setStatus('error');
        setMessage(`Erro na autorização: ${error}`);
        setTimeout(() => navigate('/linkedin-accounts'), 3000);
        return;
      }

      if (!code) {
        setStatus('error');
        setMessage('Código de autorização não recebido');
        setTimeout(() => navigate('/linkedin-accounts'), 3000);
        return;
      }

      // Enviar código para o backend processar
      const response = await api.get(`/auth/linkedin/callback?code=${code}`);

      if (response.data.success) {
        setStatus('success');
        setMessage('Conta LinkedIn conectada com sucesso!');
        
        // Redirecionar para página de contas LinkedIn após 2 segundos
        setTimeout(() => {
          navigate('/linkedin-accounts?success=oauth_connected');
        }, 2000);
      } else {
        setStatus('error');
        setMessage(response.data.error || 'Erro ao processar conexão');
        setTimeout(() => navigate('/linkedin-accounts'), 3000);
      }
    } catch (error) {
      setStatus('error');
      setMessage('Erro interno ao processar conexão');
      setTimeout(() => navigate('/linkedin-accounts'), 3000);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Conectando LinkedIn</CardTitle>
          <CardDescription>
            Processando sua conexão com o LinkedIn...
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {status === 'processing' && (
            <Alert>
              <Loader2 className="h-4 w-4 animate-spin" />
              <AlertDescription>{message}</AlertDescription>
            </Alert>
          )}

          {status === 'success' && (
            <Alert className="border-green-200 bg-green-50">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <AlertDescription className="text-green-800">{message}</AlertDescription>
            </Alert>
          )}

          {status === 'error' && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{message}</AlertDescription>
            </Alert>
          )}

          <div className="text-center text-sm text-gray-500">
            {status === 'success' && 'Redirecionando em alguns segundos...'}
            {status === 'error' && 'Redirecionando para página de contas...'}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default LinkedInCallbackPage;
