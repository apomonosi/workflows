# Ansible Role: n8n

An Ansible role to install and configure [n8n](https://n8n.io/), a powerful workflow automation tool, using Docker on CentOS/RHEL/Rocky Linux systems.

## Features

- Automated Docker and Docker Compose installation
- n8n deployment using Docker containers
- Configurable n8n settings (port, authentication, timezone, etc.)
- Support for custom environment variables
- Molecule tests for automated testing
- Idempotent role execution

## Requirements

- Ansible 2.9 or higher
- Target system: CentOS/RHEL/Rocky Linux 8 or 9
- Internet connection for downloading packages and Docker images

## Role Variables

### Default Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# n8n version
n8n_version: "latest"

# n8n port
n8n_port: 5678

# Data and config directories
n8n_data_dir: /opt/n8n/data
n8n_config_dir: /opt/n8n/config

# Docker configuration
n8n_docker_image: "n8nio/n8n"
n8n_container_name: "n8n"
n8n_restart_policy: "unless-stopped"

# n8n basic authentication
n8n_basic_auth_active: false
n8n_basic_auth_user: ""
n8n_basic_auth_password: ""

# n8n timezone
n8n_timezone: "UTC"

# n8n webhook URL (optional)
n8n_webhook_url: ""

# Database type (sqlite, postgresdb, mysqldb, mariadb)
n8n_db_type: "sqlite"

# Execution mode
n8n_executions_mode: "regular"

# Docker Compose settings
n8n_docker_compose_version: "3.8"
n8n_docker_compose_dir: /opt/n8n

# Additional environment variables
n8n_env_vars: {}
```

### Custom Environment Variables

You can pass additional n8n environment variables using `n8n_env_vars`:

```yaml
n8n_env_vars:
  N8N_ENCRYPTION_KEY: "your-secret-key"
  N8N_USER_MANAGEMENT_JWT_SECRET: "your-jwt-secret"
  GENERIC_TIMEZONE: "America/New_York"
```

## Dependencies

None.

## Example Playbook

### Basic Installation

```yaml
---
- hosts: servers
  become: true
  roles:
    - n8n
```

### Custom Configuration

```yaml
---
- hosts: servers
  become: true
  vars:
    n8n_version: "1.21.0"
    n8n_port: 8080
    n8n_basic_auth_active: true
    n8n_basic_auth_user: "admin"
    n8n_basic_auth_password: "secure_password"
    n8n_timezone: "America/New_York"
    n8n_webhook_url: "https://n8n.example.com"
    n8n_env_vars:
      N8N_ENCRYPTION_KEY: "my-encryption-key-123"
  roles:
    - n8n
```

### With PostgreSQL Database

```yaml
---
- hosts: servers
  become: true
  vars:
    n8n_db_type: "postgresdb"
    n8n_env_vars:
      DB_POSTGRESDB_HOST: "postgres.example.com"
      DB_POSTGRESDB_PORT: "5432"
      DB_POSTGRESDB_DATABASE: "n8n"
      DB_POSTGRESDB_USER: "n8n_user"
      DB_POSTGRESDB_PASSWORD: "db_password"
  roles:
    - n8n
```

## Testing with Molecule

This role includes Molecule tests for automated testing.

### Prerequisites

1. Run the bootstrap script to set up the testing environment:

```bash
./bootstrap-testing-env.sh
```

2. Log out and log back in (or run `newgrp docker`) to apply Docker group membership.

### Running Tests

```bash
# Navigate to the role directory
cd roles/n8n

# Run all tests
molecule test

# Run individual test steps
molecule create      # Create test containers
molecule converge    # Apply the role
molecule verify      # Run verification tests
molecule destroy     # Destroy test containers

# Test on specific platform
molecule test --platform-name rockylinux-8
```

### Test Scenarios

The Molecule tests verify:
- Docker installation and service status
- n8n container deployment
- Directory creation
- Port availability
- Container health

## Access n8n

After deployment, n8n will be available at:

```
http://<server-ip>:5678
```

Or the custom port you configured.

## Managing n8n

### View logs

```bash
docker logs n8n
```

### Restart n8n

```bash
docker restart n8n
```

### Stop n8n

```bash
docker stop n8n
```

### Update n8n

Change the `n8n_version` variable and re-run the playbook:

```bash
ansible-playbook -i inventory playbook.yml
```

## Directory Structure

```
n8n/
├── README.md
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── molecule/
│   └── default/
│       ├── converge.yml
│       ├── molecule.yml
│       ├── prepare.yml
│       └── verify.yml
├── tasks/
│   ├── deploy_n8n.yml
│   ├── install_docker.yml
│   └── main.yml
└── templates/
    └── docker-compose.yml.j2
```

## Security Considerations

1. **Basic Authentication**: Enable `n8n_basic_auth_active` and set strong credentials
2. **Encryption Key**: Set `N8N_ENCRYPTION_KEY` for credential encryption
3. **Firewall**: Configure firewall rules to restrict access to n8n port
4. **HTTPS**: Use a reverse proxy (nginx/traefik) with SSL/TLS in production
5. **Database**: Use external database (PostgreSQL/MySQL) for production
6. **Backups**: Regularly backup the n8n data directory

## Troubleshooting

### n8n container not starting

Check logs:
```bash
docker logs n8n
```

### Port already in use

Change the `n8n_port` variable to an available port.

### Permission issues

Ensure the user has proper permissions on the data directories:
```bash
sudo chown -R 1000:1000 /opt/n8n/data
```

## License

MIT

## Author Information

Created by AI Assistant for autonomous Ansible role development.

## Contributing

Contributions are welcome! Please test your changes using Molecule before submitting.

## References

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Docker Documentation](https://docs.n8n.io/hosting/installation/docker/)
- [Molecule Documentation](https://molecule.readthedocs.io/)
