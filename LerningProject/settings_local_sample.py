from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)6#7+%fn)=-cog9ebf#h$hhvqb+*@84_i!6ll46o@n7f3(5%fm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
# 本番環境ではFalseにする

# 配信するドメインやIP
ALLOWED_HOSTS = ["*"]
# PythonAnuwhereの無料プランの場合は
# ALLOWED_HOSTS = ["<username>.pythonanywhere.com"]
DOMAIN="127.0.0.1:8000"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}

# サインアップの可否
SIGNUP = True

