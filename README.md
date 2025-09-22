# SnapLinked - Automação LinkedIn

Sistema de automação LinkedIn com OAuth real, Gemini AI e Playwright.

## 🚀 Instalação Rápida

### Backend
```bash
cd snaplinked-backend
pip install -r requirements.txt
playwright install
python main.py
```

### Frontend
```bash
cd snaplinked-frontend
npm install --legacy-peer-deps
npm run dev
```

**Acesso:** http://localhost:3000

## ⚙️ Configuração

Criar arquivo `.env` no backend:
```env
LINKEDIN_CLIENT_ID=77jmwin70p0gge
LINKEDIN_CLIENT_SECRET=ZGeGVXoeopPADn4v
LINKEDIN_REDIRECT_URI=http://localhost:3000/auth/linkedin/callback
GEMINI_API_KEY=AIzaSyAoCyNdZ7wlwOTFxFGMCCCQrleZ-gmJAJE
SECRET_KEY=your-secret-key
```

## 🐳 Docker

```bash
docker-compose up -d
```

## 🔧 Funcionalidades

- OAuth LinkedIn real
- Automação Playwright (curtidas, comentários)
- Gemini AI para comentários contextuais
- Dashboard tempo real
- Sistema de filas
- Rate limiting

## 📊 API

- **Health:** `GET /api/health`
- **OAuth:** `GET /auth/linkedin/start`
- **Automação:** `POST /api/automation/like`
- **IA:** `POST /api/ai/generate-comment`

---

**SnapLinked v5.0.0** - Production Ready
