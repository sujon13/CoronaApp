from django.urls import path
from corona_stat import views

urlpatterns = [
    path('<str:day>/', views.CoronaStatList.as_view()),
    path('districts/', views.CoronaStatOfDistrict.as_view()),
    path('live_news/prothomalo/', views.CoronaLive.as_view()),


]
