# 📡 APIs Externas y Servicios Integrados — Orquestador Industrial 5.0

> **Listado de APIs, servicios y librerías externas requeridas por el sistema. Todas con licencia compatible, soporte
industrial y documentación pública.**

---

## 📚 Referencias de API del Sistema

Esta sección contiene la documentación detallada de los endpoints de la API interna del sistema.

- **[API de Activos (Assets)](assets-api.md)**: Gestión de activos físicos, tipos de activos y jerarquías.

---

## 🔌 Comunicación Industrial

| Servicio / Librería | Uso                                   | Licencia | Enlace                                      |
|---------------------|---------------------------------------|----------|---------------------------------------------|
| `opcua-asyncio`     | Conexión con PLCs modernos (OPC UA)   | MIT      | https://github.com/FreeOpcUa/opcua-asyncio  |
| `pymodbus`          | Conexión con PLCs legacy (Modbus TCP) | BSD      | https://github.com/riptideio/pymodbus       |
| `paho-mqtt`         | Sensores IoT (MQTT)                   | EPL      | https://github.com/eclipse/paho.mqtt.python |

---

## 📱 Notificaciones

| Servicio                 | Uso                             | Licencia               | Enlace                                           |
|--------------------------|---------------------------------|------------------------|--------------------------------------------------|
| Firebase Cloud Messaging | Notificaciones push a app móvil | Gratuita (con límites) | https://firebase.google.com/docs/cloud-messaging |
| Twilio SMS API           | Alertas críticas por SMS        | Pago por uso           | https://www.twilio.com/sms                       |
| SMTP (SendGrid)          | Emails de reportes y alertas    | Freemium               | https://sendgrid.com                             |

---

## 🧠 IA / Machine Learning

| Servicio / Librería | Uso                               | Licencia | Enlace                      |
|---------------------|-----------------------------------|----------|-----------------------------|
| ONNX Runtime        | Inferencia de modelos IA          | MIT      | https://onnxruntime.ai      |
| Scikit-learn        | Modelos iniciales (Random Forest) | BSD      | https://scikit-learn.org    |
| PyTorch Lightning   | Modelos avanzados (RL, LSTM)      | BSD      | https://pytorchlightning.ai |

---

## 🔐 Seguridad

| Servicio          | Uso                              | Licencia | Enlace                                 |
|-------------------|----------------------------------|----------|----------------------------------------|
| HashiCorp Vault   | Gestión de secretos industriales | MPL 2.0  | https://www.vaultproject.io            |
| JWT (python-jose) | Autenticación de APIs            | MIT      | https://github.com/mpdavis/python-jose |

---

## 🖥️ Frontend / Móvil

| Servicio / Librería | Uso                             | Licencia | Enlace                  |
|---------------------|---------------------------------|----------|-------------------------|
| React               | Dashboard web                   | MIT      | https://react.dev       |
| React Native        | App móvil                       | MIT      | https://reactnative.dev |
| Three.js            | Visualización 3D (Digital Twin) | MIT      | https://threejs.org     |

---

## 🛠️ DevOps / Infra

| Servicio             | Uso                       | Licencia   | Enlace                                      |
|----------------------|---------------------------|------------|---------------------------------------------|
| Docker               | Contenedores              | Apache 2.0 | https://www.docker.com                      |
| TimescaleDB          | Base de datos time-series | Apache 2.0 | https://www.timescale.com                   |
| Prometheus + Grafana | Monitoreo de sistema      | Apache 2.0 | https://prometheus.io + https://grafana.com |

---

## 📌 Notas Clave

- Todas las librerías son **open source con licencias permisivas**.
- Servicios cloud (Firebase, Twilio, SendGrid) tienen **planes gratuitos para MVP**.
- **Ningún dato industrial crítico sale de la planta** — solo KPIs anónimos al cloud público.

> “Elegimos herramientas que no nos encadenan, no nos espían, y no nos cuestan una fortuna.”
