# SnapLinked Platform - Documentação Técnica

## Visão Geral

SnapLinked é uma plataforma de automação para LinkedIn com funcionalidades avançadas de networking e análise.

## 1. Tecnologias

### Frontend
- React 19.1.0
- Vite 6.3.5
- TailwindCSS
- Radix UI

### Backend
- Python 3.12
- Flask 2.3.3
- Playwright
- JWT Auth

## 2. Arquitetura

### Frontend
- Single Page Application (SPA)
- Context API para estado global
- Design System próprio
- Componentização reutilizável

### Backend
- API RESTful
- Middleware de autenticação
- Cache em Redis
- Automação headless

## 3. Segurança

- JWT com rotação de tokens
- Rate limiting por IP
- CORS configurável
- Validação de inputs

## 4. Performance

- Code splitting
- Lazy loading
- Caching strategies
- Query optimization

## 5. Deployment

- Docker containers
- NGINX proxy
- CI/CD automatizado
- Monitoramento