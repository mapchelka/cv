import os
import json


class Config:
    """Центральный класс конфигурации. Отвечает за пути и чтение абсолютно всех ресурсов."""
    config_folder = "config"
    assets_folder = "assets"
    templates_folder = "templates"
    styles_folder = "styles"
    
    main_css = "main.css"
    asset_settings_json = "asset_settings.json"
    personal_settings_json = "personal_settings.json"

    # Явные константы подпапок для менеджера ассетов
    company_folder = "company"
    education_folder = "education"
    social_media_folder = "social_media"
    profile_folder = "profile"

    def __init__(self):
        # Файл лежит в core/, поднимаемся на уровень выше в корень проекта
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Основные папки проекта
        self.config_dir = os.path.join(self.root_dir, self.config_folder)
        self.assets_dir = os.path.join(self.root_dir, self.assets_folder)
        self.templates_dir = os.path.join(self.root_dir, self.templates_folder)
        self.styles_dir = os.path.join(self.root_dir, self.styles_folder)
        
        # Словари для хранения ресурсов в памяти
        self.asset_settings = {}
        self.personal_settings = {}
        self.css_content = ""

        # html-шаблоны
        self.contact_wrapper_template = ""
        self.contact_card_template = ""
        self.edu_card_template = ""
        self.job_card_template = ""
        self.print_button_template = ""

    def load(self):
        """Читает все конфигурации, стили и динамически загружает все HTML-шаблоны."""
        # 1. Читаем настройки картинок и данные резюме
        self.asset_settings = self._load_json(self.asset_settings_json)
        self.personal_settings = self._load_json(self.personal_settings_json)
        
        # 2. Читаем стили main.css
        css_path = os.path.join(self.styles_dir, self.main_css)
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                self.css_content = f.read()
        
        # 3. Читаем HTML-карточки
        self.contact_wrapper_template = self._load_html("contact_wrapper.html")
        self.contact_card_template = self._load_html("contact_card.html")
        self.edu_card_template = self._load_html("edu_card.html")
        self.job_card_template = self._load_html("job_card.html")
        self.print_button_template = self._load_html("print_button.html")

    def _load_json(self, filename: str) -> dict:
        path = os.path.join(self.config_dir, filename)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_html(self, filename: str) -> str:
        """Вспомогательный метод для безопасного чтения HTML-файла."""
        path = os.path.join(self.templates_dir, filename)
        if not os.path.exists(path):
            return ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Ошибка чтения HTML-шаблона {filename}: {e}")
            return ""
