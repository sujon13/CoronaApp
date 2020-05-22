from django.urls import path
from corona_stat import views

urlpatterns = [
    path('<str:day>/', views.CoronaStatList.as_view()),
]
