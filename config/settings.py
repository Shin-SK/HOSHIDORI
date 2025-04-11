import os
from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-i49+sc6q...')  
DEBUG = bool(os.environ.get('DEBUG', True)) 

AUTH_USER_MODEL = 'accounts.CustomUser'

if not DEBUG:
    ALLOWED_HOSTS = ['hoshidori-production.up.railway.app']
else:
    ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_browser_reload',
    'django_filters',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',  # SNSログイン使うなら
    'accounts',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',  # 必須
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ★これでプロジェクト直下の templates を参照
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ② Railwayの環境変数があればPostgreSQLに切り替え
#    例: 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT' を設定していると想定
POSTGRES_NAME = os.environ.get('DB_NAME')
POSTGRES_USER = os.environ.get('DB_USER')
POSTGRES_PASSWORD = os.environ.get('DB_PASSWORD')
POSTGRES_HOST = os.environ.get('DB_HOST')
POSTGRES_PORT = os.environ.get('DB_PORT')

if all([POSTGRES_NAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT]):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_NAME,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # 例
    # 絶対パスを書くなら
    # '/Users/skii/Library/CloudStorage/Dropbox/EXMATCH/static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
LOGIN_REDIRECT_URL = '/'     # ログイン後のリダイレクト先
ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # ログアウト後のリダイレクト先

# 旧: ACCOUNT_AUTHENTICATION_METHOD = 'username_email' は非推奨
# 新: ログイン方法をセット型で指定
ACCOUNT_LOGIN_METHODS = {
    'username',
    'email',
}
# {'username','email'} で「ユーザー名またはメール」でログイン可能
# {'email'} だけにすれば「メールでのみログイン」
# {'username'} だけなら「ユーザー名のみ」

ACCOUNT_SIGNUP_FIELDS = [
    'email*',       # 「*」を付けると必須扱い
    'password1*',   # パスワード
    'password2*',   # パスワード確認
    # 'username',    # ユーザー名を入力させたいなら追加
    # 'nickname',    # カスタムフィールドがあれば追加できる
]

# これで「メール + パスワード」でアカウント作成＆ログインが可能となる
# username は不要なので signup画面に出ない

ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',  # パスを記述
}

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False



# Cloudinary設定

# ③ Cloudinary設定
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'ddfvexdsf'),
    api_key = os.environ.get('CLOUDINARY_API_KEY', '587674237252344'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', 'O2LoXcTpe-hoA051AcFHL6hi0O0'),
    secure=True
)