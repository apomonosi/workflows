"""MCP Server for n8n - Enables Claude AI to manage n8n workflows."""

import asyncio
import json
import os
from typing import Any, Dict, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import AnyUrl

from .n8n_client import N8nClient, N8nConfig


class N8nMCPServer:
    """MCP Server for n8n integration."""

    def __init__(self):
        """Initialize the n8n MCP server."""
        self.server = Server("n8n-mcp-server")
        self.n8n_client: Optional[N8nClient] = None

        # Register handlers
        self.server.list_tools()(self.list_tools)
        self.server.call_tool()(self.call_tool)

    async def initialize(self):
        """Initialize the n8n client."""
        config = N8nConfig(
            base_url=os.getenv("N8N_BASE_URL", "http://localhost:5678"),
            api_key=os.getenv("N8N_API_KEY"),
            username=os.getenv("N8N_USERNAME"),
            password=os.getenv("N8N_PASSWORD"),
        )
        self.n8n_client = N8nClient(config)

    async def list_tools(self) -> list[Tool]:
        """List available MCP tools for n8n."""
        return [
            Tool(
                name="list_workflows",
                description="List all n8n workflows. Optionally filter by active status.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "active": {
                            "type": "boolean",
                            "description": "Filter by active status (true/false, omit for all)"
                        }
                    }
                }
            ),
            Tool(
                name="get_workflow",
                description="Get detailed information about a specific workflow by ID.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_id": {
                            "type": "string",
                            "description": "The workflow ID to retrieve"
                        }
                    },
                    "required": ["workflow_id"]
                }
            ),
            Tool(
                name="create_workflow",
                description="Create a new n8n workflow. Provide the workflow definition including name, nodes, and connections.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Workflow name"
                        },
                        "nodes": {
                            "type": "array",
                            "description": "Array of node definitions"
                        },
                        "connections": {
                            "type": "object",
                            "description": "Node connections object"
                        },
                        "settings": {
                            "type": "object",
                            "description": "Workflow settings (optional)"
                        },
                        "active": {
                            "type": "boolean",
                            "description": "Whether workflow should be active (default: false)"
                        }
                    },
                    "required": ["name", "nodes", "connections"]
                }
            ),
            Tool(
                name="update_workflow",
                description="Update an existing workflow. Provide the workflow ID and updated fields.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_id": {
                            "type": "string",
                            "description": "The workflow ID to update"
                        },
                        "name": {
                            "type": "string",
                            "description": "Updated workflow name (optional)"
                        },
                        "nodes": {
                            "type": "array",
                            "description": "Updated node definitions (optional)"
                        },
                        "connections": {
                            "type": "object",
                            "description": "Updated connections (optional)"
                        },
                        "active": {
                            "type": "boolean",
                            "description": "Active status (optional)"
                        }
                    },
                    "required": ["workflow_id"]
                }
            ),
            Tool(
                name="delete_workflow",
                description="Delete a workflow by ID. This action cannot be undone.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_id": {
                            "type": "string",
                            "description": "The workflow ID to delete"
                        }
                    },
                    "required": ["workflow_id"]
                }
            ),
            Tool(
                name="activate_workflow",
                description="Activate or deactivate a workflow.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_id": {
                            "type": "string",
                            "description": "The workflow ID"
                        },
                        "active": {
                            "type": "boolean",
                            "description": "True to activate, false to deactivate"
                        }
                    },
                    "required": ["workflow_id", "active"]
                }
            ),
            Tool(
                name="execute_workflow",
                description="Execute a workflow manually with optional input data.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_id": {
                            "type": "string",
                            "description": "The workflow ID to execute"
                        },
                        "input_data": {
                            "type": "object",
                            "description": "Optional input data for the workflow"
                        }
                    },
                    "required": ["workflow_id"]
                }
            ),
            Tool(
                name="get_execution",
                description="Get details about a workflow execution including results and status.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "execution_id": {
                            "type": "string",
                            "description": "The execution ID"
                        }
                    },
                    "required": ["execution_id"]
                }
            ),
            Tool(
                name="list_executions",
                description="List recent workflow executions. Can filter by workflow ID and status.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "workflow_id": {
                            "type": "string",
                            "description": "Filter by workflow ID (optional)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 20)",
                            "default": 20
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status: success, error, waiting, etc. (optional)"
                        }
                    }
                }
            ),
            Tool(
                name="list_node_types",
                description="List all available node types in n8n. Useful for discovering what nodes can be used in workflows.",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="list_credentials",
                description="List all configured credentials in n8n.",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="health_check",
                description="Check if n8n is healthy and responding.",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
        ]

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> list[TextContent]:
        """Execute a tool call."""
        if not self.n8n_client:
            await self.initialize()

        try:
            result = await self._execute_tool(name, arguments)
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": str(e),
                    "tool": name,
                    "arguments": arguments
                }, indent=2)
            )]

    async def _execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute the actual tool logic."""
        # Workflow Operations
        if name == "list_workflows":
            return await self.n8n_client.list_workflows(
                active=arguments.get("active")
            )

        elif name == "get_workflow":
            return await self.n8n_client.get_workflow(
                workflow_id=arguments["workflow_id"]
            )

        elif name == "create_workflow":
            workflow_data = {
                "name": arguments["name"],
                "nodes": arguments["nodes"],
                "connections": arguments["connections"],
            }
            if "settings" in arguments:
                workflow_data["settings"] = arguments["settings"]
            if "active" in arguments:
                workflow_data["active"] = arguments["active"]

            return await self.n8n_client.create_workflow(workflow_data)

        elif name == "update_workflow":
            workflow_id = arguments.pop("workflow_id")
            return await self.n8n_client.update_workflow(
                workflow_id=workflow_id,
                workflow_data=arguments
            )

        elif name == "delete_workflow":
            result = await self.n8n_client.delete_workflow(
                workflow_id=arguments["workflow_id"]
            )
            return {"success": result, "message": "Workflow deleted"}

        elif name == "activate_workflow":
            return await self.n8n_client.activate_workflow(
                workflow_id=arguments["workflow_id"],
                active=arguments["active"]
            )

        # Execution Operations
        elif name == "execute_workflow":
            return await self.n8n_client.execute_workflow(
                workflow_id=arguments["workflow_id"],
                input_data=arguments.get("input_data")
            )

        elif name == "get_execution":
            return await self.n8n_client.get_execution(
                execution_id=arguments["execution_id"]
            )

        elif name == "list_executions":
            return await self.n8n_client.list_executions(
                workflow_id=arguments.get("workflow_id"),
                limit=arguments.get("limit", 20),
                status=arguments.get("status")
            )

        # Node and Credential Operations
        elif name == "list_node_types":
            return await self.n8n_client.list_node_types()

        elif name == "list_credentials":
            return await self.n8n_client.list_credentials()

        elif name == "health_check":
            return await self.n8n_client.health_check()

        else:
            raise ValueError(f"Unknown tool: {name}")

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point for the MCP server."""
    server = N8nMCPServer()
    await server.run()


def cli():
    """CLI entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
