# Devstral Container

A containerized environment for running [Mistral's Devstral Vibe CLI](https://mistral.ai/news/devstral-2-vibe-cli) with optional API request/response logging and visualization.

This project provides a complete Docker-based setup for the Devstral CLI with three independent components.

## Features

- Containerized Devstral Vibe CLI with isolated configuration
- Optional HTTPS proxy for logging API requests and responses
- Web-based log viewer using Datasette
- Easy-to-use helper script for common workflows
- Persistent configuration and logs

## Components

This project consists of three Docker images:

### 1. devstral-cli
The main container running Mistral's Vibe CLI. Mounts your workspace directory and persists configuration to `~/.config/devstral-container/config`.

### 2. devstral-proxy (optional)
An mitmproxy-based HTTPS proxy that intercepts and logs all API calls to Mistral. Logs are stored in a SQLite database at `~/.config/devstral-container/proxy/logs.db`.

### 3. devstral-datasette (optional)
A web interface for exploring logged API calls. Provides filtering, sorting, SQL queries, and data export capabilities. Accessible at http://localhost:8001.

## Prerequisites

- Docker
- Docker Compose
- A Mistral API key (get one at https://console.mistral.ai/)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/nezhar/devstral-container.git
cd devstral-container
```

2. Make the helper scripts executable:
```bash
chmod +x bin/devstral-container run.sh
```

3. Build the Docker images:
```bash
docker compose build
```

4. (Optional) Add the bin directory to your PATH for easier access:
```bash
export PATH="$PWD/bin:$PATH"
# Or add to your shell profile for persistence
echo 'export PATH="'$PWD'/bin:$PATH"' >> ~/.bashrc
```

## Quick Start

### Basic Usage (No Logging)

Run the CLI in interactive mode:
```bash
./bin/devstral-container
```

Or run a specific command:
```bash
./bin/devstral-container "analyze the codebase structure"
```

### With API Logging

Enable the proxy to log all API requests and responses:
```bash
./bin/devstral-container --proxy
```

### With Log Visualization

Start the CLI with both logging and the Datasette web interface:
```bash
./bin/devstral-container --datasette
```

Then open http://localhost:8001 in your browser to explore the logs.

## Configuration

### Mistral API Key

On first run, Vibe CLI will prompt you for your Mistral API key. The configuration is stored in `~/.config/devstral-container/config` and persists across runs.

Alternatively, you can set up the config file manually:
```bash
mkdir -p ~/.config/devstral-container/config
# Follow Mistral's documentation to create the config.toml file
```

### Custom Configuration

The Vibe CLI uses `config.toml` for configuration. You can customize:
- Auto-approval settings
- Custom providers and local models
- Tool permissions
- Theme preferences

See the [official Vibe CLI documentation](https://mistral.ai/news/devstral-2-vibe-cli) for details.

## Using Docker Compose Directly

For more control, you can use Docker Compose directly:

### Build all images:
```bash
docker compose build
```

### Run CLI only:
```bash
docker compose run --rm devstral-cli
```

### Run with proxy services:
```bash
docker compose --profile proxy up -d devstral-proxy devstral-datasette
docker compose run --rm -e HTTPS_PROXY=http://devstral-proxy:8080 devstral-cli
```

### Stop proxy services:
```bash
docker compose --profile proxy down
```

## Project Structure

```
devstral-container/
├── Dockerfile              # Main Devstral CLI image
├── Dockerfile.proxy        # mitmproxy logging container
├── Dockerfile.datasette    # Datasette visualization container
├── compose.yml             # Docker Compose configuration
├── proxy_script.py         # API logging script for mitmproxy
├── bin/
│   └── devstral-container  # Helper script
└── README.md
```

## Configuration Directory Structure

```
~/.config/devstral-container/
├── config/                 # Vibe CLI configuration and API keys
│   └── config.toml
└── proxy/                  # Proxy certificates and logs
    ├── logs.db             # SQLite database with API logs
    └── mitmproxy-*         # SSL certificates
```

## Troubleshooting

### Proxy Connection Issues

If the CLI can't connect through the proxy:

1. Ensure proxy services are running:
```bash
docker compose --profile proxy ps
```

2. Check proxy logs:
```bash
docker compose logs devstral-proxy
```

3. The proxy automatically handles SSL certificates. On first run with proxy, it may take a moment to generate certificates.

### Permission Issues

If you encounter permission issues with mounted volumes:
```bash
sudo chown -R $USER:$USER ~/.config/devstral-container
```

### Rebuilding Images

Force rebuild all images:
```bash
./bin/devstral-container --build
```

Or rebuild specific images:
```bash
docker compose build devstral-cli
docker compose build devstral-proxy
docker compose build devstral-datasette
```

## API Costs

Be aware of Mistral API pricing when using the CLI:

- **Devstral 2**: $0.40/$2.00 per million tokens (input/output)
- **Devstral Small 2**: $0.10/$0.30 per million tokens

The logging feature helps you track your API usage and costs.

## License

This project is released under the Apache 2.0 license, matching the Vibe CLI license.

## Related Projects

This project follows the same containerization pattern as [gemini-container](https://github.com/nezhar/gemini-container), providing isolated environments with optional API logging for AI CLI tools.

## Contributing

Contributions are welcome! Please feel free to:
- Report issues at https://github.com/nezhar/devstral-container/issues
- Submit pull requests with improvements
- Share feedback and suggestions

## Author

Created by [@nezhar](https://github.com/nezhar)

Built for [Mistral's Devstral Vibe CLI](https://mistral.ai/news/devstral-2-vibe-cli)
