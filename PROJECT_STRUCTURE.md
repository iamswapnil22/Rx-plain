# Project Internal Structure: Rx-plain

This document explains the internal structure of the Rx-plain project, focusing on the backend (`fast-backend`) and frontend (`react-frontend`).

## fast-backend

A Python backend (likely FastAPI or Flask) organized as follows:

### Main Entry Point
- **run.py**: Starts the backend server. It imports the main app from `app/main.py`.

### App Package (`app/`)
- **main.py**: Defines the FastAPI/Flask app, includes route registration.
- **config.py**: Handles configuration (e.g., environment variables).
- **init.py**: (Possibly a typo, should be `__init__.py`).

#### Submodules
- **routes/**: Contains route definitions.
  - `chat.py`: Defines chat-related API endpoints. Calls service layer functions.
- **services/**: Business logic and integrations.
  - `conversation_memory.py`: Manages conversation state/memory. Main class: `ConversationMemory` (likely), with methods to store/retrieve conversation history. Arguments: user/session id, message, etc.
  - `gemini.py` & `gpt.py`: Integrations with Gemini and GPT models. Main classes/functions: likely `GeminiService`, `GPTService`. Arguments: prompt, context, model config.
- **utils/**: Utility functions and constants.
  - `formatter.py`: Formatting helpers.
  - `medical_prompts.py`: Predefined prompts for medical use cases.

#### Call Flow
1. **Client** (frontend) sends a request to a route (e.g., `/chat`).
2. **Route handler** (e.g., in `routes/chat.py`) receives the request, validates input.
3. **Service layer** (e.g., `services/gpt.py`) is called to process the request, possibly using conversation memory and model integrations.
4. **Utils** are used for formatting or prompt management.
5. **Response** is returned to the client.

## react-frontend

A React app for the user interface.
- **src/App.js**: Main React component. Handles routing and UI logic.
- **src/index.js**: Entry point, renders the app.
- **public/**: Static assets and HTML template.

### Call Flow
1. User interacts with the UI (e.g., sends a chat message).
2. Frontend sends API requests to the backend (`fast-backend`).
3. Displays responses from the backend.

## Summary Table
| Layer         | Main Classes/Files         | Key Arguments/Responsibilities                |
|---------------|---------------------------|-----------------------------------------------|
| API Routes    | `routes/chat.py`          | Request/response, calls services              |
| Services      | `conversation_memory.py`, `gpt.py`, `gemini.py` | Handles logic, model calls, memory; args: user id, prompt, context |
| Utils         | `formatter.py`, `medical_prompts.py` | Formatting, prompt templates                  |
| Frontend      | `App.js`, `index.js`      | UI, API calls                                 |

---

**Note:** For detailed class names and arguments, see the respective files. This overview is based on standard project conventions and the provided structure.
