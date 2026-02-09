# 🗺️ Roadmap Estratégico V2 - La Evolución de Astruxa

> **Visión:** Transformar Astruxa de un producto viable a una plataforma de inteligencia industrial indispensable, culminando en la visión de la "Fábrica Autónoma".
> **Estado Actual:** Fundación del MVP completada. El backend es robusto, seguro y está listo para ser consumido.

---

## 🚀 Horizonte 1: Viabilidad Comercial y Experiencia de Cliente (Próximos 3-6 Meses)

**Objetivo Estratégico:** Lograr que los primeros clientes puedan registrarse, usar y obtener valor del producto de forma autónoma, sentando las bases para el crecimiento.

### Prioridad 1: Interfaz de Usuario (Frontend MVP)
- **Descripción:** Construir la primera versión funcional del frontend que permita a los usuarios interactuar con el potente backend que hemos creado.
- **Tareas Clave:**
  - [ ] **Flujo de Autenticación:** Pantalla de login, gestión de tokens JWT, rutas protegidas.
  - [ ] **Dashboard Principal:** Visualización de KPIs clave (activos operativos, OTs abiertas, alarmas activas).
  - [ ] **Gestión de Activos:** CRUD completo para Activos y Tipos de Activos. Visualización de jerarquías.
  - [ ] **Gestión de Mantenimiento:** CRUD completo para Órdenes de Trabajo.
  - [ ] **Visualización de Telemetría:** Gráficos de series temporales para las métricas de los activos.

### Prioridad 2: Portal de Cliente Completo (Autoservicio)
- **Descripción:** Empoderar a los administradores de cada tenant para que gestionen su cuenta sin necesidad de contactar a soporte.
- **Tareas Clave:**
  - [ ] **UI de Gestión de Suscripción:** Permitir cambiar de plan (upgrade/downgrade).
  - [ ] **UI de Facturación:** Ver historial de pagos y descargar facturas.
  - [ ] **UI de Perfil de Tenant:** Permitir al cliente subir su logo, y rellenar sus datos fiscales y de contacto.
  - [ ] **UI de Gestión de Usuarios y Roles:** Interfaz para crear/editar usuarios y asignarles roles dentro de su propio tenant.

### Prioridad 3: Onboarding y Primer Uso
- **Descripción:** Asegurar que la experiencia de un nuevo cliente sea fluida y guiada, evitando el "síndrome de la pantalla en blanco".
- **Tareas Clave:**
  - [ ] **Wizard de Configuración Inicial:** Un asistente paso a paso para que el nuevo admin configure su `timezone`, `currency` y suba su logo.
  - [ ] **Generación de Datos de Ejemplo:** Un botón "Poblar con datos de demostración" para que el cliente pueda explorar la plataforma con activos y OTs de ejemplo.

---

## 🧠 Horizonte 2: Inteligencia y Excelencia Operativa (Próximos 6-12 Meses)

**Objetivo Estratégico:** Evolucionar de una plataforma de "registro de datos" a una de "toma de decisiones inteligentes", aumentando drásticamente el valor para el cliente y escalando el modelo de negocio.

### Prioridad 4: Mantenimiento Predictivo (PdM) v1.0
- **Descripción:** Utilizar los datos de telemetría para predecir fallos antes de que ocurran.
- **Tareas Clave:**
  - [ ] **Motor de Detección de Anomalías:** Implementar modelos (ej. Isolation Forest, Autoencoders) que detecten patrones inusuales.
  - [ ] **Generación Automática de OT Predictivas:** Crear automáticamente una OT de tipo "PREDICTIVA" ante una anomalía.
  - [ ] **Dashboard de Salud del Activo:** Una interfaz que muestre un "health score" para cada activo crítico.

### Prioridad 5: Gestión de Inventario y Compras Inteligentes
- **Descripción:** Optimizar la cadena de suministro de repuestos para reducir costos y tiempos de parada.
- **Tareas Clave:**
  - [ ] **Módulo de Inventario Avanzado:** Control de stock, puntos de re-orden automáticos, historial de movimientos.
  - [ ] **Asociación de Repuestos a Activos (BOM):** Definir qué repuestos necesita cada `AssetType`.
  - [ ] **Integración del SSI:** Conectar el "Sistema de Sugerencias Inteligentes" para que, al crear una OT, sugiera automáticamente qué repuestos comprar.

### Prioridad 6: Portal de Partners (Resellers)
- **Descripción:** Crear un portal para socios comerciales que les permita registrar y gestionar a sus propios clientes dentro de Astruxa, escalando las ventas.
- **Tareas Clave:**
  - [ ] **Nuevo Rol `PARTNER_ADMIN`:** Un rol global que solo puede ver y gestionar los tenants asociados a su `Partner`.
  - [ ] **API de Partner:** Endpoints dedicados (`/partner/my-tenants`) para que los partners gestionen su cartera de clientes.
  - [ ] **Dashboard de Partner:** Una interfaz para que los partners vean el estado de sus clientes y sus comisiones.

### Prioridad 7: Analítica Avanzada y Reportes Personalizados
- **Descripción:** Permitir a los gerentes y directores obtener insights de alto nivel sobre su operación.
- **Tareas Clave:**
  - [ ] **Motor de Reportes:** Un servicio para generar reportes programados en PDF (OEE, MTBF, MTTR) con el branding del tenant.
  - [ ] **Conector de Business Intelligence (BI):** Ofrecer un endpoint de API seguro para que los clientes conecten sus propias herramientas como Power BI o Tableau.

---

## 🌐 Horizonte 3: Plataforma y Ecosistema (1-2 Años)

**Objetivo Estratégico:** Convertir Astruxa en el "sistema operativo" de la planta industrial, una plataforma abierta que se integra con el ecosistema del cliente.

### Prioridad 8: Gestión de Plataforma Avanzada (Multi-Admin)
- **Descripción:** Implementar un sistema de roles de plataforma más granular para mejorar la seguridad y la delegación operativa interna.
- **Tareas Clave:**
  - [ ] **Nuevo Rol `PLATFORM_ADMIN`:** Un rol de empleado de Astruxa que puede gestionar tenants pero no puede crear otros administradores.
  - [ ] **Flujo de Aprobación Dual:** Implementar un sistema "Maker-Checker" para acciones destructivas como el borrado de tenants.

### Prioridad 9: Integraciones de Terceros (Connectors)
- **Descripción:** Romper los silos de datos conectando Astruxa con los sistemas que el cliente ya utiliza.
- **Tareas Clave:**
  - [ ] **Conector ERP:** Sincronización con SAP, Oracle o Microsoft Dynamics.
  - [ ] **Conector SCADA/Historian:** Integración con OSIsoft PI, Ignition.
  - [ ] **Conector de Comunicación:** Enviar alertas a Slack o Microsoft Teams.

### Prioridad 10: API Pública y Webhooks
- **Descripción:** Permitir a los clientes y partners construir sus propias automatizaciones sobre Astruxa.
- **Tareas Clave:**
  - [ ] **API Pública Segura:** Exponer una parte de la API con autenticación por API Key.
  - [ ] **Sistema de Webhooks:** Notificar a sistemas externos en tiempo real.
  - [ ] **Portal para Desarrolladores:** Documentación interactiva para la API pública.

---

## 🤖 Horizonte 4: La Fábrica Autónoma (Visión a Largo Plazo)

**Objetivo Estratégico:** Posicionar a Astruxa como el cerebro central que no solo monitoriza, sino que orquesta la operación de la planta de forma autónoma.

- **Digital Twin (Gemelo Digital):** Crear una réplica virtual 1:1 de la planta del cliente para simular cambios.
- **Operaciones Autónomas:** El sistema no solo predice un fallo, sino que automatiza toda la cadena de respuesta (OT, compra, asignación).
- **Analítica Prescriptiva:** El sistema no solo dice "qué va a pasar", sino que recomienda "qué se debe hacer".

---

### 📝 NOTA: Estimación de Recursos para Horizonte 2 (Inteligencia y Excelencia Operativa)

**Alcance:** Implementación de Mantenimiento Predictivo, Gestión Avanzada de Inventario, Portal de Partners y Analítica Avanzada.

**Tiempo Estimado:**
*   **Desarrollo:** 4 a 6 meses.
*   **Equipo Sugerido:** 2 Desarrolladores Full-Stack Senior, 1 Ingeniero de Datos/ML (parcial), 1 QA Engineer.

**Presupuesto Estimado (Aprox.):**
*   **Rango:** $60,000 - $100,000 USD.
*   **Desglose:**
    *   Desarrollo Backend/Frontend: ~65%
    *   Infraestructura ML/Datos: ~15%
    *   QA y Pruebas Automatizadas: ~20%

*Esta estimación asume una arquitectura base estable (Horizonte 1 completado) y puede variar según la complejidad específica de los modelos de ML y las integraciones requeridas.*
