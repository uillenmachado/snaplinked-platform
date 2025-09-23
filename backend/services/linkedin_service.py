#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SnapLinked v3.0 - Serviço LinkedIn
Integração com LinkedIn via OAuth e automação via Playwright
"""

import asyncio
import json
import logging
import random
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


class LinkedInOAuthService:
    """Serviço de autenticação OAuth do LinkedIn"""
    
    def __init__(self):
        self.client_id = Config.LINKEDIN_CLIENT_ID
        self.client_secret = Config.LINKEDIN_CLIENT_SECRET
        self.redirect_uri = Config.LINKEDIN_REDIRECT_URI
        self.base_url = 'https://www.linkedin.com/oauth/v2'
        self.api_url = 'https://api.linkedin.com/v2'
    
    def get_authorization_url(self, state: str = None) -> str:
        """Gerar URL de autorização OAuth"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'r_liteprofile r_emailaddress',
            'state': state or 'default_state'
        }
        return f"{self.base_url}/authorization?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """Trocar código de autorização por token de acesso"""
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
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Erro ao obter token: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erro na troca de código por token: {str(e)}")
            return None
    
    def get_user_profile(self, access_token: str) -> Optional[Dict]:
        """Obter perfil do usuário"""
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            
            # Obter informações básicas do perfil
            profile_response = requests.get(
                f"{self.api_url}/people/~",
                headers=headers
            )
            
            # Obter email
            email_response = requests.get(
                f"{self.api_url}/emailAddress?q=members&projection=(elements*(handle~))",
                headers=headers
            )
            
            if profile_response.status_code == 200 and email_response.status_code == 200:
                profile_data = profile_response.json()
                email_data = email_response.json()
                
                # Extrair email
                email = None
                if email_data.get('elements') and len(email_data['elements']) > 0:
                    email = email_data['elements'][0]['handle~']['emailAddress']
                
                return {
                    'id': profile_data.get('id'),
                    'first_name': profile_data.get('localizedFirstName', ''),
                    'last_name': profile_data.get('localizedLastName', ''),
                    'email': email,
                    'profile_picture': profile_data.get('profilePicture', {}).get('displayImage~', {}).get('elements', [{}])[-1].get('identifiers', [{}])[0].get('identifier')
                }
            else:
                logger.error(f"Erro ao obter perfil: {profile_response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao obter perfil do usuário: {str(e)}")
            return None


class LinkedInAutomationService:
    """Serviço de automação do LinkedIn usando Playwright"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.is_logged_in = False
        self.current_user_id: Optional[int] = None
    
    async def start_browser(self, headless: bool = True) -> bool:
        """Iniciar navegador"""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=headless,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1366, 'height': 768},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            self.page = await self.context.new_page()
            return True
        except Exception as e:
            logger.error(f"Erro ao iniciar navegador: {str(e)}")
            return False
    
    async def stop_browser(self):
        """Parar navegador"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
        except Exception as e:
            logger.error(f"Erro ao parar navegador: {str(e)}")
    
    async def login_manual(self, user_id: int) -> bool:
        """Login manual - usuário faz login através da interface"""
        try:
            self.current_user_id = user_id
            
            if not self.page:
                await self.start_browser(headless=False)
            
            # Navegar para LinkedIn
            await self.page.goto('https://www.linkedin.com/login')
            await self.page.wait_for_load_state('networkidle')
            
            # Aguardar login manual (verificar se está logado)
            for _ in range(60):  # Aguardar até 60 segundos
                current_url = self.page.url
                if 'feed' in current_url or 'in/' in current_url:
                    self.is_logged_in = True
                    logger.info("Login manual detectado com sucesso")
                    return True
                await asyncio.sleep(1)
            
            logger.warning("Timeout no login manual")
            return False
            
        except Exception as e:
            logger.error(f"Erro no login manual: {str(e)}")
            return False
    
    async def check_login_status(self) -> bool:
        """Verificar se está logado"""
        try:
            if not self.page:
                return False
            
            current_url = self.page.url
            if 'linkedin.com' not in current_url:
                await self.page.goto('https://www.linkedin.com/feed')
                await self.page.wait_for_load_state('networkidle')
            
            # Verificar elementos que indicam login
            try:
                await self.page.wait_for_selector('[data-control-name="nav.settings_and_privacy"]', timeout=5000)
                self.is_logged_in = True
                return True
            except:
                self.is_logged_in = False
                return False
                
        except Exception as e:
            logger.error(f"Erro ao verificar status de login: {str(e)}")
            return False
    
    async def like_posts(self, user_id: int, target_count: int = 3) -> Dict:
        """Curtir posts no feed"""
        session = AutomationSession(
            user_id=user_id,
            session_type='like',
            status='running',
            target_count=target_count,
            started_at=datetime.now(timezone.utc)
        )
        db.session.add(session)
        db.session.commit()
        
        results = {
            'success': False,
            'completed_count': 0,
            'error_count': 0,
            'errors': []
        }
        
        try:
            if not await self.check_login_status():
                raise Exception("Usuário não está logado no LinkedIn")
            
            # Navegar para o feed
            await self.page.goto('https://www.linkedin.com/feed/')
            await self.page.wait_for_load_state('networkidle')
            
            # Encontrar botões de curtir
            like_buttons = await self.page.query_selector_all('[data-control-name="like"]')
            
            completed = 0
            for i, button in enumerate(like_buttons[:target_count]):
                try:
                    # Verificar se já foi curtido
                    is_liked = await button.get_attribute('aria-pressed')
                    if is_liked == 'true':
                        continue
                    
                    # Scroll para o elemento
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Clicar no botão
                    await button.click()
                    completed += 1
                    
                    # Log da ação
                    log = AutomationLog(
                        user_id=user_id,
                        session_id=session.id,
                        action_type='like',
                        status='success',
                        message=f'Post curtido com sucesso (#{i+1})'
                    )
                    db.session.add(log)
                    
                    # Delay entre ações
                    await asyncio.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    results['error_count'] += 1
                    results['errors'].append(str(e))
                    
                    # Log do erro
                    log = AutomationLog(
                        user_id=user_id,
                        session_id=session.id,
                        action_type='like',
                        status='failed',
                        message=f'Erro ao curtir post: {str(e)}'
                    )
                    db.session.add(log)
            
            results['completed_count'] = completed
            results['success'] = completed > 0
            
            # Atualizar sessão
            session.status = 'completed'
            session.completed_count = completed
            session.error_count = results['error_count']
            session.completed_at = datetime.now(timezone.utc)
            
            # Atualizar estatísticas
            user_stats = UserStats.query.filter_by(user_id=user_id).first()
            if not user_stats:
                user_stats = UserStats(user_id=user_id)
                db.session.add(user_stats)
            user_stats.update_stats('like', completed)
            
            db.session.commit()
            
        except Exception as e:
            results['errors'].append(str(e))
            session.status = 'failed'
            session.error_count += 1
            db.session.commit()
            logger.error(f"Erro na automação de curtidas: {str(e)}")
        
        return results
    
    async def send_connection_requests(self, user_id: int, target_count: int = 2) -> Dict:
        """Enviar solicitações de conexão"""
        session = AutomationSession(
            user_id=user_id,
            session_type='connect',
            status='running',
            target_count=target_count,
            started_at=datetime.now(timezone.utc)
        )
        db.session.add(session)
        db.session.commit()
        
        results = {
            'success': False,
            'completed_count': 0,
            'error_count': 0,
            'errors': []
        }
        
        try:
            if not await self.check_login_status():
                raise Exception("Usuário não está logado no LinkedIn")
            
            # Navegar para "Minha rede"
            await self.page.goto('https://www.linkedin.com/mynetwork/')
            await self.page.wait_for_load_state('networkidle')
            
            # Encontrar botões de conectar
            connect_buttons = await self.page.query_selector_all('button[data-control-name="invite"]')
            
            completed = 0
            for i, button in enumerate(connect_buttons[:target_count]):
                try:
                    # Scroll para o elemento
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Clicar no botão
                    await button.click()
                    
                    # Aguardar modal e confirmar
                    try:
                        send_button = await self.page.wait_for_selector('button[aria-label*="Enviar"]', timeout=3000)
                        await send_button.click()
                        completed += 1
                        
                        # Log da ação
                        log = AutomationLog(
                            user_id=user_id,
                            session_id=session.id,
                            action_type='connect',
                            status='success',
                            message=f'Solicitação de conexão enviada (#{i+1})'
                        )
                        db.session.add(log)
                        
                    except:
                        # Fechar modal se não conseguir enviar
                        try:
                            close_button = await self.page.wait_for_selector('[data-control-name="overlay.close_conversation_window"]', timeout=1000)
                            await close_button.click()
                        except:
                            pass
                    
                    # Delay entre ações
                    await asyncio.sleep(random.uniform(3, 5))
                    
                except Exception as e:
                    results['error_count'] += 1
                    results['errors'].append(str(e))
                    
                    # Log do erro
                    log = AutomationLog(
                        user_id=user_id,
                        session_id=session.id,
                        action_type='connect',
                        status='failed',
                        message=f'Erro ao enviar conexão: {str(e)}'
                    )
                    db.session.add(log)
            
            results['completed_count'] = completed
            results['success'] = completed > 0
            
            # Atualizar sessão
            session.status = 'completed'
            session.completed_count = completed
            session.error_count = results['error_count']
            session.completed_at = datetime.now(timezone.utc)
            
            # Atualizar estatísticas
            user_stats = UserStats.query.filter_by(user_id=user_id).first()
            if not user_stats:
                user_stats = UserStats(user_id=user_id)
                db.session.add(user_stats)
            user_stats.update_stats('connect', completed)
            
            db.session.commit()
            
        except Exception as e:
            results['errors'].append(str(e))
            session.status = 'failed'
            session.error_count += 1
            db.session.commit()
            logger.error(f"Erro na automação de conexões: {str(e)}")
        
        return results
    
    async def comment_on_posts(self, user_id: int, target_count: int = 1) -> Dict:
        """Comentar em posts"""
        session = AutomationSession(
            user_id=user_id,
            session_type='comment',
            status='running',
            target_count=target_count,
            started_at=datetime.now(timezone.utc)
        )
        db.session.add(session)
        db.session.commit()
        
        # Comentários profissionais pré-definidos
        comments = [
            "Excelente conteúdo! Muito útil.",
            "Parabéns pela iniciativa!",
            "Concordo plenamente com sua visão.",
            "Muito interessante, obrigado por compartilhar!",
            "Ótima reflexão sobre o tema.",
        ]
        
        results = {
            'success': False,
            'completed_count': 0,
            'error_count': 0,
            'errors': []
        }
        
        try:
            if not await self.check_login_status():
                raise Exception("Usuário não está logado no LinkedIn")
            
            # Navegar para o feed
            await self.page.goto('https://www.linkedin.com/feed/')
            await self.page.wait_for_load_state('networkidle')
            
            # Encontrar botões de comentar
            comment_buttons = await self.page.query_selector_all('[data-control-name="comment"]')
            
            completed = 0
            for i, button in enumerate(comment_buttons[:target_count]):
                try:
                    # Scroll para o elemento
                    await button.scroll_into_view_if_needed()
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Clicar no botão de comentar
                    await button.click()
                    await asyncio.sleep(1)
                    
                    # Encontrar caixa de texto do comentário
                    comment_box = await self.page.wait_for_selector('.ql-editor[data-placeholder*="comentário"]', timeout=3000)
                    
                    # Escrever comentário
                    comment_text = random.choice(comments)
                    await comment_box.fill(comment_text)
                    await asyncio.sleep(1)
                    
                    # Publicar comentário
                    post_button = await self.page.wait_for_selector('button[data-control-name="comments.post_comment"]', timeout=3000)
                    await post_button.click()
                    
                    completed += 1
                    
                    # Log da ação
                    log = AutomationLog(
                        user_id=user_id,
                        session_id=session.id,
                        action_type='comment',
                        status='success',
                        message=f'Comentário publicado: "{comment_text}"',
                        metadata={'comment': comment_text}
                    )
                    db.session.add(log)
                    
                    # Delay entre ações
                    await asyncio.sleep(random.uniform(4, 6))
                    
                except Exception as e:
                    results['error_count'] += 1
                    results['errors'].append(str(e))
                    
                    # Log do erro
                    log = AutomationLog(
                        user_id=user_id,
                        session_id=session.id,
                        action_type='comment',
                        status='failed',
                        message=f'Erro ao comentar: {str(e)}'
                    )
                    db.session.add(log)
            
            results['completed_count'] = completed
            results['success'] = completed > 0
            
            # Atualizar sessão
            session.status = 'completed'
            session.completed_count = completed
            session.error_count = results['error_count']
            session.completed_at = datetime.now(timezone.utc)
            
            # Atualizar estatísticas
            user_stats = UserStats.query.filter_by(user_id=user_id).first()
            if not user_stats:
                user_stats = UserStats(user_id=user_id)
                db.session.add(user_stats)
            user_stats.update_stats('comment', completed)
            
            db.session.commit()
            
        except Exception as e:
            results['errors'].append(str(e))
            session.status = 'failed'
            session.error_count += 1
            db.session.commit()
            logger.error(f"Erro na automação de comentários: {str(e)}")
        
        return results


# Instâncias globais dos serviços
oauth_service = LinkedInOAuthService()
automation_service = LinkedInAutomationService()
