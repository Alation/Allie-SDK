"""Example FastMCP client that talks to the Allie SDK MCP server."""

from __future__ import annotations

import asyncio
import os

from fastmcp import MCPClient


async def main() -> None:
    """Demonstrate how to call a tool exposed by ``fastmcp_server``."""

    server_url = os.environ.get("ALLIE_MCP_SERVER", "ws://127.0.0.1:8765")
    refresh_token = os.environ["ALLIE_SDK_REFRESH_TOKEN"]

    async with MCPClient(server_url, refresh_token=refresh_token) as client:
        response = await client.call_tool(
            "datasource.get_ocf_datasources",
            {
                "host": os.environ["ALATION_HOST"],
                "user_id": int(os.environ["ALATION_USER_ID"]),
                "refresh_token": refresh_token,
                "validate_ssl": bool(int(os.environ.get("ALATION_VALIDATE_SSL", "1"))),
            },
        )
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
