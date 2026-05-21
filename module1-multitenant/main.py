import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
# from elevenlabs.client import ElevenLabs
import httpx
from agent_loader import load_brand_config, list_brands
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

app = FastAPI(title="ElevenLabs Multi-Tenant Agent Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_SIGNED_URL_ENDPOINT = "https://api.elevenlabs.io/v1/convai/conversation/get_signed_url"


@app.get("/brands")
def get_brands():
    """Return list of available brand IDs for the frontend selector."""
    return {"brands": list_brands()}


@app.get("/signed-url")
def get_signed_url(brand_id: str = Query(...)):
    """
    Load brand config and return a signed URL for ElevenLabs Conversational AI.
    The signed URL allows the browser to connect directly to ElevenLabs
    without ever seeing the API key.
    """
    # Load brand config — raises ValueError for unknown brand,
    # FileNotFoundError if YAML is missing
    try:
        config = load_brand_config(brand_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Call ElevenLabs to generate a signed URL for this agent
    el_response = httpx.get(
        ELEVENLABS_SIGNED_URL_ENDPOINT,
        params={"agent_id": config["agent_id"]},
        headers={"xi-api-key": ELEVENLABS_API_KEY}
    )

    if el_response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"ElevenLabs API error: {el_response.text}"
        )
    
    signed_url = el_response.json()["signed_url"]

    # Return the signed URL plus everything the frontend needs to
    # configure itself for this brand
    return {
        "signed_url":    signed_url,
        "agent_name":    config["agent_name"],
        "first_message": config["first_message"],
        "theme_color":   config["theme_color"],
        "brand_id":      config["brand_id"],
    }


@app.get("/")
def serve_frontend():
    """Serve the brand-aware voice interface."""
    return FileResponse("frontend/index.html")