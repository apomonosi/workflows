#!/bin/bash
set -e

echo "=================================="
echo "Setting up Ansible Testing Environment"
echo "=================================="

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION=$VERSION_ID
else
    echo "Cannot detect OS"
    exit 1
fi

echo "Detected OS: $OS $VERSION"

# Install Python and pip
echo ""
echo "Installing Python and pip..."
if [[ "$OS" == "centos" ]] || [[ "$OS" == "rhel" ]] || [[ "$OS" == "rocky" ]]; then
    sudo dnf install -y python3 python3-pip python3-devel gcc || \
    sudo yum install -y python3 python3-pip python3-devel gcc
else
    echo "Unsupported OS for this script"
    exit 1
fi

# Upgrade pip
echo ""
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install Ansible
echo ""
echo "Installing Ansible..."
python3 -m pip install ansible

# Install Molecule with Docker driver
echo ""
echo "Installing Molecule with Docker support..."
python3 -m pip install "molecule[docker]" molecule-plugins[docker]

# Install Docker
echo ""
echo "Installing Docker..."
if [[ "$OS" == "centos" ]] || [[ "$OS" == "rhel" ]] || [[ "$OS" == "rocky" ]]; then
    # Remove old versions
    sudo dnf remove -y docker docker-client docker-client-latest docker-common \
        docker-latest docker-latest-logrotate docker-logrotate docker-engine \
        podman runc 2>/dev/null || true

    # Install Docker
    sudo dnf install -y dnf-plugins-core
    sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Start and enable Docker
    sudo systemctl start docker
    sudo systemctl enable docker

    # Add current user to docker group
    sudo usermod -aG docker $USER
fi

# Install Docker Compose (standalone for compatibility)
echo ""
echo "Installing Docker Compose standalone..."
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
echo ""
echo "=================================="
echo "Verifying installations..."
echo "=================================="
echo "Python version:"
python3 --version

echo ""
echo "Ansible version:"
ansible --version

echo ""
echo "Molecule version:"
molecule --version

echo ""
echo "Docker version:"
docker --version

echo ""
echo "Docker Compose version:"
docker-compose --version

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "IMPORTANT: You may need to log out and log back in for Docker group membership to take effect."
echo "Or run: newgrp docker"
echo ""
echo "Next steps:"
echo "1. Initialize your Ansible role with: molecule init role <role-name> --driver-name docker"
echo "2. Develop your role in the roles/<role-name> directory"
echo "3. Test with: molecule test"
echo ""
