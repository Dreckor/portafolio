import requests
import base64
from datetime import datetime
import re

#from models import Project

token = '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'
headers = {
        "Authorization": f"Token {token}"
    }


def obtener_repositorios(usuario):
    url = f"https://api.github.com/users/{usuario}/repos"
    
    response = requests.get(url,headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        repositorios = response.json()
        return repositorios
    else:
        print("No se pudo obtener la lista de repositorios.")
        return []
    
    
def obtener_contenido_readme(usuario, repositorios):
    readme_info = []
    for repo in repositorios:
        readme_url = f"https://api.github.com/repos/{usuario}/{repo['name']}/readme"
        
        readme_response = requests.get(readme_url,headers=headers)
        if readme_response.status_code == 200:
            readme = readme_response.json()
            readme_contenido = base64.b64decode(readme['content']).decode('utf-8')
        else:
            readme_contenido = None

        # Obtener información de fecha de actualización
        repo_url = f"https://api.github.com/repos/{usuario}/{repo['name']}"
        repo_response = requests.get(repo_url, headers=headers)
        if repo_response.status_code == 200:
            repo_info = repo_response.json()
            fecha_actualizacion = repo_info['updated_at']
        else:
            fecha_actualizacion = None

        #proyecto_existente = Project.objects.filter(title = repo['name'])
        #if not proyecto_existente:
        if readme_contenido:
            project = estandarizar_repositorios(repo, readme_contenido)
            if project != None:
                project['fecha_actualizacion'] =  fecha_actualizacion
                project['url'] = repo_url
                readme_info.append(project)

    return readme_info

def estandarizar_repositorios(repo,readme_contenido):
    match = re.search(r"Descripcion: (.+)", readme_contenido)
    descripcion = match.group(1) if match else None
    match_imagenes = re.search(r"imagenes: (.+)", readme_contenido)
    imagenes_str = match_imagenes.group(1) if match_imagenes else None

    if descripcion and imagenes_str:
        proyecto = {
            'title' : repo['name'],
            'descripcion': descripcion,
            'imagenes': imagenes_str
            }
        return proyecto
    else:
        return None
    
def listar_repositorios():
    repos = []
    usuario_github = "dreckor"
    repositorios = obtener_repositorios(usuario_github)
    readme_info = obtener_contenido_readme(usuario_github, repositorios)

    for info in readme_info:
        print(f"Repositorio: {info['title']}")
        if info['descripcion'] and info['fecha_actualizacion']:
            repos.append(info)
            print(f"Contenido del README:\n{info['descripcion']}")
        else:
            print("No se pudo obtener el contenido del README.")

        if info['fecha_actualizacion']:
            fecha = datetime.strptime(info['fecha_actualizacion'], "%Y-%m-%dT%H:%M:%SZ")
            print(f"Última fecha de actualización: {fecha}")
        if info['imagenes']:
           
            print(f"Imagen destacada: {info['imagenes']}")
        else:
            print("No se pudo obtener la imagen.")
        
    return repos

def obtener_url_imagen_perfil_github():
    usuario_github = "dreckor"
    url_api_github = f"https://api.github.com/users/{usuario_github}"

    try:
        response = requests.get(url_api_github, headers=headers)
        print(response.content)
        if response.status_code == 200:
            datos_usuario = response.json()
            imagen_perfil = datos_usuario.get("avatar_url", "")

            return imagen_perfil
        else:
            # Si la solicitud no fue exitosa, imprimir el mensaje de error
            print(f"Error al obtener datos del perfil de GitHub: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {str(e)}")
        return None


