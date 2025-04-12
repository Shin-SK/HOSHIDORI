import os
from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api
import dotenv
import dj_database_url


# envをロード
dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-i49+sc6q...')

#カスタムユーザーモデル
AUTH_USER_MODEL = 'accounts.CustomUser'

#デバッグで本番とローカルを分ける
debug_str = os.environ.get('DEBUG', 'True')
DEBUG = (debug_str.lower() == 'true')

if not DEBUG:
    ALLOWED_HOSTS = ['hoshidori-production.up.railway.app']
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

#app
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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


#DBはdj-database-urlを使ってpostgreSQLに対応させる
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600,
    )
}


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

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# whitenoiseでstaticfilesをまとめる

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
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


#Cloudinary
cloudinary.config(
    cloud_name=os.environ['CLOUDINARY_CLOUD_NAME'],
    api_key=os.environ['CLOUDINARY_API_KEY'],
    api_secret=os.environ['CLOUDINARY_API_SECRET'],
    secure=True
)

#メール系
EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT', '25'))
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = (os.environ.get('DJANGO_EMAIL_USE_TLS', 'False') == 'True')
EMAIL_USE_SSL = (os.environ.get('DJANGO_EMAIL_USE_SSL', 'False') == 'True')

DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', 'webmaster@localhost')


#CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://hoshidori-production.up.railway.app",
]
