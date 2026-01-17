"""n8n API Client for MCP Server."""

import httpx
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class N8nConfig(BaseModel):
    """Configuration for n8n connection."""

    base_url: str = Field(default="http://localhost:5678", description="n8n base URL")
    api_key: Optional[str] = Field(default=None, description="n8n API key")
    username: Optional[str] = Field(default=None, description="Basic auth username")
    password: Optional[str] = Field(default=None, description="Basic auth password")


class N8nClient:
    """Client for interacting with n8n API."""

    def __init__(self, config: N8nConfig):
        """Initialize n8n client with configuration."""
        self.config = config
        self.base_url = config.base_url.rstrip('/')

        # Set up authentication
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        auth = None

        if config.api_key:
            headers["X-N8N-API-KEY"] = config.api_key
        elif config.username and config.password:
            auth = (config.username, config.password)

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            auth=auth,
            timeout=30.0
        )

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    # Workflow Operations

    async def list_workflows(self, active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        List all workflows.

        Args:
            active: Filter by active status (True/False/None for all)

        Returns:
            List of workflow objects
        """
        params = {}
        if active is not None:
            params["active"] = str(active).lower()

        response = await self.client.get("/api/v1/workflows", params=params)
        response.raise_for_status()
        result = response.json()
        return result.get("data", [])

    async def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get a specific workflow by ID.

        Args:
            workflow_id: The workflow ID

        Returns:
            Workflow object
        """
        response = await self.client.get(f"/api/v1/workflows/{workflow_id}")
        response.raise_for_status()
        return response.json()

    async def create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new workflow.

        Args:
            workflow_data: Workflow definition (name, nodes, connections, etc.)

        Returns:
            Created workflow object
        """
        response = await self.client.post("/api/v1/workflows", json=workflow_data)
        response.raise_for_status()
        return response.json()

    async def update_workflow(
        self, workflow_id: str, workflow_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing workflow.

        Args:
            workflow_id: The workflow ID
            workflow_data: Updated workflow definition

        Returns:
            Updated workflow object
        """
        response = await self.client.patch(
            f"/api/v1/workflows/{workflow_id}",
            json=workflow_data
        )
        response.raise_for_status()
        return response.json()

    async def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow.

        Args:
            workflow_id: The workflow ID

        Returns:
            True if successful
        """
        response = await self.client.delete(f"/api/v1/workflows/{workflow_id}")
        response.raise_for_status()
        return True

    async def activate_workflow(self, workflow_id: str, active: bool = True) -> Dict[str, Any]:
        """
        Activate or deactivate a workflow.

        Args:
            workflow_id: The workflow ID
            active: True to activate, False to deactivate

        Returns:
            Updated workflow object
        """
        response = await self.client.patch(
            f"/api/v1/workflows/{workflow_id}",
            json={"active": active}
        )
        response.raise_for_status()
        return response.json()

    # Execution Operations

    async def execute_workflow(
        self,
        workflow_id: str,
        input_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a workflow manually.

        Args:
            workflow_id: The workflow ID
            input_data: Optional input data for the workflow

        Returns:
            Execution result
        """
        payload = {"workflowId": workflow_id}
        if input_data:
            payload["data"] = input_data

        response = await self.client.post("/api/v1/executions", json=payload)
        response.raise_for_status()
        return response.json()

    async def get_execution(self, execution_id: str) -> Dict[str, Any]:
        """
        Get execution details.

        Args:
            execution_id: The execution ID

        Returns:
            Execution object with results
        """
        response = await self.client.get(f"/api/v1/executions/{execution_id}")
        response.raise_for_status()
        return response.json()

    async def list_executions(
        self,
        workflow_id: Optional[str] = None,
        limit: int = 20,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List workflow executions.

        Args:
            workflow_id: Filter by workflow ID
            limit: Maximum number of results
            status: Filter by status (success, error, waiting, etc.)

        Returns:
            List of execution objects
        """
        params = {"limit": limit}
        if workflow_id:
            params["workflowId"] = workflow_id
        if status:
            params["status"] = status

        response = await self.client.get("/api/v1/executions", params=params)
        response.raise_for_status()
        result = response.json()
        return result.get("data", [])

    async def delete_execution(self, execution_id: str) -> bool:
        """
        Delete an execution.

        Args:
            execution_id: The execution ID

        Returns:
            True if successful
        """
        response = await self.client.delete(f"/api/v1/executions/{execution_id}")
        response.raise_for_status()
        return True

    # Node and Credential Operations

    async def list_node_types(self) -> List[Dict[str, Any]]:
        """
        List available node types.

        Returns:
            List of available node types
        """
        response = await self.client.get("/api/v1/node-types")
        response.raise_for_status()
        return response.json()

    async def list_credentials(self) -> List[Dict[str, Any]]:
        """
        List configured credentials.

        Returns:
            List of credential objects
        """
        response = await self.client.get("/api/v1/credentials")
        response.raise_for_status()
        result = response.json()
        return result.get("data", [])

    async def get_credential(self, credential_id: str) -> Dict[str, Any]:
        """
        Get credential details.

        Args:
            credential_id: The credential ID

        Returns:
            Credential object
        """
        response = await self.client.get(f"/api/v1/credentials/{credential_id}")
        response.raise_for_status()
        return response.json()

    # Health check

    async def health_check(self) -> Dict[str, Any]:
        """
        Check n8n health status.

        Returns:
            Health status object
        """
        try:
            response = await self.client.get("/healthz")
            response.raise_for_status()
            return {"status": "healthy", "details": response.json()}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
