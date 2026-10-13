import os
from core.config_loader import Config


class Social:
    folder = "social_media"

    def __init__(self,
                 name: str = None,
                 url: str = None,
                 logo: str = None):
        self.name = name  # Ключ (например, "github")
        self.url = url  # Ссылка (например, "https://github.com...")
        # HTML-тег картинки base64
        self.logo = "<span style='font-size:1.1rem; vertical-align: middle;'>🔗</span>" if not logo else logo

    def get_logo_name(self, key, config: Config):
        filename = config.asset_settings.get(self.folder, {}).get(key)
        return os.path.join(str(config.assets_dir), self.folder, filename) if filename else None


class Company:
    folder = "company"

    def __init__(self, 
                 name: str = None, 
                 url: str = None, 
                 position: str = None, 
                 period: str = None, 
                 skills: list = None):
        self.name = name
        self.url = url
        self.position = position
        self.period = period
        self.skills = skills if skills is not None else []
        self.logo = None  # Сюда запишем HTML-тег картинки из ассетов

    def get_logo_name(self, key, config: Config):
        filename = config.asset_settings.get(self.folder, {}).get(key, "default_logo.svg")
        return os.path.join(str(config.assets_dir), self.folder, filename)

    def set_info(self, **kwargs):
        self.name = kwargs.get("job_name", "")
        self.url = kwargs.get("job_url", "")
        self.position = kwargs.get("job_position", "")
        self.period = kwargs.get("job_period", "")
        self.skills = kwargs.get("job_skills", [])


class Education:
    folder = "education"

    def __init__(self, 
                 name: str = None, 
                 url: str = None, 
                 specialization: str = None, 
                 period: str = None):
        self.name = name
        self.url = url
        self.specialization = specialization
        self.period = period
        self.logo = None  # Сюда запишем HTML-тег картинки из ассетов

    def get_logo_name(self, key, config: Config):
        filename = config.asset_settings.get(self.folder, {}).get(key, "default_logo.svg")
        return os.path.join(str(config.assets_dir), self.folder, filename)

    def set_info(self, **kwargs):
        self.name = kwargs.get("edu_name", "")
        self.url = kwargs.get("edu_url", "")
        self.specialization = kwargs.get("edu_specialization", "")
        self.period = kwargs.get("edu_period", "")


class Volunteer:
    folder = "volunteer"

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 url: str = None,
                 position: str = None,
                 period: str = None,
                 skills: list = None):
        self.name = name
        self.description = description
        self.url = url
        self.position = position
        self.period = period
        self.skills = skills if skills is not None else []
        self.logo = None  # Сюда запишем HTML-тег картинки из ассетов

    def get_logo_name(self, key, config: Config):
        filename = config.asset_settings.get(self.folder, {}).get(key, "default_logo.svg")
        return os.path.join(str(config.assets_dir), self.folder, filename)

    def set_info(self, **kwargs):
        self.name = kwargs.get("act_name", "")
        self.description = kwargs.get("act_description", "")
        self.url = kwargs.get("act_url", "")
        self.position = kwargs.get("act_position", "")
        self.period = kwargs.get("act_period", "")
        self.skills = kwargs.get("act_skills", [])