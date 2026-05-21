import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from elevenlabs.client import ElevenLabs
from agent_loader import load_brand_config, list_brands

load_dotenv()

app = FastAPI(title="ElevenLabs Multi-Tenant Agent Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))