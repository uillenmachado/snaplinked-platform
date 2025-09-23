# 📡 SnapLinked v3.0 - Documentação da API

Esta documentação descreve todos os endpoints da API REST do SnapLinked v3.0.

## 🔗 Base URL

```
Desenvolvimento: http://localhost:5000
Produção: https://seudominio.com
```

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Tokens)** para autenticação. Inclua o token no header:

```http
Authorization: Bearer SEU_JWT_TOKEN
```

## 📋 Endpoints

### 🏥 Health & Status

#### GET /api/health
Verificação de saúde da aplicação.

**Resposta:**
```json
{
  "status": "ok",
  "message": "SnapLinked v3.0 funcionando perfeitamente",
  "timestamp": "2025-09-23T21:30:00Z",
  "version": "3.0.0",
  "features": {
    "oauth_linkedin": true,
    "automation": true,
    "database": true
  }
}
```

#### GET /api/status
Status detalhado da aplicação e usuário.

**Headers:** `Authorization: Bearer TOKEN` (opcional)

**Resposta (não autenticado):**
```json
{
  "authenticated": false,
  "version": "3.0.0"
}
```

**Resposta (autenticado):**
```json
{
  "authenticated": true,
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "name": "João Silva",
    "linkedin_id": "abc123",
    "avatar_url": "https://media.licdn.com/...",
    "created_at": "2025-09-23T20:00:00Z"
  },
  "stats": {
    "total_likes": 15,
    "total_connections": 8,
    "total_comments": 3,
    "total_views": 45
  },
  "automation_running": false,
  "version": "3.0.0"
}
```

### 🔐 Autenticação

#### GET /api/auth/linkedin
Iniciar processo de autenticação OAuth do LinkedIn.

**Resposta:**
```json
{
  "auth_url": "https://www.linkedin.com/oauth/v2/authorization?...",
  "state": "random_state_string"
}
```

#### GET /auth/linkedin/callback
Callback OAuth do LinkedIn (redirecionamento automático).

**Parâmetros de Query:**
- `code`: Código de autorização do LinkedIn
- `state`: Estado para validação CSRF

**Redirecionamento:**
- Sucesso: `/dashboard?auth=success&user=Nome`
- Erro: `/dashboard?auth=error`

#### POST /api/auth/manual-login
Iniciar login manual no LinkedIn.

**Body:**
```json
{
  "email": "usuario@exemplo.com",
  "name": "João Silva"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Login manual iniciado com sucesso",
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "name": "João Silva"
  },
  "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### POST /api/auth/logout
Fazer logout do usuário.

**Resposta:**
```json
{
  "success": true,
  "message": "Logout realizado com sucesso"
}
```

### 🤖 Automação

#### POST /api/automation/like
Executar automação de curtidas.

**Headers:** `Authorization: Bearer TOKEN`

**Body:**
```json
{
  "target_count": 3
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Automação de like concluída",
  "details": {
    "completed_count": 3,
    "error_count": 0,
    "errors": []
  },
  "stats": {
    "total_likes": 18,
    "total_connections": 8,
    "total_comments": 3
  }
}
```

#### POST /api/automation/connect
Executar automação de conexões.

**Headers:** `Authorization: Bearer TOKEN`

**Body:**
```json
{
  "target_count": 2
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Automação de connect concluída",
  "details": {
    "completed_count": 2,
    "error_count": 0,
    "errors": []
  },
  "stats": {
    "total_likes": 18,
    "total_connections": 10,
    "total_comments": 3
  }
}
```

#### POST /api/automation/comment
Executar automação de comentários.

**Headers:** `Authorization: Bearer TOKEN`

**Body:**
```json
{
  "target_count": 1
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Automação de comment concluída",
  "details": {
    "completed_count": 1,
    "error_count": 0,
    "errors": []
  },
  "stats": {
    "total_likes": 18,
    "total_connections": 10,
    "total_comments": 4
  }
}
```

#### GET /api/automation/sessions
Obter histórico de sessões de automação.

**Headers:** `Authorization: Bearer TOKEN`

**Resposta:**
```json
{
  "sessions": [
    {
      "id": 1,
      "session_type": "like",
      "status": "completed",
      "target_count": 3,
      "completed_count": 3,
      "error_count": 0,
      "started_at": "2025-09-23T21:00:00Z",
      "completed_at": "2025-09-23T21:02:30Z"
    }
  ]
}
```

#### GET /api/automation/logs
Obter logs detalhados de automação.

**Headers:** `Authorization: Bearer TOKEN`

**Parâmetros de Query:**
- `session_id` (opcional): ID da sessão específica

**Resposta:**
```json
{
  "logs": [
    {
      "id": 1,
      "session_id": 1,
      "action_type": "like",
      "target_url": "https://linkedin.com/feed/update/123",
      "target_name": "Post sobre tecnologia",
      "status": "success",
      "message": "Post curtido com sucesso",
      "extra_data": {
        "post_type": "article",
        "author": "Tech Expert"
      },
      "created_at": "2025-09-23T21:01:15Z"
    }
  ]
}
```

### 📊 Estatísticas

#### POST /api/stats/reset
Resetar estatísticas do usuário.

**Headers:** `Authorization: Bearer TOKEN`

**Resposta:**
```json
{
  "success": true,
  "message": "Estatísticas resetadas com sucesso",
  "stats": {
    "total_likes": 0,
    "total_connections": 0,
    "total_comments": 0,
    "total_views": 0
  }
}
```

## ❌ Códigos de Erro

### 400 - Bad Request
```json
{
  "error": "Dados inválidos",
  "message": "Email é obrigatório"
}
```

### 401 - Unauthorized
```json
{
  "error": "Token de autenticação necessário",
  "message": "Faça login para acessar este recurso"
}
```

### 403 - Forbidden
```json
{
  "error": "Acesso negado",
  "message": "Você não tem permissão para acessar este recurso"
}
```

### 404 - Not Found
```json
{
  "error": "Endpoint não encontrado",
  "message": "Verifique a URL e tente novamente"
}
```

### 500 - Internal Server Error
```json
{
  "error": "Erro interno do servidor",
  "message": "Tente novamente em alguns instantes"
}
```

## 🔧 Rate Limiting

A API implementa rate limiting para proteger contra abuso:

- **API geral**: 10 requisições/segundo
- **Autenticação**: 5 requisições/minuto
- **Automação**: 1 sessão por vez por usuário

Headers de resposta:
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1640995200
```

## 📝 Exemplos de Uso

### JavaScript/Fetch
```javascript
// Fazer login manual
const response = await fetch('/api/auth/manual-login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'usuario@exemplo.com',
    name: 'João Silva'
  })
});

const data = await response.json();
const token = data.auth_token;

// Executar automação
const automationResponse = await fetch('/api/automation/like', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    target_count: 3
  })
});
```

### Python/Requests
```python
import requests

# Fazer login manual
login_response = requests.post('http://localhost:5000/api/auth/manual-login', 
  json={
    'email': 'usuario@exemplo.com',
    'name': 'João Silva'
  }
)

token = login_response.json()['auth_token']

# Executar automação
automation_response = requests.post(
  'http://localhost:5000/api/automation/like',
  headers={'Authorization': f'Bearer {token}'},
  json={'target_count': 3}
)

print(automation_response.json())
```

### cURL
```bash
# Login manual
curl -X POST http://localhost:5000/api/auth/manual-login \
  -H "Content-Type: application/json" \
  -d '{"email":"usuario@exemplo.com","name":"João Silva"}'

# Executar automação (substitua TOKEN)
curl -X POST http://localhost:5000/api/automation/like \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target_count":3}'
```

## 🔒 Segurança

### Headers de Segurança
A API inclui headers de segurança automáticos:
```http
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Validação de Entrada
- Todos os dados de entrada são validados
- Sanitização automática de strings
- Proteção contra SQL injection
- Validação de tipos de dados

### CORS
CORS configurado para permitir apenas origens autorizadas em produção.

## 📚 SDKs e Bibliotecas

### JavaScript SDK (Planejado)
```javascript
import SnapLinked from 'snaplinked-sdk';

const client = new SnapLinked({
  baseUrl: 'https://seudominio.com',
  apiKey: 'sua-api-key'
});

await client.auth.login('usuario@exemplo.com');
await client.automation.like({ count: 3 });
```

### Python SDK (Planejado)
```python
from snaplinked import SnapLinkedClient

client = SnapLinkedClient(
  base_url='https://seudominio.com',
  api_key='sua-api-key'
)

client.auth.login('usuario@exemplo.com')
client.automation.like(count=3)
```

## 🔄 Versionamento

A API segue versionamento semântico:
- **v3.0.0**: Versão atual
- **v3.1.0**: Próxima versão com novas funcionalidades
- **v4.0.0**: Próxima versão com breaking changes

Endpoint de versão:
```http
GET /api/version
```

## 📞 Suporte

Para dúvidas sobre a API:
- **Documentação**: https://snaplinked.com/api-docs
- **GitHub Issues**: https://github.com/uillenmachado/snaplinked-platform/issues
- **Email**: api@snaplinked.com

---

**SnapLinked v3.0 API** - Automação LinkedIn programática 🚀
