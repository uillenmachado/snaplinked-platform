from flask import Blueprint, request, jsonify
import asyncio
import threading
from linkedin_automation_engine import automation_engine

feed_actions_bp = Blueprint('feed_actions', __name__)

def run_async_in_thread(coro):
    """Executa função async em thread separada"""
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()
    
    thread = threading.Thread(target=run)
    thread.start()
    thread.join()
    return run()

@feed_actions_bp.route('/api/feed/like-posts', methods=['POST'])
def like_posts():
    """Curtir posts no feed do LinkedIn"""
    try:
        data = request.get_json() or {}
        max_likes = data.get('max_likes', 5)
        
        # Verificar se está logado
        if not automation_engine.is_logged_in:
            return jsonify({
                'success': False,
                'error': 'LinkedIn não conectado. Faça login primeiro.'
            }), 400
        
        # Executar curtidas de forma assíncrona
        def execute_likes():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    automation_engine.like_posts(max_likes=max_likes)
                )
                return result
            finally:
                loop.close()
        
        # Executar em thread separada para não bloquear Flask
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(execute_likes)
            result = future.result(timeout=60)  # Timeout de 60 segundos
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao curtir posts: {str(e)}'
        }), 500

@feed_actions_bp.route('/api/feed/comment-posts', methods=['POST'])
def comment_posts():
    """Comentar em posts no feed do LinkedIn"""
    try:
        data = request.get_json() or {}
        max_comments = data.get('max_comments', 3)
        comment_templates = data.get('comment_templates', None)
        
        # Verificar se está logado
        if not automation_engine.is_logged_in:
            return jsonify({
                'success': False,
                'error': 'LinkedIn não conectado. Faça login primeiro.'
            }), 400
        
        # Executar comentários de forma assíncrona
        def execute_comments():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    automation_engine.comment_on_posts(
                        max_comments=max_comments,
                        comment_templates=comment_templates
                    )
                )
                return result
            finally:
                loop.close()
        
        # Executar em thread separada para não bloquear Flask
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(execute_comments)
            result = future.result(timeout=90)  # Timeout de 90 segundos
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao comentar posts: {str(e)}'
        }), 500

@feed_actions_bp.route('/api/feed/status', methods=['GET'])
def get_feed_status():
    """Obter status das ações no feed"""
    try:
        return jsonify({
            'success': True,
            'logged_in': automation_engine.is_logged_in,
            'stats': automation_engine.automation_stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao obter status: {str(e)}'
        }), 500
