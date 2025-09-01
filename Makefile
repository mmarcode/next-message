# Next Message - Makefile
.PHONY: help build up down restart logs status clean install setup send-single send-bulk

# Variables
COMPOSE_FILE = compose.yml
PYTHON = python
PIP = pip

help: ## Mostrar ayuda
	@echo Next Message - Comandos disponibles:
	@echo.
	@echo   install         Instalar dependencias Python
	@echo   build           Construir contenedores Docker
	@echo   up              Levantar servicios
	@echo   down            Detener servicios
	@echo   restart         Reiniciar servicios
	@echo   logs            Ver logs de Evolution API
	@echo   status          Ver estado de contenedores
	@echo   clean           Limpiar contenedores y volumenes
	@echo   setup           Configuracion completa inicial
	@echo   dev             Desarrollo completo desde cero
	@echo   send-single     Enviar mensaje individual
	@echo   send-bulk       Enviar mensajes masivos
	@echo   check-status    Verificar estado de WhatsApp

install: ## Instalar dependencias Python
	$(PIP) install -r requirements.txt

build: ## Construir contenedores Docker
	docker compose -f $(COMPOSE_FILE) build

up: ## Levantar servicios
	docker compose -f $(COMPOSE_FILE) up -d

down: ## Detener servicios
	docker compose -f $(COMPOSE_FILE) down

restart: ## Reiniciar servicios
	docker compose -f $(COMPOSE_FILE) restart

logs: ## Ver logs de Evolution API
	docker compose -f $(COMPOSE_FILE) logs -f

status: ## Ver estado de contenedores
	docker compose -f $(COMPOSE_FILE) ps

clean: ## Limpiar contenedores y volúmenes
	docker compose -f $(COMPOSE_FILE) down -v
	docker system prune -f

setup: install up ## Configuración completa inicial
	@echo "Esperando que Evolution API esté listo..."
	@timeout /t 10 /nobreak > nul
	$(PYTHON) setup.py

dev: clean build up setup ## Desarrollo completo desde cero

send-single: ## Enviar mensaje individual (usar: make send-single PHONE=+525512345678 MESSAGE="Hola")
	$(PYTHON) main.py --mode single --phone $(PHONE) --message "$(MESSAGE)" --type text

send-bulk: ## Enviar mensajes masivos
	$(PYTHON) main.py --mode bulk --contacts contacts/contacts.csv

check-status: ## Verificar estado de WhatsApp
	$(PYTHON) main.py --mode status