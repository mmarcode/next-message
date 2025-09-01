#!/usr/bin/env python3
import sys
import argparse
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core import EvolutionAPIClient, MessageSender
from exceptions import APIConnectionError, ConfigurationError
from utils import sanitize_for_log

def check_status():
  """Check WhatsApp connection status"""
  try:
    print("Verificando estado de Evolution API...")
    client = EvolutionAPIClient()

    if client.check_connection_status():
      print("WhatsApp esta conectado y listo")
      return True
    else:
      print("WhatsApp no esta conectado")
      print("Ejecuta 'python setup.py' para conectar")
      return False

  except (APIConnectionError, ConfigurationError) as e:
    print(f"Error verificando estado: {e}")
    return False

def send_single_message(phone: str, message: str, message_type: str, caption: str = ''):
  """Send single message"""
  try:
    print(f"Enviando mensaje individual a {sanitize_for_log(phone)}")
    sender = MessageSender()

    contact = {
      'phone': phone,
      'message_type': message_type,
      'content': message,
      'caption': caption,
      'name': 'Usuario'
    }

    success = asyncio.run(sender.send_single_message(contact))

    if success:
      print("Mensaje enviado exitosamente")
    else:
      print("Error enviando mensaje")

  except Exception as e:
    print(f"Error en envio individual: {e}")

def send_bulk_messages(contacts_file: str):
  """Send bulk messages"""
  try:
      print("Iniciando envio masivo...")
      print("Verificando conexion de WhatsApp...")

      # Verify connection
      client = EvolutionAPIClient()
      if not client.check_connection_status():
        print("WhatsApp no esta conectado")
        print("Ejecuta 'python setup.py' para conectar primero")
        return

      print("WhatsApp conectado, iniciando envio...")

      # Start bulk sending
      sender = MessageSender()
      results = sender.send_bulk_messages(contacts_file)

      # Show final summary
      print("\n" + "="*50)
      print("RESUMEN FINAL DEL ENVIO MASIVO")
      print("="*50)
      print(f"Mensajes exitosos: {results['success']}")
      print(f"Mensajes fallidos: {results['failed']}")
      print(f"Total procesados: {results['total']}")

      if results['total'] > 0:
        success_rate = (results['success'] / results['total']) * 100
        print(f"Tasa de exito: {success_rate:.1f}%")

      print("="*50)
      
      if results['success'] > 0:
        print("Envio masivo completado exitosamente!")
      else:
        print("No se enviaron mensajes. Revisa la configuracion.")

  except Exception as e:
    print(f"Error en envio masivo: {e}")

def main():
  parser = argparse.ArgumentParser(description='Evolution WhatsApp Sender - Envío masivo gratuito')
  parser.add_argument('--mode', choices=['bulk', 'single', 'status'], default='bulk',
                      help='Modo: bulk (masivo), single (individual), status (verificar)')
  parser.add_argument('--phone', help='Número para envío individual')
  parser.add_argument('--message', help='Mensaje para envío individual')
  parser.add_argument('--type', choices=['text', 'image'], default='text',
                      help='Tipo de mensaje: text o image')
  parser.add_argument('--caption', default='', help='Texto para imagen (opcional)')
  parser.add_argument('--contacts', default='contacts/contacts.csv',
                      help='Archivo de contactos para envío masivo')

  args = parser.parse_args()

  try:
    if args.mode == 'status':
      check_status()
    elif args.mode == 'single':
      if not args.phone or not args.message:
        print("Error: Para envio individual necesitas --phone y --message")
        print("Ejemplo: python main.py --mode single --phone +525512345678 --message 'Hola mundo'")
        return
      send_single_message(args.phone, args.message, args.type, args.caption)
    elif args.mode == 'bulk':
      send_bulk_messages(args.contacts)
  except KeyboardInterrupt:
    print("\nOperacion cancelada por el usuario")
  except Exception as e:
    print(f"Error inesperado: {e}")
    sys.exit(1)

if __name__ == "__main__":
  main()