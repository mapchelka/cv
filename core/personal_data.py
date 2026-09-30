import os
import base64
from io import BytesIO
from PIL import Image
from core.config_loader import Config
from core.model import Company, Education, Social


class PersonalData:
    """Класс для загрузки, парсинга и предоставления текстовых данных резюме."""
    def __init__(self, config: Config):
        self.config = config
        self._data = config.personal_settings

    @property
    def name(self): 
        return self._data.get("NAME", "")

    @property
    def page_title(self): 
        return self._data.get("PAGE_TITLE", "")

    @property
    def page_icon(self): 
        return self._data.get("PAGE_ICON", "")

    @property
    def description(self): 
        return self._data.get("DESCRIPTION", "")

    @property
    def social_media(self) -> list[Social]: 
        """Возвращает список готовых объектов Social с вшитыми логотипами."""
        social_list = []
        raw_socials = self._data.get("SOCIAL_MEDIA", {})
        
        for platform_name, url in raw_socials.items():
            social_obj = Social()
            social_obj.name = platform_name
            social_obj.url = url
            
            # На этапе парсинга сразу находим и вшиваем логотип соцсети
            filename = self.config.asset_settings.get(self.config.social_media_folder, {}).get(platform_name)
            if filename:
                social_obj.logo = self._to_base64(self.config.social_media_folder, filename, width=18)
            else:
                # Фоллбэк: если иконки нет, ставим символ ссылки
                social_obj.logo = "<span style='font-size:1.1rem; vertical-align: middle;'>🔗</span>"
                
            social_list.append(social_obj)
        return social_list


    @property
    def profile_pic(self) -> Image.Image or None:
        """Безопасно загружает главное фото профиля как объект PIL Image."""
        # 1. Забираем имя файла аватарки из JSON (ищем под ключами AVATAR или PROFILE)
        filename = self._data.get("AVATAR")
        if not filename:
            return None
            
        # 2. Собираем полный путь к папке assets/profile/
        file_path = os.path.join(self.config.assets_dir, self.config.profile_folder, filename)
        
        # 3. Безопасно открываем картинку через Pillow
        if os.path.exists(file_path):
            try:
                return Image.open(file_path)
            except Exception as e:
                print(f"Ошибка чтения фото профиля {filename}: {e}")
                return None
        return None

    @property
    def profile_pic_html(self) -> str:
        """Возвращает готовый HTML-тег аватарки со вшитым CSS-классом profile-avatar."""
        # 1. Забираем имя файла аватарки из JSON
        filename = self._data.get("AVATAR")
        if not filename:
            return ""
            
        # 2. Генерируем базовый Base64 HTML-тег через наш универсальный метод
        avatar_html = self._to_base64(self.config.profile_folder, filename, width=210)
        
        # 3. Инжектируем наш кастомный класс для CSS-оформления
        if avatar_html:
            avatar_html = avatar_html.replace('<img ', '<img class="profile-avatar" ')
            
        return avatar_html

    @property
    def work_history(self) -> list[Company]: 
        """Возвращает список готовых объектов Company, прочитанных из словаря EXPERIENCE."""
        history_list = []
        raw_experience = self._data.get("EXPERIENCE", {})
        
        for key, item in raw_experience.items():
            comp_obj = Company()
            comp_obj.name = item.get("job_name", "")
            comp_obj.url = item.get("job_url", "")
            comp_obj.position = item.get("job_position", "")
            comp_obj.period = item.get("job_period", "")
            comp_obj.skills = item.get("job_skills", [])
            
            # Ищем логотип компании в asset_settings.json
            filename = self.config.asset_settings.get(self.config.company_folder, {}).get(key)
            if not filename:
                filename = "default_logo.svg"

            if filename:
                comp_obj.logo = self._to_base64(self.config.company_folder, filename, width=44)
                
            history_list.append(comp_obj)
        return history_list

    @property
    def education(self) -> list[Education]: 
        """Возвращает список готовых объектов Education, прочитанных из словаря EDUCATION."""
        edu_list = []
        raw_edu = self._data.get("EDUCATION", {})
        
        for key, item in raw_edu.items():
            edu_obj = Education()
            # Берем ваши точные ключи со спецификацией edu_
            edu_obj.name = item.get("edu_name", "")
            edu_obj.url = item.get("edu_url", "")
            edu_obj.specialization = item.get("edu_specialization", "")
            edu_obj.period = item.get("edu_period", "")
            
            # Ищем логотип образования в asset_settings.json по ключу "karpov" или "mtuci"
            filename = self.config.asset_settings.get(self.config.education_folder, {}).get(key)
            if not filename:
                filename = "default_logo.svg"

            if filename:
                edu_obj.logo = self._to_base64(self.config.education_folder, filename, width=44)
                
            edu_list.append(edu_obj)
        return edu_list

    def _to_base64(self, folder: str, filename: str, width: int) -> str:
        """Универсальный метод конвертации изображений (включая SVG) в HTML-тег Base64."""
        if not filename:
            return ""
            
        file_path = os.path.join(self.config.assets_dir, folder, filename)
        if not os.path.exists(file_path): 
            return ""
        
        try:
            # Получаем расширение файла в нижнем регистре (например, '.svg' или '.png')
            ext = os.path.splitext(filename)[1].lower()
            
            # --- ОСОБАЯ ОБРАБОТКА ДЛЯ SVG ---
            if ext == ".svg":
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
            
            # Возвращаем готовый HTML-тег, который Streamlit идеально отобразит
            return (
                f'<img src="data:{mime_type};base64,{img_str}" '
                f'width="{width}" height="{width}" '
                f'style="vertical-align: middle; object-fit: contain;">'
            )
            
        except Exception as e:
            print(f"Ошибка конвертации изображения {filename} в папке {folder}: {e}")
            return ""

