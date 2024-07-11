import os
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urljoin
import time
import json
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

def mostrar_banner():
    banner = """
 ____                 _________       _                 
/ ___|  ___ _ __ _ __|__  / ___| __ _| | ___ _ __ _   _ 
\___ \ / __| '__| '_ \ / / |  _ / _` | |/ _ \ '__| | | |
 ___) | (__| |  | |_) / /| |_| | (_| | |  __/ |  | |_| |
|____/ \___|_|  | .__/____\____|\__,_|_|\___|_|   \__, |
                |_|                               |___/ 
         BY @AvastrOficial / Version : 0.0.2
    """
    print(Fore.RED + banner)
    print("=" * 50)
    print("      Bienvenido al Scraper de Imágenes de Projz      ")
    print("=" * 50)
    print("1. Introducir perfil de usuario")
    print("2. Mostrar mensaje de redes sociales")
    print("3. Introducir el URL del chat o fiesta")
    print("=" * 50)

def guardar_imagen(img_src, carpeta, nombre):
    os.makedirs(carpeta, exist_ok=True)
    img_path = os.path.join(carpeta, nombre)
    try:
        img_response = requests.get(img_src)
        img_response.raise_for_status()
        with open(img_path, 'wb') as f:
            f.write(img_response.content)
        print(f'Imagen guardada: {img_path}')
    except requests.RequestException as e:
        print(f'Error al descargar la imagen {img_src}: {e}')

def descargar_imagenes(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')

    driver = webdriver.Chrome(service=Service('chromedriver'), options=options)
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    image_urls = []
    images = soup.find_all('img')

    for img in images:
        img_src = img.get('src')
        if img_src.startswith('data:image'):
            print(f'Ignorando imagen en formato base64: {img_src[:30]}...')
            continue
        img_src = urljoin(url, img_src)
        image_urls.append(img_src)
        img_name = os.path.basename(img_src)

        if 'header-logo' in img_name:
            guardar_imagen(img_src, 'logo de la app', img_name)
        elif 'ant-avatar ant-avatar-circle ant-avatar-image' in img.get('class', []):
            guardar_imagen(img_src, 'ultimos usuarios unidos', img_name)
        else:
            guardar_imagen(img_src, 'Fotos de usuarios unidos', img_name)

    styles = soup.find_all(style=True)
    for style in styles:
        style_content = style.get('style')
        urls = re.findall(r'background-image:\s*url\(["\']?(.*?)["\']?\)', style_content)
        for img_url in urls:
            img_src = urljoin(url, img_url)
            image_urls.append(img_src)
            img_name = os.path.basename(img_src)
            guardar_imagen(img_src, 'portada de fiesta', img_name)

    with open('Fotos de usuarios unidos/imagenes.json', 'w') as f:
        json.dump({'imagenes': image_urls}, f, indent=4)
    print('Las URLs de las imágenes han sido guardadas en Fotos de usuarios unidos/imagenes.json')

def obtener_id_chat(url):
    api_url = f'https://www.projz.com/api/f/v1/parse-share-link?url={url}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Apptype': 'z-web',
        'Devicetype': '1',
        'Origin': 'https://www.projz.com',
        'Ostype': '1',
        'Referer': url,
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        share_link = data.get('shareLink', '')
        print(f'Link compartido: {share_link}')

        match = re.search(r'/s/ch/(\w+)', share_link)
        if match:
            object_id = match.group(1)
            print(f'objectId encontrado: {object_id}')

            id_api_url = f'https://www.projz.com/api/f/v1/id?objectId={object_id}'
            response = requests.get(id_api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            path = data.get('path', 'No encontrado')
            print(f'Path del chat: {path}')

            os.makedirs('Fotos de usuarios unidos', exist_ok=True)
            with open('Fotos de usuarios unidos/chat_id.txt', 'w') as f:
                f.write(str(path))
            print('El path del chat ha sido guardado en Fotos de usuarios unidos/chat_id.txt')
        else:
            print('No se encontró objectId en el shareLink.')
    except requests.exceptions.RequestException as e:
        print(f'Error al hacer la solicitud: {e}')
    except json.JSONDecodeError:
        print('La respuesta no es un JSON válido.')

def mostrar_mensaje_redes_sociales():
    print("¡Síguenos en nuestras redes sociales!")
    print("Github : @AvastrOficial")
    print("Telegram : https://t.me/+sOf-gqn6SClmNDcx")

if __name__ == "__main__":
    while True:
        os.system('clear')  # Limpiar pantalla (sistema Unix/Linux)
        mostrar_banner()
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            perfil_usuario = input("Por favor, introduce la URL del perfil del usuario: ").strip()
            descargar_imagenes(perfil_usuario)
        elif opcion == "2":
            mostrar_mensaje_redes_sociales()
        elif opcion == "3":
            url_chat_fiesta = input("Por favor, introduce la URL del chat o fiesta: ").strip()
            obtener_id_chat(url_chat_fiesta)
            descargar_imagenes(url_chat_fiesta)
        else:
            print("Opción no válida. Por favor, selecciona 1, 2 o 3.")

        respuesta = input("¿Deseas volver a usar esta herramienta? (si/no): ").strip().lower()
        if respuesta != "si":
            break
