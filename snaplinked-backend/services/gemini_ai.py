"""
SnapLinked - Serviço Gemini AI Real
Implementação completa da integração com Google Gemini AI
"""
import os
import google.generativeai as genai
import logging
import json
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class GeminiAI:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            logger.error("GEMINI_API_KEY não configurada")
            raise ValueError("GEMINI_API_KEY é obrigatória")
        
        # Configurar Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Templates de prompts
        self.comment_templates = {
            'profissional': """
            Como um profissional experiente no LinkedIn, gere um comentário contextual e engajador para este post:
            
            Contexto do Post: {context}
            
            Diretrizes:
            - Tom profissional e respeitoso
            - Máximo 150 caracteres
            - Adicione valor à discussão
            - Use emojis moderadamente (máximo 2)
            - Seja autêntico e relevante
            - Evite ser genérico
            
            Responda apenas com o comentário, sem explicações adicionais.
            """,
            
            'casual': """
            Gere um comentário casual e amigável para este post do LinkedIn:
            
            Contexto: {context}
            
            Estilo:
            - Tom casual mas profissional
            - Máximo 100 caracteres
            - Use emojis (2-3)
            - Seja genuíno
            - Mostre interesse real
            
            Apenas o comentário:
            """,
            
            'especialista': """
            Como especialista na área, comente este post com insights valiosos:
            
            Post: {context}
            
            Características:
            - Demonstre conhecimento técnico
            - Máximo 200 caracteres
            - Adicione perspectiva única
            - Tom de autoridade mas acessível
            - 1-2 emojis relevantes
            
            Comentário:
            """
        }
    
    def generate_comment(self, context, tone='profissional', max_length=150):
        """Gera comentário contextual usando Gemini AI"""
        try:
            # Selecionar template baseado no tom
            template = self.comment_templates.get(tone, self.comment_templates['profissional'])
            prompt = template.format(context=context)
            
            # Gerar resposta
            response = self.model.generate_content(prompt)
            
            if response.text:
                comment = response.text.strip()
                
                # Limitar tamanho
                if len(comment) > max_length:
                    comment = comment[:max_length-3] + "..."
                
                logger.info(f"Comentário gerado: {comment[:50]}...")
                return {
                    'success': True,
                    'comment': comment,
                    'tone': tone,
                    'model': 'gemini-1.5-flash',
                    'length': len(comment)
                }
            else:
                logger.error("Gemini não retornou texto")
                return {
                    'success': False,
                    'error': 'Gemini não gerou resposta'
                }
                
        except Exception as e:
            logger.error(f"Erro ao gerar comentário: {str(e)}")
            return {
                'success': False,
                'error': f"Erro Gemini AI: {str(e)}"
            }
    
    def generate_post_content(self, topic, style='profissional'):
        """Gera conteúdo para post LinkedIn"""
        try:
            prompt = f"""
            Crie um post profissional para LinkedIn sobre: {topic}
            
            Estilo: {style}
            Requisitos:
            - Entre 100-300 palavras
            - Tom engajador
            - Call-to-action no final
            - Use hashtags relevantes (3-5)
            - Estrutura clara com parágrafos
            
            Post:
            """
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                content = response.text.strip()
                logger.info(f"Post gerado sobre: {topic}")
                return {
                    'success': True,
                    'content': content,
                    'topic': topic,
                    'style': style,
                    'word_count': len(content.split())
                }
            else:
                return {
                    'success': False,
                    'error': 'Falha ao gerar conteúdo'
                }
                
        except Exception as e:
            logger.error(f"Erro ao gerar post: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_post_sentiment(self, text):
        """Analisa sentimento de um post"""
        try:
            prompt = f"""
            Analise o sentimento deste post do LinkedIn:
            
            "{text}"
            
            Retorne apenas um JSON com:
            {{
                "sentiment": "positivo/neutro/negativo",
                "confidence": 0.0-1.0,
                "keywords": ["palavra1", "palavra2"],
                "tone": "profissional/casual/formal"
            }}
            """
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                # Tentar extrair JSON da resposta
                try:
                    result = json.loads(response.text.strip())
                    return {
                        'success': True,
                        'analysis': result
                    }
                except json.JSONDecodeError:
                    return {
                        'success': False,
                        'error': 'Resposta não é JSON válido'
                    }
            else:
                return {
                    'success': False,
                    'error': 'Sem resposta do Gemini'
                }
                
        except Exception as e:
            logger.error(f"Erro na análise de sentimento: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def suggest_hashtags(self, content):
        """Sugere hashtags relevantes para o conteúdo"""
        try:
            prompt = f"""
            Sugira 5-8 hashtags relevantes para este conteúdo LinkedIn:
            
            "{content}"
            
            Retorne apenas os hashtags separados por vírgula, sem explicações.
            Exemplo: #marketing, #vendas, #linkedin
            """
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                hashtags = [tag.strip() for tag in response.text.strip().split(',')]
                return {
                    'success': True,
                    'hashtags': hashtags,
                    'count': len(hashtags)
                }
            else:
                return {
                    'success': False,
                    'error': 'Falha ao gerar hashtags'
                }
                
        except Exception as e:
            logger.error(f"Erro ao sugerir hashtags: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_connection(self):
        """Testa conexão com Gemini AI"""
        try:
            response = self.model.generate_content("Diga apenas 'OK' se você está funcionando.")
            
            if response.text and 'OK' in response.text:
                return {
                    'success': True,
                    'message': 'Gemini AI conectado e funcionando',
                    'model': 'gemini-1.5-flash'
                }
            else:
                return {
                    'success': False,
                    'error': 'Resposta inesperada do Gemini'
                }
                
        except Exception as e:
            logger.error(f"Erro no teste de conexão: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

# Instância global
gemini_ai = GeminiAI()
