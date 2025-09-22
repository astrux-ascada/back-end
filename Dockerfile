# ---- Stage 1: Builder ----
# This stage is responsible for installing dependencies into a virtual environment.
# By isolating this, we can copy the result into the final image without
# including build tools or system dependencies, keeping the final image small.
FROM python:3.12-slim AS builder

# Prevents Python from writing .pyc files and ensures output is sent
# straight to the terminal without being buffered.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container.
WORKDIR /app

# Create a virtual environment in a standard location.
RUN python -m venv /opt/venv
# Add the venv to the PATH, so 'pip' and 'python' commands use it.
ENV PATH="/opt/venv/bin:$PATH"

# Copy only the requirements file first to leverage Docker's layer caching.
# The layer will only be rebuilt if the requirements file changes.
# --- CAMBIO: Usamos requirements-dev.txt para el entorno de desarrollo ---
# Este archivo contiene todas las dependencias, incluyendo las de producción y las de desarrollo como 'debugpy'.
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt


# ---- Stage 2: Final Image ----
# This is the lean, secure image that will run in production.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo principal.
WORKDIR /app

# 1. Create a non-root user and group for security purposes.
#    Running the application as a non-root user is a critical security best practice.
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

# 2. Copy the virtual environment with all dependencies from the 'builder' stage.
COPY --from=builder /opt/venv /opt/venv

# 3. Copy the application code and necessary configuration files.
COPY ./app ./app
COPY alembic.ini .
# COPY ./templates ./templates
COPY alembic ./alembic

# 4. Copy the entrypoint script and make it executable.
#    This script will run tasks like database migrations before starting the app.
COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# 5. Change the ownership of all application files to the non-root user.
#    This is a crucial step to ensure the application has the correct permissions to run.
RUN chown -R appuser:appgroup /app

# 6. Activate the virtual environment for all subsequent commands.
ENV PATH="/opt/venv/bin:$PATH"

# 7. Switch to the non-root user.
USER appuser

# 8. Set the entrypoint script to be executed when the container starts.
ENTRYPOINT ["./entrypoint.sh"]

# 9. Expose the port the application will run on.
EXPOSE 8000
# 10. Define the default command to start the application.
#     The entrypoint script will execute this command after it finishes.
CMD ["python", "-Xfrozen_modules=off", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]