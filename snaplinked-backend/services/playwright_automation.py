"""
SnapLinked - Serviço Playwright Automação Real
Implementação completa de automação LinkedIn com Playwright
"""
import asyncio
import os
import logging
import json
import time
from datetime import datetime
from playwright.async_api import async_playwright
from .gemini_ai import gemini_ai

logger = logging.getLogger(__name__)

class PlaywrightAutomation:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.is_logged_in = False
        self.user_email = None
        self.storage_state = None
        
    async def initialize_browser(self, headless=True):
        """Inicializa navegador Playwright"""
        try:
            playwright = await async_playwright().start()
            
            self.browser = await playwright.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            # Criar contexto com user agent realista
            self.context = await self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            self.page = await self.context.new_page()
            
            logger.info("Navegador Playwright inicializado")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar navegador: {str(e)}")
            return False
    
    async def login_linkedin(self, email, password):
        """Login real no LinkedIn"""
        try:
            if not self.page:
                await self.initialize_browser()
            
            logger.info(f"Iniciando login LinkedIn para: {email}")
            
            # Navegar para LinkedIn
            await self.page.goto('https://www.linkedin.com/login', wait_until='networkidle')
            await asyncio.sleep(2)
            
            # Preencher email
            await self.page.fill('#username', email)
            await asyncio.sleep(1)
            
            # Preencher senha
            await self.page.fill('#password', password)
            await asyncio.sleep(1)
            
            # Clicar em entrar
            await self.page.click('button[type="submit"]')
            await asyncio.sleep(3)
            
            # Verificar se login foi bem-sucedido
            current_url = self.page.url
            
            if 'feed' in current_url or 'mynetwork' in current_url:
                self.is_logged_in = True
                self.user_email = email
                
                # Salvar estado da sessão
                self.storage_state = await self.context.storage_state()
                
                logger.info(f"Login realizado com sucesso: {current_url}")
                return {
                    'success': True,
                    'message': 'Login realizado com sucesso',
                    'redirect_url': current_url,
                    'user_email': email
                }
            else:
                logger.error(f"Login falhou - URL atual: {current_url}")
                return {
                    'success': False,
                    'error': 'Credenciais inválidas ou bloqueio de segurança',
                    'current_url': current_url
                }
                
        except Exception as e:
            logger.error(f"Erro no login LinkedIn: {str(e)}")
            return {
                'success': False,
                'error': f"Erro no login: {str(e)}"
            }
    
    async def like_post(self, post_url=None):
        """Curte posts no LinkedIn"""
        try:
            if not self.is_logged_in:
                return {
                    'success': False,
                    'error': 'Usuário não está logado'
                }
            
            # Se URL específica fornecida, navegar para ela
            if post_url:
                await self.page.goto(post_url, wait_until='networkidle')
                await asyncio.sleep(2)
            else:
                # Navegar para feed se não estiver lá
                if 'feed' not in self.page.url:
                    await self.page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
                    await asyncio.sleep(3)
            
            # Procurar botões de curtir
            like_buttons = await self.page.query_selector_all('button[aria-label*="curtir"], button[aria-label*="like"]')
            
            if not like_buttons:
                # Tentar seletores alternativos
                like_buttons = await self.page.query_selector_all('.react-button__trigger, [data-control-name="like_toggle"]')
            
            if like_buttons:
                # Curtir primeiro post não curtido
                for button in like_buttons[:3]:  # Máximo 3 curtidas
                    try:
                        # Verificar se já está curtido
                        is_liked = await button.get_attribute('aria-pressed')
                        if is_liked != 'true':
                            await button.click()
                            await asyncio.sleep(2)
                            
                            logger.info("Post curtido com sucesso")
                            return {
                                'success': True,
                                'message': 'Post curtido com sucesso',
                                'action': 'like',
                                'timestamp': datetime.now().isoformat()
                            }
                    except:
                        continue
                
                return {
                    'success': False,
                    'error': 'Todos os posts visíveis já foram curtidos'
                }
            else:
                return {
                    'success': False,
                    'error': 'Nenhum botão de curtir encontrado'
                }
                
        except Exception as e:
            logger.error(f"Erro ao curtir post: {str(e)}")
            return {
                'success': False,
                'error': f"Erro ao curtir: {str(e)}"
            }
    
    async def comment_post(self, post_url=None, comment_text=None, use_ai=True):
        """Comenta em posts do LinkedIn"""
        try:
            if not self.is_logged_in:
                return {
                    'success': False,
                    'error': 'Usuário não está logado'
                }
            
            # Navegar para post específico ou feed
            if post_url:
                await self.page.goto(post_url, wait_until='networkidle')
                await asyncio.sleep(2)
            else:
                if 'feed' not in self.page.url:
                    await self.page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
                    await asyncio.sleep(3)
            
            # Procurar botões de comentário
            comment_buttons = await self.page.query_selector_all('button[aria-label*="comentar"], button[aria-label*="comment"]')
            
            if not comment_buttons:
                comment_buttons = await self.page.query_selector_all('[data-control-name="comment_toggle"]')
            
            if comment_buttons:
                # Clicar no primeiro botão de comentário
                await comment_buttons[0].click()
                await asyncio.sleep(2)
                
                # Gerar comentário com IA se solicitado
                if use_ai and not comment_text:
                    # Tentar extrair contexto do post
                    try:
                        post_content = await self.page.text_content('.feed-shared-text')
                        if post_content:
                            ai_result = gemini_ai.generate_comment(post_content[:200])
                            if ai_result['success']:
                                comment_text = ai_result['comment']
                            else:
                                comment_text = "Excelente post! Muito interessante. 👍"
                        else:
                            comment_text = "Ótimo conteúdo! Obrigado por compartilhar. 🚀"
                    except:
                        comment_text = "Parabéns pelo post! Muito relevante. ✨"
                
                # Procurar campo de comentário
                comment_field = await self.page.query_selector('div[contenteditable="true"], textarea[placeholder*="comentário"]')
                
                if comment_field:
                    # Escrever comentário
                    await comment_field.fill(comment_text)
                    await asyncio.sleep(1)
                    
                    # Procurar botão de publicar
                    publish_buttons = await self.page.query_selector_all('button:has-text("Publicar"), button:has-text("Post")')
                    
                    if publish_buttons:
                        await publish_buttons[0].click()
                        await asyncio.sleep(2)
                        
                        logger.info(f"Comentário postado: {comment_text[:50]}...")
                        return {
                            'success': True,
                            'message': 'Comentário postado com sucesso',
                            'comment': comment_text,
                            'action': 'comment',
                            'ai_generated': use_ai,
                            'timestamp': datetime.now().isoformat()
                        }
                    else:
                        return {
                            'success': False,
                            'error': 'Botão de publicar não encontrado'
                        }
                else:
                    return {
                        'success': False,
                        'error': 'Campo de comentário não encontrado'
                    }
            else:
                return {
                    'success': False,
                    'error': 'Botão de comentário não encontrado'
                }
                
        except Exception as e:
            logger.error(f"Erro ao comentar post: {str(e)}")
            return {
                'success': False,
                'error': f"Erro ao comentar: {str(e)}"
            }
    
    async def send_connection_request(self, profile_url, message=None):
        """Envia solicitação de conexão"""
        try:
            if not self.is_logged_in:
                return {
                    'success': False,
                    'error': 'Usuário não está logado'
                }
            
            # Navegar para perfil
            await self.page.goto(profile_url, wait_until='networkidle')
            await asyncio.sleep(3)
            
            # Procurar botão de conectar
            connect_buttons = await self.page.query_selector_all('button:has-text("Conectar"), button:has-text("Connect")')
            
            if connect_buttons:
                await connect_buttons[0].click()
                await asyncio.sleep(2)
                
                # Se houver mensagem personalizada
                if message:
                    # Procurar opção de adicionar nota
                    add_note_button = await self.page.query_selector('button:has-text("Adicionar nota")')
                    if add_note_button:
                        await add_note_button.click()
                        await asyncio.sleep(1)
                        
                        # Escrever mensagem
                        message_field = await self.page.query_selector('textarea')
                        if message_field:
                            await message_field.fill(message)
                            await asyncio.sleep(1)
                
                # Enviar solicitação
                send_buttons = await self.page.query_selector_all('button:has-text("Enviar"), button:has-text("Send")')
                if send_buttons:
                    await send_buttons[0].click()
                    await asyncio.sleep(2)
                    
                    logger.info(f"Solicitação de conexão enviada para: {profile_url}")
                    return {
                        'success': True,
                        'message': 'Solicitação de conexão enviada',
                        'profile_url': profile_url,
                        'custom_message': bool(message),
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Botão de enviar não encontrado'
                    }
            else:
                return {
                    'success': False,
                    'error': 'Botão de conectar não encontrado'
                }
                
        except Exception as e:
            logger.error(f"Erro ao enviar conexão: {str(e)}")
            return {
                'success': False,
                'error': f"Erro ao enviar conexão: {str(e)}"
            }
    
    async def get_user_profile(self):
        """Obtém informações do perfil do usuário logado"""
        try:
            if not self.is_logged_in:
                return {
                    'success': False,
                    'error': 'Usuário não está logado'
                }
            
            # Navegar para perfil próprio
            await self.page.goto('https://www.linkedin.com/in/me/', wait_until='networkidle')
            await asyncio.sleep(3)
            
            # Extrair informações do perfil
            name = await self.page.text_content('h1')
            headline = await self.page.text_content('.text-body-medium')
            
            return {
                'success': True,
                'profile': {
                    'name': name.strip() if name else 'N/A',
                    'headline': headline.strip() if headline else 'N/A',
                    'email': self.user_email,
                    'url': self.page.url
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter perfil: {str(e)}")
            return {
                'success': False,
                'error': f"Erro ao obter perfil: {str(e)}"
            }
    
    async def close_browser(self):
        """Fecha navegador e limpa recursos"""
        try:
            if self.browser:
                await self.browser.close()
                self.browser = None
                self.context = None
                self.page = None
                self.is_logged_in = False
                self.user_email = None
                logger.info("Navegador fechado")
                return True
        except Exception as e:
            logger.error(f"Erro ao fechar navegador: {str(e)}")
            return False
    
    def get_status(self):
        """Retorna status atual da automação"""
        return {
            'browser_active': self.browser is not None,
            'logged_in': self.is_logged_in,
            'user_email': self.user_email,
            'current_url': self.page.url if self.page else None
        }

# Instância global
playwright_automation = PlaywrightAutomation()
