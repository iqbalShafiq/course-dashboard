FROM python:3.13-slim

WORKDIR /app

# Install Node.js & npm
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy package.json and install Node deps
COPY package.json package-lock.json* ./
RUN npm install

# Copy all project files
COPY . .

# Build Tailwind CSS
RUN npm run tw:prod

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic

# Django will serve the compiled CSS
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]