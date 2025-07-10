# mcp_server.py

import asyncio
import uvicorn
from fastapi import FastAPI
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
import re

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("🔌 Starting MCP session in background...")

    async def maintain_session():
        try:
            async with streamablehttp_client("https://mcp.fi.money:8080/mcp/stream") as (read_stream, write_stream, _):
                async with ClientSession(read_stream, write_stream) as session:
                    print("🟡 Initializing MCP session...")

                    result = await session.call_tool("fetch_net_worth", {})
                    content = result.content or []

                    for item in content:
                        if getattr(item, "type", None) == "text" and "login" in item.text.lower():
                            urls = re.findall(r"https?://[^\s)]+", item.text)
                            login_url = urls[0] if urls else None
                            print("🔐 Login required.")
                            print(f"🔗 {login_url}")
                            print("💡 Please open the link in your browser to authenticate.")
                            break

                    app.state.mcp_session = session
                    print("✅ MCP session ready and running")

                    while True:
                        await asyncio.sleep(60)

        except Exception as e:
            print("❌ MCP session crashed:")
            import traceback
            traceback.print_exc()

    asyncio.create_task(maintain_session())


@app.get("/networth")
async def get_networth():
    session = getattr(app.state, "mcp_session", None)
    if not session:
        return {"status": "error", "message": "MCP session not ready yet"}

    result = await session.call_tool("fetch_net_worth", {})
    content = result.content or []

    for item in content:
        if getattr(item, "type", None) == "text" and "login" in item.text.lower():
            urls = re.findall(r"https?://[^\s)]+", item.text)
            login_url = urls[0] if urls else None
            return {
                "status": "login_required",
                "login_url": login_url,
                "message": "🔐 Login required. Open this in your browser."
            }

        if getattr(item, "type", None) == "text":
            return {
                "status": "success",
                "data": item.text
            }

    return {"status": "error", "message": "Could not extract net worth text"}
