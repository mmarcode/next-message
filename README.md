# 📱 Next Message

**Sistema de envío masivo de mensajes de WhatsApp** usando Evolution API con arquitectura moderna, seguridad reforzada y fácil configuración.

## ✨ Características Principales

- 🚀 **Envío masivo** de mensajes de texto e imágenes
- 🔄 **Envío asíncrono** con control de concurrencia
- 🛡️ **Arquitectura segura** con validación y sanitización
- 📈 **Logs detallados** para monitoreo y debugging
- ⚙️ **Configuración flexible** mediante variables de entorno
- 🔧 **Fácil instalación** con Docker y scripts automatizados
- 📝 **Caption personalizable** para imágenes
- 🎯 **Imágenes locales** desde carpeta images/


## 📎 Tabla de Contenidos

- [Requisitos](#-requisitos)
- [Instalación Rápida](#-instalación-rápida)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Comandos Make](#-comandos-make)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Troubleshooting](#-troubleshooting)
- [Contribuir](#-contribuir)

## 💻 Requisitos

### Software Necesario
- **Python 3.8+** (recomendado 3.10+)
- **Docker Desktop** (para Evolution API)
- **Git** (para clonar el repositorio)
- **Make** (opcional, para comandos automatizados)

### Sistemas Operativos Soportados
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+)

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Recomendada)

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd next-message

# 2. Configuración completa automática
make dev
```

### Opción 2: Instalación Manual

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd next-message

# 2. Instalar dependencias Python
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 4. Configurar contactos
cp contacts/contacts.example.csv contacts/contacts.csv
# Editar contacts/contacts.csv con tus contactos reales

# 5. Levantar Evolution API
docker compose up -d

# 6. Configurar WhatsApp
python setup.py
```

## ⚙️ Configuración

### 1. Variables de Entorno

Copia y edita el archivo de configuración:

```bash
cp .env.example .env
```

Edita `.env` con tus configuraciones:

```bash
# Evolution API Configuration
EVOLUTION_API_URL=http://localhost:8080
INSTANCE_NAME=whatsapp_new
# IMPORTANTE: Cambia esta API key por una segura
API_KEY=tu_api_key_segura_aqui

# Message Configuration
DELAY_BETWEEN_MESSAGES=2          # Segundos entre mensajes
MAX_CONCURRENT_MESSAGES=5         # Máximo mensajes simultáneos
RETRY_ATTEMPTS=3                  # Intentos de reenvío

# Logging
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR

# Security
ENFORCE_HTTPS=false               # true en producción
```

### 2. Configurar Contactos

Copia y edita el archivo de contactos:

```bash
cp contacts/contacts.example.csv contacts/contacts.csv
```

Edita `contacts/contacts.csv` con tus contactos:

```csv
name,phone,message_type,content,caption
Juan Perez,+525512345678,text,Hola Juan! Este es un mensaje de prueba.,
Maria Lopez,+525587654321,text,Hola Maria! Saludos desde Next Message.,
Carlos Imagen con texto,+525511111111,image,mi_imagen.png,Mi imagen personalizada
Carlos Imagen sin texto,+525511111111,image,mi_imagen.png,
```

**Nueva columna `caption`**:
- **Con texto**: Escribe el texto que acompañará la imagen
- **Sin texto**: Deja el campo vacío para enviar solo la imagen
- **Mensajes de texto**: Siempre dejar vacío el caption

**Formato de teléfonos**: 
- **Recomendado**: Formato internacional con `+` (ej: `+525512345678`)
- **También acepta**: Sin `+` para códigos de país comunes (ej: `525512345678`)
- **Códigos soportados**: México (52), USA/Canadá (1), España (34), Reino Unido (44), etc.

### 3. Añadir Imágenes

**✅ Funcionalidad Completa**: El sistema envía imágenes locales desde la carpeta `images/`.

#### **Cómo Usar Imágenes:**

1. **Colocar imagen en carpeta**:
```bash
cp mi_imagen.png images/
```

2. **Configurar en CSV**:
```csv
name,phone,message_type,content,caption
Juan con texto,+525512345678,image,mi_imagen.png,Mi imagen favorita
Juan sin texto,+525512345678,image,mi_imagen.png,
```

3. **Enviar**:
```bash
# Individual con caption
python main.py --mode single --phone +525512345678 --message "mi_imagen.png" --type image --caption "Mi texto"

# Individual sin caption
python main.py --mode single --phone +525512345678 --message "mi_imagen.png" --type image

# Masivo
python main.py --mode bulk
```

**Especificaciones**:
- ✅ **Formatos soportados**: JPG, PNG, GIF
- ✅ **Tamaño máximo**: 5MB
- ✅ **Caption personalizable**: Con texto o sin texto
- ✅ **Validación automática**: Formato y tamaño
- ⚠️ **Solo carpeta images/**: No acepta rutas externas

## 📱 Uso

### Verificar Estado de WhatsApp

Antes de enviar mensajes, verifica que WhatsApp esté conectado:

```bash
python main.py --mode status
```

### Envío Individual

```bash
# Mensaje de texto
python main.py --mode single --phone +525512345678 --message "Hola mundo" --type text

# Imagen con caption personalizado
python main.py --mode single --phone +525512345678 --message "mi_imagen.png" --type image --caption "Mi texto personalizado"

# Imagen sin caption (solo imagen)
python main.py --mode single --phone +525512345678 --message "mi_imagen.png" --type image
```

### Envío Masivo

```bash
# Usar archivo de contactos por defecto
python main.py --mode bulk

# Usar archivo de contactos personalizado
python main.py --mode bulk --contacts mi_lista.csv
```

### Ejemplos de Uso Completo

```bash
# 1. Verificar conexión
make check-status

# 2. Envío masivo con archivo por defecto
make send-bulk

# 3. Envío individual rápido
make send-single PHONE="+525512345678" MESSAGE="Hola desde Next Message"
```

## 🛠️ Comandos Make

### Comandos de Instalación
```bash
make install      # Instalar dependencias Python
make build        # Construir contenedores Docker
make up           # Levantar Evolution API
make setup        # Configuración inicial completa
make dev          # Desarrollo completo desde cero
```

### Comandos de Uso
```bash
make check-status # Verificar estado de WhatsApp
make send-single  # Envío individual (requiere PHONE y MESSAGE)
make send-bulk    # Envío masivo
```

### Comandos de Desarrollo
```bash
make logs         # Ver logs de Evolution API
```

### Comandos de Mantenimiento
```bash
make down         # Detener servicios
make restart      # Reiniciar servicios
make clean        # Limpiar contenedores y volúmenes
```

## Estructura

## 📁 Estructura del Proyecto

```
next-message/
├── src/                      # Código fuente modular
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py       # Configuración centralizada y validada
│   ├── core/
│   │   ├── __init__.py
│   │   ├── client.py         # Cliente Evolution API con manejo de errores
│   │   └── sender.py         # Envío masivo asíncrono optimizado
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logging.py        # Logging seguro (previene log injection)
│   │   └── validators.py     # Validadores de entrada
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── custom_exceptions.py  # Excepciones personalizadas
│   ├── constants.py          # Constantes centralizadas
│   └── __init__.py
├── contacts/                 # Archivos CSV de contactos
│   ├── contacts.csv          # Tus contactos (no se sube a git)
│   └── contacts.example.csv  # Plantilla de ejemplo
├── images/                   # Imágenes para envío
│   ├── .gitkeep              # Mantiene carpeta en git
│   └── README.txt            # Instrucciones
├── logs/                     # Logs de aplicación (generados automáticamente)
├── evolution_data/           # Datos de WhatsApp (generado automáticamente)
├── main.py                   # Ejecutable principal
├── setup.py                  # Script de configuración inicial
├── requirements.txt          # Dependencias Python
├── Makefile                  # Comandos automatizados
├── compose.yml               # Configuración Docker para Evolution API
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Archivos ignorados por Git
├── CHANGELOG.md              # Historial de cambios
└── README.md                 # Esta documentación
```

### Descripción de Archivos Importantes

- **`main.py`**: Punto de entrada principal con CLI
- **`setup.py`**: Configuración automática de WhatsApp y dependencias
- **`src/core/client.py`**: Cliente Evolution API con manejo robusto de errores
- **`src/core/sender.py`**: Lógica de envío masivo asíncrono
- **`src/config/settings.py`**: Configuración centralizada con validación
- **`contacts/contacts.csv`**: Lista de contactos en formato CSV
- **`.env`**: Variables de entorno (copiar a `.env.local` y personalizar)

## 🔍 Troubleshooting

### Problemas Comunes

#### 1. "❌ Error creando instancia" durante `make dev`
```bash
# Causa: La instancia ya existe
# Solución automática: El setup.py detecta instancias existentes
python setup.py  # Debería mostrar "WhatsApp ya esta conectado"

# Verificar estado:
make check-status

# Si necesitas recrear la instancia:
make clean  # Limpia datos de WhatsApp
make dev    # Reconfigura desde cero
```

#### 2. "WhatsApp no está conectado"
```bash
# Solución:
python setup.py  # Reconfigurar WhatsApp
# O usar:
make setup
```

#### 3. "Docker no está corriendo"
```bash
# Solución:
# 1. Abrir Docker Desktop
# 2. Esperar que inicie completamente
# 3. Ejecutar:
make up
```

#### 4. "Error de conexión a Evolution API"
```bash
# Verificar estado:
docker compose ps

# Ver logs:
make logs

# Reiniciar servicios:
make restart
```

#### 5. "Número de teléfono inválido"
```bash
# Formatos válidos:
+525512345678    # Con + (recomendado)
525512345678     # Sin + (México)
15551234567      # Sin + (USA/Canadá)

# Formatos inválidos:
5512345678       # Sin código de país
123456789        # Muy corto
999123456789     # Código de país desconocido
```

## 🔒 Seguridad

### ⚠️ **IMPORTANTE - Archivos Sensibles**

Este proyecto incluye un `.gitignore` que protege archivos sensibles:

```bash
# Archivos que NO se suben a GitHub:
contacts/*.csv          # Tus contactos reales
images/*               # Tus imágenes personales
evolution_data/        # Datos de WhatsApp
logs/                  # Logs con información sensible
.env                   # Variables de entorno con credenciales
```

### 🛡️ **Configuración Inicial Segura**

```bash
# 1. Copiar archivos de ejemplo
cp .env.example .env
cp contacts/contacts.example.csv contacts/contacts.csv

# 2. Editar con tus datos reales (estos archivos NO se suben a git)
vim .env                    # Configurar API_KEY y otros
vim contacts/contacts.csv   # Añadir tus contactos reales

# 3. Añadir tus imágenes
cp mi_imagen.png images/    # Tus imágenes NO se suben a git
```

### Buenas Prácticas Implementadas
- ✅ Sanitización de logs (previene log injection)
- ✅ Validación de entrada de datos
- ✅ Variables de entorno para credenciales
- ✅ Manejo seguro de excepciones
- ✅ Dependencias sin vulnerabilidades conocidas
- ✅ **.gitignore robusto** que protege datos sensibles

### Recomendaciones
- 🔐 **Cambia el API_KEY** por defecto en producción
- 🚫 **Nunca subas** archivos `.env` o `contacts.csv` a repositorios públicos
- 🔄 **Rota credenciales** periódicamente
- 📱 **Usa números verificados** para evitar bloqueos de WhatsApp
- ⏱️ **Respeta delays** entre mensajes para evitar spam detection

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abre** un Pull Request

### Formato de Commits
```bash
feat: nueva funcionalidad
fix: corrección de bug
docs: actualización de documentación
refactor: refactorización de código
test: agregar pruebas
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Si tienes problemas o preguntas:

1. **Revisa** la sección [Troubleshooting](#-troubleshooting)
2. **Busca** en los issues existentes
3. **Crea** un nuevo issue con detalles del problema

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**r código de país** siempre
- **No usar espacios ni guiones** en el CSV
- **El sistema agrega `+` automáticamente** si falta

#### 6. "Dependencias no instaladas"
```bash
# Reinstalar dependencias:
make install

# O manualmente:
pip install -r requirements.txt
```

#### 7. "Imagen no se encuentra"
```bash
# Error: Image file not found: images/mi_imagen.png
# Solución:

# 1. Verificar que la imagen existe
ls images/

# 2. Copiar imagen a la carpeta correcta
cp mi_imagen.png images/

# 3. Verificar formato soportado
# Soportados: .jpg, .jpeg, .png, .gif
# No soportados: .webp, .bmp, .tiff

# 4. Verificar tamaño (máximo 5MB)
ls -lh images/mi_imagen.png
```

#### 8. "Caption no aparece en WhatsApp"
```bash
# Verificar formato CSV:
name,phone,message_type,content,caption
Juan,+525512345678,image,mi_imagen.png,Mi texto aquí

# Caption vacío (solo imagen):
Juan,+525512345678,image,mi_imagen.png,

# En CLI:
python main.py --mode single --phone +525512345678 --message "mi_imagen.png" --type image --caption "Mi texto"
```

### Logs y Debugging

```bash
# Ver logs de la aplicación
tail -f logs/evolution_api.log
tail -f logs/message_sender.log

# Ver logs de Docker
make logs

# Ejecutar en modo debug
LOG_LEVEL=DEBUG python main.py --mode status
```

### Limpiar y Reiniciar

```bash
# Limpiar todo y empezar de nuevo
make clean
make dev
```

## 📊 Monitoreo y Logs

### Ubicación de Logs
- **Aplicación**: `logs/evolution_api.log`, `logs/message_sender.log`
- **Docker**: `docker compose logs evolution-api`

### Niveles de Log
- **DEBUG**: Información detallada para debugging
- **INFO**: Información general de operación
- **WARNING**: Advertencias que no detienen la ejecución
- **ERROR**: Errores que requieren atención

## 🔒 Seguridad

### ⚠️ **IMPORTANTE - Archivos Sensibles**

Este proyecto incluye un `.gitignore` que protege archivos sensibles:

```bash
# Archivos que NO se suben a GitHub:
contacts/*.csv          # Tus contactos reales
images/*               # Tus imágenes personales
evolution_data/        # Datos de WhatsApp
logs/                  # Logs con información sensible
.env                   # Variables de entorno con credenciales
```

### 🛡️ **Configuración Inicial Segura**

```bash
# 1. Copiar archivos de ejemplo
cp .env.example .env
cp contacts/contacts.example.csv contacts/contacts.csv

# 2. Editar con tus datos reales (estos archivos NO se suben a git)
vim .env                    # Configurar API_KEY y otros
vim contacts/contacts.csv   # Añadir tus contactos reales

# 3. Añadir tus imágenes
cp mi_imagen.png images/    # Tus imágenes NO se suben a git
```

### Buenas Prácticas Implementadas
- ✅ Sanitización de logs (previene log injection)
- ✅ Validación de entrada de datos
- ✅ Variables de entorno para credenciales
- ✅ Manejo seguro de excepciones
- ✅ Dependencias sin vulnerabilidades conocidas
- ✅ **.gitignore robusto** que protege datos sensibles

### Recomendaciones
1. **Cambiar API_KEY** por defecto en `.env.local`
2. **No commitear** archivos `.env.local` con credenciales
3. **Usar HTTPS** en producción (`ENFORCE_HTTPS=true`)
4. **Monitorear logs** regularmente
5. **Actualizar dependencias** periódicamente

## 🤝 Contribuir

### Desarrollo

```bash
# 1. Fork del repositorio
# 2. Clonar tu fork
git clone <tu-fork-url>
cd next-message

# 3. Instalar dependencias de desarrollo
make install

# 4. Ejecutar pruebas
make test

# 5. Verificar calidad de código
make lint
make format
```

### Estructura de Commits
```
feat: agregar nueva funcionalidad
fix: corregir bug
docs: actualizar documentación
test: agregar o modificar pruebas
refactor: refactorizar código
```

## 📝 Licencia

Este proyecto es de código abierto. Ver archivo `LICENSE` para más detalles.

## ⚠️ Disclaimer

**Uso Responsable**: Este software debe usarse de manera responsable y cumpliendo con los términos de servicio de WhatsApp. El uso excesivo o inapropiado puede resultar en la suspensión de tu cuenta de WhatsApp.

---

🚀 **¡Listo para enviar mensajes!** Si tienes problemas, revisa la sección de [Troubleshooting](#-troubleshooting) o abre un issue en el repositorio.

