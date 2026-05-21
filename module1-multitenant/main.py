import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from elevenlabs.client import ElevenLabs
from agent_loader import load_brand_config, list_brands

load_dotenv()