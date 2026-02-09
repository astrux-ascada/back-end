 `11-decisiones-tecnicas.md` — TUS “POR QUÉ” TÉCNICOS

```markdown
# ⚙️ Decisiones Técnicas — Por qué elegimos cada tecnología

> **Justificación técnica, industrial y económica de cada elección. Para futuros desarrolladores, auditores y tu yo del futuro.**

---

## 🐘 Base de Datos: PostgreSQL + TimescaleDB (NO MongoDB)

### ¿Por qué?
- **Consistencia ACID**: Esencial para órdenes, usuarios, inventario.
- **Time-Series Optimizado**: TimescaleDB maneja millones de puntos de sensor/día.
- **JSONB**: Flexible para modelos de IA y metadatos, sin sacrificar consistencia.
- **Madurez Industrial**: 25+ años en entornos críticos (bancos, hospitales, fábricas).
- **Herramientas**: Grafana, Prometheus, backups, replicación → todo integrado.

### ¿Por qué NO MongoDB?
- Eventual consistency → riesgoso para control industrial.
- Menos maduro en transacciones complejas.
- Doble mantenimiento si se usa híbrido.

---

## 🐍 Backend: FastAPI (NO Django/Flask)

### ¿Por qué?
- **Asíncrono**: Ideal para IIoT (miles de conexiones simultáneas).
- **Autodocumentación**: Swagger/OpenAPI nativo → ahorra semanas de documentación.
- **Rendimiento**: Uno de los frameworks Python más rápidos.
- **Tipado**: Pydantic → menos bugs, código más mantenible.

### ¿Por qué NO Node.js/Go?
- Equipo con experiencia en Python.
- Ecosistema científico (IA, NumPy, Pandas) es más maduro en Python.

---

## 📱 Frontend/Móvil: React + React Native

### ¿Por qué?
- **Reutilización de lógica**: Hooks, contextos, utilidades compartidas entre web y móvil.
- **Ecosistema maduro**: Miles de librerías, comunidad enorme.
- **Rendimiento aceptable**: Con optimizaciones, funciona bien en plantas.
- **Talentos disponibles**: Fácil contratar desarrolladores React.

### ¿Por qué NO Flutter?
- Menor reutilización de lógica con web (aunque sea Dart).
- Menor madurez en entornos industriales.

---

## 🤖 IA: ONNX Runtime + Scikit-learn/PyTorch

### ¿Por qué?
- **ONNX**: Modelo empaquetado, sin código fuente → protege IP industrial.
- **Portabilidad**: Funciona en cualquier hardware (x86, ARM, sin GPU).
- **Scikit-learn primero**: Simple, interpretable, rápido para MVP.
- **PyTorch después**: Para modelos avanzados (RL, LSTM).

### ¿Por qué NO TensorFlow.js en navegador?
- Datos industriales no deben salir del servidor.
- Latencia y seguridad inaceptables para control en tiempo real.

---

## 🌐 Comunicación Industrial: OPC UA + Modbus TCP

### ¿Por qué?
- **OPC UA**: Estándar moderno, seguro (certificados X.509), ampliamente adoptado.
- **Modbus TCP**: Legacy, pero presente en el 70% de las fábricas → necesario para compatibilidad.
- **MQTT**: Solo para sensores IoT de bajo consumo.

### ¿Por qué NO Profinet directo?
- Requiere hardware especializado → usamos pasarelas OPC UA ↔ Profinet.

---

## 🔐 Seguridad: Zero Trust + MFA + Vault

### ¿Por qué?
- **Zero Trust**: La red industrial ya no es un castillo con murallas. Es un entorno hostil.
- **MFA Obligatorio**: Humanos cometen errores. La MFA los corrige.
- **HashiCorp Vault**: Secretos industriales (credenciales de PLC, tokens) nunca en código.

---

## 🐳 Infraestructura: Docker + Docker Compose (NO Kubernetes al inicio)

### ¿Por qué?
- **Simplicidad**: MVP no necesita orquestación compleja.
- **Portabilidad**: Funciona igual en laptop, servidor, gateway.
- **Aislamiento**: Cada módulo en su contenedor → fácil debug y actualización.

### ¿Cuándo Kubernetes?
- Fase 3: cuando escalemos a múltiples plantas o necesitemos alta disponibilidad extrema.

---

## 📌 Conclusión

> “No elegimos lo más nuevo. Elegimos lo más confiable, mantenible y alineado con el valor industrial.  
> Cada decisión aquí está pensada para durar años — no meses.”

➡️ **Este documento es la constitución técnica del sistema. Edítalo con respeto.**
```

---

## ✅ ACCIONES INMEDIATAS

1. Crea cada archivo en su ubicación correspondiente.
2. Pega el contenido.
3. Haz commit en Git:
   ```bash
   git add .
   git commit -m "docs: completada documentación estratégica (roadmap, presupuesto, casos de uso, APIs, seguridad, glosario, decisiones técnicas)"
   ```

---
