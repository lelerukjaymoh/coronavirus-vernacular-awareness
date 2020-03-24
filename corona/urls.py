from django.urls import path
from corona import views

urlpatterns = [
    path('', views.index, name="index"),
    path('jay', views.jay, name="jay"),  
    path('send_messages', views.send_messages, name="send_messages")
]