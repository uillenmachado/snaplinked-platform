"""
Implementação simples e robusta do login LinkedIn
"""
import asyncio
from playwright.async_api import async_playwright
import logging

logger = logging.getLogger(__name__)

class SimpleLinkedInLogin:
    def __init__(self):
        self.browser = None
        self.page = None
        self.is_logged_in = False
        
    async def login(self, email, password):
        """Login simples e direto no LinkedIn"""
        try:
            logger.info("Iniciando login no LinkedIn...")
            
            # Inicializar Playwright
            playwright = await async_playwright().start()
            
            # Abrir navegador
            self.browser = await playwright.chromium.launch(
                headless=True,  # Modo headless para ambiente sandbox
                args=[
                    '--no-sandbox', 
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu'
                ]
            )
            
            # Criar contexto
            context = await self.browser.new_context()
            self.page = await context.new_page()
            
            # Navegar para LinkedIn
            logger.info("Navegando para LinkedIn...")
            await self.page.goto('https://www.linkedin.com/login')
            await self.page.wait_for_load_state('networkidle')
            
            # Preencher email
            logger.info("Preenchendo email...")
            await self.page.fill('#username', email)
            await asyncio.sleep(1)
            
            # Preencher senha
            logger.info("Preenchendo senha...")
            await self.page.fill('#password', password)
            await asyncio.sleep(1)
            
            # Clicar em entrar
            logger.info("Clicando em entrar...")
            await self.page.click('button[type="submit"]')
            
            # Aguardar redirecionamento com múltiplas estratégias
            logger.info("Aguardando redirecionamento...")
            
            try:
                # Estratégia 1: Aguardar URL do feed
                await self.page.wait_for_url('**/feed/**', timeout=30000)
            except:
                try:
                    # Estratégia 2: Aguardar elemento do feed
                    await self.page.wait_for_selector('[data-view-name="feed"]', timeout=20000)
                except:
                    try:
                        # Estratégia 3: Aguardar qualquer mudança de URL
                        await asyncio.sleep(10)
                        current_url = self.page.url
                        if 'login' not in current_url.lower():
                            logger.info(f"Login detectado - URL mudou para: {current_url}")
                        else:
                            raise Exception("Ainda na página de login")
                    except:
                        # Estratégia 4: Verificar se há elementos do LinkedIn logado
                        try:
                            await self.page.wait_for_selector('nav[aria-label="Primary Navigation"]', timeout=10000)
                            logger.info("Login detectado - navegação principal encontrada")
                        except:
                            raise Exception("Login falhou - não conseguiu detectar sucesso")
            
            # Verificar se chegou no feed ou área logada
            current_url = self.page.url
            if any(keyword in current_url.lower() for keyword in ['/feed/', '/dashboard/', '/in/', 'linkedin.com/feed']):
                self.is_logged_in = True
                logger.info(f"✅ Login realizado com sucesso! URL: {current_url}")
                return {
                    'success': True,
                    'message': 'Login realizado com sucesso!',
                    'url': current_url
                }
            else:
                # Tentar navegar para o feed manualmente
                logger.info("Tentando navegar para o feed...")
                await self.page.goto('https://www.linkedin.com/feed/')
                await asyncio.sleep(5)
                
                if '/feed/' in self.page.url:
                    self.is_logged_in = True
                    logger.info("✅ Login realizado com sucesso após navegação manual!")
                    return {
                        'success': True,
                        'message': 'Login realizado com sucesso!',
                        'url': self.page.url
                    }
                else:
                    logger.error(f"❌ Login falhou - URL final: {current_url}")
                    return {
                        'success': False,
                        'error': f'Login falhou - URL final: {current_url}'
                    }
                
        except Exception as e:
            logger.error(f"❌ Erro no login: {e}")
            return {
                'success': False,
                'error': f'Erro no login: {str(e)}'
            }
    
    async def like_posts(self, max_likes=3, user_id=None):
        """Curtir posts no feed"""
        try:
            if not self.is_logged_in or not self.page:
                return {'success': False, 'error': 'Não está logado'}
            
            logger.info(f"Iniciando curtidas de {max_likes} posts...")
            
            # Navegar para o feed se não estiver lá
            if '/feed/' not in self.page.url:
                await self.page.goto('https://www.linkedin.com/feed/')
                await self.page.wait_for_load_state('networkidle')
            
            # Encontrar botões de curtir
            like_buttons = await self.page.locator('button[aria-label*="Curtir"]').all()
            
            likes_given = 0
            results = []
            
            for i, button in enumerate(like_buttons[:max_likes]):
                try:
                    # Verificar se já foi curtido
                    aria_label = await button.get_attribute('aria-label')
                    if 'Descurtir' in aria_label:
                        logger.info(f"Post {i+1} já curtido, pulando...")
                        continue
                    
                    # Rolar até o botão
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(2)
                    
                    # Clicar no botão curtir
                    await button.click()
                    await asyncio.sleep(3)
                    
                    likes_given += 1
                    logger.info(f"✅ Post {i+1} curtido com sucesso!")
                    
                    results.append({
                        'post': i+1,
                        'success': True,
                        'action': 'like'
                    })
                    
                except Exception as e:
                    logger.error(f"❌ Erro ao curtir post {i+1}: {e}")
                    results.append({
                        'post': i+1,
                        'success': False,
                        'error': str(e)
                    })
            
            result_data = {
                'success': True,
                'message': f'{likes_given} posts curtidos com sucesso!',
                'likes_given': likes_given,
                'results': results
            }
            
            # Registrar no banco de dados se user_id fornecido
            if user_id:
                try:
                    from analytics_service import analytics
                    analytics.process_automation_result(user_id, 'like_posts', result_data)
                except Exception as e:
                    logger.warning(f"Erro ao registrar estatísticas: {e}")
            
            return result_data
            
        except Exception as e:
            logger.error(f"❌ Erro na automação de curtidas: {e}")
            return {
                'success': False,
                'error': f'Erro na automação de curtidas: {str(e)}'
            }
    
    async def comment_posts(self, max_comments=2, comment_text="Excelente conteúdo! 👏", user_id=None):
        """Comentar em posts no feed"""
        try:
            if not self.is_logged_in or not self.page:
                return {'success': False, 'error': 'Não está logado'}
            
            logger.info(f"Iniciando comentários em {max_comments} posts...")
            
            # Navegar para o feed se não estiver lá
            if '/feed/' not in self.page.url:
                await self.page.goto('https://www.linkedin.com/feed/')
                await self.page.wait_for_load_state('networkidle')
            
            # Encontrar botões de comentar
            comment_buttons = await self.page.locator('button[aria-label*="Comentar"]').all()
            
            comments_posted = 0
            results = []
            
            for i, button in enumerate(comment_buttons[:max_comments]):
                try:
                    # Rolar até o botão
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(2)
                    
                    # Clicar no botão comentar
                    await button.click()
                    await asyncio.sleep(3)
                    
                    # Encontrar campo de comentário
                    comment_field = self.page.locator('div[contenteditable="true"]').first
                    if await comment_field.count() > 0:
                        # Digitar comentário
                        await comment_field.fill(comment_text)
                        await asyncio.sleep(2)
                        
                        # Encontrar e clicar no botão publicar
                        publish_button = self.page.locator('button:has-text("Publicar")').first
                        if await publish_button.count() > 0:
                            await publish_button.click()
                            await asyncio.sleep(4)
                            
                            comments_posted += 1
                            logger.info(f"✅ Comentário {i+1} postado com sucesso!")
                            
                            results.append({
                                'post': i+1,
                                'success': True,
                                'action': 'comment',
                                'comment': comment_text
                            })
                        else:
                            logger.warning(f"⚠️ Botão publicar não encontrado para post {i+1}")
                    else:
                        logger.warning(f"⚠️ Campo de comentário não encontrado para post {i+1}")
                    
                except Exception as e:
                    logger.error(f"❌ Erro ao comentar post {i+1}: {e}")
                    results.append({
                        'post': i+1,
                        'success': False,
                        'error': str(e)
                    })
            
            result_data = {
                'success': True,
                'message': f'{comments_posted} comentários postados com sucesso!',
                'comments_posted': comments_posted,
                'results': results
            }
            
            # Registrar no banco de dados se user_id fornecido
            if user_id:
                try:
                    from analytics_service import analytics
                    analytics.process_automation_result(user_id, 'comment_posts', result_data)
                except Exception as e:
                    logger.warning(f"Erro ao registrar estatísticas: {e}")
            
            return result_data
            
        except Exception as e:
            logger.error(f"❌ Erro na automação de comentários: {e}")
            return {
                'success': False,
                'error': f'Erro na automação de comentários: {str(e)}'
            }
    
    async def close(self):
        """Fechar navegador"""
        try:
            if self.browser:
                await self.browser.close()
                self.is_logged_in = False
                logger.info("Navegador fechado")
        except Exception as e:
            logger.error(f"Erro ao fechar navegador: {e}")

    async def send_connections(self, keywords, max_connections=3, message="", user_id=None):
        """Enviar solicitações de conexão reais"""
        try:
            if not self.is_logged_in:
                return {'success': False, 'error': 'Não está logado no LinkedIn'}
            
            # Navegar para busca de pessoas
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords}"
            await self.page.goto(search_url)
            await asyncio.sleep(5)
            
            # Aguardar resultados carregarem
            try:
                await self.page.wait_for_selector('[data-view-name="search-entity-result"]', timeout=20000)
            except:
                # Tentar seletor alternativo
                await self.page.wait_for_selector('.search-result__wrapper', timeout=15000)
            
            # Encontrar botões de conectar
            connect_buttons = await self.page.locator('button:has-text("Conectar")').all()
            
            connections_sent = 0
            results = []
            
            for i, button in enumerate(connect_buttons[:max_connections]):
                try:
                    # Rolar até o botão
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(2)
                    
                    # Clicar no botão conectar
                    await button.click()
                    await asyncio.sleep(3)
                    
                    # Verificar se apareceu modal de mensagem
                    if message:
                        try:
                            # Tentar adicionar nota
                            add_note_btn = await self.page.locator('button:has-text("Adicionar nota")').first
                            if await add_note_btn.count() > 0:
                                await add_note_btn.click()
                                await asyncio.sleep(2)
                                
                                # Preencher mensagem
                                message_field = await self.page.locator('textarea[name="message"]').first
                                if await message_field.count() > 0:
                                    await message_field.fill(message)
                                    await asyncio.sleep(1)
                        except:
                            pass  # Se não conseguir adicionar nota, continua sem
                    
                    # Enviar convite
                    send_btn = await self.page.locator('button:has-text("Enviar convite")').first
                    if await send_btn.count() > 0:
                        await send_btn.click()
                        await asyncio.sleep(3)
                        
                        connections_sent += 1
                        logger.info(f"✅ Conexão {i+1} enviada com sucesso!")
                        
                        results.append({
                            'connection': i+1,
                            'success': True,
                            'action': 'connect',
                            'message': message if message else 'Sem mensagem'
                        })
                    else:
                        # Tentar fechar modal se não conseguir enviar
                        close_btn = await self.page.locator('button[aria-label="Fechar"]').first
                        if await close_btn.count() > 0:
                            await close_btn.click()
                            await asyncio.sleep(1)
                        
                        results.append({
                            'connection': i+1,
                            'success': False,
                            'error': 'Botão enviar não encontrado'
                        })
                    
                except Exception as e:
                    logger.error(f"❌ Erro ao enviar conexão {i+1}: {e}")
                    results.append({
                        'connection': i+1,
                        'success': False,
                        'error': str(e)
                    })
            
            result_data = {
                'success': True,
                'message': f'{connections_sent} solicitações de conexão enviadas!',
                'connections_sent': connections_sent,
                'results': results
            }
            
            # Registrar no banco de dados se user_id fornecido
            if user_id:
                try:
                    from analytics_service import analytics
                    analytics.process_automation_result(user_id, 'send_connections', result_data)
                except Exception as e:
                    logger.warning(f"Erro ao registrar estatísticas: {e}")
            
            return result_data
            
        except Exception as e:
            logger.error(f"❌ Erro na automação de conexões: {e}")
            return {
                'success': False,
                'error': f'Erro na automação de conexões: {str(e)}'
            }


# Instância global
simple_login = SimpleLinkedInLogin()
