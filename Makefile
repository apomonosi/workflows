.PHONY: help install test deploy clean lint

help:
	@echo "Available targets:"
	@echo "  install    - Install Python dependencies"
	@echo "  test       - Run Molecule tests"
	@echo "  deploy     - Deploy n8n using the playbook"
	@echo "  clean      - Clean up Molecule test environment"
	@echo "  lint       - Lint Ansible playbooks and roles"
	@echo "  bootstrap  - Set up testing environment (requires sudo)"

bootstrap:
	@echo "Setting up testing environment..."
	sudo ./bootstrap-testing-env.sh
	@echo "Done! You may need to log out and back in."

install:
	@echo "Installing Python dependencies..."
	pip3 install -r requirements.txt

test:
	@echo "Running Molecule tests..."
	cd roles/n8n && molecule test

test-create:
	@echo "Creating Molecule test instances..."
	cd roles/n8n && molecule create

test-converge:
	@echo "Running Molecule converge..."
	cd roles/n8n && molecule converge

test-verify:
	@echo "Running Molecule verify..."
	cd roles/n8n && molecule verify

test-destroy:
	@echo "Destroying Molecule test instances..."
	cd roles/n8n && molecule destroy

deploy:
	@echo "Deploying n8n..."
	ansible-playbook -i inventory.ini playbook.yml

deploy-check:
	@echo "Running deployment in check mode..."
	ansible-playbook -i inventory.ini playbook.yml --check

lint:
	@echo "Linting Ansible files..."
	ansible-lint playbook.yml roles/n8n/

clean:
	@echo "Cleaning up..."
	cd roles/n8n && molecule destroy
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.retry" -delete 2>/dev/null || true
