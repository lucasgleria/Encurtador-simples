# """
# Módulo principal do encurtador de URLs
# """
# import hashlib
# import time
# from typing import Optional, Dict, Any
# from datetime import datetime
# from .database import db_manager
# from .validators import URLValidator

# class URLShortener:
#     """Classe principal para encurtamento de URLs"""
    
#     def __init__(self):
#         self.url_prefix = "lleria"
#         self.validator = URLValidator()
        
#     def generate_short_code(self, original_url: str) -> str:
#         """
#         Gera um código único para a URL encurtada
        
#         Args:
#             original_url (str): URL original
            
#         Returns:
#             str: Código único para a URL encurtada
#         """
#         # Cria um hash baseado na URL original e timestamp
#         timestamp = str(int(time.time()))
#         hash_input = f"{original_url}{timestamp}"
        
#         # Gera hash MD5 e pega os primeiros 8 caracteres
#         hash_object = hashlib.md5(hash_input.encode())
#         hash_hex = hash_object.hexdigest()[:8]
        
#         # Retorna o código com prefixo
#         return f"{self.url_prefix}{hash_hex}"
    
#     def shorten_url(self, original_url: str) -> Dict[str, Any]:
#         """
#         Encurta uma URL
        
#         Args:
#             original_url (str): URL original a ser encurtada
            
#         Returns:
#             Dict[str, Any]: Dicionário com resultado da operação
#         """
#         try:
#             # Valida a URL
#             is_valid, error_message = self.validator.validate_url(original_url)
#             if not is_valid:
#                 return {
#                     'success': False,
#                     'error': error_message,
#                     'short_url': None,
#                     'original_url': original_url
#                 }
            
#             # Normaliza a URL
#             normalized_url = self.validator.normalize_url(original_url)
            
#             # Verifica se a URL já foi encurtada
#             existing_url = self.get_short_url_by_original(normalized_url)
#             if existing_url:
#                 return {
#                     'success': True,
#                     'short_url': existing_url['short_url'],
#                     'original_url': normalized_url,
#                     'already_exists': True
#                 }
            
#             # Gera código único
#             short_code = self.generate_short_code(normalized_url)
            
#             # Cria documento para salvar no MongoDB
#             url_document = {
#                 'original_url': normalized_url,
#                 'short_url': short_code,
#                 'created_at': datetime.now(),
#                 'created_timestamp': int(time.time())
#             }
            
#             # Salva no banco de dados
#             collection = db_manager.get_collection()
#             if collection is not None:
#                 result = collection.insert_one(url_document)
#                 if result.inserted_id:
#                     return {
#                         'success': True,
#                         'short_url': short_code,
#                         'original_url': normalized_url,
#                         'already_exists': False
#                     }
#                 else:
#                     return {
#                         'success': False,
#                         'error': 'Erro ao salvar no banco de dados',
#                         'short_url': None,
#                         'original_url': normalized_url
#                     }
#             else:
#                 return {
#                     'success': False,
#                     'error': 'Banco de dados não conectado',
#                     'short_url': None,
#                     'original_url': normalized_url
#                 }
                
#         except Exception as e:
#             return {
#                 'success': False,
#                 'error': f'Erro inesperado: {str(e)}',
#                 'short_url': None,
#                 'original_url': original_url
#             }
    
#     def get_original_url(self, short_url: str) -> Optional[str]:
#         """
#         Recupera a URL original a partir da URL encurtada
        
#         Args:
#             short_url (str): URL encurtada
            
#         Returns:
#             Optional[str]: URL original ou None se não encontrada
#         """
#         try:
#             collection = db_manager.get_collection()
#             if collection is not None:
#                 document = collection.find_one({'short_url': short_url})
#                 if document:
#                     return document['original_url']
#             return None
#         except Exception as e:
#             print(f"Erro ao recuperar URL original: {e}")
#             return None
    
#     def get_short_url_by_original(self, original_url: str) -> Optional[Dict[str, Any]]:
#         """
#         Recupera informações da URL encurtada a partir da URL original
        
#         Args:
#             original_url (str): URL original
            
#         Returns:
#             Optional[Dict[str, Any]]: Documento do MongoDB ou None se não encontrado
#         """
#         try:
#             collection = db_manager.get_collection()
#             if collection is not None:
#                 document = collection.find_one({'original_url': original_url})
#                 return document
#             return None
#         except Exception as e:
#             print(f"Erro ao recuperar URL encurtada: {e}")
#             return None
    
#     def get_all_urls(self) -> list:
#         """
#         Recupera todas as URLs encurtadas
        
#         Returns:
#             list: Lista de todas as URLs encurtadas
#         """
#         try:
#             collection = db_manager.get_collection()
#             if collection is not None:
#                 # Ordena por data de criação (mais recentes primeiro)
#                 documents = collection.find().sort('created_at', -1)
#                 return list(documents)
#             return []
#         except Exception as e:
#             print(f"Erro ao recuperar URLs: {e}")
#             return [] 

import hashlib
import time
from typing import Optional, Dict, Any
from datetime import datetime
from .database import db_manager
from .validators import URLValidator
# Importar exceções específicas do pymongo
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError

class URLShortener:
    """Classe principal para encurtamento de URLs"""

    def __init__(self):
        self.url_prefix = "lleria"
        self.validator = URLValidator()

    def generate_short_code(self, original_url: str) -> str:
        """
        Gera um código único para a URL encurtada

        Args:
            original_url (str): URL original

        Returns:
            str: Código único para a URL encurtada
        """
        # Cria um hash baseado na URL original e timestamp
        timestamp = str(int(time.time()))
        hash_input = f"{original_url}{timestamp}"

        # Gera hash MD5 e pega os primeiros 8 caracteres
        hash_object = hashlib.md5(hash_input.encode())
        hash_hex = hash_object.hexdigest()[:8]

        # Retorna o código com prefixo
        return f"{self.url_prefix}{hash_hex}"

    def shorten_url(self, original_url: str) -> Dict[str, Any]:
        """
        Encurta uma URL

        Args:
            original_url (str): URL original a ser encurtada

        Returns:
            Dict[str, Any]: Dicionário com resultado da operação
        """
        try:
            # Valida a URL
            is_valid, error_message = self.validator.validate_url(original_url)
            if not is_valid:
                return {
                    'success': False,
                    'error': error_message,
                    'short_url': None,
                    'original_url': original_url
                }

            # Normaliza a URL
            normalized_url = self.validator.normalize_url(original_url)

            # Verifica se a URL já foi encurtada
            existing_url_doc = self.get_short_url_by_original(normalized_url)
            if existing_url_doc:
                return {
                    'success': True,
                    'short_url': existing_url_doc['short_url'],
                    'original_url': normalized_url,
                    'already_exists': True
                }

            # --- Início da nova lógica para garantir código único ---
            short_code = ""
            max_attempts = 5  # Limita as tentativas
            base_url_for_hash = normalized_url # Usado para gerar o hash

            for attempt in range(max_attempts):
                current_hash_input = f"{base_url_for_hash}-{attempt}" # Adiciona contador para variar o hash
                short_code = self.generate_short_code(current_hash_input) # Usa generate_short_code com o input variado

                # Verifica se o código gerado já existe no banco de dados
                if not self.get_original_url(short_code):
                    break # Se não existir, podemos usar este código
            else: # Este else é executado se o loop terminar sem um 'break'
                return {
                    'success': False,
                    'error': 'Falha ao gerar um código único após múltiplas tentativas. Tente novamente.',
                    'short_url': None,
                    'original_url': original_url
                }
            # --- Fim da nova lógica ---

            # Cria documento para salvar no MongoDB
            url_document = {
                'original_url': normalized_url,
                'short_url': short_code,
                'created_at': datetime.now(),
                'created_timestamp': int(time.time())
            }

            # Salva no banco de dados
            collection = db_manager.get_collection()
            if collection is not None:
                result = collection.insert_one(url_document)
                if result.inserted_id:
                    return {
                        'success': True,
                        'short_url': short_code,
                        'original_url': normalized_url,
                        'already_exists': False
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Erro ao salvar no banco de dados',
                        'short_url': None,
                        'original_url': normalized_url
                    }
            else:
                return {
                    'success': False,
                    'error': 'Banco de dados não conectado. Verifique sua conexão.',
                    'short_url': None,
                    'original_url': normalized_url
                }

        except (ConnectionFailure, OperationFailure, PyMongoError) as e:
            # Erros específicos do PyMongo
            return {
                'success': False,
                'error': f'Erro de banco de dados: {str(e)}. Verifique se o MongoDB está rodando.',
                'short_url': None,
                'original_url': original_url
            }
        except Exception as e:
            # Outros erros inesperados
            return {
                'success': False,
                'error': f'Erro inesperado: {str(e)}',
                'short_url': None,
                'original_url': original_url
            }

    def get_original_url(self, short_url: str) -> Optional[str]:
        """
        Recupera a URL original a partir da URL encurtada

        Args:
            short_url (str): URL encurtada

        Returns:
            Optional[str]: URL original ou None se não encontrada
        """
        try:
            collection = db_manager.get_collection()
            if collection is not None:
                document = collection.find_one({'short_url': short_url})
                if document:
                    return document['original_url']
            return None
        except (ConnectionFailure, OperationFailure, PyMongoError) as e:
            print(f"Erro de banco de dados ao recuperar URL original: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao recuperar URL original: {e}")
            return None

    def get_short_url_by_original(self, original_url: str) -> Optional[Dict[str, Any]]:
        """
        Recupera informações da URL encurtada a partir da URL original

        Args:
            original_url (str): URL original

        Returns:
            Optional[Dict[str, Any]]: Documento do MongoDB ou None se não encontrado
        """
        try:
            collection = db_manager.get_collection()
            if collection is not None:
                document = collection.find_one({'original_url': original_url})
                return document
            return None
        except (ConnectionFailure, OperationFailure, PyMongoError) as e:
            print(f"Erro de banco de dados ao recuperar URL encurtada: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao recuperar URL encurtada: {e}")
            return None

    def get_all_urls(self) -> list:
        """
        Recupera todas as URLs encurtadas

        Returns:
            list: Lista de todas as URLs encurtadas
        """
        try:
            collection = db_manager.get_collection()
            if collection is not None:
                # Ordena por data de criação (mais recentes primeiro)
                documents = collection.find().sort('created_at', -1)
                return list(documents)
            return []
        except (ConnectionFailure, OperationFailure, PyMongoError) as e:
            print(f"Erro de banco de dados ao recuperar URLs: {e}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao recuperar URLs: {e}")
            return []