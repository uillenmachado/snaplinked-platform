#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Serviço LinkedIn Seguro
Integração com LinkedIn via OAuth e automação via Playwright com segurança aprimorada
"""

import asyncio
import json
import logging
import secrets
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlencode, parse_qs, urlparse

import requests
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from config import Config
from models import db, User, AutomationSession, AutomationLog, UserStats

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecureRandomGenerator:
    """Gerador de números aleatórios seguro para automação"""
    
    @staticmethod
    def uniform(min_val: float, max_val: float) -> float:
        """Gerar float aleatório seguro entre min_val e max_val"""
        # Usar secrets para gerar número seguro
        random_bytes = secrets.randbits(32)
        # Normalizar para range 0-1
        normalized = random_bytes / (2**32 - 1)
        # Escalar para range desejado
        return min_val + (max_val - min_val) * normalized
    
    @staticmethod
    def choice(sequence: List) -> any:
        """Escolher elemento aleatório seguro de uma sequência"""
        if not sequence:
            raise ValueError("Sequence cannot be empty")
        
        # Gerar índice seguro
        index = secrets.randbelow(len(sequence))
        return sequence[index]
    
    @staticmethod
    def randint(min_val: int, max_val: int) -> int:
        """Gerar inteiro aleatório seguro entre min_val e max_val (inclusive)"""
        if min_val > max_val:
            raise ValueError("min_val must be <= max_val")
        
        range_size = max_val - min_val + 1
        return min_val + secrets.randbelow(range_size)


class LinkedInOAuthService:
    """Serviço de autenticação OAuth do LinkedIn com segurança aprimorada"""
    
    def __init__(self):
        self.client_id = Config.LINKEDIN_CLIENT_ID
        self.client_secret = Config.LINKEDIN_CLIENT_SECRET
        self.redirect_uri = Config.LINKEDIN_REDIRECT_URI
        self.base_url = 'https://www.linkedin.com/oauth/v2'
        self.api_url = 'https://api.linkedin.com/v2'
        
        # Validar configurações
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            logger.warning("LinkedIn OAuth not fully configured")
    
    def get_authorization_url(self, state: str = None) -> str:
        """Gerar URL de autorização OAuth com state seguro"""
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'r_liteprofile r_emailaddress',
            'state': state
        }
        return f"{self.base_url}/authorization?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """Trocar código de autorização por token de acesso com validação"""
        if not code or len(code) < 10:
            logger.error("Invalid authorization code provided")
            return None
        
        try:
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            
            response = requests.post(
                f"{self.base_url}/accessToken",
                data=data,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'SnapLinked/3.0'
                },
                timeout=30
            )
            
            if response.status_code == 200:
                token_data = response.json()
                # Validar resposta
                if 'access_token' in token_data:
                    return token_data
                else:
                    logger.error("Invalid token response format")
                    return None
            else:
                logger.error(f"Token exchange failed: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Network error during token exchange: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in token exchange: {str(e)}")
            return None
    
    def get_user_profile(self, access_token: str) -> Optional[Dict]:
        """Obter perfil do usuário com validação de token"""
        if not access_token or len(access_token) < 10:
            logger.error("Invalid access token provided")
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'User-Agent': 'SnapLinked/3.0'
            }
            
            # Obter informações básicas do perfil
            profile_response = requests.get(
                f"{self.api_url}/people/~",
                headers=headers,
                timeout=30
            )
            
            if profile_response.status_code != 200:
                logger.error(f"Profile request failed: {profile_response.status_code}")
                return None
            
            profile_data = profile_response.json()
            
            # Obter email
            email_response = requests.get(
                f"{self.api_url}/emailAddress?q=members&projection=(elements*(handle~))",
                headers=headers,
                timeout=30
            )
            
            email_data = {}
            if email_response.status_code == 200:
                email_data = email_response.json()
            
            # Combinar dados
            user_data = {
                'id': profile_data.get('id'),
                'name': f"{profile_data.get('firstName', {}).get('localized', {}).get('en_US', '')} {profile_data.get('lastName', {}).get('localized', {}).get('en_US', '')}".strip(),
                'email': self._extract_email(email_data),
                'profile_picture': profile_data.get('profilePicture', {}).get('displayImage~', {}).get('elements', [{}])[-1].get('identifiers', [{}])[0].get('identifier')
            }
            
            return user_data
            
        except requests.RequestException as e:
            logger.error(f"Network error getting user profile: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting user profile: {str(e)}")
            return None
    
    def _extract_email(self, email_data: Dict) -> Optional[str]:
        """Extrair email dos dados da API"""
        try:
            elements = email_data.get('elements', [])
            if elements:
                handle = elements[0].get('handle~', {})
                return handle.get('emailAddress')
        except (KeyError, IndexError, TypeError):
            pass
        return None


class LinkedInAutomationService:
    """Serviço de automação do LinkedIn com segurança aprimorada"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.is_logged_in = False
        self.current_user_id = None
        self.secure_random = SecureRandomGenerator()
        
        # Comentários seguros para posts
        self.safe_comments = [
            "Excelente conteúdo! 👏",
            "Muito interessante, obrigado por compartilhar!",
            "Perspectiva valiosa! 💡",
            "Concordo completamente!",
            "Ótima reflexão! 🎯",
            "Conteúdo de qualidade!",
            "Muito bem colocado!",
            "Inspirador! ✨"
        ]
    
    async def initialize_browser(self) -> bool:
        """Inicializar navegador com configurações seguras"""
        try:
            playwright = await async_playwright().start()
            
            # Configurações de segurança do navegador
            self.browser = await playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-images',  # Economizar banda
                    '--disable-javascript-harmony-shipping',
                    '--disable-background-timer-throttling',
                    '--disable-renderer-backgrounding',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-ipc-flooding-protection',
                    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
            )
            
            # Criar contexto com configurações de privacidade
            self.context = await self.browser.new_context(
                viewport={'width': 1366, 'height': 768},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='pt-BR',
                timezone_id='America/Sao_Paulo',
                permissions=['notifications'],
                extra_http_headers={
                    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'DNT': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Upgrade-Insecure-Requests': '1'
                }
            )
            
            self.page = await self.context.new_page()
            
            # Configurar timeouts
            self.page.set_default_timeout(30000)
            self.page.set_default_navigation_timeout(30000)
            
            logger.info("Browser initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing browser: {str(e)}")
            await self.cleanup()
            return False
    
    async def login_manual(self, user_id: int) -> bool:
        """Login manual no LinkedIn com validação"""
        try:
            if not self.browser:
                if not await self.initialize_browser():
                    return False
            
            self.current_user_id = user_id
            
            # Navegar para LinkedIn
            await self.page.goto('https://www.linkedin.com/login', wait_until='networkidle')
            
            # Aguardar elementos de login
            await self.page.wait_for_selector('input[name="session_key"]', timeout=10000)
            await self.page.wait_for_selector('input[name="session_password"]', timeout=10000)
            
            logger.info(f"LinkedIn login page loaded for user {user_id}")
            
            # Aguardar login manual (simulado - em produção seria real)
            await asyncio.sleep(self.secure_random.uniform(2, 4))
            
            # Verificar se login foi bem-sucedido
            try:
                await self.page.wait_for_url('**/feed/**', timeout=30000)
                self.is_logged_in = True
                logger.info(f"Manual login successful for user {user_id}")
                return True
            except Exception:
                # Tentar verificar por outros indicadores
                feed_elements = await self.page.query_selector_all('[data-test-id="feed-container"], .feed-container, #main')
                if feed_elements:
                    self.is_logged_in = True
                    logger.info(f"Manual login successful for user {user_id} (alternative check)")
                    return True
                
                logger.warning(f"Manual login may have failed for user {user_id}")
                return False
            
        except Exception as e:
            logger.error(f"Error in manual login: {str(e)}")
            return False
    
    async def like_posts(self, user_id: int, target_count: int = 3) -> Dict[str, any]:
        """Curtir posts com validação e segurança"""
        if not self.is_logged_in:
            return {'success': False, 'message': 'Usuário não está logado'}
        
        try:
            # Criar sessão de automação
            session = AutomationSession(
                user_id=user_id,
                action_type='like',
                target_count=target_count,
                status='running'
            )
            db.session.add(session)
            db.session.commit()
            
            # Navegar para feed se necessário
            if not self.page.url.endswith('/feed/'):
                await self.page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
            
            # Aguardar carregamento do feed
            await self.page.wait_for_selector('[data-test-id="like-button"], button[aria-label*="curtir"], button[aria-label*="like"]', timeout=15000)
            
            liked_count = 0
            attempts = 0
            max_attempts = target_count * 3  # Máximo de tentativas
            
            while liked_count < target_count and attempts < max_attempts:
                attempts += 1
                
                try:
                    # Buscar botões de curtir não clicados
                    like_buttons = await self.page.query_selector_all(
                        'button[aria-label*="curtir"]:not([aria-pressed="true"]), '
                        'button[aria-label*="like"]:not([aria-pressed="true"]), '
                        '[data-test-id="like-button"]:not(.active)'
                    )
                    
                    if not like_buttons:
                        # Scroll para carregar mais posts
                        await self.page.evaluate('window.scrollBy(0, 800)')
                        await asyncio.sleep(self.secure_random.uniform(2, 3))
                        continue
                    
                    # Selecionar botão aleatório
                    button_index = self.secure_random.randint(0, min(len(like_buttons) - 1, 2))
                    button = like_buttons[button_index]
                    
                    # Scroll para o botão
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(self.secure_random.uniform(1, 2))
                    
                    # Clicar no botão
                    await button.click()
                    liked_count += 1
                    
                    # Log da ação
                    log_entry = AutomationLog(
                        session_id=session.id,
                        user_id=user_id,
                        action='like',
                        target_element='post',
                        success=True,
                        details={'post_index': attempts, 'button_index': button_index}
                    )
                    db.session.add(log_entry)
                    
                    logger.info(f"Post liked successfully ({liked_count}/{target_count})")
                    
                    # Delay entre ações para parecer humano
                    await asyncio.sleep(self.secure_random.uniform(2, 4))
                    
                except Exception as e:
                    logger.warning(f"Error liking post: {str(e)}")
                    # Continuar tentando outros posts
                    continue
            
            # Atualizar sessão
            session.actual_count = liked_count
            session.status = 'completed' if liked_count > 0 else 'failed'
            session.completed_at = datetime.now(timezone.utc)
            
            # Atualizar estatísticas do usuário
            stats = UserStats.query.filter_by(user_id=user_id).first()
            if stats:
                stats.total_likes += liked_count
                stats.updated_at = datetime.now(timezone.utc)
            
            db.session.commit()
            
            return {
                'success': liked_count > 0,
                'count': liked_count,
                'target': target_count,
                'message': f'Curtiu {liked_count} de {target_count} posts solicitados'
            }
            
        except Exception as e:
            logger.error(f"Error in like_posts: {str(e)}")
            # Marcar sessão como falha
            if 'session' in locals():
                session.status = 'failed'
                session.error_message = str(e)
                db.session.commit()
            
            return {
                'success': False,
                'count': 0,
                'message': f'Erro na automação: {str(e)}'
            }
    
    async def send_connections(self, user_id: int, target_count: int = 2) -> Dict[str, any]:
        """Enviar solicitações de conexão com validação"""
        if not self.is_logged_in:
            return {'success': False, 'message': 'Usuário não está logado'}
        
        try:
            # Criar sessão de automação
            session = AutomationSession(
                user_id=user_id,
                action_type='connect',
                target_count=target_count,
                status='running'
            )
            db.session.add(session)
            db.session.commit()
            
            # Navegar para página de pessoas sugeridas
            await self.page.goto('https://www.linkedin.com/mynetwork/', wait_until='networkidle')
            
            # Aguardar carregamento
            await self.page.wait_for_selector('button[aria-label*="Conectar"], button[data-test-id="connect-button"]', timeout=15000)
            
            connected_count = 0
            attempts = 0
            max_attempts = target_count * 3
            
            while connected_count < target_count and attempts < max_attempts:
                attempts += 1
                
                try:
                    # Buscar botões de conectar
                    connect_buttons = await self.page.query_selector_all(
                        'button[aria-label*="Conectar"]:not(:disabled), '
                        'button[data-test-id="connect-button"]:not(:disabled)'
                    )
                    
                    if not connect_buttons:
                        # Scroll para carregar mais sugestões
                        await self.page.evaluate('window.scrollBy(0, 600)')
                        await asyncio.sleep(self.secure_random.uniform(2, 3))
                        continue
                    
                    # Selecionar botão aleatório
                    button_index = self.secure_random.randint(0, min(len(connect_buttons) - 1, 1))
                    button = connect_buttons[button_index]
                    
                    # Scroll para o botão
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(self.secure_random.uniform(1, 2))
                    
                    # Clicar no botão
                    await button.click()
                    
                    # Verificar se apareceu modal de personalização
                    try:
                        send_button = await self.page.wait_for_selector(
                            'button[aria-label*="Enviar"], button[data-test-id="send-invite"]',
                            timeout=3000
                        )
                        if send_button:
                            await send_button.click()
                    except Exception:
                        # Modal pode não aparecer, continuar
                        pass
                    
                    # Verificar se apareceu modal de "fechar"
                    try:
                        close_button = await self.page.wait_for_selector(
                            'button[aria-label*="Fechar"], button[data-test-id="close"]',
                            timeout=2000
                        )
                        if close_button:
                            await close_button.click()
                    except Exception:
                        # Ignorar se não houver modal
                        pass
                    
                    connected_count += 1
                    
                    # Log da ação
                    log_entry = AutomationLog(
                        session_id=session.id,
                        user_id=user_id,
                        action='connect',
                        target_element='profile',
                        success=True,
                        details={'attempt': attempts, 'button_index': button_index}
                    )
                    db.session.add(log_entry)
                    
                    logger.info(f"Connection sent successfully ({connected_count}/{target_count})")
                    
                    # Delay entre ações
                    await asyncio.sleep(self.secure_random.uniform(3, 5))
                    
                except Exception as e:
                    logger.warning(f"Error sending connection: {str(e)}")
                    continue
            
            # Atualizar sessão
            session.actual_count = connected_count
            session.status = 'completed' if connected_count > 0 else 'failed'
            session.completed_at = datetime.now(timezone.utc)
            
            # Atualizar estatísticas
            stats = UserStats.query.filter_by(user_id=user_id).first()
            if stats:
                stats.total_connections += connected_count
                stats.updated_at = datetime.now(timezone.utc)
            
            db.session.commit()
            
            return {
                'success': connected_count > 0,
                'count': connected_count,
                'target': target_count,
                'message': f'Enviou {connected_count} de {target_count} solicitações de conexão'
            }
            
        except Exception as e:
            logger.error(f"Error in send_connections: {str(e)}")
            if 'session' in locals():
                session.status = 'failed'
                session.error_message = str(e)
                db.session.commit()
            
            return {
                'success': False,
                'count': 0,
                'message': f'Erro na automação: {str(e)}'
            }
    
    async def comment_posts(self, user_id: int, target_count: int = 1) -> Dict[str, any]:
        """Comentar em posts com validação"""
        if not self.is_logged_in:
            return {'success': False, 'message': 'Usuário não está logado'}
        
        try:
            # Criar sessão de automação
            session = AutomationSession(
                user_id=user_id,
                action_type='comment',
                target_count=target_count,
                status='running'
            )
            db.session.add(session)
            db.session.commit()
            
            # Navegar para feed
            if not self.page.url.endswith('/feed/'):
                await self.page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
            
            # Aguardar carregamento
            await self.page.wait_for_selector('button[aria-label*="comentar"], button[aria-label*="comment"]', timeout=15000)
            
            commented_count = 0
            attempts = 0
            max_attempts = target_count * 5
            
            while commented_count < target_count and attempts < max_attempts:
                attempts += 1
                
                try:
                    # Buscar botões de comentar
                    comment_buttons = await self.page.query_selector_all(
                        'button[aria-label*="comentar"], button[aria-label*="comment"]'
                    )
                    
                    if not comment_buttons:
                        await self.page.evaluate('window.scrollBy(0, 800)')
                        await asyncio.sleep(self.secure_random.uniform(2, 3))
                        continue
                    
                    # Selecionar botão aleatório
                    button_index = self.secure_random.randint(0, min(len(comment_buttons) - 1, 2))
                    button = comment_buttons[button_index]
                    
                    # Scroll para o botão
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(self.secure_random.uniform(1, 2))
                    
                    # Clicar no botão de comentar
                    await button.click()
                    
                    # Aguardar caixa de comentário aparecer
                    comment_box = await self.page.wait_for_selector(
                        'div[contenteditable="true"], textarea[placeholder*="comentário"]',
                        timeout=5000
                    )
                    
                    if comment_box:
                        # Escrever comentário
                        comment_text = self.secure_random.choice(self.safe_comments)
                        await comment_box.fill(comment_text)
                        
                        # Aguardar um pouco antes de enviar
                        await asyncio.sleep(self.secure_random.uniform(1, 2))
                        
                        # Buscar e clicar no botão de enviar
                        send_button = await self.page.wait_for_selector(
                            'button[data-test-id="comment-submit"], button[type="submit"]',
                            timeout=3000
                        )
                        
                        if send_button:
                            await send_button.click()
                            commented_count += 1
                            
                            # Log da ação
                            log_entry = AutomationLog(
                                session_id=session.id,
                                user_id=user_id,
                                action='comment',
                                target_element='post',
                                success=True,
                                details={'comment': comment_text, 'attempt': attempts}
                            )
                            db.session.add(log_entry)
                            
                            logger.info(f"Comment posted successfully ({commented_count}/{target_count})")
                            
                            # Delay entre ações
                            await asyncio.sleep(self.secure_random.uniform(4, 6))
                    
                except Exception as e:
                    logger.warning(f"Error commenting on post: {str(e)}")
                    continue
            
            # Atualizar sessão
            session.actual_count = commented_count
            session.status = 'completed' if commented_count > 0 else 'failed'
            session.completed_at = datetime.now(timezone.utc)
            
            # Atualizar estatísticas
            stats = UserStats.query.filter_by(user_id=user_id).first()
            if stats:
                stats.total_comments += commented_count
                stats.updated_at = datetime.now(timezone.utc)
            
            db.session.commit()
            
            return {
                'success': commented_count > 0,
                'count': commented_count,
                'target': target_count,
                'message': f'Comentou em {commented_count} de {target_count} posts'
            }
            
        except Exception as e:
            logger.error(f"Error in comment_posts: {str(e)}")
            if 'session' in locals():
                session.status = 'failed'
                session.error_message = str(e)
                db.session.commit()
            
            return {
                'success': False,
                'count': 0,
                'message': f'Erro na automação: {str(e)}'
            }
    
    async def cleanup(self):
        """Limpar recursos do navegador"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            
            self.page = None
            self.context = None
            self.browser = None
            self.is_logged_in = False
            self.current_user_id = None
            
            logger.info("Browser cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")


# Instâncias globais dos serviços
oauth_service = LinkedInOAuthService()
automation_service = LinkedInAutomationService()

# Alias para compatibilidade
LinkedInService = LinkedInAutomationService
