from django.urls import path
from .views import home, detailed_project, enviar_mensaje

app_name = 'entrys' 

urlpatterns = [
    path('', home, name='home'),
    path('<int:post>', detailed_project, name='project'),
    path('enviar_mensaje/', detailed_project, name='enviar_mensaje')
]