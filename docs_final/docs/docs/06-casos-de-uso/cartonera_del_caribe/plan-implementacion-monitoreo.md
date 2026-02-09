# 📦 Plan de Implementación: Monitoreo de Paradas y Arranques - Cartonera del Caribe

> **Estrategia para despliegue rápido ("Quick Win") de Astruxa Lite: monitoreo no intrusivo de 2 máquinas mediante lectura de sensores análogos, con visualización Web y Móvil.**

---

## 🎯 Objetivo del Proyecto

Proporcionar al cliente visibilidad inmediata sobre el comportamiento de sus máquinas críticas, respondiendo a:
1.  ¿Está la máquina andando o parada ahora mismo?
2.  ¿Cuántas veces paró hoy?
3.  ¿Cuánto tiempo total se perdió en paradas?

**Restricción Clave:** La solución debe ser **no intrusiva** (no modificar lógica del PLC existente) y de bajo costo inicial.

---

## 🏗️ Arquitectura de Solución ("Astruxa Lite")

Para este caso, no desplegaremos la suite completa. Activaremos solo los módulos esenciales para minimizar consumo de recursos y complejidad.

### 1. Módulos Activos
| Módulo | Función Específica para este Caso |
| :--- | :--- |
| **Core Engine** | Ingesta de datos del sensor análogo (4-20mA / 0-10V). Detección de cambio de estado (Run/Stop). |
| **Assets** | Registro de las 2 máquinas y configuración de sus umbrales de parada. |
| **Reporting** | Cálculo de KPIs: Disponibilidad, Tiempo de Parada, Conteo de Arranques. |
| **Identity** | Gestión de 2 usuarios: 1 Web (Gerencia/Supervisor), 1 Móvil (Piso de planta). |
| **Notifications** | (Opcional) Alerta si la parada excede X minutos. |

### 2. Estrategia de Conexión (Pendiente de Definición)

Tenemos dos escenarios preparados. El software es agnóstico a cuál se elija:

*   **Escenario A (Hardware Splitter):** Duplicamos la señal análoga física. Nuestro Gateway lee la copia.
    *   *Ventaja:* 100% seguro, cero riesgo para el PLC.
*   **Escenario B (Lectura de Red):** Leemos vía Modbus TCP/IP si el PLC tiene tarjeta de red.
    *   *Ventaja:* Sin cableado eléctrico nuevo.

---

## 💰 Propuesta de Monetización (Borrador)

### Costo de Instalación (Setup Fee)
*   **Concepto:** Hardware (Gateway + Accesorios) + Ingeniería de despliegue.
*   **Rango Estimado:** $1,500 - $2,500 USD (Pago único).

### Suscripción Mensual (SaaS / Soporte)
*   **Concepto:** Licencia de uso Astruxa Lite (2 activos), almacenamiento de datos, acceso remoto.
*   **Rango Estimado:** $100 - $150 USD / mes.

---

## 📅 Roadmap de Trabajo (Adelantando Tareas)

Aunque no tengamos la conexión física, podemos avanzar el 80% del trabajo de software **AHORA**.

### Fase 1: Preparación y Simulación (INMEDIATO)
- [ ] **Backend:** Configurar `Core Engine` para recibir una señal análoga genérica.
- [ ] **Simulador:** Crear script `plc_simulator.py` que genere una señal oscilante (simulando paradas y arranques) para probar el sistema.
- [ ] **Lógica:** Implementar regla de negocio: `Si señal < X durante Y segundos -> Estado = PARADA`.
- [ ] **Base de Datos:** Asegurar que la tabla `sensor_data` (TimescaleDB) esté lista para recibir series temporales de alta frecuencia.

### Fase 2: Visualización (Frontend)
- [ ] **Web Dashboard:** Crear vista simplificada con:
    - Semáforo de estado actual (Grande: Verde/Rojo).
    - Gráfico de "Timeline" (Barra de tiempo mostrando periodos de actividad/inactividad).
    - KPI: % Disponibilidad del turno actual.
- [ ] **App Móvil:** Vista rápida de lista de máquinas con su estado.

### Fase 3: Despliegue Físico (Cuando el cliente apruebe)
- [ ] Adquisición de Gateway (Raspberry Pi industrial o similar).
- [ ] Instalación en gabinete.
- [ ] Conexión de señal (Splitter o Red).
- [ ] Validación de datos reales vs. observados.

---

## 🔮 Visión de Futuro (Upselling)

Una vez que el cliente vea los datos de paradas, el siguiente paso natural es venderle:
1.  **Mantenimiento:** "¿Quieres que se genere una orden de trabajo automática cuando la máquina pare 3 veces seguidas?"
2.  **IA Predictiva:** "Podemos avisarte *antes* de que pare analizando la tendencia de esa señal análoga."

---
*Documento generado para planificación interna del proyecto Cartonera del Caribe.*
