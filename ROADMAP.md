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

**Objetivo Estratégico:** Evolucionar de una plataforma de "registro de datos" a una de "toma de decisiones inteligentes", aumentando drásticamente el valor para el cliente.

### Prioridad 4: Mantenimiento Predictivo (PdM) v1.0
- **Descripción:** Utilizar los datos de telemetría para predecir fallos antes de que ocurran.
- **Tareas Clave:**
  - [ ] **Motor de Detección de Anomalías:** Implementar modelos (ej. Isolation Forest, Autoencoders) que detecten patrones de vibración, temperatura o consumo inusuales.
  - [ ] **Generación Automática de OT Predictivas:** Cuando se detecta una anomalía con alta confianza, crear automáticamente una OT de tipo "PREDICTIVA".
  - [ ] **Dashboard de Salud del Activo:** Una interfaz que muestre un "health score" para cada activo crítico.

### Prioridad 5: Gestión de Inventario y Compras Inteligentes
- **Descripción:** Optimizar la cadena de suministro de repuestos para reducir costos y tiempos de parada.
- **Tareas Clave:**
  - [ ] **Módulo de Inventario Avanzado:** Control de stock, puntos de re-orden automáticos, historial de movimientos.
  - [ ] **Asociación de Repuestos a Activos (BOM):** Definir qué repuestos necesita cada `AssetType`.
  - [ ] **Integración del SSI:** Conectar el "Sistema de Sugerencias Inteligentes" para que, al crear una OT, sugiera automáticamente qué repuestos comprar y a qué proveedor.

### Prioridad 6: Analítica Avanzada y Reportes Personalizados
- **Descripción:** Permitir a los gerentes y directores obtener insights de alto nivel sobre su operación.
- **Tareas Clave:**
  - [ ] **Motor de Reportes:** Un servicio para generar reportes programados en PDF (OEE, MTBF, MTTR, costos de mantenimiento) con el logo y branding del tenant.
  - [ ] **Conector de Business Intelligence (BI):** Ofrecer un endpoint de API seguro (o una réplica de BD de solo lectura) para que los clientes puedan conectar sus propias herramientas como Power BI o Tableau.

---

## 🌐 Horizonte 3: Plataforma y Ecosistema (1-2 Años)

**Objetivo Estratégico:** Convertir Astruxa en el "sistema operativo" de la planta industrial, una plataforma abierta que se integra con el ecosistema del cliente.

### Prioridad 7: Integraciones de Terceros (Connectors)
- **Descripción:** Romper los silos de datos conectando Astruxa con los sistemas que el cliente ya utiliza.
- **Tareas Clave:**
  - [ ] **Conector ERP:** Sincronización bidireccional con SAP, Oracle o Microsoft Dynamics (órdenes de compra, costos).
  - [ ] **Conector SCADA/Historian:** Integración con OSIsoft PI, Ignition, para ingesta de datos de alta frecuencia.
  - [ ] **Conector de Comunicación:** Enviar alertas críticas a canales de Slack o Microsoft Teams.

### Prioridad 8: API Pública y Webhooks
- **Descripción:** Permitir a los clientes y partners construir sus propias automatizaciones sobre Astruxa.
- **Tareas Clave:**
  - [ ] **API Pública Segura:** Exponer una parte de la API con autenticación por API Key para clientes del plan Enterprise.
  - [ ] **Sistema de Webhooks:** Notificar a sistemas externos en tiempo real cuando ocurran eventos (ej. `workorder:created`, `asset:status_changed`).
  - [ ] **Portal para Desarrolladores:** Documentación interactiva y herramientas para la API pública.

### Prioridad 9: Multi-Región y Cumplimiento Normativo
- **Descripción:** Preparar la plataforma para una expansión global, cumpliendo con las leyes de residencia de datos.
- **Tareas Clave:**
  - [ ] **Infraestructura como Código (Terraform):** Automatizar el despliegue de la pila completa de Astruxa en cualquier región de GCP.
  - [ ] **Gestión de Datos Regional:** Lógica para asegurar que los datos de un tenant europeo residan en servidores europeos (GDPR).

---

## 🤖 Horizonte 4: La Fábrica Autónoma (Visión a Largo Plazo)

**Objetivo Estratégico:** Posicionar a Astruxa como el cerebro central que no solo monitoriza, sino que orquesta la operación de la planta de forma autónoma.

- **Digital Twin (Gemelo Digital):** Crear una réplica virtual 1:1 de la planta del cliente, donde se puedan simular cambios y predecir su impacto antes de implementarlos en el mundo real.
- **Operaciones Autónomas:** El sistema no solo predice un fallo, sino que automáticamente crea la OT, verifica el inventario de repuestos, genera la orden de compra al proveedor óptimo, asigna al técnico disponible con las mejores habilidades y reprograma la producción afectada.
- **Analítica Prescriptiva:** El sistema no solo dice "qué va a pasar" (predictivo), sino que recomienda "qué se debe hacer" (prescriptivo). Ejemplo: "Recomendamos operar la línea 5 a un 92% de su capacidad durante las próximas 48 horas para evitar un fallo crítico con un costo estimado de 50.000€. ¿Aplicar recomendación?".
