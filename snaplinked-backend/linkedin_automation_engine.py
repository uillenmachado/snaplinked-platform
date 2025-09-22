"""
SnapLinked - Motor de Automação LinkedIn
Sistema completo de automação que executa ações automaticamente
"""

import asyncio
import random
import time
import json
import logging
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
import requests

logger = logging.getLogger(__name__)

class LinkedInAutomationEngine:
    def __init__(self):
        self.browser = None
        self.page = None
        self.is_logged_in = False
        self.user_profile = {}
        self.automation_stats = {
            'connections_sent': 0,
            'messages_sent': 0,
            'profiles_viewed': 0,
            'likes_given': 0,
            'comments_posted': 0,
            'feed_interactions': 0,
            'errors': 0,
            'last_activity': None
        }
        
    async def initialize_browser(self, headless=True):
        """Inicializa o navegador Playwright"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            
            context = await self.browser.new_context(
                viewport={'width': 1366, 'height': 768},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            self.page = await context.new_page()
            
            # Configurar timeouts
            self.page.set_default_timeout(30000)
            
            logger.info("Navegador inicializado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar navegador: {e}")
            return False
    
    async def login_with_credentials(self, email, password):
        """Faz login no LinkedIn com credenciais do usuário"""
        try:
            # Inicializar navegador se necessário
            if not self.browser:
                await self.initialize_browser()
            
            # Criar nova página
            if not self.page:
                self.page = await self.browser.new_page()
                
            # Navegar para LinkedIn
            await self.page.goto('https://www.linkedin.com/login')
            await self.random_delay(2, 4)
            
            # Preencher email
            await self.page.fill('#username', email)
            await self.random_delay(1, 2)
            
            # Preencher senha
            await self.page.fill('#password', password)
            await self.random_delay(1, 2)
            
            # Clicar em entrar
            await self.page.click('button[type="submit"]')
            await self.random_delay(3, 5)
            
            # Verificar se login foi bem-sucedido
            try:
                await self.page.wait_for_selector('nav[aria-label="Primary Navigation"]', timeout=10000)
                self.is_logged_in = True
                
                # Obter dados do perfil
                await self.get_profile_data()
                
                logger.info("Login realizado com sucesso")
                return {
                    'success': True,
                    'message': 'Login realizado com sucesso',
                    'profile': self.user_profile
                }
                
            except:
                # Verificar se há desafio de segurança
                if await self.page.locator('text=Verificação de segurança').count() > 0:
                    return {
                        'success': False,
                        'error': 'verification_required',
                        'message': 'Verificação de segurança necessária. Complete manualmente.'
                    }
                else:
                    return {
                        'success': False,
                        'error': 'invalid_credentials',
                        'message': 'Credenciais inválidas'
                    }
                    
        except Exception as e:
            logger.error(f"Erro no login: {e}")
            return {
                'success': False,
                'error': 'login_error',
                'message': f'Erro no login: {str(e)}'
            }
    
    async def get_profile_data(self):
        """Obtém dados do perfil do usuário logado"""
        try:
            # Navegar para o perfil
            await self.page.goto('https://www.linkedin.com/in/me/')
            await self.random_delay(2, 3)
            
            # Extrair dados do perfil
            name_element = await self.page.locator('h1.text-heading-xlarge').first
            name = await name_element.inner_text() if await name_element.count() > 0 else "Usuário"
            
            headline_element = await self.page.locator('.text-body-medium.break-words').first
            headline = await headline_element.inner_text() if await headline_element.count() > 0 else ""
            
            self.user_profile = {
                'name': name.strip(),
                'headline': headline.strip(),
                'logged_in_at': datetime.now().isoformat(),
                'connectionType': 'manual',
                'automationEnabled': True
            }
            
            logger.info(f"Perfil obtido: {name}")
            
        except Exception as e:
            logger.error(f"Erro ao obter perfil: {e}")
            self.user_profile = {
                'name': 'Usuário LinkedIn',
                'headline': '',
                'logged_in_at': datetime.now().isoformat(),
                'connectionType': 'manual',
                'automationEnabled': True
            }
    
    async def navigate_to_feed(self):
        """Navega para o feed do LinkedIn"""
        try:
            await self.page.goto('https://www.linkedin.com/feed/')
            await self.random_delay(3, 5)
            
            # Aguardar feed carregar
            await self.page.wait_for_selector('[data-id]', timeout=10000)
            
            logger.info("Feed carregado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar feed: {e}")
            return False
    
    async def like_posts_in_feed(self, max_likes=10):
        """Curte posts no feed do LinkedIn"""
        try:
            if not self.is_logged_in:
                return {'success': False, 'error': 'not_logged_in'}
            
            # Navegar para o feed
            if not await self.navigate_to_feed():
                return {'success': False, 'error': 'failed_to_load_feed'}
            
            # Encontrar botões de curtir
            like_buttons = await self.page.locator('button[aria-label*="Curtir"]').all()
            
            likes_given = 0
            results = []
            
            for i, button in enumerate(like_buttons[:max_likes]):
                try:
                    # Verificar se já foi curtido
                    aria_label = await button.get_attribute('aria-label')
                    if 'Descurtir' in aria_label:
                        continue  # Já curtido
                    
                    # Rolar até o botão
                    await button.scroll_into_view_if_needed()
                    await self.random_delay(1, 2)
                    
                    # Clicar no botão curtir
                    await button.click()
                    await self.random_delay(2, 4)
                    
                    likes_given += 1
                    self.automation_stats['likes_given'] += 1
                    self.automation_stats['feed_interactions'] += 1
                    
                    results.append({
                        'action': 'like',
                        'success': True,
                        'post_index': i
                    })
                    
                    logger.info(f"Post {i+1} curtido com sucesso")
                    
                except Exception as e:
                    logger.error(f"Erro ao curtir post {i}: {e}")
                    self.automation_stats['errors'] += 1
                    results.append({
                        'action': 'like',
                        'success': False,
                        'error': str(e),
                        'post_index': i
                    })
                    continue
            
            self.automation_stats['last_activity'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'message': f'{likes_given} posts curtidos com sucesso',
                'likes_given': likes_given,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Erro na automação de curtidas: {e}")
            return {
                'success': False,
                'error': f'Erro na automação de curtidas: {str(e)}'
            }
    
    async def comment_on_posts(self, max_comments=5, comment_templates=None):
        """Comenta em posts do feed"""
        try:
            if not self.is_logged_in:
                return {'success': False, 'error': 'not_logged_in'}
            
            if not comment_templates:
                comment_templates = [
                    "Excelente conteúdo! 👏",
                    "Muito interessante, obrigado por compartilhar!",
                    "Concordo totalmente com sua visão.",
                    "Ótima reflexão! 💡",
                    "Parabéns pelo post inspirador!"
                ]
            
            # Navegar para o feed
            if not await self.navigate_to_feed():
                return {'success': False, 'error': 'failed_to_load_feed'}
            
            # Encontrar botões de comentar
            comment_buttons = await self.page.locator('button[aria-label*="Comentar"]').all()
            
            comments_posted = 0
            results = []
            
            for i, button in enumerate(comment_buttons[:max_comments]):
                try:
                    # Rolar até o botão
                    await button.scroll_into_view_if_needed()
                    await self.random_delay(1, 2)
                    
                    # Clicar no botão comentar
                    await button.click()
                    await self.random_delay(2, 3)
                    
                    # Encontrar campo de comentário
                    comment_field = await self.page.locator('div[contenteditable="true"][data-placeholder*="comentário"]').first
                    
                    if await comment_field.count() > 0:
                        # Escolher comentário aleatório
                        comment_text = random.choice(comment_templates)
                        
                        # Digitar comentário
                        await comment_field.fill(comment_text)
                        await self.random_delay(1, 2)
                        
                        # Encontrar e clicar no botão publicar
                        publish_button = await self.page.locator('button:has-text("Publicar")').first
                        
                        if await publish_button.count() > 0:
                            await publish_button.click()
                            await self.random_delay(3, 5)
                            
                            comments_posted += 1
                            self.automation_stats['comments_posted'] += 1
                            self.automation_stats['feed_interactions'] += 1
                            
                            results.append({
                                'action': 'comment',
                                'success': True,
                                'post_index': i,
                                'comment': comment_text
                            })
                            
                            logger.info(f"Comentário postado no post {i+1}: {comment_text}")
                        else:
                            results.append({
                                'action': 'comment',
                                'success': False,
                                'error': 'Botão publicar não encontrado',
                                'post_index': i
                            })
                    else:
                        results.append({
                            'action': 'comment',
                            'success': False,
                            'error': 'Campo de comentário não encontrado',
                            'post_index': i
                        })
                    
                except Exception as e:
                    logger.error(f"Erro ao comentar post {i}: {e}")
                    self.automation_stats['errors'] += 1
                    results.append({
                        'action': 'comment',
                        'success': False,
                        'error': str(e),
                        'post_index': i
                    })
                    continue
            
            self.automation_stats['last_activity'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'message': f'{comments_posted} comentários postados com sucesso',
                'comments_posted': comments_posted,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Erro na automação de comentários: {e}")
            return {
                'success': False,
                'error': f'Erro na automação de comentários: {str(e)}'
            }
    
    async def interact_with_feed(self, max_interactions=15, like_probability=0.7, comment_probability=0.3):
        """Interage com o feed (curtidas e comentários combinados)"""
        try:
            if not self.is_logged_in:
                return {'success': False, 'error': 'not_logged_in'}
            
            # Navegar para o feed
            if not await self.navigate_to_feed():
                return {'success': False, 'error': 'failed_to_load_feed'}
            
            # Encontrar posts no feed
            posts = await self.page.locator('[data-id]').all()
            
            interactions = 0
            results = []
            
            comment_templates = [
                "Excelente conteúdo! 👏",
                "Muito interessante, obrigado por compartilhar!",
                "Concordo totalmente com sua visão.",
                "Ótima reflexão! 💡",
                "Parabéns pelo post inspirador!",
                "Muito útil, obrigado!",
                "Perspectiva interessante! 🤔",
                "Conteúdo de qualidade!"
            ]
            
            for i, post in enumerate(posts[:max_interactions]):
                try:
                    # Rolar até o post
                    await post.scroll_into_view_if_needed()
                    await self.random_delay(2, 4)
                    
                    # Decidir ação baseada na probabilidade
                    action_rand = random.random()
                    
                    if action_rand < like_probability:
                        # Tentar curtir
                        like_button = await post.locator('button[aria-label*="Curtir"]').first
                        
                        if await like_button.count() > 0:
                            aria_label = await like_button.get_attribute('aria-label')
                            if 'Descurtir' not in aria_label:  # Não curtido ainda
                                await like_button.click()
                                await self.random_delay(1, 2)
                                
                                interactions += 1
                                self.automation_stats['likes_given'] += 1
                                self.automation_stats['feed_interactions'] += 1
                                
                                results.append({
                                    'action': 'like',
                                    'success': True,
                                    'post_index': i
                                })
                                
                                logger.info(f"Post {i+1} curtido")
                    
                    elif action_rand < (like_probability + comment_probability):
                        # Tentar comentar
                        comment_button = await post.locator('button[aria-label*="Comentar"]').first
                        
                        if await comment_button.count() > 0:
                            await comment_button.click()
                            await self.random_delay(2, 3)
                            
                            # Encontrar campo de comentário
                            comment_field = await self.page.locator('div[contenteditable="true"][data-placeholder*="comentário"]').first
                            
                            if await comment_field.count() > 0:
                                comment_text = random.choice(comment_templates)
                                await comment_field.fill(comment_text)
                                await self.random_delay(1, 2)
                                
                                # Publicar comentário
                                publish_button = await self.page.locator('button:has-text("Publicar")').first
                                
                                if await publish_button.count() > 0:
                                    await publish_button.click()
                                    await self.random_delay(3, 5)
                                    
                                    interactions += 1
                                    self.automation_stats['comments_posted'] += 1
                                    self.automation_stats['feed_interactions'] += 1
                                    
                                    results.append({
                                        'action': 'comment',
                                        'success': True,
                                        'post_index': i,
                                        'comment': comment_text
                                    })
                                    
                                    logger.info(f"Comentário postado no post {i+1}")
                    
                    # Delay entre posts
                    await self.random_delay(3, 7)
                    
                except Exception as e:
                    logger.error(f"Erro ao interagir com post {i}: {e}")
                    self.automation_stats['errors'] += 1
                    continue
            
            self.automation_stats['last_activity'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'message': f'{interactions} interações realizadas no feed',
                'total_interactions': interactions,
                'results': results,
                'stats': self.automation_stats
            }
            
        except Exception as e:
            logger.error(f"Erro na interação com feed: {e}")
            return {
                'success': False,
                'error': f'Erro na interação com feed: {str(e)}'
            }
    
    async def search_people(self, keywords, max_results=25):
        """Busca pessoas por palavras-chave"""
        try:
            if not self.is_logged_in:
                return {'success': False, 'error': 'not_logged_in'}
            
            # Construir URL de busca
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords}"
            await self.page.goto(search_url)
            await self.random_delay(3, 5)
            
            # Aguardar resultados carregarem
            await self.page.wait_for_selector('[data-view-name="search-entity-result"]', timeout=10000)
            
            # Obter elementos dos resultados
            results = await self.page.locator('[data-view-name="search-entity-result"]').all()
            
            profiles = []
            for i, result in enumerate(results[:max_results]):
                try:
                    # Extrair dados do perfil
                    name_element = await result.locator('.entity-result__title-text a').first
                    name = await name_element.inner_text() if await name_element.count() > 0 else f"Perfil {i+1}"
                    
                    headline_element = await result.locator('.entity-result__primary-subtitle').first
                    headline = await headline_element.inner_text() if await headline_element.count() > 0 else ""
                    
                    # Verificar se há botão conectar
                    connect_button = await result.locator('button:has-text("Conectar")').first
                    can_connect = await connect_button.count() > 0
                    
                    profiles.append({
                        'name': name.strip(),
                        'headline': headline.strip(),
                        'can_connect': can_connect,
                        'element_index': i
                    })
                    
                except Exception as e:
                    logger.error(f"Erro ao processar resultado {i}: {e}")
                    continue
            
            logger.info(f"Encontrados {len(profiles)} perfis para: {keywords}")
            
            return {
                'success': True,
                'profiles': profiles,
                'total_found': len(profiles)
            }
            
        except Exception as e:
            logger.error(f"Erro na busca: {e}")
            return {
                'success': False,
                'error': f'Erro na busca: {str(e)}'
            }
    
    async def send_connection_request(self, profile_index, message=""):
        """Envia solicitação de conexão"""
        try:
            # Localizar o perfil específico
            results = await self.page.locator('[data-view-name="search-entity-result"]').all()
            
            if profile_index >= len(results):
                return {'success': False, 'error': 'Profile not found'}
            
            result = results[profile_index]
            
            # Procurar botão conectar
            connect_button = await result.locator('button:has-text("Conectar")').first
            
            if await connect_button.count() == 0:
                return {'success': False, 'error': 'Connect button not found'}
            
            # Clicar no botão conectar
            await connect_button.click()
            await self.random_delay(1, 2)
            
            # Verificar se apareceu modal de mensagem
            if message and await self.page.locator('button:has-text("Adicionar nota")').count() > 0:
                # Adicionar mensagem personalizada
                await self.page.click('button:has-text("Adicionar nota")')
                await self.random_delay(1, 2)
                
                # Preencher mensagem
                await self.page.fill('textarea[name="message"]', message)
                await self.random_delay(1, 2)
            
            # Enviar solicitação
            send_button = await self.page.locator('button:has-text("Enviar convite")').first
            if await send_button.count() > 0:
                await send_button.click()
                await self.random_delay(2, 3)
                
                self.automation_stats['connections_sent'] += 1
                self.automation_stats['last_activity'] = datetime.now().isoformat()
                
                logger.info("Solicitação de conexão enviada")
                
                return {
                    'success': True,
                    'message': 'Solicitação enviada com sucesso'
                }
            else:
                return {'success': False, 'error': 'Send button not found'}
                
        except Exception as e:
            logger.error(f"Erro ao enviar conexão: {e}")
            self.automation_stats['errors'] += 1
            return {
                'success': False,
                'error': f'Erro ao enviar conexão: {str(e)}'
            }
    
    async def view_profile(self, profile_index):
        """Visualiza um perfil específico"""
        try:
            results = await self.page.locator('[data-view-name="search-entity-result"]').all()
            
            if profile_index >= len(results):
                return {'success': False, 'error': 'Profile not found'}
            
            result = results[profile_index]
            
            # Encontrar link do perfil
            profile_link = await result.locator('.entity-result__title-text a').first
            
            if await profile_link.count() > 0:
                # Abrir perfil em nova aba
                async with self.page.context.expect_page() as new_page_info:
                    await profile_link.click(modifiers=['Ctrl'])
                
                new_page = await new_page_info.value
                await new_page.wait_for_load_state()
                await self.random_delay(3, 5)
                
                # Fechar aba
                await new_page.close()
                
                self.automation_stats['profiles_viewed'] += 1
                self.automation_stats['last_activity'] = datetime.now().isoformat()
                
                logger.info("Perfil visualizado")
                
                return {
                    'success': True,
                    'message': 'Perfil visualizado com sucesso'
                }
            else:
                return {'success': False, 'error': 'Profile link not found'}
                
        except Exception as e:
            logger.error(f"Erro ao visualizar perfil: {e}")
            self.automation_stats['errors'] += 1
            return {
                'success': False,
                'error': f'Erro ao visualizar perfil: {str(e)}'
            }
    
    async def run_automation(self, automation_config):
        """Executa automação completa baseada na configuração"""
        try:
            if not self.is_logged_in:
                return {'success': False, 'error': 'not_logged_in'}
            
            automation_type = automation_config.get('type')
            keywords = automation_config.get('keywords', '')
            max_actions = automation_config.get('max_actions', 25)
            message = automation_config.get('message', '')
            
            results = []
            
            if automation_type == 'feed_interactions':
                # Nova funcionalidade: interagir com feed
                return await self.interact_with_feed(max_actions)
            
            elif automation_type == 'feed_likes':
                # Nova funcionalidade: curtir posts no feed
                return await self.like_posts_in_feed(max_actions)
            
            elif automation_type == 'feed_comments':
                # Nova funcionalidade: comentar posts no feed
                comment_templates = automation_config.get('comment_templates', [])
                return await self.comment_on_posts(max_actions, comment_templates)
            
            else:
                # Automações baseadas em busca (conexões, visualizações)
                # Buscar pessoas
                search_result = await self.search_people(keywords, max_actions)
                
                if not search_result['success']:
                    return search_result
                
                profiles = search_result['profiles']
                
                # Executar ações baseadas no tipo
                for i, profile in enumerate(profiles):
                    try:
                        if automation_type == 'connection_requests':
                            if profile['can_connect']:
                                result = await self.send_connection_request(i, message)
                                results.append({
                                    'profile': profile['name'],
                                    'action': 'connection_request',
                                    'result': result
                                })
                        
                        elif automation_type == 'profile_views':
                            result = await self.view_profile(i)
                            results.append({
                                'profile': profile['name'],
                                'action': 'profile_view',
                                'result': result
                            })
                        
                        # Delay entre ações
                        await self.random_delay(3, 7)
                        
                    except Exception as e:
                        logger.error(f"Erro na ação {i}: {e}")
                        self.automation_stats['errors'] += 1
                        continue
                
                return {
                    'success': True,
                    'message': f'Automação concluída. {len(results)} ações executadas.',
                    'results': results,
                    'stats': self.automation_stats
                }
            
        except Exception as e:
            logger.error(f"Erro na automação: {e}")
            return {
                'success': False,
                'error': f'Erro na automação: {str(e)}'
            }
    
    async def random_delay(self, min_seconds=1, max_seconds=3):
        """Delay aleatório para simular comportamento humano"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    async def get_stats(self):
        """Retorna estatísticas da automação"""
        return {
            'success': True,
            'stats': {
                **self.automation_stats,
                'is_logged_in': self.is_logged_in,
                'profile': self.user_profile
            }
        }
    
    async def close(self):
        """Fecha o navegador"""
        try:
            if self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
            logger.info("Navegador fechado")
        except Exception as e:
            logger.error(f"Erro ao fechar navegador: {e}")

# Instância global do motor de automação
automation_engine = LinkedInAutomationEngine()
