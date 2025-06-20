import os 
from dotenv import load_dotenv 

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QClipboard # QClipboard já estava, mas vale a pena mencionar

load_dotenv('config.env')

class MainWindow(QWidget):
    def __init__(self, url_shortener):
        super().__init__()
        self.url_shortener = url_shortener
        self.short_url_base = os.getenv('FLASK_BASE_URL', f"http://localhost:{os.getenv('FLASK_PORT', '5000')}/")

        self.setWindowTitle('Encurtador de Links')
        self.setMinimumWidth(550)
        self.setStyleSheet('background: #f8f9fa;')
        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10) # Espaçamento entre os widgets

        # Campo de entrada
        self.input_label = QLabel('URL original:')
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('Cole ou digite a URL aqui...')
        self.input_edit.returnPressed.connect(self.handle_shorten) # Permite encurtar com Enter

        # Botão de encurtar
        self.shorten_btn = QPushButton('Encurtar')
        self.shorten_btn.clicked.connect(self.handle_shorten)

        # Exibição do link encurtado
        self.result_label = QLabel('Link encurtado:')
        self.result_edit = QLineEdit()
        self.result_edit.setReadOnly(True)
        self.copy_btn = QPushButton('Copiar')
        self.copy_btn.clicked.connect(self.handle_copy)

        # Layout para resultado
        result_layout = QHBoxLayout()
        result_layout.addWidget(self.result_edit)
        result_layout.addWidget(self.copy_btn)

        # Histórico
        self.history_label = QLabel('Histórico de links encurtados:')
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.handle_history_click)
        self.history_list.setMinimumHeight(150) # Garante um tamanho mínimo para o histórico

        # Status Label (para feedback temporário)
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #007bff; font-weight: bold; margin-top: 5px;") # Estilo inicial

        # Adiciona widgets ao layout
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_edit)
        layout.addWidget(self.shorten_btn)
        layout.addSpacing(15) # Espaço extra
        layout.addWidget(self.result_label)
        layout.addLayout(result_layout)
        layout.addWidget(self.status_label) # Adiciona a label de status aqui
        layout.addSpacing(15) # Espaço extra
        layout.addWidget(self.history_label)
        layout.addWidget(self.history_list)

        self.setLayout(layout)

    def display_status_message(self, message: str, is_error: bool = False, duration: int = 3000):
        """Exibe uma mensagem de status temporária."""
        if is_error:
            self.status_label.setStyleSheet("color: #dc3545; font-weight: bold; margin-top: 5px;") # Vermelho para erro
        else:
            self.status_label.setStyleSheet("color: #28a745; font-weight: bold; margin-top: 5px;") # Verde para sucesso

        self.status_label.setText(message)
        QTimer.singleShot(duration, lambda: self.status_label.setText('')) # Limpa a mensagem após 'duration' ms

    def handle_shorten(self):
        url = self.input_edit.text().strip()
        if not url:
            self.display_status_message('⚠️ Digite uma URL para encurtar.', is_error=True)
            self.result_edit.clear()
            return

        result = self.url_shortener.shorten_url(url)
        if result['success']:
            # Constrói o link completo com a base do servidor Flask
            full_short_url = f"{self.short_url_base}{result['short_url']}"
            self.result_edit.setText(full_short_url)
            self.add_to_history(result['original_url'], full_short_url) # Adiciona a URL completa ao histórico

            if result.get('already_exists'):
                self.display_status_message(f'🔗 URL já encurtada: {full_short_url}')
            else:
                self.display_status_message(f'✅ URL encurtada com sucesso: {full_short_url}')
            self.input_edit.clear()
        else:
            self.result_edit.clear()
            self.display_status_message(f'❌ Erro ao encurtar: {result["error"]}', is_error=True)


    def handle_copy(self):
        short_url = self.result_edit.text().strip()
        if short_url:
            clipboard = QApplication.clipboard() # Usar QApplication.clipboard() diretamente
            clipboard.setText(short_url)
            self.display_status_message('📋 Link encurtado copiado para a área de transferência!', is_error=False)
        else:
            self.display_status_message('🤔 Não há link para copiar.', is_error=True)

    def handle_history_click(self, item):
        # Ao clicar no histórico, preenche o campo de resultado e copia
        data = item.text().split(' → ')
        if len(data) == 2:
            original_url = data[0]
            short_url = data[1]
            self.input_edit.setText(original_url)
            self.result_edit.setText(short_url)
            
            # Nova funcionalidade: Copiar ao clicar no histórico
            clipboard = QApplication.clipboard()
            clipboard.setText(short_url)
            self.display_status_message('📋 Link do histórico copiado para a área de transferência!', is_error=False)


    def add_to_history(self, original_url: str, short_url_with_base: str): # Renomeado para clareza
        item_text = f'{original_url} → {short_url_with_base}'
        for i in range(self.history_list.count()):
            if self.history_list.item(i).text() == item_text:
                self.history_list.takeItem(i)
                break
        self.history_list.insertItem(0, item_text)

    def load_history(self, url_list: list):
        self.history_list.clear()
        for doc in reversed(url_list):
             # Ao carregar, garanta que a URL encurtada seja apresentada com a base do servidor
             full_short_url = f"{self.short_url_base}{doc['short_url']}"
             self.add_to_history(doc['original_url'], full_short_url)


    # Removida a lógica complexa do clipboard, usando QApplication.clipboard() diretamente
    # def clipboard(self):
    #     return self.window().windowHandle().screen().virtualSiblings()[0].clipboard() if hasattr(self.window().windowHandle().screen(), 'virtualSiblings') else QApplication.clipboard()