# n8n Ansible Deployment with AI Integration

This repository contains an Ansible role for deploying [n8n](https://n8n.io/) workflow automation tool on CentOS/RHEL/Rocky Linux systems using Docker, with optional MCP (Model Context Protocol) server integration for Claude AI.

## 🎯 Key Features

- **Automated n8n Deployment**: Complete Docker-based n8n installation
- **AI-Powered Workflow Creation**: Optional MCP server enables Claude to create and manage workflows
- **Testing Infrastructure**: Molecule tests for role validation
- **Production Ready**: Configurable authentication, databases, and security settings
- **Autonomous Development**: Perfect for AI-assisted automation development

## Quick Start

### 1. Set Up Testing Environment

If you're developing or testing this role, first set up your environment with Ansible, Molecule, and Docker:

```bash
# Make the bootstrap script executable
chmod +x bootstrap-testing-env.sh

# Run the bootstrap script
sudo ./bootstrap-testing-env.sh

# Log out and log back in (or run newgrp docker)
newgrp docker
```

### 2. Configure Your Inventory

Edit `inventory.ini` and add your target server(s):

```ini
[n8n_servers]
your-server.example.com ansible_user=root
```

### 3. Customize Variables (Optional)

Edit `playbook.yml` to customize n8n settings:

```yaml
vars:
  n8n_version: "latest"
  n8n_port: 5678
  n8n_basic_auth_active: true
  n8n_basic_auth_user: "admin"
  n8n_basic_auth_password: "YourSecurePassword"
  n8n_timezone: "America/New_York"
```

### 4. Deploy n8n

Run the playbook:

```bash
ansible-playbook -i inventory.ini playbook.yml
```

### 5. Access n8n

Once deployed, access n8n in your browser:

```
http://your-server-ip:5678
```

## 🤖 Claude AI Integration (Optional)

This repository includes an MCP (Model Context Protocol) server that enables Claude AI to create and manage n8n workflows through natural language!

### What is MCP?

MCP allows Claude to interact directly with n8n's API, enabling you to:

- **Create workflows** by describing what you want in plain English
- **Modify existing workflows** with simple instructions
- **Execute and monitor** workflows through conversation
- **Discover nodes** and capabilities without reading documentation

### Quick Enable

Add to your playbook:

```yaml
vars:
  deploy_mcp_server: true
  mcp_server_repo: https://github.com/your-org/workflows.git
```

Then deploy:

```bash
ansible-playbook -i inventory.ini playbook.yml
```

### Using with Claude

After deployment, configure Claude Desktop with the generated config file from `/opt/n8n-mcp-server/claude_desktop_config.json`.

Example conversations:

```
You: "Create a workflow that sends me a Slack message every morning at 9 AM with the weather"

Claude: I'll create a daily weather notification workflow for you...
[Creates complete workflow with Schedule Trigger, Weather API, and Slack nodes]
```

See [`mcp-server-n8n/README.md`](mcp-server-n8n/README.md) for detailed setup and usage.

## Repository Structure

```
.
├── bootstrap-testing-env.sh    # Script to set up testing environment
├── inventory.ini                # Ansible inventory file
├── playbook.yml                 # Example playbook for deploying n8n
├── README.md                    # This file
├── mcp-server-n8n/              # MCP server for Claude AI integration
│   ├── README.md                # MCP server documentation
│   ├── src/                     # MCP server source code
│   ├── docs/                    # Examples and guides
│   ├── config/                  # Configuration templates
│   ├── Dockerfile               # Container image
│   └── docker-compose.yml       # Compose setup
└── roles/
    └── n8n/                     # n8n Ansible role
        ├── README.md            # Role documentation
        ├── defaults/            # Default variables
        ├── handlers/            # Handlers for service restarts
        ├── meta/                # Role metadata
        ├── molecule/            # Molecule test scenarios
        ├── tasks/               # Role tasks
        └── templates/           # Jinja2 templates
```

## Development Workflow

### Testing with Molecule

Molecule provides automated testing for the role:

```bash
# Navigate to role directory
cd roles/n8n

# Run full test suite
molecule test

# Run individual steps
molecule create      # Create test containers
molecule converge    # Apply the role
molecule verify      # Run verification tests
molecule login       # SSH into test container
molecule destroy     # Clean up test containers
```

### Autonomous Development with AI

This role was designed for autonomous AI development. The testing environment allows AI agents to:

1. Develop role features
2. Test changes automatically with Molecule
3. Verify functionality
4. Iterate based on test results

## Role Features

- **Automated Docker Installation**: Installs Docker and Docker Compose on target systems
- **n8n Deployment**: Deploys n8n using Docker containers
- **Configurable**: Extensive variables for customization
- **Idempotent**: Safe to run multiple times
- **Tested**: Includes Molecule tests for quality assurance
- **Production-Ready**: Supports authentication, custom ports, and external databases

## Configuration Options

### Basic Configuration

```yaml
n8n_version: "latest"           # n8n version
n8n_port: 5678                  # Port to expose
n8n_basic_auth_active: true     # Enable basic auth
n8n_basic_auth_user: "admin"    # Username
n8n_basic_auth_password: "pass" # Password
```

### Advanced Configuration

```yaml
n8n_db_type: "postgresdb"       # Database type
n8n_webhook_url: "https://..."  # Webhook URL
n8n_env_vars:                   # Custom variables
  N8N_ENCRYPTION_KEY: "key"
  DB_POSTGRESDB_HOST: "db.example.com"
```

See `roles/n8n/README.md` for all available variables.

## Requirements

- **Ansible**: 2.9 or higher
- **Target OS**: CentOS/RHEL/Rocky Linux 8 or 9
- **Python**: 3.6 or higher on target systems
- **Internet**: Required for downloading packages and images

## Security Best Practices

1. **Change Default Passwords**: Always use strong, unique passwords
2. **Enable Authentication**: Set `n8n_basic_auth_active: true`
3. **Use HTTPS**: Deploy a reverse proxy with SSL/TLS
4. **Firewall Rules**: Restrict access to n8n port
5. **Encryption Key**: Set `N8N_ENCRYPTION_KEY` for credential encryption
6. **Regular Updates**: Keep n8n and Docker updated
7. **Backup Data**: Regularly backup `/opt/n8n/data`

## Troubleshooting

### Docker Not Starting

```bash
sudo systemctl status docker
sudo systemctl start docker
```

### n8n Container Issues

```bash
# Check container status
docker ps -a

# View logs
docker logs n8n

# Restart container
docker restart n8n
```

### Permission Denied

```bash
# Fix data directory permissions
sudo chown -R 1000:1000 /opt/n8n/data
```

### Port Already in Use

Change `n8n_port` in your playbook to an available port.

## Upgrading n8n

To upgrade n8n to a newer version:

1. Update `n8n_version` variable in playbook
2. Re-run the playbook
3. Molecule will pull the new image and restart the container

```yaml
vars:
  n8n_version: "1.22.0"  # Specify version or use "latest"
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Molecule
5. Submit a pull request

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [Ansible Documentation](https://docs.ansible.com/)
- [Molecule Documentation](https://molecule.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)

## License

MIT

## Support

For issues and questions:
- Role Issues: Check `roles/n8n/README.md`
- n8n Issues: Visit [n8n Community](https://community.n8n.io/)
- Ansible Issues: Check [Ansible Documentation](https://docs.ansible.com/)

## Author

Created by AI Assistant for autonomous workflow automation deployment.
