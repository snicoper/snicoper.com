from django.conf.urls import url

from . import views

app_name = 'authentication'

urlpatterns = [

    # Muestra el formulario de registro.
    url(
        regex=r'^register/$',
        view=views.RegisterUserFormView.as_view(),
        name='register'
    ),

    # El registro ha sido satisfactorio.
    url(
        regex=r'^register/success/$',
        view=views.RegisterUserSuccessView.as_view(),
        name='success'
    ),

    # Valida un token.
    url(
        regex=r'^register/validate/(?P<token>[a-zA-Z0-9]{32})/$',
        view=views.RegisterUserValidateTokenView.as_view(),
        name='validate_token'
    ),

    # Formulario login.
    url(
        regex=r'^login/$',
        view=views.LoginView.as_view(),
        name='login'
    ),

    # Logout.
    url(
        regex=r'^logout/$',
        view=views.LogoutView.as_view(),
        name='logout'
    ),

    # Formulario cambiar contraseña.
    url(
        regex=r'^password-change/$',
        view=views.PasswordChangeView.as_view(),
        name='password_change'
    ),

    # Muestra mensaje cambio password ok.
    url(
        regex=r'^password-change/done/$',
        view=views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),

    # Restablecer contraseña (Contraseña olvidada).
    url(
        regex=r'^password-reset/$',
        view=views.PasswordResetView.as_view(),
        name='password_reset'
    ),

    # Informa al usuario que se ha mandado un email para restablecer la contraseña.
    url(
        regex=r'^password-reset/done/$',
        view=views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),

    # Verifica el token, se accede desde el email.
    # Si es correcto, mostrara un formulario para crear nueva contraseña.
    url(
        regex=(
            r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
            r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'
        ),
        view=views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    # El token se ha verificado y muestra el resultado.
    url(
        regex=r'^reset/done/$',
        view=views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),

    # Actualizar el email.
    url(
        regex=r'^email/update/$',
        view=views.UserEmailUpdateView.as_view(),
        name='email_update'
    ),

    # Validación del token para cambiar el email.
    url(
        regex=r'^email/validate/(?P<token>[\w]{30})/$',
        view=views.UserEmailUpdateValidateView.as_view(),
        name='email_update_validate'
    ),

    # Token para cambiar email no existe.
    url(
        regex=r'^token/error/$',
        view=views.UserEmailUpdateNotFoundView.as_view(),
        name='token_email_not_exists'
    ),
]
