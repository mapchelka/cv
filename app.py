import streamlit as st
import streamlit.components.v1 as components
from core.config_loader import Config
from core.personal_data import PersonalData
from core.card_renderer import JobCardRenderer, EduCardRenderer, ContactCardRenderer

# 1. Инициализируем и загружаем конфигурацию (JSON, CSS и HTML-шаблоны)
config = Config()
config.load()

# 2. Подключаем глобальные CSS стили из main.css
if config.css_content:
    st.markdown(f"<style>{config.css_content}</style>", unsafe_allow_html=True)

# 3. Инициализируем бизнес-логику и рендереры карточек
person = PersonalData(config)
contact_renderer = ContactCardRenderer(config)
job_card_renderer = JobCardRenderer(config)
edu_card_renderer = EduCardRenderer(config)

# 4. Устанавливаем метаданные вкладки браузера напрямую из объекта person
st.set_page_config(page_title=person.page_title, page_icon=person.page_icon)

# --- Кнопка печати
if config.print_button_template:
    components.html(config.print_button_template, height=45)

# --- Блок профиля (Аватар + Имя + Контакты)
col1, col2 = st.columns([1, 2], gap="small")
with col1:
    if person.profile_pic_html:
        st.html(person.profile_pic_html)
with col2:
    st.title(person.name)
    st.html(contact_renderer.render_block(person.social_media))

# Краткое описание/о себе
st.markdown(person.description)

# --- СЕКЦИЯ: ОПЫТ РАБОТЫ ---
st.subheader("Опыт работы")
st.write("---")

for job in person.work_history:
    col_logo, col_info = st.columns([1, 12], gap="small")
    with col_logo:
        # Логотип автоматически подтянется из подпапки assets/company/
        if job.logo:
            st.html(job.logo)
            
    with col_info:
        st.html(job_card_renderer.render(job))
    st.write("")


# --- СЕКЦИЯ: ОБРАЗОВАНИЕ ---
st.subheader("Образование")
st.write("---")

for edu in person.education:
    col_logo, col_info = st.columns([1, 12], gap="small")
    with col_logo:
        # Логотип автоматически подтянется из подпапки assets/education/
        if edu.logo:
            st.html(edu.logo)
            
    with col_info:
        st.html(edu_card_renderer.render(edu))
    st.write("")