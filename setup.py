#!/usr/bin/env python3
import sys
import time
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core import EvolutionAPIClient
from exceptions import APIConnectionError

def install_requirements():
  """Instalar dependencias de Python"""
  print("Instalando dependencias de Python...")
  try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencias instaladas correctamente")
    return True
  except subprocess.CalledProcessError as e:
    print(f"Error instalando dependencias: {e}")
    return False

def start_evolution_api():
  """Iniciar Evolution API con Docker"""
  print("Iniciando Evolution API...")
  try:
    # Verificar si Docker está corriendo
    result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
    if result.returncode != 0:
      print("Docker no esta corriendo. Inicia Docker Desktop primero.")
      return False

    # Iniciar Evolution API
    subprocess.check_call(['docker', 'compose', 'up', '-d'])
    print("Evolution API iniciado correctamente")

    # Esperar que el servicio esté listo
    print("Esperando que Evolution API este listo...")
    time.sleep(10)
    return True

  except subprocess.CalledProcessError as e:
    print(f"Error iniciando Evolution API: {e}")
    return False

def setup_whatsapp_instance():
  """Configurar instancia de WhatsApp"""
  print("Configurando instancia de WhatsApp...")
  
  try:
      client = EvolutionAPIClient()

      # Verificar si la instancia ya existe y está conectada
      if client.check_connection_status():
        print("WhatsApp ya esta conectado y listo para usar")
        return True

      # Crear instancia si no existe
      if not client.create_instance():
          print("Error creando instancia")
          return False

      # Esperar un momento
      time.sleep(3)

      # Obtener código QR
      print("Obteniendo codigo QR para conectar WhatsApp...")
      qr_code = client.get_qr_code()

      if qr_code:
        print("\n" + "="*60)
        print("ESCANEA ESTE CODIGO QR CON TU WHATSAPP:")
        print("="*60)
        print(qr_code)
        print("="*60)
        print("\nInstrucciones:")
        print("1. Abre WhatsApp en tu telefono")
        print("2. Ve a Configuracion > Dispositivos vinculados")
        print("3. Toca 'Vincular un dispositivo'")
        print("4. Escanea el codigo QR de arriba")
        print("\nEsperando conexion...")

        # Esperar conexión
        if client.wait_for_connection(timeout=120):
          print("WhatsApp conectado exitosamente!")
          return True
        else:
          print("Timeout conectando WhatsApp. Intenta de nuevo.")
          return False
      else:
        print("No se pudo obtener codigo QR")
        return False

  except (APIConnectionError, Exception) as e:
    print(f"Error configurando WhatsApp: {e}")
    return False

def create_sample_images():
  """Crear imágenes de ejemplo"""
  try:
    from PIL import Image, ImageDraw, ImageFont
    import os

    # Ensure images directory exists
    os.makedirs('images', exist_ok=True)

    images_to_create = [
      ('promocion.jpg', 'PROMOCION ESPECIAL', 'lightcoral'),
      ('oferta.jpg', 'OFERTA LIMITADA', 'lightgreen'),
      ('catalogo.jpg', 'NUEVO CATALOGO', 'lightblue')
    ]

    for filename, text, color in images_to_create:
      filepath = f'images/{filename}'
      if os.path.exists(filepath):
        continue  # Skip if already exists

      img = Image.new('RGB', (800, 600), color=color)
      draw = ImageDraw.Draw(img)

      try:
        font = ImageFont.truetype("arial.ttf", 48)
      except (OSError, IOError):
        font = ImageFont.load_default()

      # Calculate centered position
      bbox = draw.textbbox((0, 0), text, font=font)
      text_width = bbox[2] - bbox[0]
      text_height = bbox[3] - bbox[1]
      x = (800 - text_width) // 2
      y = (600 - text_height) // 2

      draw.text((x, y), text, fill='white', font=font)

      try:
        img.save(filepath, 'JPEG')
      finally:
        img.close()  # Prevent resource leak

    print("Imagenes de ejemplo creadas en /images")
    return True

  except ImportError:
    print("Pillow no instalado. Saltando creacion de imagenes.")
    return True
  except Exception as e:
    print(f"No se pudieron crear imagenes de ejemplo: {e}")
    return False

def main():
  print("Configurando Next Message...")
  print("="*50)

  try:
    # Crear directorios necesarios
    directories = ['contacts', 'images', 'logs']
    for directory in directories:
      Path(directory).mkdir(exist_ok=True)
      print(f"Directorio verificado: {directory}")

    # Instalar dependencias
    if not install_requirements():
      return False

    # Crear imágenes de ejemplo
    create_sample_images()

    # Iniciar Evolution API
    if not start_evolution_api():
      return False

    # Configurar instancia de WhatsApp
    if not setup_whatsapp_instance():
      return False

    print("\nConfiguracion completada exitosamente!")
    print("\nProximos pasos:")
    print("1. Edita contacts/contacts.csv con tus contactos reales")
    print("2. Coloca tus imagenes en la carpeta images/")
    print("3. Ejecuta: python main.py")
    print("\nIMPORTANTE: Manten WhatsApp conectado en tu telefono")

    return True

  except KeyboardInterrupt:
    print("\nConfiguracion cancelada por el usuario")
    return False
  except Exception as e:
    print(f"Error inesperado: {e}")
    return False

if __name__ == "__main__":
  main()