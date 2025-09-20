/**
 * SnapLinked - Scripts de Automação LinkedIn
 * 
 * Scripts JavaScript para execução no console do navegador (F12)
 * que automatizam ações no LinkedIn de forma segura e eficiente.
 * 
 * IMPORTANTE: Execute estes scripts diretamente no console do LinkedIn
 * após fazer login em sua conta.
 */

class LinkedInAutomation {
  constructor() {
    this.isRunning = false;
    this.stats = {
      connectionsRequested: 0,
      messagesSent: 0,
      profilesViewed: 0,
      errors: 0
    };
    this.config = {
      delayMin: 2000,  // Delay mínimo entre ações (2s)
      delayMax: 5000,  // Delay máximo entre ações (5s)
      dailyConnectionLimit: 50,
      dailyMessageLimit: 25,
      maxErrorsBeforeStop: 5
    };
  }

  /**
   * Gera delay aleatório para simular comportamento humano
   */
  randomDelay(min = this.config.delayMin, max = this.config.delayMax) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  /**
   * Aguarda um tempo específico
   */
  async wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Log das ações com timestamp
   */
  log(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString('pt-BR');
    const prefix = type === 'error' ? '❌' : type === 'success' ? '✅' : 'ℹ️';
    console.log(`[${timestamp}] ${prefix} ${message}`);
  }

  /**
   * Busca pessoas por palavra-chave
   */
  async searchPeople(keywords, maxResults = 25) {
    try {
      this.log(`Iniciando busca por: "${keywords}"`);
      
      // Navegar para página de busca
      const searchUrl = `https://www.linkedin.com/search/results/people/?keywords=${encodeURIComponent(keywords)}`;
      window.location.href = searchUrl;
      
      await this.wait(3000); // Aguardar carregamento
      
      // Aguardar elementos carregarem
      const searchResults = document.querySelectorAll('[data-view-name="search-entity-result"]');
      
      if (searchResults.length === 0) {
        this.log('Nenhum resultado encontrado', 'error');
        return [];
      }
      
      this.log(`Encontrados ${searchResults.length} resultados`);
      return Array.from(searchResults).slice(0, maxResults);
      
    } catch (error) {
      this.log(`Erro na busca: ${error.message}`, 'error');
      this.stats.errors++;
      return [];
    }
  }

  /**
   * Envia solicitação de conexão
   */
  async sendConnectionRequest(profileElement, message = '') {
    try {
      // Procurar botão "Conectar"
      const connectButton = profileElement.querySelector('button[aria-label*="Conectar"], button[aria-label*="Connect"]');
      
      if (!connectButton) {
        this.log('Botão conectar não encontrado', 'error');
        return false;
      }

      // Verificar se já está conectado
      if (connectButton.textContent.includes('Conectado') || 
          connectButton.textContent.includes('Connected') ||
          connectButton.disabled) {
        this.log('Já conectado ou botão desabilitado');
        return false;
      }

      // Clicar no botão conectar
      connectButton.click();
      await this.wait(this.randomDelay(1000, 2000));

      // Se houver modal de mensagem personalizada
      const sendButton = document.querySelector('button[aria-label*="Enviar"], button[aria-label*="Send"]');
      const addNoteButton = document.querySelector('button[aria-label*="Adicionar nota"], button[aria-label*="Add note"]');
      
      if (message && addNoteButton) {
        // Adicionar mensagem personalizada
        addNoteButton.click();
        await this.wait(1000);
        
        const messageTextarea = document.querySelector('textarea[name="message"]');
        if (messageTextarea) {
          messageTextarea.value = message;
          messageTextarea.dispatchEvent(new Event('input', { bubbles: true }));
          await this.wait(500);
        }
      }

      // Enviar solicitação
      if (sendButton) {
        sendButton.click();
      }

      this.stats.connectionsRequested++;
      this.log(`Solicitação enviada (${this.stats.connectionsRequested})`, 'success');
      
      return true;

    } catch (error) {
      this.log(`Erro ao enviar conexão: ${error.message}`, 'error');
      this.stats.errors++;
      return false;
    }
  }

  /**
   * Visualiza perfil
   */
  async viewProfile(profileElement) {
    try {
      const profileLink = profileElement.querySelector('a[href*="/in/"]');
      
      if (!profileLink) {
        this.log('Link do perfil não encontrado', 'error');
        return false;
      }

      // Abrir perfil em nova aba
      window.open(profileLink.href, '_blank');
      
      this.stats.profilesViewed++;
      this.log(`Perfil visualizado (${this.stats.profilesViewed})`, 'success');
      
      return true;

    } catch (error) {
      this.log(`Erro ao visualizar perfil: ${error.message}`, 'error');
      this.stats.errors++;
      return false;
    }
  }

  /**
   * Envia mensagem para conexão existente
   */
  async sendMessage(profileElement, message) {
    try {
      const messageButton = profileElement.querySelector('button[aria-label*="Mensagem"], button[aria-label*="Message"]');
      
      if (!messageButton) {
        this.log('Botão de mensagem não encontrado', 'error');
        return false;
      }

      messageButton.click();
      await this.wait(this.randomDelay(2000, 3000));

      // Aguardar modal de mensagem abrir
      const messageTextarea = document.querySelector('div[role="textbox"], textarea[placeholder*="mensagem"]');
      
      if (messageTextarea) {
        messageTextarea.textContent = message;
        messageTextarea.dispatchEvent(new Event('input', { bubbles: true }));
        await this.wait(1000);

        // Procurar botão enviar
        const sendButton = document.querySelector('button[type="submit"], button[aria-label*="Enviar"]');
        if (sendButton) {
          sendButton.click();
          
          this.stats.messagesSent++;
          this.log(`Mensagem enviada (${this.stats.messagesSent})`, 'success');
          return true;
        }
      }

      return false;

    } catch (error) {
      this.log(`Erro ao enviar mensagem: ${error.message}`, 'error');
      this.stats.errors++;
      return false;
    }
  }

  /**
   * Automação principal - Buscar e conectar
   */
  async autoConnectByKeywords(keywords, maxConnections = 25, customMessage = '') {
    if (this.isRunning) {
      this.log('Automação já está rodando!', 'error');
      return;
    }

    this.isRunning = true;
    this.log('🚀 Iniciando automação de conexões...');
    
    try {
      // Buscar pessoas
      const profiles = await this.searchPeople(keywords, maxConnections);
      
      if (profiles.length === 0) {
        this.log('Nenhum perfil encontrado para conectar', 'error');
        return;
      }

      // Processar cada perfil
      for (let i = 0; i < profiles.length && this.isRunning; i++) {
        if (this.stats.connectionsRequested >= this.config.dailyConnectionLimit) {
          this.log('Limite diário de conexões atingido', 'error');
          break;
        }

        if (this.stats.errors >= this.config.maxErrorsBeforeStop) {
          this.log('Muitos erros detectados. Parando automação.', 'error');
          break;
        }

        const profile = profiles[i];
        this.log(`Processando perfil ${i + 1}/${profiles.length}`);

        // Enviar solicitação de conexão
        await this.sendConnectionRequest(profile, customMessage);
        
        // Delay entre ações
        const delay = this.randomDelay();
        this.log(`Aguardando ${delay}ms antes da próxima ação...`);
        await this.wait(delay);
      }

    } catch (error) {
      this.log(`Erro na automação: ${error.message}`, 'error');
    } finally {
      this.isRunning = false;
      this.showStats();
    }
  }

  /**
   * Automação de visualização de perfis
   */
  async autoViewProfiles(keywords, maxViews = 50) {
    if (this.isRunning) {
      this.log('Automação já está rodando!', 'error');
      return;
    }

    this.isRunning = true;
    this.log('👀 Iniciando automação de visualização de perfis...');
    
    try {
      const profiles = await this.searchPeople(keywords, maxViews);
      
      for (let i = 0; i < profiles.length && this.isRunning; i++) {
        const profile = profiles[i];
        this.log(`Visualizando perfil ${i + 1}/${profiles.length}`);

        await this.viewProfile(profile);
        
        // Delay entre visualizações
        const delay = this.randomDelay(3000, 6000);
        await this.wait(delay);
      }

    } catch (error) {
      this.log(`Erro na automação: ${error.message}`, 'error');
    } finally {
      this.isRunning = false;
      this.showStats();
    }
  }

  /**
   * Para a automação
   */
  stop() {
    this.isRunning = false;
    this.log('🛑 Automação interrompida pelo usuário');
    this.showStats();
  }

  /**
   * Mostra estatísticas
   */
  showStats() {
    console.log('\n📊 ESTATÍSTICAS DA AUTOMAÇÃO:');
    console.log(`✅ Conexões solicitadas: ${this.stats.connectionsRequested}`);
    console.log(`💬 Mensagens enviadas: ${this.stats.messagesSent}`);
    console.log(`👀 Perfis visualizados: ${this.stats.profilesViewed}`);
    console.log(`❌ Erros: ${this.stats.errors}`);
    console.log('\n');
  }

  /**
   * Reseta estatísticas
   */
  resetStats() {
    this.stats = {
      connectionsRequested: 0,
      messagesSent: 0,
      profilesViewed: 0,
      errors: 0
    };
    this.log('Estatísticas resetadas');
  }
}

// Criar instância global
window.SnapLinkedBot = new LinkedInAutomation();

// Funções de conveniência
window.conectarPorPalavraChave = (keywords, maxConnections = 25, message = '') => {
  return window.SnapLinkedBot.autoConnectByKeywords(keywords, maxConnections, message);
};

window.visualizarPerfis = (keywords, maxViews = 50) => {
  return window.SnapLinkedBot.autoViewProfiles(keywords, maxViews);
};

window.pararAutomacao = () => {
  window.SnapLinkedBot.stop();
};

window.estatisticas = () => {
  window.SnapLinkedBot.showStats();
};

// Instruções de uso
console.log(`
🚀 SNAPLINKED - AUTOMAÇÃO LINKEDIN CARREGADA!

📋 COMANDOS DISPONÍVEIS:

1️⃣ Conectar por palavra-chave:
   conectarPorPalavraChave("desenvolvedor", 25, "Olá! Gostaria de conectar.")

2️⃣ Visualizar perfis:
   visualizarPerfis("CEO startup", 50)

3️⃣ Parar automação:
   pararAutomacao()

4️⃣ Ver estatísticas:
   estatisticas()

⚠️  IMPORTANTE:
- Execute apenas no LinkedIn (linkedin.com)
- Respeite os limites diários
- Use delays para simular comportamento humano
- Monitore sempre a execução

🔒 SEGURANÇA:
- Scripts simulam comportamento humano
- Delays aleatórios entre ações
- Limites de segurança configurados
- Parada automática em caso de erros
`);

// Verificar se está no LinkedIn
if (!window.location.hostname.includes('linkedin.com')) {
  console.warn('⚠️  Este script deve ser executado apenas no LinkedIn!');
}
