# 💰 AI-Powered Personal Finance Assistant

An intelligent, cross-platform financial assistant that connects **real financial data** from [Fi Money’s MCP Server](https://github.com/epiFi/mcp-docs) to **Google’s Gemini API via Vertex AI**, delivering personalized financial advice in natural language.

---

## 🧩 Key Features

- 🔒 **Secure Integration with Fi MCP**  
  Fetch live financial data (net worth, credit score, EPF, SIPs, liabilities) from 18+ sources.

- 🧠 **AI Reasoning with Gemini**  
  Use Google’s Gemini model via Vertex AI to interpret user questions and deliver smart, contextual responses.

- 🌐 **Firebase Backend + Serverless Functions**  
  Deployed using Firebase Functions or Cloud Run to serve AI responses securely.

- 📱 **Flutter Frontend (Optional)**  
  Clean, responsive UI to interact with the assistant via chat or form input.

---

## 🚀 Demo Questions You Can Ask
> “Can I afford a ₹50L home loan in 3 years?”  
> “How is my SIP performance over time?”  
> “What can I do to improve my credit score?”  
> “What’s my net worth trend?”

---

## 🛠️ Tech Stack

| Layer        | Tool/Platform                     |
|--------------|-----------------------------------|
| AI Model     | Google Gemini (via Vertex AI)     |
| Data Layer   | Fi MCP Server                     |
| Backend      | Firebase Functions / Cloud Run    |
| Frontend     | Flutter                           |
| Auth         | Auth0 / Firebase Auth (optional)  |
| DB (optional)| Firestore (for session history)   |

---

Done by Ashwin AS and Soorej S

## 🔧 Setup Instructions

### 1. Clone the Repo 
```bash
git clone https://github.com/your-username/ai-finance-assistant.git
cd ai-finance-assistant

firebase init functions
firebase deploy --only "functions"

python generate_prompt.py  #For local viewing 

