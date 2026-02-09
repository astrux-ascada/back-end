[ FastAPI App (main.py) ]
        │
        ├── [ Servicios Comunes (core/) ]
        │     ├── database.py       → Conexión a PostgreSQL + TimescaleDB
        │     ├── redis.py          → Conexión a Redis (cache, eventos)
        │     ├── rabbitmq.py       → Conexión a RabbitMQ (eventos asíncronos)
        │     ├── security.py       → JWT, MFA, RBAC
        │     ├── config.py         → Variables de entorno
        │     └── logging.py        → Auditoría centralizada
        │
        ├── [ Módulos Independientes ]
        │     ├── core_engine/      → Conexión con PLCs, sensores, control en tiempo real
        │     ├── ai_orchestrator/  → IA predictiva, optimización, gemelo digital
        │     ├── maintenance/      → Gestión de OTs, inventario, técnicos
        │     ├── assets/           → Catálogo de máquinas, salud, metadatos
        │     ├── procurement/      → Compras, proveedores, proyectos
        │     ├── reporting/        → KPIs, dashboards, exportación
        │     ├── notifications/    → Alertas push, email, SMS, sirenas
        │     ├── identity/         → Auth, roles, permisos, Zero Trust
        │     └── digital_twin/     → Simulación, 3D, “qué pasaría si…”
        │
        └── [ APIs y Eventos ]
              ├── REST/WebSocket → Para web, móvil, HMIs
              └── Redis/RabbitMQ → Comunicación entre módulos (eventos)