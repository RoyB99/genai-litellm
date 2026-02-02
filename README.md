# GenAI LiteLLM Configuration

This repository contains LiteLLM proxy configuration for routing AI model requests through Azure API Management (APIM).

## Prerequisites

- Docker (recommended) OR Python 3.8+ with LiteLLM installed

## Running with Docker (Recommended)

```bash
docker run -d \
  --name litellm \
  -p 4000:4000 \
  -v $(pwd)/config:/app/config \
  --env-file .env \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config/config.yaml
```

### Docker Options

```bash
# Run on a different port
docker run -d \
  --name litellm \
  -p 8000:4000 \
  -v $(pwd)/config:/app/config \
  --env-file .env \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config/config.yaml

# Run with debug logging
docker run -d \
  --name litellm \
  -p 4000:4000 \
  -v $(pwd)/config:/app/config \
  --env-file .env \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config/config.yaml --detailed_debug

# View logs
docker logs -f litellm

# Stop and remove
docker stop litellm && docker rm litellm
```

## Running with pip (Alternative)

### Installation

```bash
pip install litellm
```

### Start the Proxy

## Configuration

1. Copy the example environment file and add your API key:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set your APIM subscription key:
   ```
   AZURE_APIM_API_KEY=your-actual-subscription-key
   ```

### Start the Proxy

```bash
litellm --config config/config.yaml
```

The proxy will start on `http://localhost:4000` by default.

### pip Additional Options

```bash
# Run on a specific port
litellm --config config/config.yaml --port 8000

# Run with debug logging
litellm --config config/config.yaml --debug

# Run in detailed debug mode
litellm --config config/config.yaml --detailed_debug
```

## Usage

Once running, send requests to the proxy using the model names defined in the config:

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```


## Environment Variables

| Variable | Description |
|----------|-------------|
| `AZURE_APIM_API_KEY` | Your Azure APIM subscription key |
## Model Mappings

| Request Model Name | Backend Deployment |
|-------------------|-------------------|
| claude-sonnet-4-5 | azure/gpt-4.1-2025-04-14 |
| claude-haiku-4-5 | azure/gpt-4.1-mini-2025-04-14 |
