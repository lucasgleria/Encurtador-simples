"""
Módulo de validação de URLs
"""
import validators
from typing import Tuple

class URLValidator:
    """Classe para validação de URLs"""
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, str]:
        """
        Valida se uma URL é válida
        
        Args:
            url (str): URL a ser validada
            
        Returns:
            Tuple[bool, str]: (é_válida, mensagem_erro)
        """
        # Remove espaços em branco
        url = url.strip()
        
        # Verifica se a URL não está vazia
        if not url:
            return False, "URL não pode estar vazia"
        
        # Verifica se a URL tem um formato válido
        if not validators.url(url):
            return False, "Formato de URL inválido"
        
        # Verifica se a URL tem um protocolo
        if not url.startswith(('http://', 'https://')):
            return False, "URL deve começar com http:// ou https://"
        
        return True, ""
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normaliza uma URL (remove espaços, adiciona protocolo se necessário)
        
        Args:
            url (str): URL a ser normalizada
            
        Returns:
            str: URL normalizada
        """
        url = url.strip()
        
        # Adiciona https:// se não tiver protocolo
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        return url 