"""
SnapLinked - Serviço de Automação LinkedIn
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
            if not self.page:
                await self.initialize_browser()
            
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
                'logged_in_at': datetime.now().isoformat()
            }
            
            logger.info(f"Perfil obtido: {name}")
            
        except Exception as e:
            logger.error(f"Erro ao obter perfil: {e}")
            self.user_profile = {
                'name': 'Usuário LinkedIn',
                'headline': '',
                'logged_in_at': datetime.now().isoformat()
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
