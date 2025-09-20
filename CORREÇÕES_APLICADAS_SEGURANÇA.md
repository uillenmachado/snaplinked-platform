# Registro de atividades e falhas de segurança
CORREÇÕES_APLICADAS_SEGURANÇA = {
    "Autenticação": {
        "Proteção contra força bruta": "Implementado limite de tentativas e timeout",
        "Rate limiting": "Aplicado limite de requisições por IP",
        "Tokens JWT": "Configurado com chave secreta segura e expiração adequada"
    },
    "Autorização": {
        "CORS": "Restrito a origens permitidas",
        "Headers de segurança": "Implementado headers de segurança padrão",
        "CSP": "Configurada política de segurança de conteúdo"
    },
    "Dados sensíveis": {
        "Senhas": "Removidas senhas hardcoded",
        "Chaves secretas": "Movidas para variáveis de ambiente",
        "Logs": "Configurados para não expor dados sensíveis"
    },
    "Infraestrutura": {
        "TLS/SSL": "Forçado HTTPS em produção",
        "Headers": "Adicionados headers de segurança",
        "Session": "Configurada com segurança adequada"
    }
}