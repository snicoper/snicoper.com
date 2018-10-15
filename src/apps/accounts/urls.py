from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [

    # Perfil de usuario.
    url(
        regex=r'^profile/$',
        view=views.UserProfileView.as_view(),
        name='profile'
    ),

    # Actualizar perfil.
    url(
        regex=r'^profile/update/$',
        view=views.UserProfileUpdateView.as_view(),
        name='profile_update'
    ),

    # Cambiar/añadir avatar de usuario.
    url(
        regex=r'^avatar/update/$',
        view=views.UserAvatarUpdateView.as_view(),
        name='avatar_update'
    ),
]
