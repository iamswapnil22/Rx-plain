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

