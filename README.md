# 💊 Rxplain – Understand Your Prescriptions with AI

**Rxplain** is an AI-powered chatbot that helps users understand their prescription medications, including usage, side effects, precautions, and interactions — all explained in simple, user-friendly language.

Built using **React**, **FastAPI**, and **Gemini/GPT**, Rxplain bridges the gap between complex pharmaceutical data and everyday health literacy.

---

## 💡 Why I Built This

Many people take prescription medicines without fully understanding what they are for, how to take them properly, or what side effects to expect. This confusion often leads to anxiety, misuse, or over-reliance on unverified internet sources.

I built **Rxplain** to solve this real-world problem by giving users a safe and smart assistant that:
- Provides **easy-to-understand explanations** of drug information
- Uses trusted AI models (Gemini or GPT)
- Encourages users to be informed, not misinformed

> Rxplain is not a replacement for a doctor — it’s a **digital explainer** built to support patient awareness.

---

## 🧠 Features

- 💬 Chat with an AI about any medicine
- 📖 Summaries of usage, dosage, and side effects
- ⚠️ Safety warnings and precautions
- 🧾 Optional integration with real drug databases (DrugBank, MedlinePlus)
- 🌐 Mobile-friendly UI with a smooth chat experience
- 🧪 Gemini or GPT-powered backend with prompt safety filters

---

## 🔧 Tech Stack

| Layer         | Technology                  |
|---------------|------------------------------|
| Frontend      | React + Tailwind CSS         |
| Backend       | FastAPI (Python)             |
| LLM API       | Gemini Pro / GPT-4o (OpenAI) |
| Optional DB   | DrugBank CSV, MedlinePlus API|
| Hosting       | Vercel + Render (optional)   |

---

## 🚀 How It Works

1. The user asks a question like:
   > “What is Metformin used for?”

2. The backend fetches structured drug info (if available).
3. That info is passed to the LLM with a custom prompt:
   > “Explain this drug to a patient in simple language. Mention its use, dosage, side effects, and when to consult a doctor.”

4. The result is returned to the frontend as a clean chatbot reply.

---

## Project Structure
rxplain/
│<br>
├── backend/<br>
│   ├── app/<br>
│   │   ├── init.py<br>
│   │   ├── main.py                    # FastAPI app entry point<br>
│   │   ├── routes/<br>
│   │   │   ├── init.py<br>
│   │   │   └── chat.py               # LLM chat route<br>
│   │   ├── services/<br>
│   │   │   └── llm_handler.py        # GPT/Gemini wrapper<br>
│   │   ├── utils/<br>
│   │   │   └── prompt_templates.py   # Reusable prompt templates<br>
│   │   └── config.py                 # Env & settings management<br>
│   ├── requirements.txt<br>
│   ├── .env.example<br>
│   └── README.md<br>
│<br>
├── frontend/<br>
│   ├── public/<br>
│   │   └── favicon.ico<br>
│   ├── src/<br>
│   │   ├── assets/<br>
│   │   ├── components/<br>
│   │   │   ├── ChatBox.jsx<br>
│   │   │   ├── MessageBubble.jsx<br>
│   │   │   └── Loader.jsx<br>
│   │   ├── pages/<br>
│   │   │   └── Home.jsx<br>
│   │   ├── App.jsx<br>
│   │   ├── index.js<br>
│   │   └── api.js                    # Axios/fetch client for backend<br>
│   ├── tailwind.config.js<br>
│   ├── package.json<br>
│   └── README.md<br>
│<br>
├── docs/<br>
│   ├── wireframes.png<br>
│   ├── prompt_design.md<br>
│   └── sample_responses/<br>
│       └── metformin_response.txt<br>
│<br>
├── .gitignore<br>
├── LICENSE<br>
└── README.md
