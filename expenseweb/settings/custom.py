# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q++(!8%hw60cox98fvprx1w#r4xu2b1pq*nnw$8!)z^*@(^qi&'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'expense_db',
        'HOST': '34.64.134.218',
        'USER': 'postgres',
        'PASSWORD': '1Ck5Dh711^^',
        'PORT': 5432
        
    }
}