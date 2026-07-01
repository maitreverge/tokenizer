FROM python:3.11-slim

# Install system dependencies: Node.js (for OpenZeppelin), npm, and make
RUN apt-get update && \
    apt-get install -y nodejs npm make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY deployment/package.json deployment/Makefile ./deployment/

WORKDIR /app/deployment
RUN make openzepellin

WORKDIR /app
COPY . .

ENV VIRTUAL_ENV=/app/.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r deployment/requirements.txt

WORKDIR /app/deployment

# The TUI requires an interactive terminal, we set the default command
CMD ["python", "contract_uploader.py"]
