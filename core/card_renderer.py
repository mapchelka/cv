# core/card_renderer.py
from core.config_loader import Config
from core.model import Company, Education, Social


class JobCardRenderer:
    """Рендеринг карточки опыта работы на основе HTML-шаблона."""
    def __init__(self, config: Config):
        self.template = config.job_card_template

    def render(self, job: Company) -> str:
        if not self.template:
            return f"<div><h3>{job.position}</h3><p>{job.name}</p></div>"
            
        # Собираем навыки в красивую строку через запятую для HTML
        skills_str = ", ".join(job.skills) if isinstance(job.skills, list) else job.skills
        
        # Обращаемся к атрибутам объекта через точку
        return self.template.format(
            job_position=job.position or "",
            job_url=job.url or "#",
            job_name=job.name or "",
            job_period=job.period or "",
            job_skills=skills_str or ""
        )


class EduCardRenderer:
    """Рендеринг карточки образования на основе HTML-шаблона."""
    def __init__(self, config: Config):
        self.template = config.edu_card_template

    def render(self, edu: Education) -> str:
        if not self.template:
            return f"<div><h3>{edu.specialization}</h3><p>{edu.name}</p></div>"
        
        return self.template.format(
            edu_name=edu.name or "",
            edu_url=edu.url or "#",
            edu_specialization=edu.specialization or "",
            edu_period=edu.period or ""
        )


class ContactCardRenderer:
    """Рендеринг блока контактов в стиле Хабра (логотип + короткий никнейм)."""
    def __init__(self, config: Config):
        self.config = config
        self.wrapper_template = config.contact_wrapper_template
        self.card_template = config.contact_card_template

    def render_block(self, social_media_list: list[Social]) -> str:
        """Принимает список объектов Social и собирает единый HTML блок контактов."""
        rendered_items = []
        
        for social in social_media_list:
            url = social.url or "#"
            
            # --- УМНЫЙ И ПРОСТОЙ ПАРСИНГ НИКНЕЙМА КАК НА ХАБРЕ ---
            # 1. Отрезаем закрывающий слэш для очистки
            clean_url = url.strip().rstrip("/")
            
            # 2. Разбиваем по слэшам
            url_parts = clean_url.split("/")
            
            # 3. Если в ссылке нет никнейма (например, просто "https://github.com"),
            # то отобразим имя самой платформы ("github"). Иначе — возьмем никнейм.
            if len(url_parts) <= 3:
                display_text = social.name  # Фоллбэк на ключ ("github", "telegram")
            else:
                display_text = url_parts[-1] # Забираем сам никнейм
            
            # Добавляем красивую собачку для Telegram
            if "t.me" in url or "telegram" in social.name.lower():
                # Убедимся, что не прилепим вторую собачку, если она уже есть
                if not display_text.startswith("@") and display_text != "telegram":
                    display_text = f"@{display_text}"

            # 4. Берём готовый логотип из объекта (там уже вшит Base64 код вашей картинки!)
            logo_html = social.logo if social.logo else "<span style='font-size:1.1rem;'>🔗</span>"

            # 5. Подставляем в HTML-шаблон contact_card.html
            if self.card_template:
                item_html = self.card_template.format(
                    contact_icon=logo_html,
                    contact_url=url,
                    contact_text=display_text
                )
            else:
                # Безопасный инлайн-фоллбэк, если файла шаблона нет
                item_html = f'<div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">{logo_html} <a href="{url}" style="text-decoration:none; color:#333; font-weight:500;">{display_text}</a></div>'
                
            rendered_items.append(item_html)

        # 6. Оборачиваем в контейнер-wrapper
        if not self.wrapper_template:
            return f'<div class="contacts-block" style="display: flex; flex-direction: column; margin-top: 10px;">{"".join(rendered_items)}</div>'

        return self.wrapper_template.format(contacts_items="\n".join(rendered_items))
