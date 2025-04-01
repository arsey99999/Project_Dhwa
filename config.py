import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'minhwa.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "minhwa_is_amazing_secret_key"

# 쿠키관련 설정
SESSION_COOKIE_NAME = 'session'  
SESSION_COOKIE_PATH = '/'  
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_PERMANENT = False

# 세션관련 설정
PERMANENT_SESSION_LIFETIME = 1800 #30분

#WTF_CSRF_ENABLED = False  # CSRF 보호 비활성화