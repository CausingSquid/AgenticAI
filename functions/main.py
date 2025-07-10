from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app
from flask import jsonify
from generate_prompt import generate_financial_answer

set_global_options(max_instances=10)
initialize_app()
@https_fn.on_request()
def ask(req: https_fn.Request) -> https_fn.Response:
    try:
        data = req.get_json()
        question = data.get("question", "")
        if not question:
            return https_fn.Response("Missing question", status=400)

        mcp_data = """
Net Worth: ₹8,68,721
Credit Score: 746
Outstanding Loans: ₹75,000
EPF Balance: ₹2.1L
SIPs:
- Canara Robeco: 129% XIRR
- ICICI Balanced Advantage: -17.4%
- UTI Overnight: -82%
"""
        full_prompt = f"""You are a smart financial assistant. Here's the user's financial data:

{mcp_data}

User question: {question}

Answer in clear, simple financial advice."""

        answer = generate_financial_answer(full_prompt)

        import json
        return https_fn.Response(json.dumps({"answer": answer}), status=200, content_type="application/json")

    except Exception as e:
        print(f" ERROR: {e}")
        return https_fn.Response("Internal error: " + str(e), status=500)

