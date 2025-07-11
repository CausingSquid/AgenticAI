# generate_prompt.py
from google import genai
from google.genai import types
import asyncio
from mcp_package import fetch_networth

def get_networth_text(result):
    for item in result.content or []:
        if getattr(item, "type", None) == "text":
            return item.text
    return "Could not fetch net worth info."

def generate_financial_answer(question: str) -> str:
    # 🧠 Run async MCP client 
    result = asyncio.run(fetch_networth())
    mcp_text = get_networth_text(result)

    full_prompt = f"""You are a smart financial assistant. Here's the user's financial data:

{mcp_text}

User question: {question}

Answer in clear, simple financial advice."""

    client = genai.Client(
        vertexai=True,
        project="your-project-id",
        location="location-place",
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=full_prompt)]
        )
    ]

    config = types.GenerateContentConfig(
        temperature=1,
        top_p=1,
        max_output_tokens=4096,
    )

    output = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=contents,
        config=config,
    ):
        output += chunk.text

    return output

if __name__ == "__main__":
    question = input("Enter your financial question: ")
    answer = generate_financial_answer(question)
    print("\nAI Answer:\n", answer)
