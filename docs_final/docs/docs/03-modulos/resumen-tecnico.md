# 📘 Resumen Técnico de Módulos Implementados

> **Documento complementario a `openapi.json`. Describe la funcionalidad, arquitectura y valor de negocio de los módulos actualmente desplegados en el backend de Astruxa.**

---

## 1. 🔐 Identity (Seguridad y Acceso)
**Estado:** ✅ Implementado | **Ruta API:** `/auth`, `/users`, `/roles`

El guardián del sistema. Implementa una arquitectura **Zero Trust** donde cada petición es verificada.
*   **Funcionalidad:** Autenticación (JWT), MFA obligatorio para acciones críticas, y RBAC (Control de Acceso Basado en Roles) granular hasta el nivel de máquina/acción.
*   **Valor para el Cliente:** Protege la planta de accesos no autorizados y sabotajes. Garantiza que un operario de la "Línea 1" no pueda detener accidentalmente la "Línea 2".
*   **Diferenciador:** No es solo login; es gestión de sesiones con revocación en tiempo real y auditoría de seguridad.

## 2. 🏭 Assets (Gestión de Activos)
**Estado:** ✅ Implementado | **Ruta API:** `/assets`

El inventario digital vivo de la planta.
*   **Funcionalidad:** Catalogación jerárquica de activos (Plantas -> Sectores -> Líneas -> Máquinas -> Componentes). Gestiona el ciclo de vida, especificaciones técnicas y ubicación física.
*   **Valor para el Cliente:** Elimina los Excel desactualizados. Proporciona una "fuente única de verdad" sobre qué equipos existen, dónde están y cuál es su estado operativo.
*   **Diferenciador:** Cada activo tiene un "Gemelo Digital" incipiente (metadatos JSONB) listo para futuras simulaciones.

## 3. 📍 Sectors (Organización Espacial)
**Estado:** ✅ Implementado | **Ruta API:** `/sectors`

La estructura lógica y física de la fábrica.
*   **Funcionalidad:** Define áreas (ej: "Nave de Corrugado", "Calderas") y asocia usuarios y activos a ellas.
*   **Valor para el Cliente:** Permite segmentar la visualización y las alertas. Un jefe de mantenimiento puede ver solo las alertas de su sector asignado.

## 4. ⚙️ Core Engine (Motor de Tiempo Real)
**Estado:** ✅ Implementado | **Ruta API:** `/core` (WebSockets)

El sistema nervioso central.
*   **Funcionalidad:** Ingesta de datos de alta velocidad, gestión de conexiones con PLCs (vía adaptadores OPC-UA/Modbus) y distribución de eventos en tiempo real mediante Redis Pub/Sub.
*   **Valor para el Cliente:** Latencia de milisegundos. Permite ver el estado de la máquina "ahora mismo", no "hace 5 minutos".
*   **Diferenciador:** Arquitectura resiliente; si la base de datos se ralentiza, el control en tiempo real sigue funcionando gracias a Redis.

## 5. 📡 Telemetry (Series Temporales)
**Estado:** ✅ Implementado | **Ruta API:** `/telemetry`

La memoria histórica de la planta.
*   **Funcionalidad:** Almacenamiento optimizado de lecturas de sensores (temperatura, vibración, velocidad) usando TimescaleDB (hipertablas). Soporta ingestión masiva y consultas agregadas (promedios por hora/día).
*   **Valor para el Cliente:** Permite el análisis de tendencias. "¿Por qué la caldera falló hoy? Miremos la presión de los últimos 3 meses".

## 6. 🚨 Alarming (Detección de Anomalías)
**Estado:** ✅ Implementado | **Ruta API:** `/alarming`

El sistema de vigilancia proactiva.
*   **Funcionalidad:** Motor de reglas que evalúa cada dato de telemetría en tiempo real. Genera alertas con niveles de severidad (Info, Warning, Critical) y gestiona su ciclo de vida (Activa -> Reconocida -> Resuelta).
*   **Valor para el Cliente:** Convierte datos en acción. Evita que los operarios tengan que mirar pantallas todo el día; el sistema les avisa solo cuando es necesario.

## 7. 🛠️ Maintenance (Gestión de Mantenimiento)
**Estado:** ✅ Implementado | **Ruta API:** `/maintenance`

El ejecutor de soluciones.
*   **Funcionalidad:** Gestión de Órdenes de Trabajo (OTs). Asignación inteligente de técnicos basada en disponibilidad y skills. Integración con inventario de repuestos.
*   **Valor para el Cliente:** Reduce el Tiempo Medio de Reparación (MTTR). Digitaliza el flujo de trabajo del técnico (adiós al papel).
*   **Diferenciador:** Las alertas del módulo `Alarming` pueden disparar automáticamente la creación de OTs.

## 8. 💰 Procurement (Compras Inteligentes)
**Estado:** ✅ Implementado | **Ruta API:** `/procurement`

El optimizador de recursos.
*   **Funcionalidad:** Gestión de proveedores y sugerencias de compra basadas en niveles de stock de repuestos.
*   **Valor para el Cliente:** Evita paradas por falta de repuestos críticos. Ayuda a negociar mejor con proveedores basándose en datos de calidad y tiempos de entrega.

## 9. 📜 Auditing (Auditoría Forense)
**Estado:** ✅ Implementado | **Ruta API:** `/auditing`

La caja negra inmutable.
*   **Funcionalidad:** Registro de "quién hizo qué y cuándo" para todas las operaciones críticas (cambios de configuración, comandos de control, accesos).
*   **Valor para el Cliente:** Cumplimiento normativo y seguridad. Permite investigar incidentes y depurar responsabilidades.

## 10. 🎛️ Configuration (Panel de Control)
**Estado:** ✅ Implementado | **Ruta API:** `/configuration`

La flexibilidad del sistema.
*   **Funcionalidad:** Gestión de parámetros globales y enums dinámicos (ej: añadir un nuevo tipo de prioridad de OT) sin redeployar código.
*   **Valor para el Cliente:** Adaptabilidad. El cliente puede ajustar reglas de negocio simples sin depender del equipo de desarrollo.

---

## 🧩 Lo que falta (Próximos Pasos para la Demo Completa)

Para cerrar el ciclo y tener una demo "end-to-end" impactante para la planta de cartón, faltaría integrar visualmente:

1.  **Reporting:** Un dashboard simple que consuma la API de `Telemetry` para mostrar gráficos históricos.
2.  **Notifications:** El envío real de correos/SMS cuando salta una alarma crítica (actualmente la alarma se crea en DB, pero no "suena" fuera del sistema).
3.  **Simulador de Datos:** Un script que inyecte datos falsos de "vibración de rodillos" y "temperatura de caldera" para que los gráficos se muevan durante la presentación.
