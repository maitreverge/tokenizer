FROM python:3.11-slim

RUN apt-get update
RUN apt-get install -y nodejs npm vim
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY deployment/package.json ./deployment/

WORKDIR /app/deployment

# Install pinned dependencies from package.json
RUN npm install

WORKDIR /app
COPY . .

# Init virtual env + install pip dependencies
ENV VIRTUAL_ENV=/app/.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r deployment/requirements.txt

WORKDIR /app/deployment

# Run bash as entrypoint
CMD ["/bin/bash"]
