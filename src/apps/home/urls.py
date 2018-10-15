from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [

    # /home/
    url(
        regex=r'^$',
        view=views.IndexView.as_view(),
        name='index',
    ),
]
