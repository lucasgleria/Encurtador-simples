# 🔗 Encurtador de Links

**Um aplicativo de desktop simples e eficiente para encurtar URLs, com histórico e persistência de dados em MongoDB, e um servidor de redirecionamento em Flask.**

[![Licença](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.5-green.svg)]()
[![Status](https://img.shields.io/badge/status-concluído-greend.svg)]()
[![deploy](https://img.shields.io/badge/depoly-inactive-red.svg)]()


## 📌 Sumário

1. [Sobre o Projeto](#-sobre-o-projeto)  
2. [Objetivos](#-objetivos)  
3. [Tecnologias](#-tecnologias)  
4. [Funcionalidades](#-funcionalidades)  
5. [Pré-requisitos](#%EF%B8%8F-pré-requisitos)  
6. [Instalação](#%EF%B8%8F-instalação)  
7. [Como utilizar](#-como-utilizar)
8. [Estrutura do Projeto](#-estrutura-do-projeto)
9. [Contribuição](#-contribuição)  
10. [Licença](#-licença)  
11. [Contato](#-contato)  
12. [Recursos Adicionais](#-recursos-adicionais)  


## 💻 Sobre o Projeto

O **Encurtador de Links** é um projeto pessoal que oferece uma solução de desktop intuitiva para encurtar URLs longas em códigos curtos e fáceis de compartilhar. Ele gerencia o histórico de links encurtados, oferece validação robusta de URLs e persiste todos os dados em um banco de dados MongoDB local. Para o redirecionamento dos links encurtados, um pequeno servidor web baseado em Flask é utilizado, funcionando em conjunto com a aplicação principal.

  - *Motivação*: Proporcionar uma ferramenta prática e demonstrar a integração entre uma interface gráfica de desktop (PyQt6) e um backend de persistência de dados (MongoDB), além de um servidor web dedicado para a funcionalidade de redirecionamento.
  - *Público-alvo*: Desenvolvedores Python e usuários que buscam uma ferramenta simples para encurtar e gerenciar links localmente.


## 🎯 Objetivos

### 🛠️ Técnicos

  - Implementar uma interface gráfica de usuário (GUI) intuitiva usando **PyQt6**.
  - Desenvolver uma lógica de backend robusta para geração e gerenciamento de links encurtados.
  - Configurar a persistência de dados utilizando **MongoDB** local para armazenar URLs originais e seus respectivos códigos curtos.
  - Criar um servidor web dedicado com **Flask** para gerenciar o redirecionamento de links encurtados para suas URLs originais.
  - Garantir a validação adequada das URLs de entrada.
  - Manter um histórico de links encurtados para fácil acesso e reutilização.


## 🚀 Tecnologias

**Núcleo do Sistema**

  - Python 3.8+
  - PyQt6 
  - Flask 
  - MongoDB 
  - pymongo 
  - validators 
  - python-dotenv 


## ✨ Funcionalidades

  - ✅ **Encurtamento de URLs**: Transforma URLs longas em códigos curtos com o prefixo "lleria".
  - ✅ **Validação de URLs**: Garante que apenas URLs válidas sejam encurtadas.
  - ✅ **Histórico de Links**: Mantém um registro dos links encurtados para fácil consulta.
  - ✅ **Copiar para Área de Transferência**: Copia o link encurtado ou o link do histórico para a área de transferência com um clique.
  - ✅ **Persistência de Dados**: Armazena todos os links encurtados no MongoDB, mantendo-os disponíveis entre as sessões.
  - ✅ **Servidor de Redirecionamento**: Um servidor Flask dedicado que redireciona o usuário da URL encurtada para a URL original.
  - ✅ **Interface Intuitiva**: Design limpo e fácil de usar.


## ⚙️ Pré-requisitos

  - **Python 3.8+**
  - **MongoDB**: Servidor MongoDB rodando localmente (padrão na porta `27017`).
  - Conexão estável à internet (necessária apenas para instalar dependências).


## 🛠️ Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/lucasgleria/encurtador-simples.git
    ```

2.  **Navegue até a pasta do projeto:**

    ```bash
    cd encurtador
    ```

3.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # No Windows
    # source venv/bin/activate # No Linux/macOS
    ```

4.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

    (Certifique-se de que o arquivo `requirements.txt` na raiz do projeto contenha: `PyQt6`, `pymongo`, `validators`, `python-dotenv`, `Flask`)

5.  **Crie um arquivo `.env` na pasta raiz do projeto (`encurtador/`):**

    ```ini
    # .env
    MONGODB_URI=mongodb://localhost:27017/
    MONGODB_DATABASE=url_shortener
    MONGODB_COLLECTION=urls
    FLASK_PORT=5000
    FLASK_BASE_URL=http://localhost:5000/
    ```

    *Ajuste as portas ou URI conforme a configuração do seu MongoDB e Flask.*


## ❗ Como Utilizar

Para utilizar o Encurtador de Links, você precisará iniciar **dois processos separados**: o servidor de redirecionamento Flask e a aplicação de desktop PyQt6.

1.  **Inicie o Servidor MongoDB:**
    Certifique-se de que o seu servidor MongoDB esteja em execução. Em um terminal, você pode iniciar com:

    ```bash
    mongod
    ```

2.  **Inicie o Servidor de Redirecionamento (Flask):**
    Abra um novo terminal na pasta raiz do projeto (`encurtador/`), ative o ambiente virtual e execute:

    ```bash
    .\venv\Scripts\activate
    python redirect_server.py
    ```

    Mantenha este terminal aberto e rodando.

3.  **Inicie a Aplicação de Desktop (PyQt6):**
    Abra **outro terminal** na pasta raiz do projeto (`encurtador/`), ative o ambiente virtual e execute:

    ```bash
    .\venv\Scripts\activate
    python src/main.py
    ```

4.  **Utilize a Aplicação:**
    A janela do Encurtador de Links será aberta.

      - Digite ou cole uma URL no campo "URL original" e clique em "Encurtar".
      - O link encurtado completo (ex: `http://localhost:5000/lleriaABCD`) aparecerá no campo "Link encurtado".
      - Clique em "Copiar" para copiar o link.
      - Cole o link encurtado em seu navegador para ser redirecionado para a URL original.
      - Os links encurtados serão salvos no histórico e no seu MongoDB.


### ▶️ Demonstração

![](https://media1.tenor.com/m/1nQJd92WjAgAAAAC/send-me.gif)

*(Gif meramente ilustrativo)*


## 📂 Estrutura do Projeto

```plaintext
encurtador/
├── src/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── url_shortener.py    # Lógica central do encurtador
│   │   ├── database.py         # Gerenciamento da conexão com MongoDB
│   │   └── validators.py       # Validação e normalização de URLs
│   ├── frontend/
│   │   ├── __init__.py
│   │   ├── main_window.py      # Interface gráfica (PyQt6)
│   │   └── styles.py           # Estilos CSS para PyQt6
│   └── main.py                 # Ponto de entrada da aplicação desktop
├── redirect_server.py          # Servidor web Flask para redirecionamento
├── requirements.txt            # Dependências do projeto
├── config.env                  # Variáveis de ambiente
├── LICENSE                     # Licença
├── README.md                   # Este arquivo
└── .gitignore                  # Arquivos/pastas a serem ignorados pelo Git
```


## 🤝 Contribuição

Contribuições são bem-vindas\! Siga estas etapas:

1.  **Reporte bugs**: Abra uma [issue](https://www.google.com/search?q=https://github.com/lucasgleria/encurtador-simples/issues) no GitHub.
2.  **Sugira melhorias**: Envie ideias ou *pull requests* com novas funcionalidades.
3.  **Desenvolva**:
      - Faça um *fork* do projeto.
      - Crie uma branch (`git checkout -b feature/nova-funcionalidade`).
      - Faça suas alterações e *commit* (`git commit -m 'feat: nova funcionalidade'`).
      - Envie um *Pull Request*.


## 📜 Licença

MIT License - Veja [LICENSE](https://www.google.com/search?q=LICENSE) para detalhes.


## 📞 Contato & Evidências

  - **Autor**: [Lucas Leria](https://github.com/lucasgleria)
  - **LinkedIn**: [lucasgleria](https://www.linkedin.com/in/lucasgleria/)


## 🔍 Recursos Adicionais

  - [Python](https://www.python.org/doc/) - Documentação oficial
  - [PyQt6](https://doc.qt.io/qtforpython/) - Documentação oficial
  - [Flask](https://flask.palletsprojects.com/en/latest/) - Documentação oficial
  - [MongoDB](https://docs.mongodb.com/) - Documentação oficial
  - [PyMongo](https://pymongo.readthedocs.io/en/stable/) - Documentação oficial
