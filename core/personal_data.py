import os
from PIL import Image
from core.config_loader import Config
from core.model import Company, Education, Social, Volunteer


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

            file_path = social_obj.get_logo_name(platform_name, self.config)
            if file_path:
                social_obj.logo = self.config.to_base64(file_path, width=18)

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
        file_path = os.path.join(self.config.assets_dir, self.config.profile_folder, filename)
        avatar_html = self.config.to_base64(file_path, width=210)
        
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
            comp_obj.set_info(**item)

            file_path = comp_obj.get_logo_name(key, self.config)
            comp_obj.logo = self.config.to_base64(file_path, width=44)

            history_list.append(comp_obj)
        return history_list

    @property
    def education(self) -> list[Education]: 
        """Возвращает список готовых объектов Education, прочитанных из словаря EDUCATION."""
        edu_list = []
        raw_edu = self._data.get("EDUCATION", {})
        
        for key, item in raw_edu.items():
            edu_obj = Education()
            edu_obj.set_info(**item)

            file_path = edu_obj.get_logo_name(key, self.config)
            edu_obj.logo = self.config.to_base64(file_path, width=44)
                
            edu_list.append(edu_obj)
        return edu_list

    @property
    def volunteer(self) -> list[Volunteer]:
        """Возвращает список готовых объектов Company, прочитанных из словаря EXPERIENCE."""
        volunteer_list = []
        raw_experience = self._data.get("VOLUNTEER", {})

        for key, item in raw_experience.items():
            volunteer_obj = Volunteer()
            volunteer_obj.set_info(**item)

            file_path = volunteer_obj.get_logo_name(key, self.config)
            volunteer_obj.logo = self.config.to_base64(file_path, width=44)

            volunteer_list.append(volunteer_obj)
        return volunteer_list