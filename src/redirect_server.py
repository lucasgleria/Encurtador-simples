# redirect_server.py
import os
from flask import Flask, redirect, abort
from backend.database import db_manager
from backend.url_shortener import URLShortener # Importa para usar o get_original_url
from dotenv import load_dotenv

# Carrega variáveis de ambiente do config.env
load_dotenv('config.env')

app = Flask(__name__)
shortener_instance = URLShortener() # Instancia o URLShortener para acesso ao banco

# Endpoint para redirecionamento
@app.route('/<short_code>')
def redirect_to_original(short_code):
    """
    Redireciona o usuário para a URL original com base no short_code.
    """
    if not db_manager.is_connected():
        print("Servidor de Redirecionamento: Tentando reconectar ao MongoDB...")
        if not db_manager.connect():
            print("Servidor de Redirecionamento: Falha na conexão com MongoDB.")
            abort(500, "Internal Server Error: Database connection failed.")

    original_url = shortener_instance.get_original_url(short_code)

    if original_url:
        print(f"Redirecionando '{short_code}' para '{original_url}'")
        return redirect(original_url)
    else:
        print(f"Código curto '{short_code}' não encontrado.")
        abort(404, "Short URL not found.")

@app.route('/')
def index():
    """Página inicial simples para o servidor de redirecionamento."""
    return "Servidor de Encurtamento de Links Rodando. Use /<codigo_curto> para redirecionar."

if __name__ == '__main__':
    print("🚀 Iniciando Servidor de Redirecionamento...")
    # Conecta ao banco de dados ao iniciar o servidor
    if not db_manager.connect():
        print("❌ Servidor de Redirecionamento: Não foi possível conectar ao MongoDB. Por favor, verifique se o MongoDB está rodando.")
        exit(1) # Sai se não conseguir conectar ao DB

    # Obtém a porta do ambiente ou usa 5000 como padrão
    port = int(os.getenv('FLASK_PORT', 5000))
    # Define o host para 0.0.0.0 para que possa ser acessível de outras máquinas na rede, se necessário
    # Em um ambiente de produção, você usaria um servidor WSGI como Gunicorn/Waitress
    app.run(host='0.0.0.0', port=port, debug=False) # debug=True em desenvolvimento é útil, mas False para "produção"