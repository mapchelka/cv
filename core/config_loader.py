import os
import json
import base64
from io import BytesIO
from PIL import Image


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
        self.volunteer_card_template = ""
        self.print_button_template = ""
        self.logo_template = ""

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
        self.volunteer_card_template = self._load_html("volunteer.html")
        self.print_button_template = self._load_html("print_button.html")
        self.logo_template = self._load_html("logo.html")

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

    def to_base64(self, file_path: str, width: int) -> str:
        """Универсальный метод конвертации изображений (включая SVG) в HTML-тег Base64."""
        if not os.path.exists(file_path):
            return ""

        try:
            # --- ОСОБАЯ ОБРАБОТКА ДЛЯ SVG ---
            if file_path.endswith(".svg"):
                with open(file_path, "r", encoding="utf-8") as f:
                    svg_content = f.read()
                # Кодируем текстовое содержимое SVG в base64 байты, затем декодируем в строку
                img_str = base64.b64encode(svg_content.encode("utf-8")).decode()
                mime_type = "image/svg+xml"

            # --- ОБЫЧНАЯ ОБРАБОТКА ДЛЯ РАСТРОВЫХ КАРТИНОК (PNG, JPG и др.) ---
            else:
                with Image.open(file_path) as img:
                    buffered = BytesIO()
                    fmt = img.format if img.format else "PNG"
                    img.save(buffered, format=fmt)
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    mime_type = f"image/{fmt.lower()}"

            rendered_html = (
                self.logo_template
                .replace("{{mime_type}}", mime_type)
                .replace("{{img_str}}", img_str)
                .replace("{{width}}", str(width))
            )

            # Возвращаем готовый HTML-тег, который Streamlit идеально отобразит
            return rendered_html

        except Exception as e:
            print(f"Ошибка конвертации изображения {file_path}: {e}")
            return ""