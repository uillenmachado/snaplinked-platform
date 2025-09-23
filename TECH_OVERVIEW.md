# 🔧 SnapLinked v3.0 - Visão Técnica para Desenvolvedores

## 📋 Resumo Executivo

O **SnapLinked** é uma plataforma de automação profissional para LinkedIn desenvolvida em Python, que utiliza web scraping inteligente e automação de navegador para executar ações reais na rede social. O projeto implementa uma arquitetura moderna com Flask, SQLAlchemy, Playwright e OAuth 2.0, oferecendo uma API REST completa e interface web responsiva.

## 🏗️ Arquitetura do Sistema

### Padrão Arquitetural
O projeto segue uma **arquitetura em camadas (Layered Architecture)** com separação clara de responsabilidades:

```
┌─────────────────────────────────────────┐
│           Frontend (HTML/CSS/JS)        │
├─────────────────────────────────────────┤
│              API REST Layer             │
├─────────────────────────────────────────┤
│            Business Logic               │
├─────────────────────────────────────────┤
│          Data Access Layer              │
├─────────────────────────────────────────┤
│            Database (SQLite)            │
└─────────────────────────────────────────┘
```

### Componentes Principais

#### 1. **API REST (Flask)**
- **Framework**: Flask 3.0.3
- **Responsabilidade**: Exposição de endpoints HTTP
- **Autenticação**: JWT + OAuth 2.0
- **Serialização**: JSON nativo

#### 2. **Camada de Negócio (Services)**
- **LinkedIn Service**: Automação e integração
- **OAuth Service**: Autenticação LinkedIn
- **Automation Service**: Lógica de automação

#### 3. **Camada de Dados (Models)**
- **ORM**: SQLAlchemy 2.0.35
- **Banco**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Migrations**: Alembic (planejado)

#### 4. **Automação (Playwright)**
- **Engine**: Playwright 1.48.0
- **Browser**: Chromium headless
- **Estratégia**: Page Object Model

## 🛠️ Stack Tecnológico

### Backend Core
```python
# Framework Web
Flask==3.0.3              # Micro-framework web
Flask-CORS==5.0.0          # Cross-Origin Resource Sharing
Flask-SQLAlchemy==3.1.1    # ORM integration

# Banco de Dados
SQLAlchemy==2.0.35         # ORM avançado
sqlite3                    # Banco embarcado (dev)

# Automação Web
playwright==1.48.0         # Browser automation
pyee==12.0.0              # Event emitter (Playwright dependency)

# Autenticação e Segurança
PyJWT==2.9.0              # JSON Web Tokens
bcrypt==4.2.0             # Hash de senhas
cryptography==43.0.1      # Criptografia avançada

# HTTP e Integração
requests==2.32.3          # Cliente HTTP
urllib3                   # HTTP client low-level

# Configuração
python-dotenv==1.0.1      # Variáveis de ambiente
```

### Frontend
```javascript
// Vanilla JavaScript (ES6+)
- Fetch API para requisições
- LocalStorage para cache
- CSS Grid e Flexbox
- Responsive Design
- Progressive Enhancement
```

### DevOps e Deploy
```yaml
# Containerização
Docker                    # Containerização
Docker Compose           # Orquestração

# Proxy Reverso
Nginx                    # Load balancer e SSL termination

# CI/CD
GitHub Actions           # Pipeline automatizado
```

### Ferramentas de Desenvolvimento
```python
# Qualidade de Código
pylint==3.3.8            # Análise estática
flake8==7.3.0            # Style guide enforcement
black==25.9.0            # Code formatter

# Segurança
bandit==1.8.6            # Security linter
safety==3.6.1            # Dependency vulnerability scanner

# Testes
unittest                 # Framework de testes nativo
pytest                   # Framework de testes avançado (planejado)
```

## 🔄 Fluxo de Funcionamento

### 1. **Autenticação OAuth 2.0**
```python
# Fluxo de autenticação LinkedIn
def linkedin_oauth_flow():
    # 1. Gerar URL de autorização
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization"
    params = {
        'response_type': 'code',
        'client_id': LINKEDIN_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': generate_csrf_token(),
        'scope': 'r_liteprofile r_emailaddress'
    }
    
    # 2. Usuário autoriza no LinkedIn
    # 3. Callback recebe código de autorização
    # 4. Trocar código por access token
    token_response = requests.post(
        'https://www.linkedin.com/oauth/v2/accessToken',
        data=token_data
    )
    
    # 5. Obter dados do perfil
    profile = requests.get(
        'https://api.linkedin.com/v2/people/~',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    # 6. Gerar JWT interno
    jwt_token = jwt.encode(user_data, SECRET_KEY, algorithm='HS256')
    return jwt_token
```

### 2. **Automação com Playwright**
```python
# Engine de automação
class LinkedInAutomation:
    def __init__(self):
        self.browser = None
        self.page = None
        self.context = None
    
    async def initialize_browser(self):
        """Inicializa browser headless"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (compatible; SnapLinked/3.0)',
            viewport={'width': 1920, 'height': 1080}
        )
        self.page = await self.context.new_page()
    
    async def like_posts(self, target_count: int):
        """Automatiza curtidas em posts"""
        await self.page.goto('https://www.linkedin.com/feed/')
        
        liked_count = 0
        for i in range(target_count):
            # Localizar botões de like não clicados
            like_buttons = await self.page.query_selector_all(
                'button[aria-label*="Like"]:not([aria-pressed="true"])'
            )
            
            if like_buttons:
                button = like_buttons[0]
                await button.click()
                liked_count += 1
                
                # Log da ação
                await self.log_action('like', button, 'success')
                
                # Delay humano
                await self.page.wait_for_timeout(
                    random.randint(2000, 5000)
                )
            
            # Scroll para carregar mais posts
            await self.page.evaluate('window.scrollBy(0, 800)')
            await self.page.wait_for_timeout(1000)
        
        return liked_count
```

### 3. **Persistência de Dados**
```python
# Modelos SQLAlchemy
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    linkedin_id = db.Column(db.String(100), unique=True)
    avatar_url = db.Column(db.String(500))
    access_token = db.Column(db.Text)  # Encrypted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    automation_sessions = db.relationship('AutomationSession', backref='user')
    stats = db.relationship('UserStats', backref='user', uselist=False)

class AutomationSession(db.Model):
    __tablename__ = 'automation_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    session_type = db.Column(db.String(50))  # 'like', 'connect', 'comment'
    status = db.Column(db.String(20))        # 'running', 'completed', 'failed'
    target_count = db.Column(db.Integer)
    completed_count = db.Column(db.Integer, default=0)
    error_count = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Logs detalhados
    logs = db.relationship('AutomationLog', backref='session')
```

### 4. **API REST Endpoints**
```python
# Estrutura da API
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'version': '3.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'features': {
            'oauth_linkedin': True,
            'automation': True,
            'database': True
        }
    })

@app.route('/api/automation/like', methods=['POST'])
@jwt_required
def automation_like():
    """Endpoint de automação de curtidas"""
    data = request.get_json()
    target_count = data.get('target_count', 1)
    
    # Validação
    if not 1 <= target_count <= 50:
        return jsonify({'error': 'Invalid target_count'}), 400
    
    # Executar automação
    result = automation_service.execute_like_automation(
        user_id=current_user.id,
        target_count=target_count
    )
    
    return jsonify(result)
```

## 🔐 Segurança Implementada

### 1. **Autenticação e Autorização**
```python
# JWT Token Management
def generate_jwt_token(user_data):
    payload = {
        'user_id': user_data['id'],
        'email': user_data['email'],
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow(),
        'iss': 'snaplinked-v3'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Decorator para proteção de rotas
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Token required'}), 401
        
        try:
            token = token.split(' ')[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                raise jwt.InvalidTokenError()
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated_function
```

### 2. **Proteção CSRF**
```python
# State validation para OAuth
def generate_csrf_token():
    return secrets.token_urlsafe(32)

def validate_csrf_token(state):
    # Validar state parameter no callback OAuth
    stored_state = session.get('oauth_state')
    return stored_state and secrets.compare_digest(stored_state, state)
```

### 3. **Rate Limiting**
```python
# Implementação de rate limiting
from collections import defaultdict
from time import time

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_allowed(self, key, limit=10, window=60):
        now = time()
        # Limpar requests antigas
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if now - req_time < window
        ]
        
        if len(self.requests[key]) >= limit:
            return False
        
        self.requests[key].append(now)
        return True
```

## 🧪 Estratégia de Testes

### 1. **Testes Unitários**
```python
# Exemplo de teste de modelo
class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def test_user_creation(self):
        user = User(
            email='test@example.com',
            name='Test User',
            linkedin_id='test123'
        )
        db.session.add(user)
        db.session.commit()
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertIsNotNone(user.created_at)
```

### 2. **Testes de Integração**
```python
# Teste de endpoint da API
class TestAPI(unittest.TestCase):
    def test_health_endpoint(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['version'], '3.0.0')
```

## 🚀 Deploy e DevOps

### 1. **Containerização Docker**
```dockerfile
# Multi-stage build para otimização
FROM python:3.11-slim as builder

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage final
FROM python:3.11-slim

# Copiar dependências do builder
COPY --from=builder /root/.local /root/.local

# Configurar PATH
ENV PATH=/root/.local/bin:$PATH

# Copiar aplicação
COPY . /app
WORKDIR /app

# Usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash snaplinked
USER snaplinked

EXPOSE 5000
CMD ["python", "app.py"]
```

### 2. **Orquestração com Docker Compose**
```yaml
# Configuração para produção
version: '3.8'
services:
  snaplinked:
    build: .
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/snaplinked
    depends_on:
      - db
      - redis
    
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: snaplinked
      POSTGRES_USER: snaplinked
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

## 📊 Performance e Otimizações

### 1. **Otimizações de Banco**
```python
# Índices para performance
class User(db.Model):
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    linkedin_id = db.Column(db.String(100), unique=True, index=True)

# Query optimization
def get_user_stats_optimized(user_id):
    return db.session.query(
        func.count(AutomationLog.id).label('total_actions'),
        func.sum(case([(AutomationLog.action_type == 'like', 1)], else_=0)).label('likes'),
        func.sum(case([(AutomationLog.action_type == 'connect', 1)], else_=0)).label('connects')
    ).filter(AutomationLog.user_id == user_id).first()
```

### 2. **Cache e Otimizações**
```python
# Cache de sessão
from functools import lru_cache

@lru_cache(maxsize=128)
def get_user_by_id(user_id):
    return User.query.get(user_id)

# Lazy loading para relacionamentos
class User(db.Model):
    automation_sessions = db.relationship(
        'AutomationSession', 
        backref='user',
        lazy='dynamic'  # Carregamento sob demanda
    )
```

## 🔮 Extensibilidade e Futuro

### 1. **Plugin Architecture**
```python
# Sistema de plugins para novas redes sociais
class SocialNetworkPlugin:
    def __init__(self, name):
        self.name = name
    
    def authenticate(self, credentials):
        raise NotImplementedError
    
    def like_post(self, post_id):
        raise NotImplementedError
    
    def send_connection(self, user_id):
        raise NotImplementedError

class TwitterPlugin(SocialNetworkPlugin):
    def __init__(self):
        super().__init__('twitter')
    
    def like_post(self, post_id):
        # Implementação específica do Twitter
        pass
```

### 2. **API Versioning**
```python
# Versionamento da API
@app.route('/api/v1/automation/like', methods=['POST'])
def automation_like_v1():
    # Versão 1 da API
    pass

@app.route('/api/v2/automation/like', methods=['POST'])
def automation_like_v2():
    # Versão 2 com melhorias
    pass
```

## 📈 Monitoramento e Observabilidade

### 1. **Logging Estruturado**
```python
import logging
import json

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
    
    def log_automation_action(self, user_id, action, status, metadata=None):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'action': action,
            'status': status,
            'metadata': metadata or {}
        }
        self.logger.info(json.dumps(log_data))
```

### 2. **Métricas de Performance**
```python
# Decorator para medir tempo de execução
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        # Log métrica
        logger.info(f"{func.__name__} executed in {execution_time:.2f}s")
        return result
    return wrapper
```

## 🎯 Conclusão Técnica

O **SnapLinked v3.0** representa uma implementação robusta e escalável de automação web, combinando:

- **Arquitetura moderna** com separação de responsabilidades
- **Stack tecnológico atual** e bem suportado
- **Segurança de nível empresarial** com múltiplas camadas
- **Automação real** usando tecnologias de ponta
- **Extensibilidade** para futuras funcionalidades
- **Observabilidade** completa para produção

O projeto demonstra boas práticas de desenvolvimento Python, arquitetura de software e DevOps, sendo uma excelente referência para sistemas de automação web profissionais.

---

**Desenvolvido com foco em qualidade, segurança e escalabilidade** 🚀
