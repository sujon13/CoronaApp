from django.urls import path
from corona_stat import views

urlpatterns = [
    path('', views.CoronaStatList.as_view()),
    path('districts/', views.CoronaStatOfDistrict.as_view()),


]
