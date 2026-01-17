# n8n MCP Server

An MCP (Model Context Protocol) server that enables Claude AI to interact with n8n workflows. This allows you to use natural language to create, modify, execute, and monitor n8n workflows.

## Features

### 🎯 Core Capabilities

- **Create Workflows**: Describe what you want and Claude generates the complete n8n workflow
- **Read Workflows**: Claude can analyze and explain existing workflows
- **Modify Workflows**: Update workflows with natural language instructions
- **Execute Workflows**: Trigger workflow runs and get results
- **Monitor Executions**: Check status and results of workflow runs
- **Discover Nodes**: Explore available n8n nodes and their capabilities

### 🔧 Available Tools

The MCP server exposes these tools to Claude:

| Tool | Description |
|------|-------------|
| `list_workflows` | List all workflows (filter by active status) |
| `get_workflow` | Get detailed workflow information |
| `create_workflow` | Create new workflows from definitions |
| `update_workflow` | Modify existing workflows |
| `delete_workflow` | Delete workflows |
| `activate_workflow` | Activate/deactivate workflows |
| `execute_workflow` | Manually trigger workflow execution |
| `get_execution` | Get execution details and results |
| `list_executions` | List recent executions with filtering |
| `list_node_types` | Discover available node types |
| `list_credentials` | List configured credentials |
| `health_check` | Check n8n server health |

## Installation

### Prerequisites

- Python 3.10 or higher
- n8n instance (running and accessible)
- n8n API key or credentials

### Option 1: Install from Source

```bash
# Clone and navigate to directory
cd mcp-server-n8n

# Install dependencies
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Option 2: Docker

```bash
# Build image
docker build -t mcp-server-n8n .

# Run with environment variables
docker run -e N8N_BASE_URL=http://n8n:5678 \
           -e N8N_API_KEY=your-key \
           mcp-server-n8n
```

## Configuration

### Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# n8n connection
N8N_BASE_URL=http://localhost:5678

# Authentication (choose one)
N8N_API_KEY=your-api-key-here
# OR
# N8N_USERNAME=admin
# N8N_PASSWORD=password
```

### Getting n8n API Key

1. Open your n8n instance
2. Go to Settings → API
3. Create a new API key
4. Copy the key to your `.env` file

## Usage

### With Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "n8n": {
      "command": "python",
      "args": ["-m", "n8n_mcp_server"],
      "env": {
        "N8N_BASE_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Restart Claude Desktop.

### With Claude Code (CLI)

Add to MCP settings file (`~/.config/claude/mcp_config.json`):

```json
{
  "mcpServers": {
    "n8n": {
      "command": "python",
      "args": ["-m", "n8n_mcp_server"],
      "env": {
        "N8N_BASE_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Standalone Testing

```bash
# Run the MCP server directly
python -m n8n_mcp_server

# With environment variables
N8N_BASE_URL=http://localhost:5678 N8N_API_KEY=key python -m n8n_mcp_server
```

## Example Conversations

### Creating a Workflow

**You:** Create a workflow that sends me a Slack message every day at 9 AM with the current weather

**Claude:** I'll create a daily weather notification workflow for you.

*Claude uses the `create_workflow` tool to generate a workflow with:*
- Schedule Trigger (cron: `0 9 * * *`)
- HTTP Request node (weather API)
- Slack node (send message)

### Modifying a Workflow

**You:** Update the "Daily Report" workflow to also send an email

**Claude:** I'll add an email node to your Daily Report workflow.

*Claude uses `get_workflow` to read it, then `update_workflow` to add an email node*

### Executing and Monitoring

**You:** Run the "Data Sync" workflow and tell me if it succeeded

**Claude:** I'll execute the workflow and check its status.

*Claude uses `execute_workflow`, then `get_execution` to check results*

### Discovering Capabilities

**You:** What nodes are available for working with databases?

**Claude:** Let me check the available database nodes.

*Claude uses `list_node_types` and filters for database-related nodes*

## Example Workflow Structures

### Simple HTTP Request Workflow

```json
{
  "name": "Fetch API Data",
  "nodes": [
    {
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 300],
      "parameters": {}
    },
    {
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300],
      "parameters": {
        "url": "https://api.example.com/data",
        "method": "GET"
      }
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [[{"node": "HTTP Request", "type": "main", "index": 0}]]
    }
  }
}
```

### Scheduled Workflow with Multiple Actions

```json
{
  "name": "Daily Automation",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [250, 300],
      "parameters": {
        "rule": {
          "interval": [{
            "field": "hours",
            "hoursInterval": 24
          }]
        }
      }
    },
    {
      "name": "Fetch Data",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300],
      "parameters": {
        "url": "https://api.example.com/daily"
      }
    },
    {
      "name": "Send Notification",
      "type": "n8n-nodes-base.slack",
      "position": [650, 300],
      "parameters": {
        "channel": "#general",
        "text": "=Daily report: {{$json.data}}"
      }
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [[{"node": "Fetch Data", "type": "main", "index": 0}]]
    },
    "Fetch Data": {
      "main": [[{"node": "Send Notification", "type": "main", "index": 0}]]
    }
  },
  "active": true
}
```

## Development

### Project Structure

```
mcp-server-n8n/
├── src/
│   └── n8n_mcp_server/
│       ├── __init__.py          # Main MCP server
│       └── n8n_client.py        # n8n API client
├── config/
│   └── config.example.yaml      # Configuration template
├── docs/
│   └── API.md                   # API documentation
├── tests/                       # Tests (coming soon)
├── .env.example                 # Environment template
├── pyproject.toml              # Project configuration
├── Dockerfile                   # Container image
└── README.md                    # This file
```

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=n8n_mcp_server
```

### Code Quality

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

## Deployment

### Docker Compose

See the main repository's Docker Compose setup for deploying both n8n and the MCP server together.

### Kubernetes

Kubernetes manifests are available in the `k8s/` directory (coming soon).

### Ansible

The main repository includes an Ansible role that can optionally deploy the MCP server alongside n8n.

## Security Considerations

1. **API Key Protection**: Never commit API keys to version control
2. **Network Security**: Use HTTPS for production n8n instances
3. **Access Control**: Limit MCP server access to trusted clients only
4. **Credential Management**: n8n credentials are not exposed through MCP (only listed, not retrieved)
5. **Audit Logging**: All MCP operations are logged for audit purposes

## Troubleshooting

### Connection Issues

```bash
# Test n8n connectivity
curl http://localhost:5678/healthz

# Check MCP server logs
python -m n8n_mcp_server 2>&1 | tee mcp-server.log
```

### Authentication Errors

- Verify API key is correct
- Check if basic auth credentials match n8n settings
- Ensure n8n API is enabled in settings

### Tool Execution Failures

- Verify workflow IDs exist
- Check n8n error logs
- Validate workflow JSON structure

## API Documentation

Detailed API documentation is available in [`docs/API.md`](docs/API.md).

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure code passes linting
5. Submit a pull request

## License

MIT

## Resources

- [n8n API Documentation](https://docs.n8n.io/api/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Claude AI](https://claude.ai/)

## Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- n8n Community: [community.n8n.io](https://community.n8n.io/)

## Changelog

### v0.1.0 (Initial Release)

- Complete MCP server implementation
- All workflow CRUD operations
- Execution management
- Node discovery
- Health checks
- Docker support
- Comprehensive documentation

## Roadmap

- [ ] Workflow templates library
- [ ] Advanced execution filtering
- [ ] Workflow validation before creation
- [ ] Bulk operations
- [ ] Webhook management
- [ ] Enhanced error handling
- [ ] Performance metrics
- [ ] Multi-instance support

---

**Built for autonomous AI-assisted workflow development** 🤖✨
