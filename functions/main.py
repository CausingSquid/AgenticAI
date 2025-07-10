# functions/main.py

from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app
from generate_prompt_mock import generate_financial_answer
import json
import traceback

# 🔧 Optional: limit concurrent containers for cost control
set_global_options(max_instances=10)

# 🔑 Initialize Firebase Admin SDK
initialize_app()

@https_fn.on_request()
def ask(req: https_fn.Request) -> https_fn.Response:
    try:
        # 📥 Safely parse request JSON
        data = req.get_json(silent=True)
        question = data.get("question", "") if data else ""

        if not question.strip():
            return https_fn.Response(
                json.dumps({"error": "Missing or empty 'question'."}),
                status=400,
                content_type="application/json"
            )

        print(f"📩 Received question: {question}")

        # 🧠 Call Gemini with mock MCP
        answer = generate_financial_answer(question)

        return https_fn.Response(
            json.dumps({"answer": answer}),
            status=200,
            content_type="application/json"
        )

    except Exception as e:
        print("🔥 ERROR:", e)
        traceback.print_exc()
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )
