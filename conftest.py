import sys
import os

# Добавляем папку yatube_api в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yatube_api'))

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatube_api.settings')


# Настройки для pytest
def pytest_configure():
    import django
    django.setup()
