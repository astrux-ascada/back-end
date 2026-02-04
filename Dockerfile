# ---- Stage 1: Builder ----
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar solo el archivo unificado de dependencias
COPY requirements-dev.txt .

RUN pip install --no-cache-dir -r requirements-dev.txt


# ---- Stage 2: Final Image ----
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 1. Create a non-root user and group for security.
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

# 2. Copy the virtual environment from the 'builder' stage.
COPY --from=builder /opt/venv /opt/venv

# 3. Copy the application code and necessary configuration files.
COPY ./app ./app
COPY alembic.ini .
COPY alembic ./alembic

# 4. Copy the entrypoint script and make it executable.
COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# 5. Create directories for scripts and storage.
RUN mkdir -p /app/scripts && \
    mkdir -p /app/storage && \
    chown -R appuser:appgroup /app/scripts && \
    chown -R appuser:appgroup /app/storage

# 6. Change the ownership of all application files to the non-root user.
RUN chown -R appuser:appgroup /app

# 7. Activate the virtual environment.
ENV PATH="/opt/venv/bin:$PATH"

# 8. Switch to the non-root user.
USER appuser

# 9. Set the entrypoint script.
ENTRYPOINT ["./entrypoint.sh"]

# 10. Expose the port and define the default command.
EXPOSE 8000
CMD ["python", "-Xfrozen_modules=off", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
