"""
Módulo de configuração e conexão com MongoDB
"""
import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv('config.env')

class DatabaseManager:
    """Gerenciador de conexão com MongoDB"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None
        self.collection: Optional[Collection] = None
        
    def connect(self) -> bool:
        """
        Estabelece conexão com MongoDB
        
        Returns:
            bool: True se conectou com sucesso, False caso contrário
        """
        try:
            # Obtém configurações do ambiente
            mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
            database_name = os.getenv('MONGODB_DATABASE', 'url_shortener')
            collection_name = os.getenv('MONGODB_COLLECTION', 'urls')
            
            # Conecta ao MongoDB
            self.client = MongoClient(mongo_uri)
            
            # Testa a conexão
            self.client.admin.command('ping')
            
            # Configura database e collection
            self.database = self.client[database_name]
            self.collection = self.database[collection_name]
            
            print(f"Conectado ao MongoDB: {database_name}.{collection_name}")
            return True
            
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Fecha conexão com MongoDB"""
        if self.client:
            self.client.close()
            print("Conexão com MongoDB fechada")
    
    def get_collection(self) -> Optional[Collection]:
        """
        Retorna a collection configurada
        
        Returns:
            Collection: Collection do MongoDB ou None se não conectado
        """
        return self.collection
    
    def is_connected(self) -> bool:
        """
        Verifica se está conectado ao MongoDB
        
        Returns:
            bool: True se conectado, False caso contrário
        """
        return self.client is not None and self.collection is not None

# Instância global do gerenciador de banco
db_manager = DatabaseManager() 