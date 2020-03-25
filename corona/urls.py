from django.urls import path
from corona import views

urlpatterns = [
    path('', views.index, name="index"),
    path('jay', views.jay, name="jay"),  
    path('translate-message', views.translate, name="translate"),  
    path('validate-translations', views.validate, name="validate"),  
    path('send_messages', views.send_messages, name="send_messages"),
    path('notify_volunteers', views.notify_volunteers, name="notify_volunteers")
    
]