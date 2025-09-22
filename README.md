# Astruxa - Industrial Orchestrator 5.0 (Backend)

Este proyecto es el backend principal para **Astruxa**, un sistema de control, monitoreo y automatización industrial de última generación, construido con **FastAPI**.

## Descripción

Astruxa es el cerebro digital de una planta industrial. Su propósito es unificar sistemas dispares (SCADA, MES, ERP), predecir fallos mediante IA y automatizar operaciones. Este backend proporciona una API modular, segura y de alto rendimiento para gestionar todos los aspectos de la planta, desde la identidad de los usuarios hasta la ingesta de datos de telemetría en tiempo real.

## Arquitectura y Principios

El sistema está construido siguiendo un manifiesto estricto:

- **Arquitectura Limpia y Modular:** La lógica está organizada por dominios de negocio (`identity`, `assets`, `maintenance`, etc.), no por capas técnicas.
- **Principios SOLID:** Cada componente tiene una única responsabilidad, promoviendo un código mantenible y escalable.
- **Seguridad Zero Trust:** Ningún componente confía en otro por defecto. Se aplica autenticación y autorización en cada capa.
- **Enfoque Industrial e IoT:** Diseñado para ser robusto, operar on-premise y comunicarse con hardware industrial a través de protocolos como OPC UA.

## Stack Tecnológico

- **Backend:** FastAPI
- **Base de Datos:** PostgreSQL + TimescaleDB (para series temporales)
- **ORM:** SQLAlchemy 2.0
- **Migraciones:** Alembic
- **Contenedores:** Docker y Docker Compose
- **Protocolos Industriales:** OPC UA (implementado), Modbus (planificado)

---

## Development & Testing Workflow

Esta sección describe la secuencia exacta de comandos para levantar el entorno de desarrollo completo, incluyendo el PLC simulado para probar el flujo de datos en tiempo real.

**Necesitarás dos terminales abiertas en la raíz del proyecto.**

### Terminal 1: Docker (La Aplicación Principal)

En esta terminal, gestionaremos los servicios de la aplicación (backend y base de datos).

**1. Limpieza Total (Paso Inicial y Crucial)**

Para asegurar un inicio 100% limpio y eliminar cualquier resto de ejecuciones anteriores (contenedores, redes, volúmenes de base de datos), ejecuta:

```sh
docker-compose down -v
```

> **¿Qué hace?** El flag `-v` es la clave. Destruye los contenedores y, lo más importante, elimina el volumen donde se guardan los datos de la base de datos, forzando a Alembic a recrearla desde cero.

**2. Construir y Levantar los Contenedores**

Este comando reconstruirá las imágenes con el último código y las iniciará en segundo plano.

```sh
docker-compose up --build -d
```

> **¿Qué hace?** `--build` le dice a Docker que reconstruya la imagen de la aplicación, incluyendo cualquier nueva dependencia o cambio en el código. `-d` (detached) lo ejecuta en segundo plano.

**3. Poblar la Base de Datos (Seeding)**

Una vez que los contenedores estén corriendo, ejecuta este comando para poblar la base de datos con datos iniciales, como la configuración de nuestro PLC simulado.

```sh
docker-compose run --rm runner python -m app.db.seeding.seed_all
```

> **¿Qué hace?** `run --rm` crea un contenedor temporal del servicio `runner` para ejecutar un único comando (nuestro script de siembra) y luego lo elimina automáticamente (`--rm`).

**4. Monitorear los Logs**

Deja esta terminal abierta observando los logs de la aplicación. Aquí es donde veremos llegar los datos del PLC.

```sh
docker-compose logs -f backend_api
```

> **¿Qué hace?** `logs -f` muestra los logs de un servicio en tiempo real (`-f` significa "follow").

### Terminal 2: Local (El PLC Simulador)

En esta terminal, ejecutaremos el script que simula el hardware de la planta.

**1. Activar el Entorno Virtual**

Esto aísla las librerías de Python para este proyecto.

```sh
source .venv/bin/activate
```

**2. Instalar las Dependencias**

Instala todas las librerías, incluyendo `asyncua`, en tu entorno local para poder ejecutar el simulador.

```sh
pip install -r requirements-dev.txt
```

**3. Iniciar el Simulador**

Con las dependencias instaladas, ejecuta el script:

```sh
python simulators/plc_simulator.py
```

> **¿Qué hace?** Inicia un servidor OPC UA en tu máquina local (`localhost`) en el puerto 4840. El `CoreEngine` dentro de Docker se conectará a él.

---

## Documentación de la API

Con la aplicación corriendo, puedes acceder a la documentación interactiva de la API:

- **Swagger UI**: [http://localhost:8051/api/v1/docs](http://localhost:8051/api/v1/docs)
- **ReDoc**: [http://localhost:8051/api/v1/redoc](http://localhost:8051/api/v1/redoc)
