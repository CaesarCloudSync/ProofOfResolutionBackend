# Lightweight Python image
FROM python:3.11-slim

# Environment setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/user/.local/bin:$PATH"

# No extra system deps needed – sqlite3 ships with Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 user

# Copy app files and pre-create app.db as root so we can set ownership
COPY --chown=user . /home/user/blustorymicroservices/BluStoryAccounts/

USER user

# Install requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /home/user/blustorymicroservices/BluStoryAccounts/requirements.txt

# Set PYTHONPATH so Python can find the top-level package
ENV PYTHONPATH=/home/user
WORKDIR /home/user/blustorymicroservices/BluStoryAccounts

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]