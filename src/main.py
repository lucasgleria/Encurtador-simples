"""
Ponto de entrada principal da aplicação Encurtador de Links
"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from backend.database import db_manager
from backend.url_shortener import URLShortener
from frontend.main_window import MainWindow
from frontend.styles import STYLE_SHEET
from pymongo.errors import ConnectionFailure, PyMongoError

def test_database_connection():
    """Testa a conexão com o banco de dados"""
    print("\n=== Teste de Conexão com MongoDB ===")
    
    if db_manager.connect():
        print("✅ Conexão com MongoDB estabelecida com sucesso!")
        return True
    else:
        print("❌ Falha na conexão com MongoDB")
        print("Certifique-se de que o MongoDB está rodando localmente e que config.env está correto.")
        return False

def test_url_shortener():
    """Testa as funcionalidades do encurtador"""
    print("\n=== Teste do Encurtador de URLs ===")

    shortener = URLShortener()

    # Teste 1: Validação de URLs
    print("\n1. Testando validação de URLs:")
    test_urls = [
        "https://www.google.com",                  # Válida, comum
        "http://www.example.com/path?query=1&param=2#fragment", # Válida, completa
        "https://sub.domain.com/page",            # Válida, subdomínio
        "ftp://ftp.example.com/file.txt",         # Inválida: protocolo não http/https
        "www.facebook.com",                       # Inválida: falta protocolo
        "google.com",                             # Inválida: falta protocolo
        "http://",                                # Inválida: incompleta
        "https://",                               # Inválida: incompleta
        "http://a.b",                             # Inválida: muito curta (domínio genérico)
        "justtext",                               # Inválida: não é URL
        "",                                       # Inválida: vazia
        "  https://  whitespace.com  ",           # Válida: com espaços (deve ser tratada pelo strip)
        "https://192.168.1.1/admin",              # Válida: IP local
        "https://user:pass@example.com",          # Válida: com credenciais (válido, mas pode ser um caso a considerar)
        "https://日本語.jp",                      # Válida: caracteres Unicode (IDN)
        "https://-invalid-host.com",              # Inválida: host inválido (começa com hífen)
        "https://longurl.com/" + "a"*2000,        # Válida: URL muito longa (teste de stress)
        "http://www.site.co.uk",                  # Válida: TLD diferente
        "http://site",                            # Inválida: domínio não público/completo
    ]

    for url in test_urls:
        is_valid, error = shortener.validator.validate_url(url)
        status = "✅ Válida" if is_valid else f"❌ Inválida: {error}"
        print(f"   {url} -> {status}")
    
    # Teste 2: Geração de códigos e encurtamento
    print("\n2. Testando encurtamento de URL:")
    test_urls_for_shortening = [
        "https://www.alura.com.br/cursos-online-programacao/",
        "https://www.python.org/",
        "https://www.alura.com.br/cursos-online-programacao/" # Testar duplicação
    ]

    if not db_manager.is_connected():
        print("Conectando ao MongoDB para testes de encurtamento...")
        if not db_manager.connect():
            print("Não foi possível conectar ao MongoDB para testes. Pulando testes de encurtamento.")
            return

    for url_to_shorten in test_urls_for_shortening:
        print(f"\n   Tentando encurtar: {url_to_shorten}")
        result = shortener.shorten_url(url_to_shorten)
        if result['success']:
            print(f"   ✅ URL encurtada com sucesso!")
            print(f"      Original: {result['original_url']}")
            print(f"      Encurtada: {result['short_url']}")
            print(f"      Já existia: {result.get('already_exists', False)}")
        else:
            print(f"   ❌ Erro ao encurtar: {result['error']}")

    db_manager.disconnect() # Desconecta após os testes

def main():
    print("🚀 Iniciando Encurtador de Links (Interface Gráfica)")

    # Tenta conectar ao banco de dados
    try:
        if not db_manager.connect():
            QMessageBox.critical(None, "Erro de Conexão", 
                                 "Não foi possível conectar ao MongoDB. "
                                 "Certifique-se de que o MongoDB está rodando e que 'config.env' está correto."
                                 "\n\nA aplicação será encerrada.")
            sys.exit(1)
    except (ConnectionFailure, PyMongoError) as e:
        QMessageBox.critical(None, "Erro Crítico de MongoDB",
                             f"Erro ao conectar ao MongoDB: {e}\n\nA aplicação será encerrada.")
        sys.exit(1)
    except Exception as e:
        QMessageBox.critical(None, "Erro Inesperado",
                             f"Um erro inesperado ocorreu ao iniciar o banco de dados: {e}\n\nA aplicação será encerrada.")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    
    url_shortener = URLShortener()
    window = MainWindow(url_shortener)
    
    # Carrega histórico do banco
    try:
        url_list = url_shortener.get_all_urls()
        window.load_history(url_list)
    except Exception as e:
        QMessageBox.warning(None, "Erro ao Carregar Histórico",
                            f"Não foi possível carregar o histórico de URLs: {e}")
        # A aplicação continua, mas sem o histórico carregado

    window.show()
    
    exit_code = app.exec()
    db_manager.disconnect()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
    # Para executar os testes, descomente as linhas abaixo e comente 'main()'
    # test_database_connection()
    test_url_shortener()