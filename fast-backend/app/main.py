from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router

app = FastAPI(title="Rxplain Backend")

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(chat_router, prefix="/api")
