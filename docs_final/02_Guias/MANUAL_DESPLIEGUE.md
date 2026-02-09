# Manual de Despliegue y Evaluación de Nube - Astruxa

Este documento analiza las opciones de infraestructura en la nube (AWS vs GCP) y proporciona una guía paso a paso para desplegar el backend de Astruxa en la plataforma recomendada.

---

## 1. Evaluación de Nube: AWS vs GCP

Para una startup SaaS B2B como Astruxa, la elección de la nube debe basarse en tres pilares: **Costo**, **Facilidad de Gestión** y **Escalabilidad**.

### Amazon Web Services (AWS)
*   **Pros:** Ecosistema inmenso, líder del mercado, servicios muy granulares (ej. IoT Core es muy potente).
*   **Contras:** Curva de aprendizaje empinada, gestión de IAM compleja, costos ocultos (NAT Gateways, transferencia de datos).
*   **Servicio Clave:** AWS App Runner o ECS Fargate.

### Google Cloud Platform (GCP)
*   **Pros:** Experiencia de desarrollador superior, **Cloud Run** (Serverless Containers) es ideal para APIs stateless, precios transparentes, red global de fibra óptica muy rápida.
*   **Contras:** Menos servicios de nicho que AWS, soporte técnico a veces lento.
*   **Servicio Clave:** Cloud Run.

### 🏆 Recomendación: Google Cloud Platform (GCP)
Para la fase actual (MVP y Horizonte 2), recomendamos **GCP** por las siguientes razones:
1.  **Cloud Run:** Permite desplegar el contenedor Docker tal cual, sin gestionar servidores (Kubernetes por debajo, pero invisible). Escala a cero cuando no se usa (ahorro total en entornos de desarrollo/QA).
2.  **Cloud SQL:** PostgreSQL gestionado con backups automáticos y alta disponibilidad fácil de configurar.
3.  **Costos:** El "Free Tier" de GCP es generoso y Cloud Run cobra por segundo de uso real.

---

## 2. Arquitectura de Despliegue en GCP

```mermaid
graph TD
    User[Cliente Web/Mobile] --> LB[Cloud Load Balancer]
    LB --> CR[Cloud Run (Backend API)]
    CR --> SQL[Cloud SQL (PostgreSQL 16)]
    CR --> Redis[Memorystore (Redis)]
    CR --> SM[Secret Manager (Credenciales)]
```

---

## 3. Guía de Despliegue Manual (GCP Cloud Run)

### Prerrequisitos
*   Cuenta de Google Cloud activa.
*   `gcloud` CLI instalado en tu máquina local.
*   Docker instalado.

### Paso 1: Configuración Inicial
1.  Crear un nuevo proyecto en GCP: `astruxa-prod`.
2.  Habilitar las APIs necesarias:
    ```bash
    gcloud services enable run.googleapis.com sqladmin.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
    ```

### Paso 2: Base de Datos (Cloud SQL)
1.  Crear una instancia de PostgreSQL 16:
    ```bash
    gcloud sql instances create astruxa-db-prod \
        --database-version=POSTGRES_16 \
        --cpu=1 --memory=3840MiB \
        --region=us-central1
    ```
2.  Crear la base de datos y el usuario:
    ```bash
    gcloud sql databases create astruxa_prod --instance=astruxa-db-prod
    gcloud sql users create astruxa_user --instance=astruxa-db-prod --password=TU_PASSWORD_SEGURO
    ```

### Paso 3: Secretos (Secret Manager)
Para no hardcodear contraseñas en el `docker-compose` o variables de entorno visibles.
1.  Crear el secreto para la URL de la base de datos:
    ```bash
    echo -n "postgresql://astruxa_user:TU_PASSWORD_SEGURO@/astruxa_prod?host=/cloudsql/astruxa-prod:us-central1:astruxa-db-prod" | \
    gcloud secrets create DATABASE_URL --data-file=-
    ```
2.  Crear el secreto para `JWT_SECRET`, `SMTP_PASSWORD`, etc.

### Paso 4: Construir y Subir Imagen Docker
1.  Crear un repositorio en Artifact Registry:
    ```bash
    gcloud artifacts repositories create astruxa-repo --repository-format=docker --location=us-central1
    ```
2.  Construir la imagen localmente (usando Buildpacks o Dockerfile):
    ```bash
    gcloud builds submit --tag us-central1-docker.pkg.dev/astruxa-prod/astruxa-repo/backend:v1
    ```

### Paso 5: Desplegar en Cloud Run
Este comando despliega el contenedor, conecta con Cloud SQL y monta los secretos.

```bash
gcloud run deploy astruxa-api \
    --image us-central1-docker.pkg.dev/astruxa-prod/astruxa-repo/backend:v1 \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --add-cloudsql-instances astruxa-prod:us-central1:astruxa-db-prod \
    --set-secrets="DATABASE_URL=DATABASE_URL:latest" \
    --set-env-vars="ENV=production,LOG_LEVEL=info"
```

---

## 4. Automatización CI/CD con GitHub Actions

Para no ejecutar comandos manuales cada vez, configuraremos un pipeline que despliegue automáticamente al hacer push a la rama `main`.

### 4.1. Configurar Autenticación (Workload Identity Federation)
Es la forma segura de conectar GitHub con GCP sin usar claves JSON estáticas.
1.  En GCP IAM, crea un "Workload Identity Pool" y un "Provider" para GitHub.
2.  Crea una Service Account en GCP con permisos de `Cloud Run Admin`, `Artifact Registry Writer` y `Service Account User`.

### 4.2. Secretos en GitHub
Ve a tu repositorio -> Settings -> Secrets and variables -> Actions y agrega:
*   `GCP_PROJECT_ID`: `astruxa-prod`
*   `GCP_SA_EMAIL`: Email de la Service Account creada.
*   `GCP_WIF_PROVIDER`: ID del proveedor de identidad (ej. `projects/123.../locations/global/workloadIdentityPools/...`).

### 4.3. Archivo del Workflow (`.github/workflows/deploy.yml`)
Crea este archivo en tu repositorio:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ "main" ]

env:
  PROJECT_ID: astruxa-prod
  REGION: us-central1
  REPO_NAME: astruxa-repo
  SERVICE_NAME: astruxa-api

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: 'read'
      id-token: 'write'

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      # Autenticación con Google Cloud
      - name: Google Auth
        id: auth
        uses: 'google-github-actions/auth@v2'
        with:
          workload_identity_provider: '${{ secrets.GCP_WIF_PROVIDER }}'
          service_account: '${{ secrets.GCP_SA_EMAIL }}'

      # Configurar Docker para usar gcloud como helper
      - name: Configure Docker
        run: gcloud auth configure-docker ${{ env.REGION }}-docker.pkg.dev

      # Construir y Subir Imagen
      - name: Build and Push Container
        run: |
          docker build -t ${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPO_NAME }}/${{ env.SERVICE_NAME }}:${{ github.sha }} .
          docker push ${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPO_NAME }}/${{ env.SERVICE_NAME }}:${{ github.sha }}

      # Desplegar a Cloud Run
      - name: Deploy to Cloud Run
        uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: ${{ env.SERVICE_NAME }}
          region: ${{ env.REGION }}
          image: ${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPO_NAME }}/${{ env.SERVICE_NAME }}:${{ github.sha }}
          flags: '--add-cloudsql-instances=${{ env.PROJECT_ID }}:${{ env.REGION }}:astruxa-db-prod --allow-unauthenticated'
          secrets: |
            DATABASE_URL=DATABASE_URL:latest
          env_vars: |
            ENV=production
            LOG_LEVEL=info
```

---

## 5. Costos Estimados (Mensual - Escenario MVP)

| Servicio | Configuración | Costo Aprox. |
| :--- | :--- | :--- |
| **Cloud Run** | 1 vCPU, 512MB RAM (Bajo demanda) | ~$5 - $15 USD |
| **Cloud SQL** | db-f1-micro (Shared Core) | ~$10 - $15 USD |
| **Artifact Registry** | Almacenamiento de imágenes | ~$0.50 USD |
| **Cloud Build** | Minutos de construcción | Gratis (hasta 120 min/día) |
| **Total** | | **~$20 - $35 USD/mes** |

*Nota: Estos precios son estimados y pueden variar según el tráfico y la región.*
