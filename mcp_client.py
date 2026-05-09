import asyncio
from contextlib import AsyncExitStack  # Fix: Import from contextlib
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self):
        self.session = None
        self.exit_stack = None

    async def connect(self):
        """Connects to the server and keeps the session alive."""
        # Note: Ensure mcp_server.py is in the same directory
        server_params = StdioServerParameters(
            command="python3",
            args=["mcp_server.py"],
        )
        
        self.exit_stack = AsyncExitStack()
        
        # Connect to the server via stdio
        read, write = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        
        # Initialize the MCP protocol
        await self.session.initialize()

    async def call_tool(self, tool_name, arguments):
        # Auto-connect if session isn't active
        if self.session is None:
            await self.connect()
            
        try:
            result = await self.session.call_tool(tool_name, arguments)
            return result.content[0].text
        except Exception as e:
            return f"Error calling tool: {str(e)}"

    async def disconnect(self):
        if self.exit_stack:
            await self.exit_stack.aclose()
            self.session = None