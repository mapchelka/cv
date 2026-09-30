class Company:
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


class Education:
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


class Social:
    def __init__(self, 
                 name: str = None, 
                 url: str = None, 
                 logo: str = None):
        self.name = name     # Ключ (например, "github")
        self.url = url       # Ссылка (например, "https://github.com...")
        self.logo = logo     # HTML-тег картинки base64