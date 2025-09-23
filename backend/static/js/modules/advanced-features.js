/**
 * SnapLinked v3.0 - Funcionalidades Avançadas
 * Dark mode, notificações, analytics, PWA e mais
 */

class AdvancedFeatures {
    constructor() {
        this.darkMode = false;
        this.notifications = {
            permission: 'default',
            enabled: false
        };
        this.analytics = {
            enabled: true,
            sessionId: this.generateSessionId(),
            events: []
        };
        this.pwa = {
            installed: false,
            installPrompt: null
        };
        this.performance = {
            startTime: performance.now(),
            metrics: {}
        };
        
        this.init();
    }
    
    init() {
        this.setupDarkMode();
        this.setupNotifications();
        this.setupAnalytics();
        this.setupPWA();
        this.setupPerformanceMonitoring();
        this.setupAdvancedUI();
        this.setupKeyboardShortcuts();
        this.setupOfflineSupport();
    }
    
    // ===== DARK MODE =====
    setupDarkMode() {
        // Verificar preferência salva
        const savedTheme = localStorage.getItem('snaplinked-theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        this.darkMode = savedTheme === 'dark' || (savedTheme === null && systemPrefersDark);
        this.applyDarkMode();
        
        // Monitorar mudanças do sistema
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('snaplinked-theme')) {
                this.darkMode = e.matches;
                this.applyDarkMode();
            }
        });
        
        this.createDarkModeToggle();
    }
    
    applyDarkMode() {
        document.body.classList.toggle('dark-mode', this.darkMode);
        
        // Atualizar meta theme-color
        const themeColorMeta = document.querySelector('meta[name="theme-color"]');
        if (themeColorMeta) {
            themeColorMeta.content = this.darkMode ? '#1a1a1a' : '#0077b5';
        }
        
        // Anunciar mudança
        if (window.accessibilityManager) {
            window.accessibilityManager.announce(
                `Modo ${this.darkMode ? 'escuro' : 'claro'} ativado`
            );
        }
    }
    
    createDarkModeToggle() {
        const toggle = document.createElement('button');
        toggle.id = 'dark-mode-toggle';
        toggle.className = 'dark-mode-toggle';
        toggle.innerHTML = this.darkMode ? '☀️' : '🌙';
        toggle.setAttribute('aria-label', `Alternar para modo ${this.darkMode ? 'claro' : 'escuro'}`);
        toggle.title = `Modo ${this.darkMode ? 'claro' : 'escuro'} (Ctrl+Shift+D)`;
        
        toggle.addEventListener('click', () => this.toggleDarkMode());
        
        // Adicionar ao header
        const headerButtons = document.querySelector('.header-buttons');
        if (headerButtons) {
            headerButtons.appendChild(toggle);
        }
        
        this.addDarkModeStyles();
    }
    
    toggleDarkMode() {
        this.darkMode = !this.darkMode;
        localStorage.setItem('snaplinked-theme', this.darkMode ? 'dark' : 'light');
        this.applyDarkMode();
        
        // Atualizar botão
        const toggle = document.getElementById('dark-mode-toggle');
        if (toggle) {
            toggle.innerHTML = this.darkMode ? '☀️' : '🌙';
            toggle.setAttribute('aria-label', `Alternar para modo ${this.darkMode ? 'claro' : 'escuro'}`);
        }
        
        // Analytics
        this.trackEvent('theme_changed', { theme: this.darkMode ? 'dark' : 'light' });
    }
    
    addDarkModeStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .dark-mode-toggle {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 8px 12px;
                border-radius: var(--border-radius);
                cursor: pointer;
                font-size: 1.2rem;
                transition: all var(--transition-base);
                backdrop-filter: blur(10px);
            }
            
            .dark-mode-toggle:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
            
            /* Dark mode styles */
            .dark-mode {
                --white: #1a1a1a;
                --gray-50: #2d2d2d;
                --gray-100: #3a3a3a;
                --gray-200: #4a4a4a;
                --gray-300: #5a5a5a;
                --gray-400: #6a6a6a;
                --gray-500: #8a8a8a;
                --gray-600: #a0a0a0;
                --gray-700: #c0c0c0;
                --gray-800: #e0e0e0;
                --gray-900: #ffffff;
            }
            
            .dark-mode .linkedin-frame {
                filter: invert(1) hue-rotate(180deg);
            }
            
            .dark-mode .iframe-placeholder {
                background: var(--gray-100);
                color: var(--gray-800);
            }
        `;
        document.head.appendChild(style);
    }
    
    // ===== NOTIFICAÇÕES =====
    async setupNotifications() {
        if ('Notification' in window) {
            this.notifications.permission = Notification.permission;
            
            if (this.notifications.permission === 'granted') {
                this.notifications.enabled = true;
            }
            
            this.createNotificationToggle();
        }
    }
    
    async requestNotificationPermission() {
        if ('Notification' in window) {
            const permission = await Notification.requestPermission();
            this.notifications.permission = permission;
            this.notifications.enabled = permission === 'granted';
            
            if (this.notifications.enabled) {
                this.showNotification('Notificações ativadas!', 'Você receberá notificações sobre suas automações.');
            }
            
            this.updateNotificationToggle();
            return permission === 'granted';
        }
        return false;
    }
    
    showNotification(title, body, options = {}) {
        if (!this.notifications.enabled) return;
        
        const defaultOptions = {
            body: body,
            icon: '/static/images/icon-192x192.png',
            badge: '/static/images/badge-72x72.png',
            tag: 'snaplinked-notification',
            requireInteraction: false,
            silent: false,
            ...options
        };
        
        const notification = new Notification(title, defaultOptions);
        
        notification.onclick = () => {
            window.focus();
            notification.close();
        };
        
        // Auto-close após 5 segundos
        setTimeout(() => notification.close(), 5000);
        
        return notification;
    }
    
    createNotificationToggle() {
        const toggle = document.createElement('button');
        toggle.id = 'notification-toggle';
        toggle.className = 'notification-toggle';
        toggle.innerHTML = this.notifications.enabled ? '🔔' : '🔕';
        toggle.setAttribute('aria-label', 'Alternar notificações');
        toggle.title = 'Notificações (Ctrl+Shift+N)';
        
        toggle.addEventListener('click', async () => {
            if (!this.notifications.enabled) {
                await this.requestNotificationPermission();
            } else {
                this.notifications.enabled = false;
                this.updateNotificationToggle();
            }
        });
        
        // Adicionar ao header
        const headerButtons = document.querySelector('.header-buttons');
        if (headerButtons) {
            headerButtons.appendChild(toggle);
        }
        
        this.addNotificationStyles();
    }
    
    updateNotificationToggle() {
        const toggle = document.getElementById('notification-toggle');
        if (toggle) {
            toggle.innerHTML = this.notifications.enabled ? '🔔' : '🔕';
            toggle.setAttribute('aria-label', 
                this.notifications.enabled ? 'Desativar notificações' : 'Ativar notificações'
            );
        }
    }
    
    addNotificationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .notification-toggle {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 8px 12px;
                border-radius: var(--border-radius);
                cursor: pointer;
                font-size: 1.2rem;
                transition: all var(--transition-base);
                backdrop-filter: blur(10px);
            }
            
            .notification-toggle:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
        `;
        document.head.appendChild(style);
    }
    
    // ===== ANALYTICS =====
    setupAnalytics() {
        this.trackEvent('app_loaded', {
            timestamp: new Date().toISOString(),
            user_agent: navigator.userAgent,
            screen_resolution: `${screen.width}x${screen.height}`,
            viewport: `${window.innerWidth}x${window.innerHeight}`
        });
        
        // Track page visibility
        document.addEventListener('visibilitychange', () => {
            this.trackEvent('page_visibility_changed', {
                hidden: document.hidden
            });
        });
        
        // Track errors
        window.addEventListener('error', (event) => {
            this.trackEvent('javascript_error', {
                message: event.message,
                filename: event.filename,
                line: event.lineno,
                column: event.colno
            });
        });
        
        // Track performance
        window.addEventListener('load', () => {
            setTimeout(() => this.trackPerformanceMetrics(), 1000);
        });
    }
    
    trackEvent(eventName, properties = {}) {
        const event = {
            name: eventName,
            properties: {
                ...properties,
                session_id: this.analytics.sessionId,
                timestamp: new Date().toISOString(),
                url: window.location.href
            }
        };
        
        this.analytics.events.push(event);
        
        // Enviar para servidor (implementar endpoint)
        if (this.analytics.enabled) {
            this.sendAnalytics(event);
        }
        
        console.log('📊 Analytics:', event);
    }
    
    async sendAnalytics(event) {
        try {
            // Implementar envio para servidor de analytics
            // await fetch('/api/analytics', {
            //     method: 'POST',
            //     headers: { 'Content-Type': 'application/json' },
            //     body: JSON.stringify(event)
            // });
        } catch (error) {
            console.error('Erro ao enviar analytics:', error);
        }
    }
    
    trackPerformanceMetrics() {
        if ('performance' in window) {
            const navigation = performance.getEntriesByType('navigation')[0];
            const paint = performance.getEntriesByType('paint');
            
            this.performance.metrics = {
                page_load_time: navigation.loadEventEnd - navigation.loadEventStart,
                dom_content_loaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                first_paint: paint.find(p => p.name === 'first-paint')?.startTime,
                first_contentful_paint: paint.find(p => p.name === 'first-contentful-paint')?.startTime,
                total_load_time: performance.now() - this.performance.startTime
            };
            
            this.trackEvent('performance_metrics', this.performance.metrics);
        }
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    // ===== PWA =====
    setupPWA() {
        // Detectar se já está instalado
        if (window.matchMedia('(display-mode: standalone)').matches) {
            this.pwa.installed = true;
        }
        
        // Capturar prompt de instalação
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.pwa.installPrompt = e;
            this.showInstallButton();
        });
        
        // Detectar instalação
        window.addEventListener('appinstalled', () => {
            this.pwa.installed = true;
            this.hideInstallButton();
            this.trackEvent('pwa_installed');
            
            if (this.notifications.enabled) {
                this.showNotification('SnapLinked instalado!', 'O app foi instalado com sucesso.');
            }
        });
        
        // Registrar Service Worker
        this.registerServiceWorker();
    }
    
    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/static/sw.js');
                console.log('✅ Service Worker registrado:', registration);
                
                // Verificar atualizações
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            this.showUpdateNotification();
                        }
                    });
                });
                
                this.trackEvent('service_worker_registered');
            } catch (error) {
                console.error('❌ Erro ao registrar Service Worker:', error);
                this.trackEvent('service_worker_error', { error: error.message });
            }
        }
    }
    
    showInstallButton() {
        if (this.pwa.installed) return;
        
        const installBtn = document.createElement('button');
        installBtn.id = 'pwa-install-btn';
        installBtn.className = 'pwa-install-btn';
        installBtn.innerHTML = '📱 Instalar App';
        installBtn.title = 'Instalar SnapLinked como app';
        
        installBtn.addEventListener('click', () => this.installPWA());
        
        // Adicionar ao header
        const headerButtons = document.querySelector('.header-buttons');
        if (headerButtons) {
            headerButtons.appendChild(installBtn);
        }
        
        this.addPWAStyles();
    }
    
    hideInstallButton() {
        const installBtn = document.getElementById('pwa-install-btn');
        if (installBtn) {
            installBtn.remove();
        }
    }
    
    async installPWA() {
        if (!this.pwa.installPrompt) return;
        
        try {
            const result = await this.pwa.installPrompt.prompt();
            this.trackEvent('pwa_install_prompted', { outcome: result.outcome });
            
            if (result.outcome === 'accepted') {
                this.pwa.installPrompt = null;
            }
        } catch (error) {
            console.error('Erro na instalação PWA:', error);
        }
    }
    
    showUpdateNotification() {
        const notification = document.createElement('div');
        notification.className = 'update-notification';
        notification.innerHTML = `
            <div class="update-content">
                <span>🔄 Nova versão disponível!</span>
                <button onclick="window.location.reload()">Atualizar</button>
                <button onclick="this.parentElement.parentElement.remove()">Depois</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 10000);
    }
    
    addPWAStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .pwa-install-btn {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 8px 12px;
                border-radius: var(--border-radius);
                cursor: pointer;
                font-size: 0.875rem;
                transition: all var(--transition-base);
                backdrop-filter: blur(10px);
            }
            
            .pwa-install-btn:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
            
            .update-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--primary-color);
                color: white;
                padding: 1rem;
                border-radius: var(--border-radius-lg);
                box-shadow: var(--shadow-xl);
                z-index: 10000;
                animation: slideIn 0.3s ease-out;
            }
            
            .update-content {
                display: flex;
                align-items: center;
                gap: 1rem;
            }
            
            .update-content button {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: var(--border-radius);
                cursor: pointer;
                font-size: 0.875rem;
            }
            
            @keyframes slideIn {
                from { transform: translateX(100%); }
                to { transform: translateX(0); }
            }
        `;
        document.head.appendChild(style);
    }
    
    // ===== MONITORAMENTO DE PERFORMANCE =====
    setupPerformanceMonitoring() {
        // Monitor de FPS
        this.setupFPSMonitor();
        
        // Monitor de memória
        this.setupMemoryMonitor();
        
        // Monitor de rede
        this.setupNetworkMonitor();
    }
    
    setupFPSMonitor() {
        let lastTime = performance.now();
        let frameCount = 0;
        let fps = 0;
        
        const measureFPS = (currentTime) => {
            frameCount++;
            
            if (currentTime - lastTime >= 1000) {
                fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
                frameCount = 0;
                lastTime = currentTime;
                
                // Log FPS baixo
                if (fps < 30) {
                    this.trackEvent('low_fps_detected', { fps });
                }
            }
            
            requestAnimationFrame(measureFPS);
        };
        
        requestAnimationFrame(measureFPS);
    }
    
    setupMemoryMonitor() {
        if ('memory' in performance) {
            setInterval(() => {
                const memory = performance.memory;
                const memoryUsage = {
                    used: Math.round(memory.usedJSHeapSize / 1048576), // MB
                    total: Math.round(memory.totalJSHeapSize / 1048576), // MB
                    limit: Math.round(memory.jsHeapSizeLimit / 1048576) // MB
                };
                
                // Log uso alto de memória
                if (memoryUsage.used > 100) {
                    this.trackEvent('high_memory_usage', memoryUsage);
                }
            }, 30000); // A cada 30 segundos
        }
    }
    
    setupNetworkMonitor() {
        if ('connection' in navigator) {
            const connection = navigator.connection;
            
            const logConnection = () => {
                this.trackEvent('network_info', {
                    effective_type: connection.effectiveType,
                    downlink: connection.downlink,
                    rtt: connection.rtt,
                    save_data: connection.saveData
                });
            };
            
            connection.addEventListener('change', logConnection);
            logConnection(); // Log inicial
        }
    }
    
    // ===== ATALHOS DE TECLADO AVANÇADOS =====
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Shift + combinações
            if ((e.ctrlKey || e.metaKey) && e.shiftKey) {
                switch (e.key) {
                    case 'D':
                        e.preventDefault();
                        this.toggleDarkMode();
                        break;
                        
                    case 'N':
                        e.preventDefault();
                        this.requestNotificationPermission();
                        break;
                        
                    case 'I':
                        e.preventDefault();
                        if (this.pwa.installPrompt) {
                            this.installPWA();
                        }
                        break;
                        
                    case 'F':
                        e.preventDefault();
                        this.toggleFullscreen();
                        break;
                        
                    case 'S':
                        e.preventDefault();
                        this.exportStats();
                        break;
                }
            }
            
            // Teclas de função
            switch (e.key) {
                case 'F11':
                    e.preventDefault();
                    this.toggleFullscreen();
                    break;
            }
        });
    }
    
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.error('Erro ao entrar em tela cheia:', err);
            });
        } else {
            document.exitFullscreen();
        }
    }
    
    // ===== SUPORTE OFFLINE =====
    setupOfflineSupport() {
        // Detectar status de conexão
        window.addEventListener('online', () => {
            this.handleConnectionChange(true);
        });
        
        window.addEventListener('offline', () => {
            this.handleConnectionChange(false);
        });
        
        // Status inicial
        this.handleConnectionChange(navigator.onLine);
    }
    
    handleConnectionChange(isOnline) {
        const statusIndicator = this.createConnectionIndicator();
        
        if (isOnline) {
            statusIndicator.textContent = '🟢 Online';
            statusIndicator.className = 'connection-status online';
            
            if (this.notifications.enabled) {
                this.showNotification('Conexão restaurada', 'Você está online novamente.');
            }
        } else {
            statusIndicator.textContent = '🔴 Offline';
            statusIndicator.className = 'connection-status offline';
            
            // Mostrar banner offline
            this.showOfflineBanner();
        }
        
        this.trackEvent('connection_changed', { online: isOnline });
    }
    
    createConnectionIndicator() {
        let indicator = document.getElementById('connection-indicator');
        
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'connection-indicator';
            indicator.className = 'connection-status';
            
            // Adicionar ao header
            const header = document.querySelector('.header');
            if (header) {
                header.appendChild(indicator);
            }
            
            this.addConnectionStyles();
        }
        
        return indicator;
    }
    
    showOfflineBanner() {
        const banner = document.createElement('div');
        banner.className = 'offline-banner';
        banner.innerHTML = `
            <div class="offline-content">
                <span>📡 Você está offline</span>
                <span>Algumas funcionalidades podem não estar disponíveis</span>
                <button onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;
        
        document.body.insertBefore(banner, document.body.firstChild);
        
        // Auto-remove quando voltar online
        const removeOnOnline = () => {
            if (navigator.onLine && banner.parentElement) {
                banner.remove();
                window.removeEventListener('online', removeOnOnline);
            }
        };
        
        window.addEventListener('online', removeOnOnline);
    }
    
    addConnectionStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .connection-status {
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 0.5rem 1rem;
                border-radius: var(--border-radius-full);
                font-size: 0.875rem;
                font-weight: 600;
                z-index: 1000;
                transition: all var(--transition-base);
            }
            
            .connection-status.online {
                background: var(--success-color);
                color: white;
            }
            
            .connection-status.offline {
                background: var(--error-color);
                color: white;
            }
            
            .offline-banner {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: var(--warning-color);
                color: white;
                z-index: 10000;
                animation: slideDown 0.3s ease-out;
            }
            
            .offline-content {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 1rem;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .offline-content button {
                background: none;
                border: none;
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            @keyframes slideDown {
                from { transform: translateY(-100%); }
                to { transform: translateY(0); }
            }
        `;
        document.head.appendChild(style);
    }
    
    // ===== UI AVANÇADA =====
    setupAdvancedUI() {
        this.createFloatingActionButton();
        this.setupTooltips();
        this.setupContextMenu();
    }
    
    createFloatingActionButton() {
        const fab = document.createElement('div');
        fab.className = 'floating-action-button';
        fab.innerHTML = `
            <button class="fab-main" aria-label="Menu de ações rápidas">
                ⚡
            </button>
            <div class="fab-menu">
                <button class="fab-item" data-action="like" title="Curtir posts (Ctrl+L)">👍</button>
                <button class="fab-item" data-action="connect" title="Enviar conexões (Ctrl+K)">🤝</button>
                <button class="fab-item" data-action="comment" title="Comentar posts (Ctrl+J)">💬</button>
                <button class="fab-item" data-action="stats" title="Ver estatísticas">📊</button>
            </div>
        `;
        
        document.body.appendChild(fab);
        
        // Toggle menu
        const fabMain = fab.querySelector('.fab-main');
        const fabMenu = fab.querySelector('.fab-menu');
        
        fabMain.addEventListener('click', () => {
            fab.classList.toggle('open');
        });
        
        // Ações dos itens
        fab.addEventListener('click', (e) => {
            const action = e.target.dataset.action;
            if (action && window.snapLinkedApp) {
                switch (action) {
                    case 'like':
                    case 'connect':
                    case 'comment':
                        window.snapLinkedApp.executeAutomation(action);
                        break;
                    case 'stats':
                        this.showStatsModal();
                        break;
                }
                fab.classList.remove('open');
            }
        });
        
        this.addFABStyles();
    }
    
    addFABStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .floating-action-button {
                position: fixed;
                bottom: 80px;
                right: 20px;
                z-index: 1000;
            }
            
            .fab-main {
                width: 56px;
                height: 56px;
                border-radius: 50%;
                background: var(--primary-color);
                color: white;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                box-shadow: var(--shadow-lg);
                transition: all var(--transition-base);
            }
            
            .fab-main:hover {
                transform: scale(1.1);
                box-shadow: var(--shadow-xl);
            }
            
            .fab-menu {
                position: absolute;
                bottom: 70px;
                right: 0;
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
                opacity: 0;
                transform: scale(0);
                transition: all var(--transition-base);
                transform-origin: bottom right;
            }
            
            .floating-action-button.open .fab-menu {
                opacity: 1;
                transform: scale(1);
            }
            
            .fab-item {
                width: 48px;
                height: 48px;
                border-radius: 50%;
                background: var(--white);
                border: 1px solid var(--gray-300);
                font-size: 1.2rem;
                cursor: pointer;
                box-shadow: var(--shadow-md);
                transition: all var(--transition-base);
            }
            
            .fab-item:hover {
                transform: scale(1.1);
                box-shadow: var(--shadow-lg);
            }
            
            @media (max-width: 768px) {
                .floating-action-button {
                    bottom: 20px;
                    right: 20px;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    setupTooltips() {
        // Implementar tooltips avançados
        document.addEventListener('mouseover', (e) => {
            if (e.target.hasAttribute('title') && !e.target.hasAttribute('data-tooltip-shown')) {
                this.showTooltip(e.target);
            }
        });
    }
    
    showTooltip(element) {
        const tooltip = document.createElement('div');
        tooltip.className = 'advanced-tooltip';
        tooltip.textContent = element.title;
        
        document.body.appendChild(tooltip);
        
        // Posicionar tooltip
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
        
        // Remover após 3 segundos
        setTimeout(() => {
            if (tooltip.parentElement) {
                tooltip.remove();
            }
        }, 3000);
        
        element.setAttribute('data-tooltip-shown', 'true');
        setTimeout(() => element.removeAttribute('data-tooltip-shown'), 3000);
    }
    
    setupContextMenu() {
        // Menu de contexto personalizado
        document.addEventListener('contextmenu', (e) => {
            if (e.target.closest('.automation-buttons')) {
                e.preventDefault();
                this.showContextMenu(e);
            }
        });
    }
    
    showContextMenu(event) {
        const menu = document.createElement('div');
        menu.className = 'context-menu';
        menu.innerHTML = `
            <div class="context-item" data-action="export-stats">📊 Exportar Estatísticas</div>
            <div class="context-item" data-action="reset-stats">🔄 Resetar Estatísticas</div>
            <div class="context-item" data-action="automation-help">❓ Ajuda</div>
        `;
        
        document.body.appendChild(menu);
        
        menu.style.left = event.pageX + 'px';
        menu.style.top = event.pageY + 'px';
        
        // Fechar ao clicar fora
        const closeMenu = (e) => {
            if (!menu.contains(e.target)) {
                menu.remove();
                document.removeEventListener('click', closeMenu);
            }
        };
        
        setTimeout(() => document.addEventListener('click', closeMenu), 100);
        
        // Ações do menu
        menu.addEventListener('click', (e) => {
            const action = e.target.dataset.action;
            if (action) {
                switch (action) {
                    case 'export-stats':
                        this.exportStats();
                        break;
                    case 'reset-stats':
                        if (window.snapLinkedApp) {
                            window.snapLinkedApp.resetStats();
                        }
                        break;
                    case 'automation-help':
                        this.showHelpModal();
                        break;
                }
                menu.remove();
            }
        });
    }
    
    // ===== MÉTODOS UTILITÁRIOS =====
    
    exportStats() {
        if (window.snapLinkedApp) {
            const stats = {
                ...window.snapLinkedApp.stats,
                exported_at: new Date().toISOString(),
                session_id: this.analytics.sessionId
            };
            
            const blob = new Blob([JSON.stringify(stats, null, 2)], {
                type: 'application/json'
            });
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `snaplinked-stats-${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            
            URL.revokeObjectURL(url);
            
            this.trackEvent('stats_exported');
        }
    }
    
    showStatsModal() {
        // Implementar modal de estatísticas detalhadas
        console.log('Mostrar modal de estatísticas');
    }
    
    showHelpModal() {
        // Implementar modal de ajuda
        console.log('Mostrar modal de ajuda');
    }
    
    // Métodos públicos para integração
    
    notifyAutomationComplete(type, result) {
        if (this.notifications.enabled) {
            const messages = {
                like: 'Curtidas realizadas com sucesso!',
                connect: 'Conexões enviadas com sucesso!',
                comment: 'Comentários realizados com sucesso!'
            };
            
            this.showNotification(
                'Automação Concluída',
                messages[type] || 'Automação concluída',
                { tag: `automation-${type}` }
            );
        }
        
        this.trackEvent('automation_completed', {
            type,
            success: result.success,
            count: result.count
        });
    }
    
    trackUserAction(action, details = {}) {
        this.trackEvent('user_action', {
            action,
            ...details
        });
    }
}

// Exportar para uso global
window.AdvancedFeatures = AdvancedFeatures;
