from django.conf import settings

# Tipo de authentication, por defecto username
# both|email|username
AUTH_TYPE = getattr(settings, 'AUTH_TYPE', 'username')

# Tiempo en días antes de expirar el registro temporal, por defecto 3.
AUTH_REGISTER_EXPIRE_DAYS = getattr(settings, 'AUTH_REGISTER_EXPIRE_DAYS', 3)

# Validación username, esto es valido ('PeriCoPalotE123')
regex_username = r'^[a-zA-Z]{1}[a-zA-Z0-9]+$'
AUTH_REGEX_USERNAME = getattr(settings, 'AUTH_REGEX_USERNAME', regex_username)

# Mínimo caracteres en username.
AUTH_MIN_LENGTH_USERNAME = getattr(settings, 'AUTH_MIN_LENGTH_USERNAME', 5)

# usernames black list
AUTH_USERNAME_BLACKLIST = getattr(
    settings,
    'AUTH_USERNAME_BLACKLIST',
    [
        'admin',
        'superadmin',
        'superuser',
        'anonimous',
        'anonimo',
        'staff'
    ]
)
