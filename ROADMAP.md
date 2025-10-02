# Roadmap del Proyecto Astruxa

Este documento proporciona una visión de alto nivel del estado actual del proyecto, las funcionalidades implementadas y los objetivos a futuro.

---

## Visión del Producto

Astruxa aspira a ser un **Orquestador Industrial 5.0**, un sistema nervioso central para operaciones industriales que no solo monitorea, sino que también audita, analiza y reacciona de forma proactiva. Su arquitectura modular y segura está diseñada para integrar sistemas dispares (SCADA, MES, ERP) y habilitar capacidades de autodiagnóstico e inteligencia artificial.

---

## ✅ Funcionalidades Implementadas

Esta sección lista las capacidades que están completas, probadas o listas para la prueba final.

| Módulo/Funcionalidad | Descripción | Estado |
| :--- | :--- | :--- |
| **Arquitectura del Núcleo** | Implementación de una arquitectura limpia, modular y basada en dominios de negocio. | ✅ Completado |
| **Gestión de Identidad (RBAC)** | Sistema completo de Roles y Permisos, incluyendo `SuperUser` y `Administrator`. | ✅ Completado |
| **Gestión de Sesiones (Redis)** | Ciclo de vida de sesión robusto con creación, validación y logout individual/masivo. | ✅ Completado |
| **Módulo de Sectores** | Gestión de áreas físicas/lógicas de la planta. | ✅ Completado |
| **Módulo de Activos** | Gestión del catálogo de activos, jerarquías (BOM) e instancias físicas. | ✅ Completado |
| **Motor de Comunicación (OPC UA)** | El `CoreEngine` se conecta a un PLC (simulado) vía OPC UA y recibe datos. | ✅ Completado |
| **Ingesta de Telemetría (TimescaleDB)** | Almacenamiento eficiente de datos de series temporales en una hypertable. | ✅ Completado |
| **API de Dashboard** | Endpoint `GET /telemetry/readings/{id}` para consultar datos agregados. | ✅ Completado |
| **Sistema de Auditoría** | Módulo `auditing` que registra operaciones críticas (creación, actualizaciones, consultas). | ✅ Completado |
| **Logging Estructurado (JSON)** | Los logs de la aplicación se generan en formato JSON para análisis automático. | ✅ Completado |
| **Sistema de Autodiagnóstico v1** | El `AstruxaLogHandler` detecta errores de conexión y crea órdenes de trabajo correctivas. | ✅ **Listo para Probar** |
| **Siembra de Datos Completa** | Sistema de siembra modular que puebla la base de datos con un entorno de planta realista. | ✅ Completado |

---

## 📝 Funcionalidades Planificadas

Esta sección lista los próximos grandes objetivos de desarrollo.

| Módulo/Funcionalidad | Descripción | Estado |
| :--- | :--- | :--- |
| **Integración de Videovigilancia** | El "Ojo Digital": integrar cámaras IP para grabación por evento y análisis con IA. | 📝 Diseñado |
| **Módulo de Compras (Procurement) v2** | Expandir el módulo para incluir la gestión de cotizaciones y la sugerencia de proveedores con IA. | ⏳ Pendiente |
| **Módulo de Mantenimiento v2** | Implementar la generación automática de órdenes de trabajo preventivas basadas en calendarios o contadores de uso. | ⏳ Pendiente |
| **Motor de Comunicación (Modbus)** | Añadir un nuevo conector al `CoreEngine` para soportar el protocolo Modbus TCP. | ⏳ Pendiente |
| **Sistema de Alertas v1** | Un nuevo módulo para definir y gestionar umbrales de alerta para los datos de telemetría. | ⏳ Pendiente |
