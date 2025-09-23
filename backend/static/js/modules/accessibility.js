/**
 * SnapLinked v3.0 - Módulo de Acessibilidade
 * Funcionalidades avançadas de acessibilidade e inclusão
 */

class AccessibilityManager {
    constructor() {
        this.isHighContrast = false;
        this.isReducedMotion = false;
        this.fontSize = 'normal';
        this.focusVisible = true;
        this.screenReaderAnnouncements = [];
        
        this.init();
    }
    
    init() {
        this.detectPreferences();
        this.setupKeyboardNavigation();
        this.setupScreenReaderSupport();
        this.setupFocusManagement();
        this.setupColorContrastToggle();
        this.setupMotionControls();
        this.setupFontSizeControls();
        this.createAccessibilityPanel();
    }
    
    // Detectar preferências do sistema
    detectPreferences() {
        // Detectar preferência por movimento reduzido
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.isReducedMotion = true;
            document.body.classList.add('reduced-motion');
        }
        
        // Detectar preferência por alto contraste
        if (window.matchMedia('(prefers-contrast: high)').matches) {
            this.isHighContrast = true;
            document.body.classList.add('high-contrast');
        }
        
        // Detectar preferência por esquema de cores
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.body.classList.add('dark-mode');
        }
        
        // Monitorar mudanças
        window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
            this.isReducedMotion = e.matches;
            document.body.classList.toggle('reduced-motion', e.matches);
        });
        
        window.matchMedia('(prefers-contrast: high)').addEventListener('change', (e) => {
            this.isHighContrast = e.matches;
            document.body.classList.toggle('high-contrast', e.matches);
        });
        
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            document.body.classList.toggle('dark-mode', e.matches);
        });
    }
    
    // Configurar navegação por teclado
    setupKeyboardNavigation() {
        // Trap focus em modais
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                const modal = document.querySelector('[role="dialog"][aria-modal="true"]');
                if (modal && modal.style.display !== 'none') {
                    this.trapFocus(e, modal);
                }
            }
            
            // Esc para fechar modais
            if (e.key === 'Escape') {
                const modal = document.querySelector('[role="dialog"][aria-modal="true"]');
                if (modal && modal.style.display !== 'none') {
                    this.closeModal(modal);
                }
            }
        });
        
        // Navegação por setas em grupos de botões
        document.addEventListener('keydown', (e) => {
            if (e.target.closest('[role="group"]')) {
                this.handleArrowNavigation(e);
            }
        });
        
        // Skip links
        this.createSkipLinks();
    }
    
    // Trap focus dentro de um elemento
    trapFocus(event, element) {
        const focusableElements = element.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        if (event.shiftKey && document.activeElement === firstElement) {
            event.preventDefault();
            lastElement.focus();
        } else if (!event.shiftKey && document.activeElement === lastElement) {
            event.preventDefault();
            firstElement.focus();
        }
    }
    
    // Navegação por setas
    handleArrowNavigation(event) {
        const group = event.target.closest('[role="group"]');
        const items = Array.from(group.querySelectorAll('button, [role="button"]'));
        const currentIndex = items.indexOf(event.target);
        
        let nextIndex;
        
        switch (event.key) {
            case 'ArrowDown':
            case 'ArrowRight':
                event.preventDefault();
                nextIndex = (currentIndex + 1) % items.length;
                items[nextIndex].focus();
                break;
                
            case 'ArrowUp':
            case 'ArrowLeft':
                event.preventDefault();
                nextIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
                items[nextIndex].focus();
                break;
                
            case 'Home':
                event.preventDefault();
                items[0].focus();
                break;
                
            case 'End':
                event.preventDefault();
                items[items.length - 1].focus();
                break;
        }
    }
    
    // Criar skip links
    createSkipLinks() {
        const skipLinks = document.createElement('div');
        skipLinks.className = 'skip-links';
        skipLinks.innerHTML = `
            <a href="#main-content" class="skip-link">Pular para o conteúdo principal</a>
            <a href="#sidebar" class="skip-link">Pular para o painel de controle</a>
            <a href="#automation-buttons" class="skip-link">Pular para os botões de automação</a>
        `;
        
        document.body.insertBefore(skipLinks, document.body.firstChild);
        
        // Estilos para skip links
        const style = document.createElement('style');
        style.textContent = `
            .skip-links {
                position: absolute;
                top: -100px;
                left: 0;
                z-index: 10000;
            }
            
            .skip-link {
                position: absolute;
                top: -100px;
                left: 0;
                background: var(--primary-color);
                color: white;
                padding: 8px 16px;
                text-decoration: none;
                border-radius: 0 0 4px 0;
                font-weight: 600;
                transition: top 0.3s ease;
            }
            
            .skip-link:focus {
                top: 0;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Configurar suporte a leitores de tela
    setupScreenReaderSupport() {
        // Criar região para anúncios
        this.createAnnouncementRegion();
        
        // Anunciar mudanças de estado
        this.observeStateChanges();
        
        // Melhorar labels e descrições
        this.enhanceLabels();
    }
    
    // Criar região para anúncios de leitores de tela
    createAnnouncementRegion() {
        const announcer = document.createElement('div');
        announcer.id = 'screen-reader-announcements';
        announcer.setAttribute('aria-live', 'polite');
        announcer.setAttribute('aria-atomic', 'true');
        announcer.className = 'sr-only';
        document.body.appendChild(announcer);
    }
    
    // Anunciar mensagem para leitores de tela
    announce(message, priority = 'polite') {
        const announcer = document.getElementById('screen-reader-announcements');
        if (announcer) {
            announcer.setAttribute('aria-live', priority);
            announcer.textContent = message;
            
            // Limpar após 1 segundo
            setTimeout(() => {
                announcer.textContent = '';
            }, 1000);
        }
    }
    
    // Observar mudanças de estado
    observeStateChanges() {
        // Observer para mudanças no DOM
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes') {
                    this.handleAttributeChange(mutation);
                } else if (mutation.type === 'childList') {
                    this.handleContentChange(mutation);
                }
            });
        });
        
        observer.observe(document.body, {
            attributes: true,
            childList: true,
            subtree: true,
            attributeFilter: ['aria-expanded', 'aria-selected', 'aria-checked', 'disabled']
        });
    }
    
    // Lidar com mudanças de atributos
    handleAttributeChange(mutation) {
        const element = mutation.target;
        const attributeName = mutation.attributeName;
        
        switch (attributeName) {
            case 'aria-expanded':
                const isExpanded = element.getAttribute('aria-expanded') === 'true';
                this.announce(`${element.textContent} ${isExpanded ? 'expandido' : 'recolhido'}`);
                break;
                
            case 'disabled':
                const isDisabled = element.hasAttribute('disabled');
                if (isDisabled) {
                    this.announce(`${element.textContent} desabilitado`);
                } else {
                    this.announce(`${element.textContent} habilitado`);
                }
                break;
        }
    }
    
    // Lidar com mudanças de conteúdo
    handleContentChange(mutation) {
        // Anunciar novos alertas
        mutation.addedNodes.forEach((node) => {
            if (node.nodeType === Node.ELEMENT_NODE && node.classList.contains('alert')) {
                this.announce(node.textContent, 'assertive');
            }
        });
    }
    
    // Melhorar labels e descrições
    enhanceLabels() {
        // Adicionar descrições para botões de automação
        const automationButtons = document.querySelectorAll('.btn-automation');
        automationButtons.forEach((button, index) => {
            if (!button.getAttribute('aria-describedby')) {
                const descId = `automation-desc-${index}`;
                const description = document.createElement('div');
                description.id = descId;
                description.className = 'sr-only';
                
                if (button.classList.contains('btn-like')) {
                    description.textContent = 'Automaticamente curte 3 posts no seu feed do LinkedIn';
                } else if (button.classList.contains('btn-connect-action')) {
                    description.textContent = 'Automaticamente envia 2 solicitações de conexão';
                } else if (button.classList.contains('btn-comment')) {
                    description.textContent = 'Automaticamente comenta em 1 post relevante';
                }
                
                button.setAttribute('aria-describedby', descId);
                button.parentNode.appendChild(description);
            }
        });
    }
    
    // Configurar gerenciamento de foco
    setupFocusManagement() {
        // Indicador visual de foco
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });
        
        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
        
        // Restaurar foco após ações
        this.setupFocusRestoration();
    }
    
    // Configurar restauração de foco
    setupFocusRestoration() {
        let lastFocusedElement = null;
        
        // Salvar foco antes de abrir modal
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-opens-modal]')) {
                lastFocusedElement = e.target;
            }
        });
        
        // Restaurar foco ao fechar modal
        window.addEventListener('modalClosed', () => {
            if (lastFocusedElement) {
                lastFocusedElement.focus();
                lastFocusedElement = null;
            }
        });
    }
    
    // Fechar modal
    closeModal(modal) {
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
        
        // Disparar evento personalizado
        window.dispatchEvent(new CustomEvent('modalClosed'));
        
        this.announce('Modal fechado');
    }
    
    // Toggle de alto contraste
    setupColorContrastToggle() {
        const toggleButton = document.createElement('button');
        toggleButton.id = 'contrast-toggle';
        toggleButton.className = 'accessibility-toggle';
        toggleButton.innerHTML = '🎨 Alto Contraste';
        toggleButton.setAttribute('aria-pressed', this.isHighContrast);
        
        toggleButton.addEventListener('click', () => {
            this.isHighContrast = !this.isHighContrast;
            document.body.classList.toggle('high-contrast', this.isHighContrast);
            toggleButton.setAttribute('aria-pressed', this.isHighContrast);
            
            this.announce(`Alto contraste ${this.isHighContrast ? 'ativado' : 'desativado'}`);
        });
        
        return toggleButton;
    }
    
    // Controles de movimento
    setupMotionControls() {
        const toggleButton = document.createElement('button');
        toggleButton.id = 'motion-toggle';
        toggleButton.className = 'accessibility-toggle';
        toggleButton.innerHTML = '🎭 Reduzir Movimento';
        toggleButton.setAttribute('aria-pressed', this.isReducedMotion);
        
        toggleButton.addEventListener('click', () => {
            this.isReducedMotion = !this.isReducedMotion;
            document.body.classList.toggle('reduced-motion', this.isReducedMotion);
            toggleButton.setAttribute('aria-pressed', this.isReducedMotion);
            
            this.announce(`Movimento ${this.isReducedMotion ? 'reduzido' : 'normal'}`);
        });
        
        return toggleButton;
    }
    
    // Controles de tamanho da fonte
    setupFontSizeControls() {
        const container = document.createElement('div');
        container.className = 'font-size-controls';
        
        const decreaseBtn = document.createElement('button');
        decreaseBtn.innerHTML = '🔤 A-';
        decreaseBtn.className = 'accessibility-toggle';
        decreaseBtn.setAttribute('aria-label', 'Diminuir tamanho da fonte');
        
        const increaseBtn = document.createElement('button');
        increaseBtn.innerHTML = '🔤 A+';
        increaseBtn.className = 'accessibility-toggle';
        increaseBtn.setAttribute('aria-label', 'Aumentar tamanho da fonte');
        
        const resetBtn = document.createElement('button');
        resetBtn.innerHTML = '🔤 A';
        resetBtn.className = 'accessibility-toggle';
        resetBtn.setAttribute('aria-label', 'Resetar tamanho da fonte');
        
        decreaseBtn.addEventListener('click', () => this.changeFontSize('decrease'));
        increaseBtn.addEventListener('click', () => this.changeFontSize('increase'));
        resetBtn.addEventListener('click', () => this.changeFontSize('reset'));
        
        container.appendChild(decreaseBtn);
        container.appendChild(resetBtn);
        container.appendChild(increaseBtn);
        
        return container;
    }
    
    // Alterar tamanho da fonte
    changeFontSize(action) {
        const root = document.documentElement;
        let currentSize = parseFloat(getComputedStyle(root).fontSize);
        
        switch (action) {
            case 'increase':
                if (currentSize < 24) {
                    root.style.fontSize = (currentSize + 2) + 'px';
                    this.fontSize = 'large';
                    this.announce('Fonte aumentada');
                }
                break;
                
            case 'decrease':
                if (currentSize > 12) {
                    root.style.fontSize = (currentSize - 2) + 'px';
                    this.fontSize = 'small';
                    this.announce('Fonte diminuída');
                }
                break;
                
            case 'reset':
                root.style.fontSize = '';
                this.fontSize = 'normal';
                this.announce('Fonte resetada');
                break;
        }
    }
    
    // Criar painel de acessibilidade
    createAccessibilityPanel() {
        const panel = document.createElement('div');
        panel.id = 'accessibility-panel';
        panel.className = 'accessibility-panel';
        panel.setAttribute('role', 'region');
        panel.setAttribute('aria-label', 'Opções de acessibilidade');
        
        const header = document.createElement('h3');
        header.textContent = '♿ Acessibilidade';
        header.style.margin = '0 0 1rem 0';
        
        const toggleButton = document.createElement('button');
        toggleButton.id = 'accessibility-toggle';
        toggleButton.className = 'accessibility-panel-toggle';
        toggleButton.innerHTML = '♿';
        toggleButton.setAttribute('aria-label', 'Abrir painel de acessibilidade');
        toggleButton.setAttribute('aria-expanded', 'false');
        
        const content = document.createElement('div');
        content.className = 'accessibility-panel-content';
        content.style.display = 'none';
        
        content.appendChild(header);
        content.appendChild(this.setupColorContrastToggle());
        content.appendChild(this.setupMotionControls());
        content.appendChild(this.setupFontSizeControls());
        
        panel.appendChild(toggleButton);
        panel.appendChild(content);
        
        // Toggle panel
        toggleButton.addEventListener('click', () => {
            const isOpen = content.style.display !== 'none';
            content.style.display = isOpen ? 'none' : 'block';
            toggleButton.setAttribute('aria-expanded', !isOpen);
            
            if (!isOpen) {
                this.announce('Painel de acessibilidade aberto');
            } else {
                this.announce('Painel de acessibilidade fechado');
            }
        });
        
        // Estilos
        this.addAccessibilityStyles();
        
        // Adicionar ao DOM
        document.body.appendChild(panel);
    }
    
    // Adicionar estilos de acessibilidade
    addAccessibilityStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .accessibility-panel {
                position: fixed;
                top: 50%;
                right: 20px;
                transform: translateY(-50%);
                z-index: 10000;
                font-family: var(--font-family);
            }
            
            .accessibility-panel-toggle {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: var(--primary-color);
                color: white;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                box-shadow: var(--shadow-lg);
                transition: all var(--transition-base);
            }
            
            .accessibility-panel-toggle:hover {
                transform: scale(1.1);
                box-shadow: var(--shadow-xl);
            }
            
            .accessibility-panel-content {
                position: absolute;
                right: 60px;
                top: 0;
                background: white;
                border: 1px solid var(--gray-300);
                border-radius: var(--border-radius-lg);
                padding: 1rem;
                box-shadow: var(--shadow-xl);
                min-width: 250px;
                max-width: 300px;
            }
            
            .accessibility-toggle {
                display: block;
                width: 100%;
                margin-bottom: 0.5rem;
                padding: 0.5rem;
                border: 1px solid var(--gray-300);
                border-radius: var(--border-radius);
                background: white;
                cursor: pointer;
                font-size: 0.875rem;
                transition: all var(--transition-fast);
            }
            
            .accessibility-toggle:hover {
                background: var(--gray-100);
            }
            
            .accessibility-toggle[aria-pressed="true"] {
                background: var(--primary-color);
                color: white;
                border-color: var(--primary-color);
            }
            
            .font-size-controls {
                display: flex;
                gap: 0.25rem;
            }
            
            .font-size-controls .accessibility-toggle {
                flex: 1;
                margin-bottom: 0;
            }
            
            /* Estilos para alto contraste */
            .high-contrast {
                filter: contrast(150%);
            }
            
            .high-contrast .btn,
            .high-contrast .form-input {
                border: 2px solid currentColor !important;
            }
            
            /* Estilos para movimento reduzido */
            .reduced-motion *,
            .reduced-motion *::before,
            .reduced-motion *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
            
            /* Indicador de navegação por teclado */
            .keyboard-navigation *:focus {
                outline: 3px solid var(--primary-color) !important;
                outline-offset: 2px !important;
            }
            
            @media (max-width: 768px) {
                .accessibility-panel {
                    right: 10px;
                }
                
                .accessibility-panel-content {
                    right: 60px;
                    max-width: calc(100vw - 80px);
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Métodos públicos para integração
    
    // Anunciar ação de automação
    announceAutomation(type, status) {
        const messages = {
            like: {
                start: 'Iniciando automação de curtidas',
                success: 'Automação de curtidas concluída com sucesso',
                error: 'Erro na automação de curtidas'
            },
            connect: {
                start: 'Iniciando envio de conexões',
                success: 'Conexões enviadas com sucesso',
                error: 'Erro no envio de conexões'
            },
            comment: {
                start: 'Iniciando automação de comentários',
                success: 'Comentários realizados com sucesso',
                error: 'Erro na automação de comentários'
            }
        };
        
        const message = messages[type]?.[status];
        if (message) {
            this.announce(message, status === 'error' ? 'assertive' : 'polite');
        }
    }
    
    // Anunciar mudança de estatísticas
    announceStatsUpdate(stats) {
        const message = `Estatísticas atualizadas: ${stats.total_likes} curtidas, ${stats.total_connections} conexões, ${stats.total_comments} comentários`;
        this.announce(message);
    }
    
    // Anunciar mudança de status de conexão
    announceConnectionStatus(isConnected) {
        const message = isConnected ? 'Conectado ao LinkedIn' : 'Desconectado do LinkedIn';
        this.announce(message, 'assertive');
    }
}

// Exportar para uso global
window.AccessibilityManager = AccessibilityManager;
