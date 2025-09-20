from flask import Blueprint, request, jsonify
import asyncio
import threading
from simple_linkedin_login import simple_login

simple_login_bp = Blueprint('simple_login', __name__)

def run_async_in_thread(coro):
    """Executa função async em thread separada"""
    result = {'data': None, 'error': None}
    
    def run():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result['data'] = loop.run_until_complete(coro)
        except Exception as e:
            result['error'] = str(e)
        finally:
            try:
                loop.close()
            except:
                pass
    
    thread = threading.Thread(target=run)
    thread.start()
    thread.join(timeout=120)  # Timeout de 2 minutos
    
    if thread.is_alive():
        return {'success': False, 'error': 'Timeout na operação'}
    
    if result['error']:
        return {'success': False, 'error': result['error']}
    
    return result['data']

@simple_login_bp.route('/api/simple-login', methods=['POST'])
def simple_linkedin_login():
    """Login simples no LinkedIn"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email e senha são obrigatórios'
            }), 400
        
        # Executar login
        result = run_async_in_thread(simple_login.login(email, password))
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro no login: {str(e)}'
        }), 500

@simple_login_bp.route('/api/simple-like', methods=['POST'])
def simple_like_posts():
    """Curtir posts usando login simples"""
    try:
        data = request.get_json() or {}
        max_likes = data.get('max_likes', 3)
        
        # Executar curtidas
        result = run_async_in_thread(simple_login.like_posts(max_likes))
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao curtir posts: {str(e)}'
        }), 500

@simple_login_bp.route('/api/simple-comment', methods=['POST'])
def simple_comment_posts():
    """Comentar em posts usando login simples"""
    try:
        data = request.get_json() or {}
        max_comments = data.get('max_comments', 2)
        comment_text = data.get('comment', 'Excelente conteúdo! 👏')
        
        # Executar comentários
        result = run_async_in_thread(simple_login.comment_posts(max_comments, comment_text))
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao comentar posts: {str(e)}'
        }), 500

@simple_login_bp.route('/api/simple-status', methods=['GET'])
def simple_status():
    """Status do login simples"""
    try:
        return jsonify({
            'success': True,
            'logged_in': simple_login.is_logged_in,
            'page_url': simple_login.page.url if simple_login.page else None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao obter status: {str(e)}'
        }), 500


@simple_login_bp.route('/api/simple-connect', methods=['POST'])
def simple_connect_people():
    """Enviar solicitações de conexão usando login simples"""
    try:
        data = request.get_json() or {}
        keywords = data.get('keywords', 'desenvolvedor')
        max_connections = data.get('max_connections', 3)
        message = data.get('message', 'Olá! Gostaria de conectar para expandir nossa rede profissional.')
        
        # Executar conexões
        result = run_async_in_thread(simple_login.send_connections(keywords, max_connections, message))
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao enviar conexões: {str(e)}'
        }), 500
