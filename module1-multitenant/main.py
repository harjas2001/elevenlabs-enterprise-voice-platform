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
    response = eleven_client.conversational_ai.get_signed_url(
        agent_id=config["agent_id"]
    )

    # Return the signed URL plus everything the frontend needs to
    # configure itself for this brand
    return {
        "signed_url":    response.signed_url,
        "agent_name":    config["agent_name"],
        "first_message": config["first_message"],
        "theme_color":   config["theme_color"],
        "brand_id":      config["brand_id"],
    }


@app.get("/")
def serve_frontend():
    """Serve the brand-aware voice interface."""
    return FileResponse("frontend/index.html")