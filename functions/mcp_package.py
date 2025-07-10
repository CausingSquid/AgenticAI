import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
import traceback
import webbrowser
import re

async def fetch_networth():
    try:
        async with streamablehttp_client("https://mcp.fi.money:8080/mcp/stream") as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                # First attempt
                result = await session.call_tool("fetch_net_worth", {})
                content = result.content or []

                login_required = False
                login_url = None

                for item in content:
                    if getattr(item, "type", None) == "text" and "login" in item.text.lower():
                        login_required = True
                        urls = re.findall(r"https?://[^\s)]+", item.text)
                        if urls:
                            login_url = urls[0]
                        break

                if login_required:
                    print("🔐 Login required.")
                    print(f"🔗 {login_url}")
                    try:
                        webbrowser.open(login_url)
                    except:
                        pass
                    input("After logging in, press Enter to continue...")

                    # Retry
                    result = await session.call_tool("fetch_net_worth", {})
                    return result

                else:
                    return result

    except Exception:
        print("An error occurred:")
        traceback.print_exc()
        return None

# Script entrypoint for CLI usage
async def main():
    result = await fetch_networth()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
