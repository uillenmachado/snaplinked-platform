# Arquitetura SnapLinked Platform

## 1. Visão Geral

### Frontend (React + Vite)
- Components/
  - Layout/
  - UI/
- Contexts/
- Hooks/
- Services/
- Utils/

### Backend (Python + Flask)
- Routes/
- Services/
- Models/
- Utils/
- Config/

## 2. Componentes

### Frontend
- AuthContext: Gerenciamento de autenticação
- ThemeContext: Tematização
- APIService: Comunicação com backend
- LinkedInService: Integração LinkedIn

### Backend
- AuthService: Autenticação e autorização
- LinkedInService: Automação LinkedIn
- AnalyticsService: Métricas e análises
- DatabaseService: Persistência

## 3. Integrações

- LinkedIn API
- Redis Cache
- PostgreSQL Database
- S3 Storage

## 4. Infraestrutura

- Docker containers
- NGINX reverse proxy
- Redis cache layer
- PostgreSQL database

## 5. Segurança

- JWT Authentication
- CORS policies
- Rate limiting
- Input validation

## 6. Monitoramento

- Performance metrics
- Error tracking
- User analytics
- System health