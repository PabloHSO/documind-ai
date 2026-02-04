# =========================
# Base image
# =========================
FROM python:3.12-slim

# =========================
# Environment variables
# =========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =========================
# System dependencies
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Working directory
# =========================
WORKDIR /app

# =========================
# Copy project files
# =========================
COPY pyproject.toml ./
COPY app ./app

# =========================
# Install Python dependencies
# =========================
# Instalar dependências do sistema
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =========================
# Expose port
# =========================
EXPOSE 8000

# =========================
# Start application
# =========================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
