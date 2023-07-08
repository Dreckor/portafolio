from django.shortcuts import render, get_object_or_404
from django.core.files import File
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

import urllib
from datetime import datetime

from .models import Project
from .functions import listar_repositorios

def home(request):
    projects = Project.objects.all()
    return render(request, 'home.html', {'projects': projects})

def detailed_project(request, post):
    #updateProjects()
    project = get_object_or_404(Project, pk=post)
    return render(request, 'project.html', {'project': project})

def enviar_mensaje(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        mensaje = request.POST.get('mensaje')
        destinatario = settings.DEFAULT_FROM_EMAIL
        
        send_mail('Nuevo mensaje', mensaje, correo, [destinatario])
        
        # Puedes enviar una respuesta JSON en lugar de redirigir a una página
        return JsonResponse({'mensaje': 'Mensaje enviado correctamente'})
    
    # Si la solicitud no es POST, devuelve un error
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def updateProjects():
    repos = listar_repositorios()
    nuevos_repos = []
    for repo in repos:
        proyecto_existente = Project.objects.filter(title=repo['title'])
        if not proyecto_existente:
            nuevo_proyecto = Project()
            nuevo_proyecto.title = repo['title']
            nuevo_proyecto.description = repo['descripcion']
            nuevo_proyecto.url = repo['url']
            fecha_actualizacion_str = repo['fecha_actualizacion'].strip('“”')
            fecha_actualizacion = datetime.strptime(fecha_actualizacion_str, "%Y-%m-%dT%H:%M:%SZ").date()
            nuevo_proyecto.fecha_modificacion = fecha_actualizacion
            if repo['imagenes']:
                image_url = repo['imagenes']
                image_name = image_url.split('/')[-1]  # Obtener el nombre de archivo de la URL
                response = urllib.request.urlopen(image_url)
                nuevo_proyecto.image.save(image_name, File(response))
            nuevo_proyecto.save()