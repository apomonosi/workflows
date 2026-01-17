"""Setup script for n8n MCP Server."""

from setuptools import setup, find_packages

setup(
    name="mcp-server-n8n",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "n8n-mcp-server=n8n_mcp_server:cli",
        ],
    },
)
