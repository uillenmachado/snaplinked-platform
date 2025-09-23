/**
 * SnapLinked v3.0 - JavaScript Principal
 * Gerenciamento do dashboard e automações
 * Versão corrigida e otimizada
 */

class SnapLinkedApp {
    constructor() {
        this.user = null;
        this.stats = { total_likes: 0, total_connections: 0, total_comments: 0 };
        this.isAuthenticated = false;
        this.automationRunning = false;
        this.authToken = localStorage.getItem('snaplinked_token');
        this.progressInterval = null;
        this.statusCheckInterval = null;
        this.eventListeners = new Map();
        
        this.init();
    }
    
    async init() {
        console.log('🚀 Iniciando SnapLinked v3.0...');
        
        try {
            // Registrar event listeners
            this.registerEventListeners();
            
            // Verificar autenticação
            await this.checkAuthStatus();
            
            // Carregar status inicial
            await this.loadStatus();
            
            // Verificar parâmetros de URL (callback OAuth)
            this.handleUrlParams();
            
            // Inicializar verificação periódica de status
            this.startStatusCheck();
            
            console.log('✅ SnapLinked inicializado com sucesso!');
        } catch (error) {
            console.error('❌ Erro na inicialização:', error);
            this.showAlert('Erro na inicialização da aplicação', 'error');
        }
    }
    
    registerEventListeners() {
        // Limpar listeners existentes
        this.clearEventListeners();
        
        // Botões de autenticação
        this.addEventListenerSafe('oauthBtn', 'click', () => this.startOAuthLogin());
        this.addEventListenerSafe('manualBtn', 'click', () => this.showManualLoginForm());
        this.addEventListenerSafe('logoutBtn', 'click', () => this.logout());
        
        // Botões de automação
        this.addEventListenerSafe('likeBtn', 'click', () => this.executeAutomation('like'));
        this.addEventListenerSafe('connectBtn', 'click', () => this.executeAutomation('connect'));
        this.addEventListenerSafe('commentBtn', 'click', () => this.executeAutomation('comment'));
        
        // Outros botões
        this.addEventListenerSafe('openLinkedInBtn', 'click', () => this.openLinkedIn());
        this.addEventListenerSafe('resetStatsBtn', 'click', () => this.resetStats());
        
        // Navegação
        this.addEventListenerSafe('backBtn', 'click', () => this.navigateBack());
        this.addEventListenerSafe('forwardBtn', 'click', () => this.navigateForward());
        this.addEventListenerSafe('refreshBtn', 'click', () => this.refreshPage());
        this.addEventListenerSafe('goBtn', 'click', () => this.navigateToUrl());
        
        // Atalhos de teclado
        this.addEventListenerSafe(document, 'keydown', (e) => this.handleKeyboardShortcuts(e));
        
        // Detectar mudanças de visibilidade da página
        this.addEventListenerSafe(document, 'visibilitychange', () => this.handleVisibilityChange());
        
        // Detectar mudanças de conexão
        if ('navigator' in window && 'onLine' in navigator) {
            this.addEventListenerSafe(window, 'online', () => this.handleConnectionChange(true));
            this.addEventListenerSafe(window, 'offline', () => this.handleConnectionChange(false));
        }
    }
    
    addEventListenerSafe(elementOrId, event, handler) {
        let element;
        if (typeof elementOrId === 'string') {
            element = document.getElementById(elementOrId);
            if (!element) return;
        } else {
            element = elementOrId;
        }
        
        // Remover listener existente se houver
        const key = `${elementOrId}-${event}`;
        if (this.eventListeners.has(key)) {
            const oldHandler = this.eventListeners.get(key);
            element.removeEventListener(event, oldHandler);
        }
        
        // Adicionar novo listener
        element.addEventListener(event, handler);
        this.eventListeners.set(key, handler);
    }
    
    clearEventListeners() {
        this.eventListeners.forEach((handler, key) => {
            const [elementId, event] = key.split('-');
            const element = document.getElementById(elementId) || document || window;
            if (element) {
                element.removeEventListener(event, handler);
            }
        });
        this.eventListeners.clear();
    }
    
    async checkAuthStatus() {
        if (!this.authToken) return;
        
        try {
            const response = await this.apiCall('/api/status');
            if (response.authenticated) {
                this.user = response.user;
                this.stats = response.stats || this.stats;
                this.isAuthenticated = true;
                this.updateUI();
            } else {
                this.clearAuthData();
            }
        } catch (error) {
            console.error('Erro ao verificar autenticação:', error);
            this.clearAuthData();
        }
    }
    
    clearAuthData() {
        localStorage.removeItem('snaplinked_token');
        this.authToken = null;
        this.user = null;
        this.isAuthenticated = false;
    }
    
    async loadStatus() {
        try {
            const response = await this.apiCall('/api/status');
            
            if (response.authenticated) {
                this.user = response.user;
                this.stats = response.stats || this.stats;
                this.isAuthenticated = true;
                this.authToken = this.authToken || 'temp-token'; // Fallback
            }
            
            this.updateUI();
        } catch (error) {
            console.error('Erro ao carregar status:', error);
            this.updateUI();
        }
    }
    
    startStatusCheck() {
        // Verificar status a cada 30 segundos se autenticado
        this.statusCheckInterval = setInterval(async () => {
            if (this.isAuthenticated && !document.hidden) {
                try {
                    await this.loadStatus();
                } catch (error) {
                    console.error('Erro na verificação periódica:', error);
                }
            }
        }, 30000);
    }
    
    handleUrlParams() {
        const urlParams = new URLSearchParams(window.location.search);
        const auth = urlParams.get('auth');
        const user = urlParams.get('user');
        const error = urlParams.get('error');
        
        if (auth === 'success' && user) {
            this.showAlert(`🎉 Autenticação realizada com sucesso! Bem-vindo, ${decodeURIComponent(user)}!`, 'success');
            // Limpar parâmetros da URL
            this.clearUrlParams();
            // Recarregar status
            setTimeout(() => this.loadStatus(), 1000);
        } else if (auth === 'error' || error) {
            const errorMsg = error ? decodeURIComponent(error) : 'Erro na autenticação';
            this.showAlert(`❌ ${errorMsg}. Tente novamente.`, 'error');
            this.clearUrlParams();
        }
    }
    
    clearUrlParams() {
        const url = new URL(window.location);
        url.search = '';
        window.history.replaceState({}, document.title, url.toString());
    }
    
    async startOAuthLogin() {
        try {
            this.showLoading('🔐 Iniciando autenticação OAuth...');
            
            const response = await this.apiCall('/api/auth/linkedin');
            if (response.auth_url) {
                // Abrir em nova janela para melhor UX
                const authWindow = window.open(
                    response.auth_url, 
                    'linkedin-auth', 
                    'width=600,height=700,scrollbars=yes,resizable=yes'
                );
                
                // Monitorar fechamento da janela
                const checkClosed = setInterval(() => {
                    if (authWindow.closed) {
                        clearInterval(checkClosed);
                        this.hideLoading();
                        // Verificar se autenticação foi bem-sucedida
                        setTimeout(() => this.loadStatus(), 1000);
                    }
                }, 1000);
                
            } else {
                throw new Error('URL de autenticação não recebida');
            }
        } catch (error) {
            console.error('Erro no OAuth:', error);
            this.showAlert('❌ Erro ao iniciar autenticação OAuth', 'error');
            this.hideLoading();
        }
    }
    
    showManualLoginForm() {
        const authCard = document.querySelector('.auth-card');
        if (authCard) {
            authCard.innerHTML = `
                <h4>🔐 Login Manual</h4>
                <p class="form-description">Digite suas informações para iniciar o login manual:</p>
                <form id="manualLoginForm" novalidate>
                    <div class="form-group">
                        <label class="form-label" for="email">
                            <span class="required">*</span> Email:
                        </label>
                        <input type="email" id="email" class="form-input" required 
                               placeholder="seu@email.com" autocomplete="email"
                               aria-describedby="email-error">
                        <div id="email-error" class="field-error" role="alert"></div>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="name">Nome completo:</label>
                        <input type="text" id="name" class="form-input" 
                               placeholder="Seu Nome Completo" autocomplete="name"
                               maxlength="100">
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-manual">
                            <span>🚀</span> Iniciar Login
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="location.reload()">
                            <span>❌</span> Cancelar
                        </button>
                    </div>
                </form>
            `;
            
            // Re-registrar event listener
            this.addEventListenerSafe('manualLoginForm', 'submit', (e) => this.handleManualLogin(e));
            
            // Focar no campo email
            setTimeout(() => {
                const emailField = document.getElementById('email');
                if (emailField) emailField.focus();
            }, 100);
        }
    }
    
    async handleManualLogin(event) {
        event.preventDefault();
        
        const emailField = document.getElementById('email');
        const nameField = document.getElementById('name');
        const emailError = document.getElementById('email-error');
        
        // Validação
        const email = emailField.value.trim();
        const name = nameField.value.trim() || 'Usuário SnapLinked';
        
        // Limpar erros anteriores
        emailError.textContent = '';
        emailField.classList.remove('error');
        
        if (!email) {
            this.showFieldError(emailField, emailError, 'Email é obrigatório');
            return;
        }
        
        if (!this.isValidEmail(email)) {
            this.showFieldError(emailField, emailError, 'Email inválido');
            return;
        }
        
        try {
            this.showLoading('🔐 Iniciando login manual...');
            
            const response = await this.apiCall('/api/auth/manual-login', 'POST', {
                email: email,
                name: name
            });
            
            if (response.success) {
                this.authToken = response.auth_token;
                localStorage.setItem('snaplinked_token', this.authToken);
                this.user = response.user;
                this.isAuthenticated = true;
                
                this.showAlert('✅ Login manual iniciado! Faça login no LinkedIn na aba que se abriu.', 'success');
                this.updateUI();
                
                // Abrir LinkedIn em nova aba
                window.open('https://www.linkedin.com/login', '_blank');
                
                // Aguardar confirmação de login
                this.waitForLinkedInLogin();
            } else {
                throw new Error(response.message || 'Erro no login manual');
            }
        } catch (error) {
            console.error('Erro no login manual:', error);
            this.showAlert(`❌ Erro no login manual: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    showFieldError(field, errorElement, message) {
        field.classList.add('error');
        errorElement.textContent = message;
        field.focus();
    }
    
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    async waitForLinkedInLogin() {
        let attempts = 0;
        const maxAttempts = 100; // 5 minutos (3s * 100)
        
        const checkInterval = setInterval(async () => {
            attempts++;
            
            try {
                const response = await this.apiCall('/api/status');
                if (response.authenticated && response.user && response.user.linkedin_id) {
                    clearInterval(checkInterval);
                    this.showAlert('🎉 Login no LinkedIn detectado com sucesso!', 'success');
                    await this.loadStatus();
                    return;
                }
            } catch (error) {
                // Ignorar erros durante verificação
            }
            
            // Parar após máximo de tentativas
            if (attempts >= maxAttempts) {
                clearInterval(checkInterval);
                this.showAlert('⏰ Tempo limite para login no LinkedIn. Tente novamente se necessário.', 'info');
            }
        }, 3000);
        
        // Armazenar para limpeza posterior
        this.loginCheckInterval = checkInterval;
    }
    
    async logout() {
        try {
            this.showLoading('🚪 Fazendo logout...');
            await this.apiCall('/api/auth/logout', 'POST');
        } catch (error) {
            console.error('Erro no logout:', error);
        }
        
        // Limpar dados locais
        this.clearAuthData();
        this.stats = { total_likes: 0, total_connections: 0, total_comments: 0 };
        
        // Limpar intervals
        if (this.loginCheckInterval) {
            clearInterval(this.loginCheckInterval);
        }
        
        this.updateUI();
        this.showAlert('👋 Logout realizado com sucesso!', 'success');
        this.hideLoading();
    }
    
    async executeAutomation(type) {
        if (!this.isAuthenticated) {
            this.showAlert('🔐 Faça login primeiro para usar as automações!', 'error');
            return;
        }
        
        if (this.automationRunning) {
            this.showAlert('⚠️ Já existe uma automação em execução!', 'error');
            return;
        }
        
        const actionConfig = {
            'like': { name: 'Curtir Posts', count: 3, emoji: '👍', color: '#28a745' },
            'connect': { name: 'Enviar Conexões', count: 2, emoji: '🤝', color: '#007bff' },
            'comment': { name: 'Comentar Posts', count: 1, emoji: '💬', color: '#fd7e14' }
        };
        
        const config = actionConfig[type];
        if (!config) return;
        
        // Confirmar ação
        if (!confirm(`Deseja executar: ${config.name} (${config.count} ações)?`)) {
            return;
        }
        
        try {
            this.automationRunning = true;
            this.updateAutomationButtons();
            
            // Mostrar overlay de progresso
            this.showAutomationOverlay(config);
            
            // Executar automação
            const response = await this.apiCall(`/api/automation/${type}`, 'POST', {
                target_count: config.count
            });
            
            if (response.success) {
                this.stats = response.stats || this.stats;
                this.updateStats();
                
                const details = response.details || {};
                const completed = details.completed_count || 0;
                const errors = details.error_count || 0;
                
                let message = `✅ ${config.name} executada com sucesso! ${completed} ações realizadas.`;
                if (errors > 0) {
                    message += ` (${errors} erros)`;
                }
                
                this.showAlert(message, 'success');
            } else {
                throw new Error(response.message || 'Erro na automação');
            }
            
        } catch (error) {
            console.error(`Erro na automação ${type}:`, error);
            this.showAlert(`❌ Erro na automação: ${error.message}`, 'error');
        } finally {
            this.automationRunning = false;
            this.updateAutomationButtons();
            this.hideAutomationOverlay();
        }
    }
    
    showAutomationOverlay(config) {
        const overlay = document.getElementById('automationOverlay');
        const icon = document.getElementById('automationIcon');
        const message = document.getElementById('automationMessage');
        const detail = document.getElementById('automationDetail');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        
        if (overlay) {
            overlay.style.display = 'flex';
            overlay.style.background = `rgba(${this.hexToRgb(config.color)}, 0.95)`;
            overlay.setAttribute('aria-live', 'polite');
        }
        
        if (icon) icon.textContent = config.emoji;
        if (message) message.textContent = `${config.emoji} ${config.name}`;
        if (detail) detail.textContent = 'Iniciando automação...';
        
        // Simular progresso realista
        let progress = 0;
        const steps = [
            { progress: 10, message: 'Conectando ao LinkedIn...' },
            { progress: 25, message: 'Verificando autenticação...' },
            { progress: 40, message: 'Analisando conteúdo...' },
            { progress: 60, message: 'Executando ações...' },
            { progress: 80, message: 'Processando resultados...' },
            { progress: 95, message: 'Finalizando...' },
            { progress: 100, message: 'Concluído!' }
        ];
        
        let stepIndex = 0;
        this.progressInterval = setInterval(() => {
            if (stepIndex < steps.length) {
                const step = steps[stepIndex];
                progress = step.progress;
                
                if (progressBar) progressBar.style.width = progress + '%';
                if (progressText) progressText.textContent = progress + '% concluído';
                if (detail) detail.textContent = step.message;
                
                stepIndex++;
            } else {
                clearInterval(this.progressInterval);
            }
        }, 800);
    }
    
    hideAutomationOverlay() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
        
        setTimeout(() => {
            const overlay = document.getElementById('automationOverlay');
            const progressBar = document.getElementById('progressBar');
            const progressText = document.getElementById('progressText');
            
            if (overlay) overlay.style.display = 'none';
            if (progressBar) progressBar.style.width = '0%';
            if (progressText) progressText.textContent = '0% concluído';
        }, 2000);
    }
    
    async resetStats() {
        if (!this.isAuthenticated) {
            this.showAlert('🔐 Faça login primeiro!', 'error');
            return;
        }
        
        if (!confirm('Deseja realmente resetar todas as estatísticas?')) {
            return;
        }
        
        try {
            this.showLoading('🔄 Resetando estatísticas...');
            
            const response = await this.apiCall('/api/stats/reset', 'POST');
            if (response.success) {
                this.stats = response.stats || { total_likes: 0, total_connections: 0, total_comments: 0 };
                this.updateStats();
                this.showAlert('✅ Estatísticas resetadas com sucesso!', 'success');
            }
        } catch (error) {
            console.error('Erro ao resetar estatísticas:', error);
            this.showAlert('❌ Erro ao resetar estatísticas', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    openLinkedIn() {
        const iframe = document.getElementById('linkedinFrame');
        const placeholder = document.getElementById('iframePlaceholder');
        const urlBar = document.getElementById('urlBar');
        
        if (iframe && placeholder) {
            iframe.src = 'https://www.linkedin.com/feed/';
            placeholder.style.display = 'none';
            iframe.style.display = 'block';
            
            if (urlBar) {
                urlBar.value = 'https://www.linkedin.com/feed/';
            }
            
            // Adicionar listener para detectar carregamento
            iframe.onload = () => {
                this.showAlert('🌐 LinkedIn carregado com sucesso!', 'success');
            };
        }
    }
    
    navigateBack() {
        const iframe = document.getElementById('linkedinFrame');
        if (iframe && iframe.contentWindow) {
            try {
                iframe.contentWindow.history.back();
            } catch (error) {
                console.warn('Não foi possível navegar para trás:', error);
            }
        }
    }
    
    navigateForward() {
        const iframe = document.getElementById('linkedinFrame');
        if (iframe && iframe.contentWindow) {
            try {
                iframe.contentWindow.history.forward();
            } catch (error) {
                console.warn('Não foi possível navegar para frente:', error);
            }
        }
    }
    
    refreshPage() {
        const iframe = document.getElementById('linkedinFrame');
        if (iframe && iframe.src) {
            this.showLoading('🔄 Atualizando página...');
            iframe.src = iframe.src;
            
            iframe.onload = () => {
                this.hideLoading();
                this.showAlert('✅ Página atualizada!', 'success');
            };
        }
    }
    
    navigateToUrl() {
        const urlBar = document.getElementById('urlBar');
        const iframe = document.getElementById('linkedinFrame');
        
        if (urlBar && iframe) {
            let url = urlBar.value.trim();
            
            // Validar URL
            if (!url.startsWith('http')) {
                url = 'https://' + url;
            }
            
            // Verificar se é URL do LinkedIn
            if (!url.includes('linkedin.com')) {
                this.showAlert('⚠️ Por segurança, apenas URLs do LinkedIn são permitidas', 'error');
                return;
            }
            
            iframe.src = url;
            document.getElementById('iframePlaceholder').style.display = 'none';
            iframe.style.display = 'block';
        }
    }
    
    handleKeyboardShortcuts(event) {
        // Ctrl/Cmd + teclas
        if (event.ctrlKey || event.metaKey) {
            switch (event.key) {
                case 'l':
                    event.preventDefault();
                    if (this.isAuthenticated) {
                        this.executeAutomation('like');
                    }
                    break;
                case 'k':
                    event.preventDefault();
                    if (this.isAuthenticated) {
                        this.executeAutomation('connect');
                    }
                    break;
                case 'j':
                    event.preventDefault();
                    if (this.isAuthenticated) {
                        this.executeAutomation('comment');
                    }
                    break;
                case 'r':
                    event.preventDefault();
                    this.refreshPage();
                    break;
            }
        }
        
        // Tecla Escape para fechar overlays
        if (event.key === 'Escape') {
            const overlay = document.getElementById('automationOverlay');
            if (overlay && overlay.style.display === 'flex') {
                this.hideAutomationOverlay();
            }
        }
    }
    
    handleVisibilityChange() {
        if (document.hidden) {
            // Página ficou oculta - pausar verificações
            if (this.statusCheckInterval) {
                clearInterval(this.statusCheckInterval);
            }
        } else {
            // Página ficou visível - retomar verificações
            this.startStatusCheck();
            // Verificar status imediatamente
            this.loadStatus();
        }
    }
    
    handleConnectionChange(isOnline) {
        if (isOnline) {
            this.showAlert('🌐 Conexão restaurada!', 'success');
            this.loadStatus();
        } else {
            this.showAlert('📡 Conexão perdida. Algumas funcionalidades podem não funcionar.', 'error');
        }
    }
    
    updateUI() {
        this.updateAuthStatus();
        this.updateStats();
        this.updateAutomationButtons();
        this.updateConnectionStatus();
    }
    
    updateAuthStatus() {
        const authCard = document.querySelector('.auth-card');
        
        if (this.isAuthenticated && this.user) {
            // Mostrar informações do usuário
            if (authCard) {
                authCard.innerHTML = `
                    <h4>👤 Usuário Conectado</h4>
                    <div class="user-info">
                        <div class="user-avatar">
                            ${this.user.avatar_url ? 
                                `<img src="${this.user.avatar_url}" alt="Avatar" style="width:100%;height:100%;border-radius:50%;">` : 
                                '👤'
                            }
                        </div>
                        <div class="user-details">
                            <h5>${this.user.name || 'Usuário'}</h5>
                            <p>${this.user.email || ''}</p>
                            ${this.user.linkedin_id ? '<p>✅ LinkedIn conectado</p>' : '<p>⚠️ LinkedIn pendente</p>'}
                        </div>
                    </div>
                    <button id="logoutBtn" class="btn btn-logout" style="width: 100%; margin-top: 12px;">
                        <span>🚪</span> Logout
                    </button>
                `;
                
                // Re-registrar event listener do logout
                this.addEventListenerSafe('logoutBtn', 'click', () => this.logout());
            }
        } else {
            // Mostrar opções de login
            if (authCard && !authCard.querySelector('#manualLoginForm')) {
                authCard.innerHTML = `
                    <h4>🔐 Conectar LinkedIn</h4>
                    <p>Escolha uma opção para conectar sua conta:</p>
                    <div class="auth-buttons">
                        <button id="oauthBtn" class="btn btn-oauth">
                            <span>🔗</span> OAuth LinkedIn
                        </button>
                        <button id="manualBtn" class="btn btn-manual">
                            <span>🖱️</span> Login Manual
                        </button>
                    </div>
                `;
                
                // Re-registrar event listeners
                this.addEventListenerSafe('oauthBtn', 'click', () => this.startOAuthLogin());
                this.addEventListenerSafe('manualBtn', 'click', () => this.showManualLoginForm());
            }
        }
    }
    
    updateConnectionStatus() {
        const statusEl = document.getElementById('connectionStatus');
        if (statusEl) {
            if (this.isAuthenticated) {
                statusEl.textContent = '🟢 Conectado';
                statusEl.classList.add('connected');
            } else {
                statusEl.textContent = '🔴 Desconectado';
                statusEl.classList.remove('connected');
            }
        }
    }
    
    updateStats() {
        const likesEl = document.getElementById('likesCount');
        const connectionsEl = document.getElementById('connectionsCount');
        const commentsEl = document.getElementById('commentsCount');
        
        if (likesEl) {
            likesEl.textContent = this.stats.total_likes || 0;
            this.animateStatUpdate(likesEl);
        }
        if (connectionsEl) {
            connectionsEl.textContent = this.stats.total_connections || 0;
            this.animateStatUpdate(connectionsEl);
        }
        if (commentsEl) {
            commentsEl.textContent = this.stats.total_comments || 0;
            this.animateStatUpdate(commentsEl);
        }
    }
    
    animateStatUpdate(element) {
        element.style.transform = 'scale(1.2)';
        element.style.transition = 'transform 0.3s ease';
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 300);
    }
    
    updateAutomationButtons() {
        const buttons = ['likeBtn', 'connectBtn', 'commentBtn'];
        
        buttons.forEach(id => {
            const btn = document.getElementById(id);
            if (btn) {
                const wasDisabled = btn.disabled;
                btn.disabled = !this.isAuthenticated || this.automationRunning;
                
                // Adicionar indicador visual de estado
                if (btn.disabled && !wasDisabled) {
                    btn.style.opacity = '0.6';
                    btn.style.cursor = 'not-allowed';
                } else if (!btn.disabled && wasDisabled) {
                    btn.style.opacity = '1';
                    btn.style.cursor = 'pointer';
                }
            }
        });
    }
    
    async apiCall(endpoint, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };
        
        if (this.authToken) {
            options.headers['Authorization'] = `Bearer ${this.authToken}`;
        }
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(endpoint, options);
            
            // Verificar se a resposta é JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error(`Resposta inválida do servidor (${response.status})`);
            }
            
            const responseData = await response.json();
            
            if (!response.ok) {
                throw new Error(responseData.message || responseData.error || `HTTP ${response.status}`);
            }
            
            return responseData;
        } catch (error) {
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error('Erro de conexão. Verifique sua internet.');
            }
            throw error;
        }
    }
    
    showAlert(message, type = 'info') {
        // Remover alertas existentes
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());
        
        // Criar novo alerta
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} fade-in`;
        alert.textContent = message;
        alert.setAttribute('role', 'alert');
        alert.setAttribute('aria-live', 'polite');
        
        // Inserir no topo da sidebar
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.insertBefore(alert, sidebar.firstChild);
            
            // Remover após 5 segundos
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.style.opacity = '0';
                    alert.style.transform = 'translateY(-20px)';
                    setTimeout(() => alert.remove(), 300);
                }
            }, 5000);
        }
    }
    
    showLoading(message = 'Carregando...') {
        const loadingEl = document.getElementById('loadingMessage');
        if (loadingEl) {
            loadingEl.innerHTML = `
                <div class="loading"></div> 
                <span>${message}</span>
            `;
            loadingEl.style.display = 'flex';
            loadingEl.style.alignItems = 'center';
            loadingEl.style.gap = '8px';
        }
    }
    
    hideLoading() {
        const loadingEl = document.getElementById('loadingMessage');
        if (loadingEl) {
            loadingEl.style.display = 'none';
        }
    }
    
    hexToRgb(hex) {
        // Remover # se presente
        hex = hex.replace('#', '');
        
        // Converter para RGB
        const result = /^([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? 
            `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : 
            '0, 123, 255';
    }
    
    // Cleanup ao sair da página
    destroy() {
        this.clearEventListeners();
        
        if (this.statusCheckInterval) {
            clearInterval(this.statusCheckInterval);
        }
        
        if (this.loginCheckInterval) {
            clearInterval(this.loginCheckInterval);
        }
        
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
    }
}

// Inicializar aplicação quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar módulos avançados
    if (window.AccessibilityManager) {
        window.accessibilityManager = new AccessibilityManager();
    }
    
    if (window.AdvancedFeatures) {
        window.advancedFeatures = new AdvancedFeatures();
    }
    
    // Inicializar aplicação principal
    window.snapLinkedApp = new SnapLinkedApp();
});

// Cleanup ao sair da página
window.addEventListener('beforeunload', () => {
    if (window.snapLinkedApp) {
        window.snapLinkedApp.destroy();
    }
});

// Exportar para uso global
window.SnapLinkedApp = SnapLinkedApp;
