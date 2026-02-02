# GenAI LiteLLM Configuration

This repository contains LiteLLM proxy configuration for routing AI model requests through Azure API Management (APIM). It includes support for **Claude Code** and other AI coding tools.

## Quick Start

### 1. Install LiteLLM Docker

```bash
docker pull ghcr.io/berriai/litellm:main-latest
```

### 2. Setup Environment

```bash
cp .env.example .env
# Edit .env and add your Azure APIM subscription key
```

### 3. Run LiteLLM

```bash
docker run -d \
  --name litellm \
  -p 4000:4000 \
  -v $(pwd)/config:/app/config \
  --env-file .env \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config/config.yaml
```

### 4. Run Claude Code

```bash
export ANTHROPIC_BASE_URL=http://localhost:4000
export ANTHROPIC_API_KEY=dummy-key
claude
```

---

## Prerequisites

- Docker
- Azure APIM subscription key

## Configuration

1. Copy the example environment file and add your API key:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set your APIM subscription key:
   ```
   AZURE_OPENAI_API_KEY=your-actual-subscription-key
   ```

## Docker Commands

```bash
# View logs
docker logs -f litellm

# Restart (after config changes)
docker restart litellm

# Run with debug logging
docker run -d \
  --name litellm \
  -p 4000:4000 \
  -v $(pwd)/config:/app/config \
  --env-file .env \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config/config.yaml --detailed_debug

# Stop and remove
docker stop litellm && docker rm litellm
```

## Using with Claude Code

Once LiteLLM is running, set the environment variables and run Claude:

```bash
export ANTHROPIC_BASE_URL=http://localhost:4000
export ANTHROPIC_API_KEY=dummy-key
claude
```

The proxy translates Claude API requests to Azure OpenAI, allowing Claude Code to work with your Azure backend.

### How It Works

Claude Code sends requests using Anthropic's API format with parameters like `context_management`. The custom callback in `config/custom_callbacks.py` strips these Anthropic-specific parameters before forwarding to Azure OpenAI, which doesn't support them.

## Running with pip (Alternative)

### Installation

```bash
pip install litellm
```

### Start the Proxy

```bash
litellm --config config/config.yaml
```

The proxy will start on `http://localhost:4000` by default.

## Testing

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Model Mappings

| Request Model Name | Backend Deployment |
|-------------------|-------------------|
| claude-sonnet-4-5 | Azure GPT model |
| claude-sonnet-4-5-20250929 | Azure GPT model |
| claude-haiku-4-5 | Azure GPT mini model |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AZURE_OPENAI_API_KEY` | Your Azure APIM subscription key |

## Files

| File | Description |
|------|-------------|
| `config/config.yaml` | LiteLLM configuration with model mappings |
| `config/custom_callbacks.py` | Custom callback to drop Anthropic-specific parameters |
| `.env` | Environment variables (API keys) |
