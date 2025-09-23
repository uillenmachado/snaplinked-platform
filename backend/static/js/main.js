/**
 * SnapLinked v3.0 - JavaScript Principal
 * Gerenciamento do dashboard e automações
 */

class SnapLinkedApp {
    constructor() {
        this.user = null;
        this.stats = { total_likes: 0, total_connections: 0, total_comments: 0 };
        this.isAuthenticated = false;
        this.automationRunning = false;
        this.authToken = localStorage.getItem('snaplinked_token');
        
        this.init();
    }
    
    async init() {
        console.log('🚀 Iniciando SnapLinked v3.0...');
        
        // Registrar event listeners
        this.registerEventListeners();
        
        // Verificar autenticação
        await this.checkAuthStatus();
        
        // Carregar status inicial
        await this.loadStatus();
        
        // Verificar parâmetros de URL (callback OAuth)
        this.handleUrlParams();
        
        console.log('✅ SnapLinked inicializado com sucesso!');
    }
    
    registerEventListeners() {
        // Botões de autenticação
        const oauthBtn = document.getElementById('oauthBtn');
        const manualBtn = document.getElementById('manualBtn');
        const logoutBtn = document.getElementById('logoutBtn');
        
        if (oauthBtn) oauthBtn.addEventListener('click', () => this.startOAuthLogin());
        if (manualBtn) manualBtn.addEventListener('click', () => this.showManualLoginForm());
        if (logoutBtn) logoutBtn.addEventListener('click', () => this.logout());
        
        // Botões de automação
        const likeBtn = document.getElementById('likeBtn');
        const connectBtn = document.getElementById('connectBtn');
        const commentBtn = document.getElementById('commentBtn');
        
        if (likeBtn) likeBtn.addEventListener('click', () => this.executeAutomation('like'));
        if (connectBtn) connectBtn.addEventListener('click', () => this.executeAutomation('connect'));
        if (commentBtn) commentBtn.addEventListener('click', () => this.executeAutomation('comment'));
        
        // Outros botões
        const openLinkedInBtn = document.getElementById('openLinkedInBtn');
        const resetStatsBtn = document.getElementById('resetStatsBtn');
        
        if (openLinkedInBtn) openLinkedInBtn.addEventListener('click', () => this.openLinkedIn());
        if (resetStatsBtn) resetStatsBtn.addEventListener('click', () => this.resetStats());
        
        // Navegação
        const backBtn = document.getElementById('backBtn');
        const forwardBtn = document.getElementById('forwardBtn');
        const refreshBtn = document.getElementById('refreshBtn');
        
        if (backBtn) backBtn.addEventListener('click', () => this.navigateBack());
        if (forwardBtn) forwardBtn.addEventListener('click', () => this.navigateForward());
        if (refreshBtn) refreshBtn.addEventListener('click', () => this.refreshPage());
        
        // Formulário de login manual
        const manualLoginForm = document.getElementById('manualLoginForm');
        if (manualLoginForm) {
            manualLoginForm.addEventListener('submit', (e) => this.handleManualLogin(e));
        }
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
                localStorage.removeItem('snaplinked_token');
                this.authToken = null;
            }
        } catch (error) {
            console.error('Erro ao verificar autenticação:', error);
            localStorage.removeItem('snaplinked_token');
            this.authToken = null;
        }
    }
    
    async loadStatus() {
        try {
            const response = await this.apiCall('/api/status');
            
            if (response.authenticated) {
                this.user = response.user;
                this.stats = response.stats || this.stats;
                this.isAuthenticated = true;
            }
            
            this.updateUI();
        } catch (error) {
            console.error('Erro ao carregar status:', error);
            this.updateUI();
        }
    }
    
    handleUrlParams() {
        const urlParams = new URLSearchParams(window.location.search);
        const auth = urlParams.get('auth');
        const user = urlParams.get('user');
        
        if (auth === 'success' && user) {
            this.showAlert(`Autenticação realizada com sucesso! Bem-vindo, ${user}!`, 'success');
            // Limpar parâmetros da URL
            window.history.replaceState({}, document.title, window.location.pathname);
            // Recarregar status
            setTimeout(() => this.loadStatus(), 1000);
        } else if (auth === 'error') {
            this.showAlert('Erro na autenticação. Tente novamente.', 'error');
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    }
    
    async startOAuthLogin() {
        try {
            this.showLoading('Iniciando autenticação OAuth...');
            
            const response = await this.apiCall('/api/auth/linkedin');
            if (response.auth_url) {
                window.location.href = response.auth_url;
            } else {
                throw new Error('URL de autenticação não recebida');
            }
        } catch (error) {
            console.error('Erro no OAuth:', error);
            this.showAlert('Erro ao iniciar autenticação OAuth', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    showManualLoginForm() {
        const authCard = document.querySelector('.auth-card');
        if (authCard) {
            authCard.innerHTML = `
                <h4>🔐 Login Manual</h4>
                <form id="manualLoginForm">
                    <div class="form-group">
                        <label class="form-label" for="email">Email:</label>
                        <input type="email" id="email" class="form-input" required 
                               placeholder="seu@email.com">
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="name">Nome (opcional):</label>
                        <input type="text" id="name" class="form-input" 
                               placeholder="Seu Nome">
                    </div>
                    <div style="display: flex; gap: 12px;">
                        <button type="submit" class="btn btn-manual">
                            <span>🚀</span> Iniciar Login
                        </button>
                        <button type="button" class="btn" onclick="location.reload()">
                            Cancelar
                        </button>
                    </div>
                </form>
            `;
            
            // Re-registrar event listener
            const form = document.getElementById('manualLoginForm');
            if (form) {
                form.addEventListener('submit', (e) => this.handleManualLogin(e));
            }
        }
    }
    
    async handleManualLogin(event) {
        event.preventDefault();
        
        const email = document.getElementById('email').value;
        const name = document.getElementById('name').value || 'Usuário SnapLinked';
        
        try {
            this.showLoading('Iniciando login manual...');
            
            const response = await this.apiCall('/api/auth/manual-login', 'POST', {
                email: email,
                name: name
            });
            
            if (response.success) {
                this.authToken = response.auth_token;
                localStorage.setItem('snaplinked_token', this.authToken);
                this.user = response.user;
                this.isAuthenticated = true;
                
                this.showAlert('Login manual iniciado! Faça login no LinkedIn na janela que se abriu.', 'success');
                this.updateUI();
                
                // Aguardar confirmação de login
                this.waitForLinkedInLogin();
            } else {
                throw new Error(response.message);
            }
        } catch (error) {
            console.error('Erro no login manual:', error);
            this.showAlert(`Erro no login manual: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async waitForLinkedInLogin() {
        // Implementar verificação periódica se o usuário fez login no LinkedIn
        const checkInterval = setInterval(async () => {
            try {
                const response = await this.apiCall('/api/status');
                if (response.authenticated && response.user) {
                    clearInterval(checkInterval);
                    this.showAlert('Login no LinkedIn detectado com sucesso!', 'success');
                    await this.loadStatus();
                }
            } catch (error) {
                // Ignorar erros durante verificação
            }
        }, 3000);
        
        // Parar verificação após 5 minutos
        setTimeout(() => {
            clearInterval(checkInterval);
        }, 300000);
    }
    
    async logout() {
        try {
            await this.apiCall('/api/auth/logout', 'POST');
        } catch (error) {
            console.error('Erro no logout:', error);
        }
        
        // Limpar dados locais
        localStorage.removeItem('snaplinked_token');
        this.authToken = null;
        this.user = null;
        this.isAuthenticated = false;
        this.stats = { total_likes: 0, total_connections: 0, total_comments: 0 };
        
        this.updateUI();
        this.showAlert('Logout realizado com sucesso!', 'success');
    }
    
    async executeAutomation(type) {
        if (!this.isAuthenticated) {
            this.showAlert('Faça login primeiro para usar as automações!', 'error');
            return;
        }
        
        if (this.automationRunning) {
            this.showAlert('Já existe uma automação em execução!', 'error');
            return;
        }
        
        const actionConfig = {
            'like': { name: 'Curtir Posts', count: 3, emoji: '👍', color: '#28a745' },
            'connect': { name: 'Enviar Conexões', count: 2, emoji: '🤝', color: '#007bff' },
            'comment': { name: 'Comentar Posts', count: 1, emoji: '💬', color: '#fd7e14' }
        };
        
        const config = actionConfig[type];
        if (!config) return;
        
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
                
                this.showAlert(
                    `${config.name} executada com sucesso! ${response.details.completed_count} ações realizadas.`,
                    'success'
                );
            } else {
                throw new Error(response.message);
            }
            
        } catch (error) {
            console.error(`Erro na automação ${type}:`, error);
            this.showAlert(`Erro na automação: ${error.message}`, 'error');
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
        }
        
        if (icon) icon.textContent = config.emoji;
        if (message) message.textContent = `${config.emoji} ${config.name}`;
        if (detail) detail.textContent = 'Iniciando automação...';
        
        // Simular progresso
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 100) progress = 100;
            
            if (progressBar) progressBar.style.width = progress + '%';
            if (progressText) progressText.textContent = Math.round(progress) + '% concluído';
            
            // Atualizar mensagens de progresso
            if (detail) {
                if (progress < 25) detail.textContent = 'Conectando ao LinkedIn...';
                else if (progress < 50) detail.textContent = 'Analisando conteúdo...';
                else if (progress < 75) detail.textContent = 'Executando ações...';
                else if (progress < 95) detail.textContent = 'Finalizando...';
                else detail.textContent = 'Concluído!';
            }
            
            if (progress >= 100) {
                clearInterval(interval);
            }
        }, 200);
        
        // Armazenar interval para limpeza
        this.progressInterval = interval;
    }
    
    hideAutomationOverlay() {
        const overlay = document.getElementById('automationOverlay');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        setTimeout(() => {
            if (overlay) overlay.style.display = 'none';
            if (progressBar) progressBar.style.width = '0%';
            if (progressText) progressText.textContent = '0% concluído';
        }, 2000);
    }
    
    async resetStats() {
        if (!this.isAuthenticated) {
            this.showAlert('Faça login primeiro!', 'error');
            return;
        }
        
        try {
            const response = await this.apiCall('/api/stats/reset', 'POST');
            if (response.success) {
                this.stats = response.stats || { total_likes: 0, total_connections: 0, total_comments: 0 };
                this.updateStats();
                this.showAlert('Estatísticas resetadas com sucesso!', 'success');
            }
        } catch (error) {
            console.error('Erro ao resetar estatísticas:', error);
            this.showAlert('Erro ao resetar estatísticas', 'error');
        }
    }
    
    openLinkedIn() {
        const iframe = document.getElementById('linkedinFrame');
        const placeholder = document.getElementById('iframePlaceholder');
        
        if (iframe && placeholder) {
            iframe.src = 'https://www.linkedin.com/feed/';
            placeholder.style.display = 'none';
            iframe.style.display = 'block';
        }
    }
    
    navigateBack() {
        const iframe = document.getElementById('linkedinFrame');
        if (iframe && iframe.contentWindow) {
            iframe.contentWindow.history.back();
        }
    }
    
    navigateForward() {
        const iframe = document.getElementById('linkedinFrame');
        if (iframe && iframe.contentWindow) {
            iframe.contentWindow.history.forward();
        }
    }
    
    refreshPage() {
        const iframe = document.getElementById('linkedinFrame');
        if (iframe && iframe.src) {
            iframe.src = iframe.src;
        }
    }
    
    updateUI() {
        this.updateAuthStatus();
        this.updateStats();
        this.updateAutomationButtons();
    }
    
    updateAuthStatus() {
        const statusEl = document.getElementById('connectionStatus');
        const authCard = document.querySelector('.auth-card');
        const userInfo = document.getElementById('userInfo');
        
        if (this.isAuthenticated && this.user) {
            if (statusEl) {
                statusEl.innerHTML = '🟢 Conectado';
                statusEl.classList.add('connected');
            }
            
            if (authCard) {
                authCard.innerHTML = `
                    <h4>👤 Perfil Conectado</h4>
                    <div class="user-info">
                        <div class="user-avatar">
                            ${this.user.avatar_url ? 
                                `<img src="${this.user.avatar_url}" alt="Avatar" style="width:100%;height:100%;border-radius:50%;">` :
                                this.user.name.charAt(0).toUpperCase()
                            }
                        </div>
                        <div class="user-details">
                            <h5>${this.user.name}</h5>
                            <p>${this.user.email}</p>
                        </div>
                    </div>
                    <button id="logoutBtn" class="btn btn-logout">
                        <span>🚪</span> Sair
                    </button>
                `;
                
                // Re-registrar event listener
                const logoutBtn = document.getElementById('logoutBtn');
                if (logoutBtn) {
                    logoutBtn.addEventListener('click', () => this.logout());
                }
            }
        } else {
            if (statusEl) {
                statusEl.innerHTML = '🔴 Desconectado';
                statusEl.classList.remove('connected');
            }
            
            if (authCard) {
                authCard.innerHTML = `
                    <h4>🔐 Conectar LinkedIn</h4>
                    <p>Escolha uma opção para conectar sua conta:</p>
                    <div style="display: flex; flex-direction: column; gap: 12px;">
                        <button id="oauthBtn" class="btn btn-oauth">
                            <span>🔗</span> OAuth LinkedIn
                        </button>
                        <button id="manualBtn" class="btn btn-manual">
                            <span>🖱️</span> Login Manual
                        </button>
                    </div>
                `;
                
                // Re-registrar event listeners
                const oauthBtn = document.getElementById('oauthBtn');
                const manualBtn = document.getElementById('manualBtn');
                
                if (oauthBtn) oauthBtn.addEventListener('click', () => this.startOAuthLogin());
                if (manualBtn) manualBtn.addEventListener('click', () => this.showManualLoginForm());
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
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 300);
    }
    
    updateAutomationButtons() {
        const buttons = ['likeBtn', 'connectBtn', 'commentBtn'];
        
        buttons.forEach(id => {
            const btn = document.getElementById(id);
            if (btn) {
                btn.disabled = !this.isAuthenticated || this.automationRunning;
            }
        });
    }
    
    async apiCall(endpoint, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (this.authToken) {
            options.headers['Authorization'] = `Bearer ${this.authToken}`;
        }
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(endpoint, options);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP ${response.status}`);
        }
        
        return await response.json();
    }
    
    showAlert(message, type = 'info') {
        // Remover alertas existentes
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());
        
        // Criar novo alerta
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} fade-in`;
        alert.textContent = message;
        
        // Inserir no topo da sidebar
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.insertBefore(alert, sidebar.firstChild);
            
            // Remover após 5 segundos
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 5000);
        }
    }
    
    showLoading(message = 'Carregando...') {
        const loadingEl = document.getElementById('loadingMessage');
        if (loadingEl) {
            loadingEl.textContent = message;
            loadingEl.style.display = 'block';
        }
    }
    
    hideLoading() {
        const loadingEl = document.getElementById('loadingMessage');
        if (loadingEl) {
            loadingEl.style.display = 'none';
        }
    }
    
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? 
            `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : 
            '0, 123, 255';
    }
}

// Inicializar aplicação quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.snapLinkedApp = new SnapLinkedApp();
});
