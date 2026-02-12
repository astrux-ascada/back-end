# 🧩 Módulos del Sistema

Este documento sirve como un mapa de los diferentes dominios de negocio y capacidades que componen la arquitectura de
Astruxa.

---

## ✅ Módulos Implementados

Estos módulos están construidos, integrados y listos para ser probados.

| Módulo            | Archivo                                | Descripción                                                                                  |
|:------------------|:---------------------------------------|:---------------------------------------------------------------------------------------------|
| **Identity**      | [`identity.md`](identity.md)           | Gestiona la autenticación, autorización (RBAC), usuarios, roles y permisos.                  |
| **Marketing**     | [`marketing.md`](marketing.md)         | Motor de crecimiento: gestiona campañas, cupones de descuento y referidos.                   |
| **Sectors**       | [`sectors.md`](sectors.md)             | Define las áreas físicas/lógicas de la planta.                                               |
| **Assets**        | [`assets.md`](assets.md)               | Gestiona el catálogo de activos, sus jerarquías y las instancias físicas.                    |
| **Core Engine**   | [`core-engine.md`](core-engine.md)     | El corazón del sistema. Se conecta a hardware (OPC UA) y gestiona el flujo de datos.         |
| **Telemetry**     | [`telemetry.md`](telemetry.md)         | Ingesta y almacena datos de series temporales en TimescaleDB. Provee la API para dashboards. |
| **Maintenance**   | [`maintenance.md`](maintenance.md)     | Gestiona las órdenes de trabajo, tareas y asignaciones a técnicos.                           |
| **Procurement**   | [`procurement.md`](procurement.md)     | Gestiona el catálogo de proveedores (base para futuras funcionalidades de compra).           |
| **Auditing**      | [`auditing.md`](auditing.md)           | Proporciona un historial inmutable de operaciones críticas del sistema.                      |
| **Configuration** | [`configuration.md`](configuration.md) | Permite a los SuperUsuarios gestionar reglas de negocio y parámetros del sistema.            |
| **Alarming**      | [`alarming.md`](alarming.md)           | Evalúa datos de telemetría en tiempo real y dispara alarmas basadas en reglas.               |

---

## 📝 Módulos Planificados

Estos módulos han sido diseñados o conceptualizados y representan los siguientes grandes pasos en el desarrollo de
Astruxa.

| Módulo              | Archivo                                                    | Descripción                                                                           |
|:--------------------|:-----------------------------------------------------------|:--------------------------------------------------------------------------------------|
| **Videovigilancia** | [`video-surveillance.md`](video-surveillance.md)           | El "Ojo Digital": integrar cámaras IP para grabación por evento y análisis con IA.    |
| **Reporting**       | [`reporting.md`](reporting.md)                             | Generación de informes, dashboards de KPIs y exportación de datos.                    |
| **Digital Twin**    | [`digital-twin.md`](digital-twin.md)                       | Creación de un gemelo digital de la planta para simulaciones y entrenamiento de IA.   |
| **AI Orchestrator** | [`ai-orchestrator.md`](ai-orchestrator.md)                 | Orquesta los diferentes modelos de IA (mantenimiento predictivo, optimización, etc.). |
| **Notifications**   | [`notifications.md`](../../../03_Modulos/notifications.md) | Sistema para enviar notificaciones a los usuarios (email, push, SMS) sobre eventos.   |
