# 🧪 Guía de Pruebas (Testing)

Este documento describe cómo ejecutar la suite de pruebas automatizadas para el backend de Astruxa.

El entorno de pruebas está completamente dockerizado y aislado del entorno de desarrollo, lo que garantiza que los tests sean reproducibles y no afecten a tus datos locales.

---

## 🚀 Ejecución Rápida

Para correr todos los tests, simplemente ejecuta este comando desde la raíz del proyecto (`back-end/`):

```bash
docker compose -f docker-compose.test.yml run --rm test_runner
```

### ¿Qué hace este comando?
1.  Levanta una base de datos de prueba efímera (TimescaleDB).
2.  Levanta un Redis de prueba.
3.  Levanta un servidor de correo Mock (Mailpit).
4.  Ejecuta las migraciones de base de datos (`alembic upgrade head`).
5.  Puebla la base de datos con datos de prueba (`seed_all.py`).
6.  Ejecuta `pytest -v`.
7.  Al finalizar, elimina el contenedor del runner (`--rm`).

---

## 🧹 Limpieza del Entorno

Es **muy importante** bajar los contenedores de prueba después de usarlos para liberar puertos y recursos. Además, esto asegura que la próxima ejecución comience con una base de datos limpia.

```bash
docker compose -f docker-compose.test.yml down -v
```

> El flag `-v` elimina los volúmenes (la base de datos), lo cual es crucial para evitar conflictos de datos entre ejecuciones.

---

## 🛠️ Comandos Útiles

### Ejecutar un test específico
Si solo quieres correr un archivo de prueba (por ejemplo, autenticación):

```bash
docker compose -f docker-compose.test.yml run --rm test_runner pytest tests/api/test_auth_flow.py
```

### Ver logs en tiempo real
Si necesitas depurar y ver los logs de la aplicación mientras corren los tests:

```bash
docker compose -f docker-compose.test.yml run --rm test_runner pytest -o log_cli=true
```

### Detenerse en el primer error
Para ahorrar tiempo cuando estás arreglando un bug:

```bash
docker compose -f docker-compose.test.yml run --rm test_runner pytest -x
```

---

## 🐛 Solución de Problemas Comunes

**Error: `Bind for 0.0.0.0:5434 failed: port is already allocated`**
*   **Causa:** Tienes otro contenedor de pruebas corriendo o algo ocupando el puerto 5434.
*   **Solución:** Ejecuta `docker compose -f docker-compose.test.yml down -v`.

**Error: `relation "xxxx" does not exist`**
*   **Causa:** Las migraciones no se aplicaron correctamente.
*   **Solución:** Asegúrate de estar usando el comando completo que incluye `alembic upgrade head` (el comando por defecto en el `docker-compose.test.yml` ya lo hace). Limpia el entorno con `down -v` y prueba de nuevo.
