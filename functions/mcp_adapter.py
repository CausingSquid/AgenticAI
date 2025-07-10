# functions/mcp_adapter.py
import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
import re

def fetch_net_worth_data() -> str:
    async def fetch():
        async with streamablehttp_client("https://mcp.fi.money:8080/mcp/stream") as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool("fetch_net_worth", {})
                return result.content or []

    try:
        # Add timeout: Cloud Run must boot and respond quickly
        content = asyncio.run(asyncio.wait_for(fetch(), timeout=10))

        for item in content:
            if getattr(item, "type", None) == "text":
                return item.text  # 🧠 This is the readable net worth summary
        return "Net worth response did not contain usable text."

    except asyncio.TimeoutError:
        print("⏱️ MCP fetch timed out")
        return "Unable to fetch live net worth (timeout)."

    except Exception as e:
        print("❌ MCP fetch error:", e)
        return "Unable to fetch net worth at the moment."
