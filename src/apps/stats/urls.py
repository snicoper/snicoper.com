from django.conf.urls import url

from . import views

app_name = 'stats'

urlpatterns = [

    # /
    url(
        regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'
    ),
]
