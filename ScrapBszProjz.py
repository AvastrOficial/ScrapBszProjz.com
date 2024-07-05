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
         BY @AvastrOficial / Verision : 0.0.1
    """
    print(Fore.RED + banner)
    print("=" * 50)
    print("      Bienvenido al Scraper de Imágenes de Projz      ")
    print("=" * 50)
    print("1. Introducir perfil de usuario")
    print("2. Mostrar mensaje de redes sociales")
    print("=" * 50)

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
    os.makedirs('imagenes', exist_ok=True)
    image_urls = []
    images = soup.find_all('img')

    for img in images:
        img_src = img.get('src')
        if img_src.startswith('data:image'):
            print(f'Ignorando imagen en formato base64: {img_src[:30]}...')
            continue
        img_src = urljoin(url, img_src)
        image_urls.append(img_src)
        try:
            img_response = requests.get(img_src)
            img_response.raise_for_status()
            img_name = os.path.basename(img_src)
            img_path = os.path.join('imagenes', img_name)
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
            print(f'Imagen guardada: {img_path}')
        except requests.RequestException as e:
            print(f'Error al descargar la imagen {img_src}: {e}')

    user_icon_images = soup.find_all('img', alt='user-icon')
    for img in user_icon_images:
        img_src = img.get('src')
        img_src = urljoin(url, img_src)
        if img_src not in image_urls:
            image_urls.append(img_src)
        try:
            img_response = requests.get(img_src)
            img_response.raise_for_status()
            img_name = os.path.basename(img_src)
            img_path = os.path.join('imagenes', img_name)
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
            print(f'Imagen guardada: {img_path}')
        except requests.RequestException as e:
            print(f'Error al descargar la imagen {img_src}: {e}')

    styles = soup.find_all(style=True)
    for style in styles:
        style_content = style.get('style')
        urls = re.findall(r'background-image:\s*url\(["\']?(.*?)["\']?\)', style_content)
        for img_url in urls:
            img_src = urljoin(url, img_url)
            image_urls.append(img_src)
            try:
                img_response = requests.get(img_src)
                img_response.raise_for_status()
                img_name = os.path.basename(img_src)
                img_path = os.path.join('imagenes', img_name)
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                print(f'Imagen guardada: {img_path}')
            except requests.RequestException as e:
                print(f'Error al descargar la imagen {img_src}: {e}')

    with open('imagenes/imagenes.json', 'w') as f:
        json.dump({'imagenes': image_urls}, f, indent=4)
    print('Las URLs de las imágenes han sido guardadas en imagenes/imagenes.json')

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
        else:
            print("Opción no válida. Por favor, selecciona 1 o 2.")

        # Preguntar si el usuario desea continuar usando la herramienta
        respuesta = input("¿Deseas volver a usar esta herramienta? (si/no): ").strip().lower()
        if respuesta != "si":
            break
