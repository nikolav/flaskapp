
# Use official Python image with slim variant to reduce size
FROM python:3.12-slim

# Set environment variables
ENV \
    CHROME_BIN=/usr/bin/google-chrome \
    CHROME_PATH=/usr/lib/chromium-browser/ \
    HEADLESS=true \
    CHROME_OPTS="--headless --disable-gpu --no-sandbox --disable-dev-shm-usage"

# Set work directory
WORKDIR /usr/app

# Install system dependencies for Chrome and clean up in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        fonts-liberation \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        xdg-utils && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y --no-install-recommends ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    google-chrome --version

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

VOLUME ["./storage"]

## Set non-root user for security
# RUN useradd -m appuser && chown -R appuser:appuser /app
# USER appuser

# Build-time argments
ARG PORT_DEFAULT=5000

# default port
ENV PORT=${PORT_DEFAULT}

# Expose Flask port
EXPOSE ${PORT}

## Health check
# HEALTHCHECK --interval=30s --timeout=3s \
#     CMD curl -f http://localhost:5000/health || exit 1

# Run app
CMD ["./wserver.sh"]
