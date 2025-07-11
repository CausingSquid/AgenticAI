from google import genai
from google.genai import types

def get_mock_mcp_data():
    return """Net Worth: ₹8,68,721
Credit Score: 746
Outstanding Loans: ₹75,000
EPF Balance: ₹2.1L
SIPs:
- Canara Robeco: 129% XIRR
- ICICI Balanced Advantage: -17.4%
- UTI Overnight: -82%"""

def generate_financial_answer(question: str) -> str:
    # 🧠 Use mock MCP data
    mcp_text = get_mock_mcp_data()

    full_prompt = f"""You are a smart financial assistant. Here's the user's financial data:

{mcp_text}

User question: {question}

Answer in clear, simple financial advice. Just make it shorter and upto the point."""

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
