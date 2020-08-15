from django.urls import path, re_path
from .views import StartGameView, GameProcessView


app_name = 'server'

urlpatterns = [
    path('startgame/', StartGameView.as_view()),
    re_path('playershoot/(?P<coord>[^/]*)/', GameProcessView.as_view())
]
