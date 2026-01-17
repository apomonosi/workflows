# Quick Start Guide

Get up and running with n8n MCP Server in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] n8n instance running (locally or remote)
- [ ] n8n API access (API key or credentials)
- [ ] Claude Desktop or Claude Code installed

## Step 1: Get n8n API Key

1. Open your n8n instance (e.g., `http://localhost:5678`)
2. Navigate to **Settings** → **API**
3. Click **Create API Key**
4. Copy the generated key
5. Save it securely

## Step 2: Install MCP Server

### Option A: Using pip (Simple)

```bash
# Clone or download the repository
cd mcp-server-n8n

# Install
pip install -e .

# Verify installation
python -m n8n_mcp_server --help
```

### Option B: Using Docker (Isolated)

```bash
# Build the image
docker build -t mcp-server-n8n .

# Test it
docker run -e N8N_BASE_URL=http://host.docker.internal:5678 \
           -e N8N_API_KEY=your-key \
           mcp-server-n8n
```

## Step 3: Configure Claude Desktop

### macOS

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

### Windows

Edit `%APPDATA%\Claude\claude_desktop_config.json` with the same content.

### Linux

Edit `~/.config/Claude/claude_desktop_config.json` with the same content.

## Step 4: Restart Claude Desktop

Close and reopen Claude Desktop to load the MCP server.

## Step 5: Test the Connection

In Claude Desktop, try these prompts:

### Test 1: List Workflows

```
Show me all my n8n workflows
```

**Expected Result:** Claude lists your workflows with names and IDs.

### Test 2: Create a Simple Workflow

```
Create a simple workflow called "Test Workflow" with just a manual trigger
```

**Expected Result:** Claude creates the workflow and confirms success.

### Test 3: Check n8n Health

```
Is my n8n instance healthy?
```

**Expected Result:** Claude reports the health status.

## Common Issues & Solutions

### Issue: "Cannot connect to n8n"

**Solutions:**
- Verify n8n is running: `curl http://localhost:5678/healthz`
- Check the URL in config matches your n8n instance
- If using Docker, use `host.docker.internal` instead of `localhost`

### Issue: "Authentication failed"

**Solutions:**
- Verify API key is correct (no extra spaces)
- Check if API access is enabled in n8n settings
- Try basic auth instead:
  ```json
  "env": {
    "N8N_BASE_URL": "http://localhost:5678",
    "N8N_USERNAME": "admin",
    "N8N_PASSWORD": "your-password"
  }
  ```

### Issue: "MCP server not showing in Claude"

**Solutions:**
- Check config file path is correct for your OS
- Verify JSON syntax is valid (use a JSON validator)
- Restart Claude Desktop completely
- Check Claude Desktop logs for errors

### Issue: "Tools not working"

**Solutions:**
- Ensure you're using a recent version of Claude Desktop
- Verify the MCP server starts without errors
- Check n8n logs for API errors

## Next Steps

Now that you're set up, try these:

1. **Create Your First Workflow**
   ```
   Create a workflow that sends me a daily Slack message at 9 AM
   ```

2. **Explore Existing Workflows**
   ```
   Analyze my "Customer Onboarding" workflow and explain what it does
   ```

3. **Modify a Workflow**
   ```
   Add error handling to my "Data Sync" workflow
   ```

4. **Execute and Monitor**
   ```
   Run my "Weekly Report" workflow and tell me if it succeeded
   ```

## Advanced Configuration

### Multiple n8n Instances

You can connect to multiple n8n instances:

```json
{
  "mcpServers": {
    "n8n-dev": {
      "command": "python",
      "args": ["-m", "n8n_mcp_server"],
      "env": {
        "N8N_BASE_URL": "http://localhost:5678",
        "N8N_API_KEY": "dev-key"
      }
    },
    "n8n-prod": {
      "command": "python",
      "args": ["-m", "n8n_mcp_server"],
      "env": {
        "N8N_BASE_URL": "https://n8n.example.com",
        "N8N_API_KEY": "prod-key"
      }
    }
  }
}
```

Then in Claude:
```
@n8n-dev list my workflows
@n8n-prod show me production workflows
```

### Custom Python Path

If Python is not in PATH:

```json
{
  "mcpServers": {
    "n8n": {
      "command": "/usr/local/bin/python3.11",
      "args": ["-m", "n8n_mcp_server"],
      "env": {
        "N8N_BASE_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-key"
      }
    }
  }
}
```

### Using Virtual Environment

```json
{
  "mcpServers": {
    "n8n": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "n8n_mcp_server"],
      "env": {
        "N8N_BASE_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-key"
      }
    }
  }
}
```

## Verification Checklist

Before asking for help, verify:

- [ ] n8n is running and accessible
- [ ] API key or credentials are correct
- [ ] MCP server can start independently
- [ ] Config file is valid JSON
- [ ] Config file is in the correct location
- [ ] Claude Desktop has been restarted
- [ ] No firewall blocking local connections

## Getting Help

If you're still stuck:

1. Check the [main README](../README.md)
2. Review [example scenarios](EXAMPLES.md)
3. Open an issue on GitHub
4. Join the n8n community forum

## Useful Commands

```bash
# Test n8n connection
curl http://localhost:5678/healthz

# Test MCP server directly
python -m n8n_mcp_server

# Check Python version
python --version

# Find Claude Desktop config
# macOS
ls ~/Library/Application\ Support/Claude/
# Linux
ls ~/.config/Claude/
# Windows
dir %APPDATA%\Claude\

# View n8n logs (Docker)
docker logs n8n
```

## Success Metrics

You'll know everything is working when:

- ✅ Claude can list your workflows
- ✅ Claude can create new workflows
- ✅ Claude can execute workflows
- ✅ Claude can explain existing workflows
- ✅ No error messages in Claude or n8n logs

Congratulations! You're now ready to build workflows with AI assistance! 🎉
